import streamlit as st
from translator_backend import (
    translate_en_to_nyanja,
    translate_nyanja_to_en,
    translate_en_to_bemba,
    translate_bemba_to_en
)

def main():
    st.set_page_config(page_title="Zambian Language Translator", page_icon="🌍", layout="centered")

    st.markdown(
        """
        <h1 style='text-align: center; color: #2E86C1;'>
            Zambian Language Translator
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")

    direction = st.selectbox(
        "Select translation direction:",
        ["English → Nyanja", "Nyanja → English", "English → Bemba", "Bemba → English"]
    )

    st.markdown("#### Enter text to translate:")
    user_text = st.text_area("", height=120, placeholder="Type or paste your text here...")

    if st.button("Translate"):
        if user_text.strip():
            with st.spinner("Translating..."):
                if direction == "English → Nyanja":
                    translation = translate_en_to_nyanja(user_text)
                elif direction == "Nyanja → English":
                    translation = translate_nyanja_to_en(user_text)
                elif direction == "English → Bemba":
                    translation = translate_en_to_bemba(user_text)
                else:
                    translation = translate_bemba_to_en(user_text)
            st.success("Translation:")
            st.info(translation)
        else:
            st.warning("Please enter some text before translating.")

    st.write("---")
    st.markdown(
        """
        <p style='text-align: center; font-size: 0.85em; color: gray;'>
        NLLB-200 Distilled 600M | <a href='https://huggingface.co/facebook/nllb-200-distilled-600M' target='_blank'>More Info</a>
        </p>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
