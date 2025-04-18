import requests
from transformers import NllbTokenizer, AutoModelForSeq2SeqLM
from apikey import apikey

# ----------  Constants  ----------
ZAM_LANGS = ["bem", "nya", "swh", "zu", "sn", "nr"]   # extend if you add more
API_KEY   = apikey

# ----------  Model load (NLLB)  ----------
NLLB_MODEL = "facebook/nllb-200-distilled-600M"
tokenizer  = NllbTokenizer.from_pretrained(NLLB_MODEL, use_fast=False)
model      = AutoModelForSeq2SeqLM.from_pretrained(NLLB_MODEL)

# ----------  NLLB helpers  ----------
def _nllb_translate(text: str, src_code: str, tgt_code: str) -> str:
    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt")
    bos    = tokenizer.convert_tokens_to_ids(tgt_code)
    out    = model.generate(**inputs, forced_bos_token_id=bos,
                            num_beams=5, early_stopping=True)
    return tokenizer.decode(out[0], skip_special_tokens=True)

# ----------  Individual wrappers  ----------
def translate_en_to_nyanja(t): return _nllb_translate(t, "eng_Latn", "nya_Latn")
def translate_nyanja_to_en(t): return _nllb_translate(t, "nya_Latn", "eng_Latn")

def translate_en_to_bemba(t):  return _nllb_translate(t, "eng_Latn", "bem_Latn")
def translate_bemba_to_en(t):  return _nllb_translate(t, "bem_Latn", "eng_Latn")

def translate_en_to_swahili(t): return _nllb_translate(t, "eng_Latn", "swh_Latn")
def translate_swahili_to_en(t): return _nllb_translate(t, "swh_Latn", "eng_Latn")

# ----------  Google v2 helpers  ----------
def _google_v2(t, src, tgt):
    r = requests.get(
        "https://translation.googleapis.com/language/translate/v2",
        params={"q": t, "source": src, "target": tgt, "key": API_KEY},
        timeout=10
    )
    r.raise_for_status()
    return r.json()["data"]["translations"][0]["translatedText"]

def translate_en_to_zulu(t):     return _google_v2(t, "en", "zu")
def translate_zulu_to_en(t):     return _google_v2(t, "zu", "en")

def translate_en_to_shona(t):    return _google_v2(t, "en", "sn")
def translate_shona_to_en(t):    return _google_v2(t, "sn", "en")

def translate_en_to_ndebele(t):  return _google_v2(t, "en", "nr")
def translate_ndebele_to_en(t):  return _google_v2(t, "nr", "en")

# ----------  Whitelist for app.py  ----------
ROUTE_WHITELIST = {
    # Nyanja
    "en_nya": translate_en_to_nyanja,
    "nya_en": translate_nyanja_to_en,
    # Bemba
    "en_bem": translate_en_to_bemba,
    "bem_en": translate_bemba_to_en,
    # Swahili
    "en_swh": translate_en_to_swahili,
    "swh_en": translate_swahili_to_en,
    # Zulu
    "en_zu":  translate_en_to_zulu,
    "zu_en":  translate_zulu_to_en,
    # Shona
    "en_sn":  translate_en_to_shona,
    "sn_en":  translate_shona_to_en,
    # Ndebele
    "en_nr":  translate_en_to_ndebele,
    "nr_en":  translate_ndebele_to_en,
}
