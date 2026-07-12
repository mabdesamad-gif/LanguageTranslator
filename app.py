import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

# -------------------------------------------------
# Custom CSS
# -------------------------------------------------

st.markdown("""
<style>

.main{
    padding-top:20px;
}

.stButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:18px;
    font-weight:bold;
}

textarea{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Languages Dictionary
# -------------------------------------------------

languages = {

    "Arabic":"ar",
    "Chinese":"zh-CN",
    "Dutch":"nl",
    "English":"en",
    "French":"fr",
    "German":"de",
    "Greek":"el",
    "Hindi":"hi",
    "Italian":"it",
    "Japanese":"ja",
    "Korean":"ko",
    "Polish":"pl",
    "Portuguese":"pt",
    "Russian":"ru",
    "Spanish":"es",
    "Swedish":"sv",
    "Turkish":"tr",
    "Urdu":"ur",
    "Vietnamese":"vi"

}

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "source_language" not in st.session_state:
    st.session_state.source_language = "English"

if "target_language" not in st.session_state:
    st.session_state.target_language = "French"

if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🌍 AI Language Translator")

st.markdown(
"""
Translate text instantly into multiple languages.

Built with ❤️ using:

- Python
- Streamlit
- Deep Translator
- Google Text To Speech
"""
)

st.divider()

# -------------------------------------------------
# Text Input
# -------------------------------------------------

text = st.text_area(
    "✍ Enter your text",
    height=180,
    placeholder="Type something here..."
)

# -------------------------------------------------
# Language Selection
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    source_language = st.selectbox(
        "From",
        list(languages.keys()),
        index=list(languages.keys()).index(
            st.session_state.source_language
        )
    )

with col2:

    target_language = st.selectbox(
        "To",
        list(languages.keys()),
        index=list(languages.keys()).index(
            st.session_state.target_language
        )
    )

# -------------------------------------------------
# Save Selected Languages
# -------------------------------------------------

st.session_state.source_language = source_language
st.session_state.target_language = target_language

# -------------------------------------------------
# Swap Button
# -------------------------------------------------

if st.button("🔄 Swap Languages"):

    st.session_state.source_language, st.session_state.target_language = (
        st.session_state.target_language,
        st.session_state.source_language,
    )

    st.rerun()

st.divider()

# -------------------------------------------------
# Translate Button
# -------------------------------------------------

translate = st.button(
    "🚀 Translate",
    use_container_width=True
)
# -------------------------------------------------
# Translation
# -------------------------------------------------

if translate:

    if text.strip() == "":
        st.warning("⚠ Please enter some text.")

    elif source_language == target_language:
        st.info("Source and target languages are the same.")

    else:

        source_code = languages[source_language]
        target_code = languages[target_language]

        try:

            translator = GoogleTranslator(
                source=source_code,
                target=target_code
            )

            translated_text = translator.translate(text)

            st.success("✅ Translation completed!")

            st.subheader("🌍 Translation")

            st.text_area(
                "Translated Text",
                translated_text,
                height=180
            )

            # ------------------------------------
            # Download Button
            # ------------------------------------

            st.download_button(
                label="📥 Download Translation",
                data=translated_text,
                file_name="translation.txt",
                mime="text/plain"
            )

            # ------------------------------------
            # Text To Speech
            # ------------------------------------

            st.subheader("🔊 Listen")

            try:

                tts_languages = {
                    "en":"en",
                    "fr":"fr",
                    "ar":"ar",
                    "es":"es",
                    "de":"de",
                    "it":"it",
                    "pt":"pt",
                    "ja":"ja",
                    "ko":"ko",
                    "ru":"ru",
                    "tr":"tr",
                    "hi":"hi",
                    "nl":"nl",
                    "pl":"pl",
                    "sv":"sv",
                    "el":"el",
                    "ur":"ur",
                    "vi":"vi"
                }

                if target_code in tts_languages:

                    tts = gTTS(
                        text=translated_text,
                        lang=tts_languages[target_code]
                    )

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp3"
                    ) as fp:

                        tts.save(fp.name)

                        with open(fp.name, "rb") as audio:

                            st.audio(
                                audio.read(),
                                format="audio/mp3"
                            )

                else:

                    st.info(
                        "🔈 Audio not available for this language."
                    )

            except Exception:

                st.warning(
                    "Unable to generate audio."
                )

            # ------------------------------------
            # Save History
            # ------------------------------------

            st.session_state.history.append(

                {
                    "from": source_language,
                    "to": target_language,
                    "input": text,
                    "output": translated_text
                }

            )

        except Exception as e:

            st.error("❌ Translation failed.")

            st.exception(e)

# -------------------------------------------------
# History
# -------------------------------------------------

if st.session_state.history:

    st.divider()

    st.subheader("🕘 Translation History")

    for item in reversed(st.session_state.history):

        with st.expander(
            f"{item['from']} ➜ {item['to']}"
        ):

            st.markdown("### ✍ Input")

            st.info(item["input"])

            st.markdown("### 🌍 Translation")

            st.success(item["output"])

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.caption(
    "Developed by Maissem Abdesmad ❤️ | CodeAlpha AI Internship"
)