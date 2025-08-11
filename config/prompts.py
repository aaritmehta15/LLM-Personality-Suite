# config/prompts.py

# This file contains all the static data structures for prompts, questions,
# and trait definitions used across the experiments.

# --- Trait Definitions for Generation and Classification ---
# Contains detailed descriptions for each of the Big Five personality traits.
# 'generation' is used for the text generation task.
# 'classification' is used for the judging task.
TRAITS_DEFINITIONS = {
    "generation": {
        "O": {"name": "Openness", "low": "A person with a low score is practical and prefers routine.", "high": "A person with a high score is imaginative, curious, and open to new experiences."},
        "C": {"name": "Conscientiousness", "low": "A person with a low score is disorganized and careless.", "high": "A person with a high score is disciplined, organized, and achievement-oriented."},
        "E": {"name": "Extraversion", "low": "A person with a low score is reserved and solitary.", "high": "A person with a high score is outgoing, sociable, and energetic."},
        "A": {"name": "Agreeableness", "low": "A person with a low score is critical and uncooperative.", "high": "A person with a high score is compassionate, cooperative, and trusting."},
        "N": {"name": "Neuroticism", "low": "A person with a low score is calm, secure, and emotionally stable.", "high": "A person with a high score is anxious, insecure, and prone to negative emotions."}
    },
    "classification": {
        "O": {"name": "Openness", "definition": "Openness to experience describes a person's tendency to be open to new ideas, creative, curious, and appreciative of art and beauty.", "low": "A person with a low score is practical, conventional, and prefers routine over new experiences.", "high": "A person with a high score is imaginative, adventurous, and receptive to a wide range of ideas and emotions."},
        "C": {"name": "Conscientiousness", "definition": "Conscientiousness refers to the tendency to be organized, responsible, and dependable.", "low": "A person with a low score is impulsive, disorganized, and less focused on long-term goals.", "high": "A person with a high score is disciplined, detail-oriented, and reliable in their commitments."},
        "E": {"name": "Extraversion", "definition": "Extraversion reflects a person's level of sociability, assertiveness, and emotional expression.", "low": "A person with a low score is reserved, reflective, and prefers solitary activities or small groups.", "high": "A person with a high score is outgoing, energetic, and thrives in social situations."},
        "A": {"name": "Agreeableness", "definition": "Agreeableness indicates a person's tendency to be compassionate, cooperative, and considerate of others.", "low": "A person with a low score is competitive, critical, and may be seen as untrusting or suspicious.", "high": "A person with a high score is friendly, helpful, and empathetic towards others."},
        "N": {"name": "Neuroticism", "definition": "Neuroticism, often referred to as emotional stability, describes the tendency to experience negative emotions like anxiety, anger, and sadness.", "low": "A person with a low score is calm, secure, and resilient to stress.", "high": "A person with a high score is emotionally reactive, prone to stress, and may experience frequent mood swings."}
    }
}

# --- General Questions for the Main Experiment ---
# These questions are used to elicit responses for personality analysis.
QUESTIONS = [
    "What is your dream career?",
    "What quality do you appreciate the most in a friend?",
    "If you had enough money to retire tomorrow, what would you do for the rest of your life?",
    "What can we learn from children?",
    "If you could play the main character in any movie, what movie would it be?",
    "What does the world need more of?"
]

# --- BFI-44 Questionnaire Data ---
# This data is from the Big Five Inventory (BFI-44) personality test.

# Defines the scoring for the Likert scale responses.
BFI44_SCORES_DICT = {
    "disagree strongly with the statement": 1,
    "disagree a little with the statement": 2,
    "agree nor disagree with the statement": 3,
    "agree a little with the statement": 4,
    "agree strongly with the statement": 5
}

