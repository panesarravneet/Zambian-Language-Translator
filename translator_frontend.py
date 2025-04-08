import streamlit as st
from translator_backend import (
    # NLLB
    translate_en_to_nyanja, translate_nyanja_to_en,
    translate_en_to_bemba,  translate_bemba_to_en,
    translate_en_to_swahili, translate_swahili_to_en,

    # Google - new languages
    translate_en_to_ndebele, translate_ndebele_to_en,
    translate_en_to_shona,   translate_shona_to_en,
    translate_en_to_zulu,    translate_zulu_to_en,
    # translate_en_to_lunda,   translate_lunda_to_en,
    # translate_en_to_kaonde,  translate_kaonde_to_en,
    # translate_en_to_tonga,   translate_tonga_to_en,
    # translate_en_to_luvale,  translate_luvale_to_en,
    # translate_en_to_lozi,    translate_lozi_to_en
)

def main():
    st.set_page_config(page_title="Zambian Languages Translator", page_icon="🌍", layout="centered")
    st.markdown(
        """
        <h2 style='text-align: center; color: #2E86C1; margin-top: 0;'>
            Zambian Language Translator
        </h2>
        """,
        unsafe_allow_html=True
    )
    st.write("Press **Enter** or click **Translate** to see results.")

    # Full set of directions
    directions = [
        # NLLB-based
        "English → Nyanja",  "Nyanja → English",
        "English → Bemba",   "Bemba → English",
        "English → Swahili", "Swahili → English",

        # Google-based for new languages
        "English → Ndebele", "Ndebele → English",
        "English → Shona",   "Shona → English",
        "English → Zulu",    "Zulu → English",
        # "English → Lunda",   "Lunda → English",
        # "English → Kaonde",  "Kaonde → English",
        # "English → Tonga",   "Tonga → English",
        # "English → Luvale",  "Luvale → English",
        # "English → Lozi",    "Lozi → English",
    ]

    with st.form("translation_form"):
        direction = st.selectbox("Select translation direction:", directions)
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
                elif direction == "Swahili → English":
                    translation = translate_swahili_to_en(user_text)

                elif direction == "English → Ndebele":
                    translation = translate_en_to_ndebele(user_text)
                elif direction == "Ndebele → English":
                    translation = translate_ndebele_to_en(user_text)
                elif direction == "English → Shona":
                    translation = translate_en_to_shona(user_text)
                elif direction == "Shona → English":
                    translation = translate_shona_to_en(user_text)
                elif direction == "English → Zulu":
                    translation = translate_en_to_zulu(user_text)
                elif direction == "Zulu → English":
                    translation = translate_zulu_to_en(user_text)
                # elif direction == "English → Lunda":
                #     translation = translate_en_to_lunda(user_text)
                # elif direction == "Lunda → English":
                #     translation = translate_lunda_to_en(user_text)
                # elif direction == "English → Kaonde":
                #     translation = translate_en_to_kaonde(user_text)
                # elif direction == "Kaonde → English":
                #     translation = translate_kaonde_to_en(user_text)
                # elif direction == "English → Tonga":
                #     translation = translate_en_to_tonga(user_text)
                # elif direction == "Tonga → English":
                #     translation = translate_tonga_to_en(user_text)
                # elif direction == "English → Luvale":
                #     translation = translate_en_to_luvale(user_text)
                # elif direction == "Luvale → English":
                #     translation = translate_luvale_to_en(user_text)
                # elif direction == "English → Lozi":
                #     translation = translate_en_to_lozi(user_text)
                # else:  # "Lozi → English"
                #     translation = translate_lozi_to_en(user_text)

            st.success("Translation:")
            st.info(translation)

if __name__ == "__main__":
    main()
