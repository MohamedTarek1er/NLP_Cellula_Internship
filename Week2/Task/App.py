import streamlit as st
from PIL import Image
from Image_Captioning import generate_caption
from database import save_result, load_results
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re


MODEL_PATH = r"C:\Users\moham\Downloads\NLP_Cellula\NLP_Cellula_Internship\Week2\Task\LSTM\lstm_model.keras"
TOKENIZER_PATH = r"C:\Users\moham\Downloads\NLP_Cellula\NLP_Cellula_Internship\Week2\Task\LSTM\tokenizer.pkl"
LABEL_ENCODER_PATH = r"C:\Users\moham\Downloads\NLP_Cellula\NLP_Cellula_Internship\Week2\Task\LSTM\label_encoder.pkl"

MAX_LEN = 28
model = tf.keras.models.load_model(MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

with open(LABEL_ENCODER_PATH, "rb") as f:
    label_encoder = pickle.load(f)

def Basic_clean_text(
    text,
    lowercase=True,
    remove_html=True,
    remove_urls=True,
    remove_emails=True,
    remove_mentions=True,
    remove_hashtags=True,
    remove_numbers=False,
    remove_punctuation=True,
    remove_extra_spaces=True,
    remove_newlines=True,
    remove_control_chars=True,
    normalize_repeated_chars=False,
    min_repeated_chars=3
):
    if text is None:
        return ""

    if not isinstance(text, str):
        text = str(text)

    if remove_html:
        text = re.sub(r"<[^>]+>", " ", text)

    if remove_urls:
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    if remove_emails:
        text = re.sub(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            " ",
            text
        )

    if remove_mentions:
        text = re.sub(r"(?<!\w)@\w+", " ", text)

    if remove_hashtags:
        text = re.sub(r"(?<!\w)#\w+", " ", text)
    else:
        text = re.sub(r"#(\w+)", r"\1", text)

    if remove_numbers:
        text = re.sub(r"\d+", " ", text)

    if normalize_repeated_chars:
        pattern = rf"(.)\1{{{min_repeated_chars},}}"
        text = re.sub(pattern, r"\1", text)

    if remove_punctuation:
        text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)

    if remove_newlines:
        text = re.sub(r"[\r\n\t]+", " ", text)

    if lowercase:
        text = text.lower()

    if remove_extra_spaces:
        text = re.sub(r"\s+", " ", text)

    return text.strip()

def predict_text(text):

    # 1. Clean
    cleaned_text = Basic_clean_text(text)

    # 2. Convert text → integer sequence
    sequence = tokenizer.texts_to_sequences([cleaned_text])

    # 3. Pad sequence
    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post",
        truncating="post"
    )

    # 4. Predict
    probabilities = model.predict(padded, verbose=0)

    # 5. Get class index
    predicted_index = probabilities.argmax(axis=1)[0]

    # 6. Convert index → class name
    predicted_label = label_encoder.inverse_transform(
        [predicted_index]
    )[0]

    confidence = probabilities[0][predicted_index]

    return predicted_label, confidence

st.set_page_config(
    page_title="Text & Image Classification",
    page_icon="🤖",
    layout="centered"
)

def get_caption(image):
    image = Image.open(image)
    return generate_caption(image)


if "caption" not in st.session_state:
    st.session_state.caption = None


st.title("🤖 Text & Image Classification")
st.markdown(
    """
    Enter text directly for classification, or upload an image
    to generate a caption and classify the caption.
    """
)

st.divider()
text_tab, image_tab, database_tab = st.tabs(
    [
        "📝 Text Classification",
        "🖼️ Image Classification",
        "📊 Database History"
    ]
)

with text_tab:
    st.subheader("Classify Text")

    text = st.text_area(
        "Enter your text:",
        height=150,
        placeholder="Type your text here..."
    )

    if st.button("🔍 Classify Text", use_container_width=True):
        if text.strip():

            with st.spinner("Classifying text..."):
                prediction, confidence = predict_text(text)

            save_result("Text", text, prediction)

            st.success("Classification completed!")
            st.markdown("### Prediction")
            st.info(prediction)
            st.metric("Confidence", f"{confidence:.2%}")

        else:
            st.warning("Please enter some text first.")


with image_tab:

    st.subheader("Classify Image")

    image = st.file_uploader(
        "Upload an image:",
        type=["jpg", "jpeg", "png"],
        help="Upload a JPG, JPEG, or PNG image."
    )

    if image:
        st.image(image, caption="Uploaded Image")

        st.divider()
        if st.button("✨ Generate Caption", use_container_width=True):

            with st.spinner("Generating caption with BLIP..."):
                st.session_state.caption = get_caption(image)

            st.success("Caption generated successfully!")

        if st.session_state.caption:
            st.markdown("### 📝 Generated Caption")

            st.info(st.session_state.caption)
            st.divider()

            if st.button("🔍 Classify Caption", use_container_width=True):

                with st.spinner("Classifying caption..."):
                    prediction, confidence = predict_text(st.session_state.caption)

                save_result(
                    "Image Caption",
                    st.session_state.caption,
                    prediction
                )

                st.success("Classification completed!")
                st.markdown("### 🎯 Prediction")
                st.success(prediction)
                st.metric("Confidence", f"{confidence:.2%}")

    else:
        st.info("👆 Upload an image to start.")


with database_tab:

    if "show_database" not in st.session_state:
        st.session_state.show_database = False

    st.divider()
    st.subheader("📊 Database")

    if st.button("📂 View Classification History", use_container_width=True):
        st.session_state.show_database = True


    if st.session_state.show_database:
        data = load_results()

        if not data.empty:
            st.markdown("### 📋 Stored Classification Records")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Records", len(data))
            col2.metric("Text Inputs", len(data[data["input_type"] == "Text"]))
            col3.metric("Image Captions", len(data[data["input_type"] == "Image Caption"]))

            st.divider()

            filter_type = st.selectbox("Filter records:",
                ["All", "Text", "Image Caption"])

            if filter_type == "All":
                filtered_data = data

            else:
                filtered_data = data[data["input_type"] == filter_type]

            st.dataframe(filtered_data, hide_index=True, use_container_width=True)

            if st.button("✖️ Hide Database",use_container_width=True):
                st.session_state.show_database = False
                st.rerun()

        else:
            st.info("📭 No classification records found.")
