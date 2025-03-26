from transformers import NllbTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = NllbTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def translate_en_to_nyanja(text: str) -> str:
    """Translate English (eng_Latn) to Nyanja (nya_Latn)."""
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("nya_Latn")
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, num_beams=5)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def translate_nyanja_to_en(text: str) -> str:
    """Translate Nyanja (nya_Latn) to English (eng_Latn)."""
    tokenizer.src_lang = "nya_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, num_beams=5)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
