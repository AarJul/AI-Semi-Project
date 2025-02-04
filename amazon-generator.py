import streamlit as st
from PIL import Image
import io
from models import (
    load_hamid_reza_model,
    generate_hamid_reza,
    load_bprateek_model,
    generate_bprateek,
    get_openai_client,
    generate_openai,
    configure_gemini,
    generate_gemini_base,
    generate_gemini_custom,
)
import time  # For loading animation

# Set Streamlit page config (MUST be the first Streamlit command)
st.set_page_config(page_title="商品説明生成AI", page_icon="🤖", layout="wide")

# Load models
@st.cache_resource
def load_models():
    hamid_tokenizer, hamid_model = load_hamid_reza_model()
    bprateek_tokenizer, bprateek_model = load_bprateek_model()
    openai_client = get_openai_client("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")  # Replace with your OpenAI API key
    gemini_model = configure_gemini("AIzaSyCa15FyEK78UAJGT-WkDzN9cVLF_LkrtXU")  # Replace with your Gemini API key
    return hamid_tokenizer, hamid_model, bprateek_tokenizer, bprateek_model, openai_client, gemini_model

hamid_tokenizer, hamid_model, bprateek_tokenizer, bprateek_model, openai_client, gemini_model = load_models()

# Streamlit App in Japanese
st.title("商品説明自動生成AIツール🤖")

# Sidebar for history
st.sidebar.title("履歴")

if "history" not in st.session_state:
    st.session_state.history = []

# Reset button
if st.sidebar.button("リセット"):
    st.session_state.history = []

# Display history with dropdowns
if st.session_state.history:
    for idx, entry in enumerate(reversed(st.session_state.history), 1):
        product_title = entry.get("product_title", "商品名なし")
        model_name = entry.get("model", "モデル不明")

        with st.sidebar.expander(f"📌 {idx}. {product_title} ({model_name})"):
            st.write(entry["description"])

# Main app inputs
st.write("商品画像をアップロードし、商品名を入力してください。AIが最適な商品説明を生成します。")

uploaded_image = st.file_uploader("商品画像をアップロード (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])
product_title = st.text_input("商品名", placeholder="例: ワイヤレスイヤホン")

model_choice = st.radio(
    "モデルを選択してください:",
    options=["GPT-4o-mini(クレジットにより使用不可可能性あり)", "Gemini", "アーロンモデル終号機", "アーロンモデル零号機", "アーロンモデル初号機"],
)

# Generate description button
if st.button("商品説明を生成"):
    if not product_title.strip():  # Only check product title (image is optional)
        st.warning("商品名を入力してください。")
    else:
        try:
            # Create a placeholder for the animation
            loading_placeholder = st.empty()

            # Animate loading dots (loop while waiting for response)
            for _ in range(10):  
                for dots in ["", ".", "..", "..."]:
                    loading_placeholder.markdown(f"### ⏳ AIが生成中です{dots}")
                    time.sleep(0.5)  # Adjust speed for effect

            # Generate description based on selected model
            if model_choice == "GPT-4o-mini(クレジットにより使用不可の可能性あり)":
                description = generate_openai(f"商品名: {product_title}\n詳細:", openai_client, "gpt-4o-mini")
            elif model_choice == "Gemini":
                description = generate_gemini_base(f"商品名: {product_title}\n詳細:", gemini_model)
            elif model_choice == "アーロンモデル終号機":
                description = generate_gemini_custom(product_title, gemini_model)
            elif model_choice == "アーロンモデル零号機":
                description = generate_hamid_reza(f"商品名: {product_title}\n詳細:", hamid_tokenizer, hamid_model)
            elif model_choice == "アーロンモデル初号機":
                description = generate_bprateek(f"商品名: {product_title}\n詳細:", bprateek_tokenizer, bprateek_model)
            else:
                description = "無効なモデルが選択されました。"

            # Clear the loading animation
            loading_placeholder.empty()

            # Display result before the image
            st.subheader(f"✅ 生成された商品説明 ({model_choice}):")
            st.write(f"**商品名:** {product_title}")
            st.write(description)

            # Display uploaded image only if provided
            if uploaded_image:
                st.subheader("アップロードされた画像:")
                st.image(uploaded_image, caption="アップロードされた商品画像", width=300, use_container_width=False)

            # Add to history
            st.session_state.history.append({
                "product_title": product_title,
                "model": model_choice,
                "description": description
            })

        except Exception as e:
            st.error(f"❌ エラーが発生しました: {str(e)}")