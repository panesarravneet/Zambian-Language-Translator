from transformers import NllbTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

tokenizer = NllbTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def translate_en_to_nyanja(text: str) -> str:
    # Beam search for better accuracy.
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("nya_Latn")
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, num_beams=5, early_stopping=True)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def translate_nyanja_to_en(text: str) -> str:
    tokenizer.src_lang = "nya_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, num_beams=5, early_stopping=True)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def translate_en_to_bemba(text: str) -> str:
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("bem_Latn")
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, num_beams=5, early_stopping=True)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def translate_bemba_to_en(text: str) -> str:
    tokenizer.src_lang = "bem_Latn"
    inputs = tokenizer(text, return_tensors="pt")
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")
    outputs = model.generate(**inputs, forced_bos_token_id=forced_bos_token_id, num_beams=5, early_stopping=True)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
