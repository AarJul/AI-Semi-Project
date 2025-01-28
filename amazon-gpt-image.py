import os
import streamlit as st
from openai import OpenAI
from PIL import Image
import io

# Initialize OpenAI client
client = OpenAI(
    api_key="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"  # Replace with your OpenAI API key
)

# Streamlit App
st.title("AI Product Description Generator")

st.write("Upload a product image and provide the product title to generate a compelling description!")

# Image Upload
uploaded_image = st.file_uploader("Upload Product Image", type=["png", "jpg", "jpeg"])

# Text Input Field for Product Title
product_title = st.text_input("Product Title", placeholder="e.g., Wireless Bluetooth Earbuds")

# Button to Generate Description
if st.button("Generate Product Description"):
    if not uploaded_image:
        st.warning("Please upload an image.")
    elif not product_title:
        st.warning("Please provide a product title.")
    else:
        # Process the uploaded image (Optional: Can be integrated with a vision model later)
        image = Image.open(uploaded_image)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_data = image_bytes.getvalue()

        # GPT-3.5-Turbo Prompt
        prompt = f"""
        You are an expert product copywriter. Write a detailed and engaging product description based on the following:
        
        Title: {product_title}
        """

        try:
            # OpenAI Chat Completion API Call
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant skilled in writing product descriptions."},
                    {"role": "user", "content": prompt},
                ],
                model="gpt-4o-mini",
                max_tokens=200,
                temperature=0.7,
            )

            # Extract and display the generated description
            description = chat_completion.choices[0].message.content
            st.subheader("Generated Product Description:")
            st.write(description)

            # Display uploaded image
            st.subheader("Uploaded Image:")
            st.image(uploaded_image, caption="Uploaded Product Image", use_column_width=True)

        except Exception as e:  # Catch all exceptions
            st.error(f"An error occurred: {str(e)}")
