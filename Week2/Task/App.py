import streamlit as st
from PIL import Image
from Image_Captioning import generate_caption
from database import save_result, load_results

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

                prediction = "hello"
                # prediction = classify_text(text)

            save_result("Text", text, prediction)

            st.success("Classification completed!")
            st.markdown("### Prediction")
            st.info(prediction)

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

                    prediction = "hello"
                    # prediction = classify_text(
                    #     st.session_state.caption
                    # )

                save_result(
                    "Image Caption",
                    st.session_state.caption,
                    prediction
                )

                st.success("Classification completed!")
                st.markdown("### 🎯 Prediction")
                st.success(prediction)

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
