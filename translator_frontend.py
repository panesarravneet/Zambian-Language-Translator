import streamlit as st
from translator_backend import (
    translate_en_to_nyanja,
    translate_nyanja_to_en,
    translate_en_to_bemba,
    translate_bemba_to_en,
    translate_en_to_swahili,
    translate_swahili_to_en
)

def main():
    st.set_page_config(page_title="Zambian Language Translator", page_icon="🌍", layout="centered")

    st.markdown(
        """
        <h2 style='text-align: center; color: #2E86C1; margin-top: 0;'>
            Zambian Language Translator
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.write("Enter text below and press **Enter** or click **Translate**.")

    # The form to handle 'Enter' or Button click
    with st.form("translator_form"):
        direction = st.selectbox(
            "Select translation direction:",
            [
                "English → Nyanja", "Nyanja → English",
                "English → Bemba",  "Bemba → English",
                "English → Swahili","Swahili → English"
            ]
        )
        user_text = st.text_input("Type your text here:", placeholder="Press Enter or click Translate")
        submitted = st.form_submit_button("Translate")
    
    if submitted:
        if not user_text.strip():
            st.warning("Please enter some text before translating.")
        else:
            with st.spinner("Translating..."):
                if direction == "English → Nyanja":
                    translation = translate_en_to_nyanja(user_text)
                elif direction == "Nyanja → English":
                    translation = translate_nyanja_to_en(user_text)
                elif direction == "English → Bemba":
                    translation = translate_en_to_bemba(user_text)
                elif direction == "Bemba → English":
                    translation = translate_bemba_to_en(user_text)
                elif direction == "English → Swahili":
                    translation = translate_en_to_swahili(user_text)
                else:
                    translation = translate_swahili_to_en(user_text)

            st.success("Translation:")
            st.info(translation)

    st.write("---")
    st.markdown(
        """
        <p style='text-align:center; font-size:0.85em; color:gray; margin-bottom: 0;'>
        Powered by <a href='https://huggingface.co/facebook/nllb-200-distilled-600M' target='_blank'>
        NLLB-200 Distilled 600M</a>
        </p>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
