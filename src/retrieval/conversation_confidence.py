from rapidfuzz import fuzz
from retrieval.query_normalizer import normalize_query
from typing import Tuple

GREETING_VOCAB = ["hi", "hello", "hey", "good morning", "good evening", "greetings"]
SMALL_TALK_VOCAB = ["thanks", "thank you", "bye", "goodbye", "ok", "okay", "yes", "no", "how are you", "who are you"]
HELP_VOCAB = ["help", "what can you do", "examples"]

def get_vocab_dict():
    d = {}
    for v in GREETING_VOCAB: d[normalize_query(v)] = "greeting"
    for v in SMALL_TALK_VOCAB: d[normalize_query(v)] = "small_talk"
    for v in HELP_VOCAB: d[normalize_query(v)] = "help"
    return d

VOCAB_MAP = get_vocab_dict()

def score_conversational_intent(normalized_query: str) -> Tuple[float, str]:
    """
    Returns (conversational_score, category) where score is 0 to 100.
    """
    if not normalized_query:
        return 0.0, "unknown"
        
    max_score = 0.0
    best_cat = "unknown"
    for vocab, cat in VOCAB_MAP.items():
        score = fuzz.ratio(normalized_query, vocab)
        if score > max_score:
            max_score = score
            best_cat = cat
            
    return max_score, best_cat
