# models/handlers.py

import time
import logging
import torch
from groq import Groq
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

def generate_response_groq(model_name: str, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_retries: int = 3):
    """
    Generates a response using the Groq API with an exponential backoff retry mechanism.

    Args:
        model_name (str): The ID of the Groq model to use.
        system_prompt (str): The system prompt to guide the model's behavior.
        user_prompt (str): The user's input prompt.
        temperature (float): The sampling temperature for generation.
        max_retries (int): The maximum number of times to retry on failure.

    Returns:
        tuple[str, str]: A tuple containing the generated text and a status ('ok' or 'fail').
    """
    try:
        client = Groq()
        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=model_name,
                    temperature=temperature,
                    max_tokens=512
                )
                response_text = chat_completion.choices[0].message.content
                logging.info(f"Groq: Successfully received response for {model_name}.")
                return response_text, 'ok'
            except Exception as e:
                wait_time = 2 ** attempt
                logging.error(f"Groq: Attempt {attempt+1} failed for {model_name} with error: {e}. Retrying in {wait_time}s.")
                time.sleep(wait_time)
        
        logging.critical(f"Groq: Max retries exceeded for {model_name}.")
        return "MODEL_FAIL", "fail"

    except Exception as e:
        logging.critical(f"Groq client failed to initialize. Error: {e}")
        return "MODEL_FAIL", "fail"

class HuggingFaceModelHandler:
    """
    A handler class to manage loading and interacting with a local Hugging Face model.
    """
    def __init__(self, model_id: str):
        """
        Initializes the handler and loads the specified model and tokenizer.

        Args:
            model_id (str): The Hugging Face model identifier (e.g., 'google/gemma-7b-it').
        """
        self.model = None
        self.tokenizer = None
        self.model_id = model_id
        self._load_model()

    def _load_model(self):
        """
        Loads the model in 4-bit quantization and its corresponding tokenizer.
        """
        logging.info(f"Loading Hugging Face model: {self.model_id}...")
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                quantization_config=quantization_config,
                device_map="auto"
            )
            logging.info(f"Successfully loaded {self.model_id}.")
        except Exception as e:
            logging.critical(f"Failed to load model {self.model_id}. Error: {e}")
            # We raise the exception to halt execution if a critical model fails to load.
            raise

    def generate_response(self, system_prompt: str, user_prompt: str, temperature: float = 0.7):
        """
        Generates a response from the loaded Hugging Face model.

        Args:
            system_prompt (str): The system prompt to guide the model's behavior.
            user_prompt (str): The user's input prompt.
            temperature (float): The sampling temperature. Must be > 0.

        Returns:
            tuple[str, str]: A tuple containing the generated text and a status ('ok' or 'fail').
        """
        if not self.model or not self.tokenizer:
            logging.error(f"Model {self.model_id} is not loaded. Cannot generate response.")
            return "MODEL_NOT_LOADED", "fail"
        
        try:
            # Combine prompts for models that don't have a dedicated system prompt input
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            messages = [{"role": "user", "content": full_prompt}]
            
            # Use the chat template for proper formatting
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=True,
                return_tensors="pt"
            ).to(self.model.device)

            outputs = self.model.generate(
                input_ids,
                max_new_tokens=512,
                do_sample=True,
                temperature=max(temperature, 0.01), # Ensure temperature is non-zero
                top_p=0.95
            )
            
            # Decode the response, skipping the prompt tokens
            response_text = self.tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
            return response_text, 'ok'
        
        except Exception as e:
            logging.error(f"Error during generation with {self.model_id}. Error: {e}")
            return "GENERATION_FAIL", "fail"
