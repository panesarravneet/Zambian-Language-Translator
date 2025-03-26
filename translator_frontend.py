import streamlit as st
from translator_backend import translate_en_to_nyanja, translate_nyanja_to_en

def main():
    st.set_page_config(
        page_title="Nyanja Translator",
        page_icon="🌍",
        layout="centered",
    )

    # Title
    st.markdown(
        """
        <h1 style='text-align: center; color: #2E86C1;'>
            English ↔ Nyanja Translator
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")

    # Implementation of drop down button
    direction = st.selectbox(
        "Select language direction:",
        ["English → Nyanja", "Nyanja → English"]
    )

    st.markdown("#### Enter text to translate:")
    user_text = st.text_area(
        label="",
        height=120,
        placeholder="Type or paste your text here..."
    )

    # Translate button
    if st.button("Translate"):
        if user_text.strip():
            with st.spinner("Translating..."):
                if direction == "English → Nyanja":
                    translation = translate_en_to_nyanja(user_text)
                else:
                    translation = translate_nyanja_to_en(user_text)

            st.success("Translation:")
            st.info(translation)
        else:
            st.warning("Please enter some text before translating.")

    st.write("---")
    st.markdown(
        """
        <p style='text-align: center; font-size: 0.85em; color: gray;'>
        Powered by <a href='https://huggingface.co/facebook/nllb-200-distilled-600M' target='_blank'>
        NLLB-200 Distilled 600M</a>
        </p>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
