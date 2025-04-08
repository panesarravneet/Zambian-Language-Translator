import requests
from transformers import NllbTokenizer, AutoModelForSeq2SeqLM
from apikey import apikey

# NLLB Setup (English, Nyanja, Bemba, Swahili)
NLLB_MODEL = "facebook/nllb-200-distilled-600M"
tokenizer = NllbTokenizer.from_pretrained(NLLB_MODEL, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL)

API_KEY = apikey

# -----------------------
# NLLB-BASED TRANSLATIONS
# -----------------------

def translate_en_to_nyanja(text: str) -> str:
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    bos = tokenizer.convert_tokens_to_ids("nya_Latn")
    out = model.generate(**inputs, forced_bos_token_id=bos, num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def translate_nyanja_to_en(text: str) -> str:
    tokenizer.src_lang = "nya_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    bos = tokenizer.convert_tokens_to_ids("eng_Latn")
    out = model.generate(**inputs, forced_bos_token_id=bos, num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def translate_en_to_bemba(text: str) -> str:
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    bos = tokenizer.convert_tokens_to_ids("bem_Latn")
    out = model.generate(**inputs, forced_bos_token_id=bos, num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def translate_bemba_to_en(text: str) -> str:
    tokenizer.src_lang = "bem_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    bos = tokenizer.convert_tokens_to_ids("eng_Latn")
    out = model.generate(**inputs, forced_bos_token_id=bos, num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def translate_en_to_swahili(text: str) -> str:
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    bos = tokenizer.convert_tokens_to_ids("swh_Latn")
    out = model.generate(**inputs, forced_bos_token_id=bos, num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

def translate_swahili_to_en(text: str) -> str:
    tokenizer.src_lang = "swh_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    bos = tokenizer.convert_tokens_to_ids("eng_Latn")
    out = model.generate(**inputs, forced_bos_token_id=bos, num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

# ---------------------------
# GOOGLE-BASED TRANSLATIONS
# ---------------------------

def translate_google_v2(text: str, source: str, target: str) -> str:
    """
    Make a direct GET request to the Google Translate v2 endpoint.
    :param text: The text to translate
    :param source: The source language code (e.g. 'en', 'sn', 'nd')
    :param target: The target language code (e.g. 'zu', 'sn', 'en')
    """
    endpoint = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "source": source,
        "target": target,
        "key": API_KEY
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()  # Throw if there's an HTTP error
    data = response.json()
    
    # Expected structure: data["data"]["translations"][0]["translatedText"]
    return data["data"]["translations"][0]["translatedText"]

def translate_en_to_ndebele(text: str) -> str:
    return translate_google_v2(text, "en", "nr")

def translate_ndebele_to_en(text: str) -> str:
    return translate_google_v2(text, "nr", "en")

def translate_en_to_shona(text: str) -> str:
    return translate_google_v2(text, "en", "sn")

def translate_shona_to_en(text: str) -> str:
    return translate_google_v2(text, "sn", "en")

def translate_en_to_zulu(text: str) -> str:
    return translate_google_v2(text, "en", "zu")

def translate_zulu_to_en(text: str) -> str:
    return translate_google_v2(text, "zu", "en")

# Following fail because Google model doesn’t support them. 
# def translate_en_to_lunda(text: str) -> str:
#     return translate_google_v2(text, "en", "lun")

# def translate_lunda_to_en(text: str) -> str:
#     return translate_google_v2(text, "lun", "en")

# def translate_en_to_kaonde(text: str) -> str:
#     return translate_google_v2(text, "en", "kqn")

# def translate_kaonde_to_en(text: str) -> str:
#     return translate_google_v2(text, "kqn", "en")

# def translate_en_to_tonga(text: str) -> str:
#     return translate_google_v2(text, "en", "toi")

# def translate_tonga_to_en(text: str) -> str:
#     return translate_google_v2(text, "toi", "en")

# def translate_en_to_luvale(text: str) -> str:
#     return translate_google_v2(text, "en", "lue")

# def translate_luvale_to_en(text: str) -> str:
#     return translate_google_v2(text, "lue", "en")

# def translate_en_to_lozi(text: str) -> str:
#     return translate_google_v2(text, "en", "loz")

# def translate_lozi_to_en(text: str) -> str:
#     return translate_google_v2(text, "loz", "en")