# The full set of 44 questions, categorized by trait.
# 'q_type' indicates whether a high score is a 'direct' or 'inverted' measure of the trait.
BFI44_QUESTIONS = {
    'openness': [
        {'q_num': 5, 'q_statement': 'I see myself as someone who Is original, comes up with new ideas', 'q_type': 'direct'},
        {'q_num': 10, 'q_statement': 'I see myself as someone who Is curious about many different things', 'q_type': 'direct'},
        {'q_num': 15, 'q_statement': 'I see myself as someone who Is ingenious, a deep thinker', 'q_type': 'direct'},
        {'q_num': 20, 'q_statement': 'I see myself as someone who Has an active imagination', 'q_type': 'direct'},
        {'q_num': 25, 'q_statement': 'I see myself as someone who Is inventive', 'q_type': 'direct'},
        {'q_num': 30, 'q_statement': 'I see myself as someone who Values artistic, aesthetic experiences', 'q_type': 'direct'},
        {'q_num': 35, 'q_statement': 'I see myself as someone who Prefers work that is routine', 'q_type': 'inverted'},
        {'q_num': 40, 'q_statement': 'I see myself as someone who Likes to reflect, play with ideas', 'q_type': 'direct'},
        {'q_num': 41, 'q_statement': 'I see myself as someone who Has few artistic interests', 'q_type': 'inverted'},
        {'q_num': 44, 'q_statement': 'I see myself as someone who Is sophisticated in art, music, or literature', 'q_type': 'direct'}
    ],
    'conscientiousness': [
        {'q_num': 3, 'q_statement': 'I see myself as someone who Does a thorough job', 'q_type': 'direct'},
        {'q_num': 8, 'q_statement': 'I see myself as someone who Can be somewhat careless', 'q_type': 'inverted'},
        {'q_num': 13, 'q_statement': 'I see myself as someone who Is a reliable worker', 'q_type': 'direct'},
        {'q_num': 18, 'q_statement': 'I see myself as someone who Tends to be disorganized', 'q_type': 'inverted'},
        {'q_num': 23, 'q_statement': 'I see myself as someone who Tends to be lazy', 'q_type': 'inverted'},
        {'q_num': 28, 'q_statement': 'I see myself as someone who Perseveres until the task is finished', 'q_type': 'direct'},
        {'q_num': 33, 'q_statement': 'I see myself as someone who Does things efficiently', 'q_type': 'direct'},
        {'q_num': 38, 'q_statement': 'I see myself as someone who Makes plans and follows through with them', 'q_type': 'direct'},
        {'q_num': 43, 'q_statement': 'I see myself as someone who Is easily distracted', 'q_type': 'inverted'}
    ],
    'extraversion': [
        {'q_num': 1, 'q_statement': 'I see myself as someone who Is talkative', 'q_type': 'direct'},
        {'q_num': 6, 'q_statement': 'I see myself as someone who Is reserved', 'q_type': 'inverted'},
        {'q_num': 11, 'q_statement': 'I see myself as someone who Is full of energy', 'q_type': 'direct'},
        {'q_num': 16, 'q_statement': 'I see myself as someone who Generates a lot of enthusiasm', 'q_type': 'direct'},
        {'q_num': 21, 'q_statement': 'I see myself as someone who Tends to be quiet', 'q_type': 'inverted'},
        {'q_num': 26, 'q_statement': 'I see myself as someone who Has an assertive personality', 'q_type': 'direct'},
        {'q_num': 31, 'q_statement': 'I see myself as someone who Is sometimes shy, inhibited', 'q_type': 'inverted'},
        {'q_num': 36, 'q_statement': 'I see myself as someone who Is outgoing, sociable', 'q_type': 'direct'}
    ],
    'agreeableness': [
        {'q_num': 2, 'q_statement': 'I see myself as someone who Tends to find fault with others', 'q_type': 'inverted'},
        {'q_num': 7, 'q_statement': 'I see myself as someone who Is helpful and unselfish with others', 'q_type': 'direct'},
        {'q_num': 12, 'q_statement': 'I see myself as someone who Starts quarrels with others', 'q_type': 'inverted'},
        {'q_num': 17, 'q_statement': 'I see myself as someone who Has a forgiving nature', 'q_type': 'direct'},
        {'q_num': 22, 'q_statement': 'I see myself as someone who Is generally trusting', 'q_type': 'direct'},
        {'q_num': 27, 'q_statement': 'I see myself as someone who Can be cold and aloof', 'q_type': 'inverted'},
        {'q_num': 32, 'q_statement': 'I see myself as someone who Is considerate and kind to almost everyone', 'q_type': 'direct'},
        {'q_num': 37, 'q_statement': 'I see myself as someone who Is sometimes rude to others', 'q_type': 'inverted'},
        {'q_num': 42, 'q_statement': 'I see myself as someone who Likes to cooperate with others', 'q_type': 'direct'}
    ],
    'neuroticism': [
        {'q_num': 4, 'q_statement': 'I see myself as someone who Is depressed, blue', 'q_type': 'direct'},
        {'q_num': 9, 'q_statement': 'I see myself as someone who Is relaxed, handles stress well', 'q_type': 'inverted'},
        {'q_num': 14, 'q_statement': 'I see myself as someone who Can be tense', 'q_type': 'direct'},
        {'q_num': 19, 'q_statement': 'I see myself as someone who Worries a lot', 'q_type': 'direct'},
        {'q_num': 24, 'q_statement': 'I see myself as someone who Is emotionally stable, not easily upset', 'q_type': 'inverted'},
        {'q_num': 29, 'q_statement': 'I see myself as someone who Can be moody', 'q_type': 'direct'},
        {'q_num': 34, 'q_statement': 'I see myself as someone who Remains calm in tense situations', 'q_type': 'inverted'},
        {'q_num': 39, 'q_statement': 'I see myself as someone who Gets nervous easily', 'q_type': 'direct'}
    ]
}
