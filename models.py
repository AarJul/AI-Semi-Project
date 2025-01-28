from transformers import AutoTokenizer, AutoModelForCausalLM
from openai import OpenAI
import google.generativeai as genai

# Load Hamid Reza GPT-2 Model
def load_hamid_reza_model():
    tokenizer = AutoTokenizer.from_pretrained("HamidRezaAttar/gpt2-product-description-generator")
    model = AutoModelForCausalLM.from_pretrained("HamidRezaAttar/gpt2-product-description-generator")
    return tokenizer, model

def generate_hamid_reza(prompt, tokenizer, model):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"],
        max_length=200,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Load Hugging Face Model (bprateek)
def load_bprateek_model():
    tokenizer = AutoTokenizer.from_pretrained("bprateek/product-description-generator")
    model = AutoModelForCausalLM.from_pretrained("bprateek/product-description-generator")
    return tokenizer, model

def generate_bprateek(prompt, tokenizer, model):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"],
        max_length=200,
        num_return_sequences=1,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# OpenAI ChatGPT Model
def get_openai_client(api_key):
    return OpenAI(api_key=api_key)

def generate_openai(prompt, client, model_name):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "商品説明を生成するプロフェッショナルなアシスタントとして行動してください。"},
            {"role": "user", "content": prompt},
        ],
        model=model_name,
        max_tokens=200,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Configure Gemini
def configure_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

# Gemini Base Prompt
def generate_gemini_base(prompt, gemini_model):
    response = gemini_model.generate_content(prompt)
    return response.text.strip()

# Gemini Custom Prompt
def generate_gemini_custom(product_title, gemini_model):
    prompt = f"{product_title}について商品詳細やお値段を教えてください"
    response = gemini_model.generate_content(prompt)
    return response.text.strip()
