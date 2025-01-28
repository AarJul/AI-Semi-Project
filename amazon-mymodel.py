import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
import io

# Load Hugging Face model and tokenizer
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("HamidRezaAttar/gpt2-product-description-generator")
    model = AutoModelForCausalLM.from_pretrained("HamidRezaAttar/gpt2-product-description-generator")
    return tokenizer, model

tokenizer, model = load_model()

# Streamlit App
st.title("AI Product Description Generator (Hugging Face Model)")

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
        # Process the uploaded image (Optional: Just for display here)
        image = Image.open(uploaded_image)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")

        # Prepare the input for the model
        prompt = f"Product: {product_title}\nDescription:"
        inputs = tokenizer(prompt, return_tensors="pt")

        # Generate text
        try:
            outputs = model.generate(
                inputs["input_ids"],
                max_length=200,
                num_return_sequences=1,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
            )
            description = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Display the generated description
            st.subheader("Generated Product Description:")
            st.write(description)

            # Display the uploaded image
            st.subheader("Uploaded Image:")
            st.image(uploaded_image, caption="Uploaded Product Image", use_column_width=True)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
