import streamlit as st
import google.generativeai as genai

# APIキーの設定
genai.configure(api_key="AIzaSyCa15FyEK78UAJGT-WkDzN9cVLF_LkrtXU")

# Geminiモデルの設定
model = genai.GenerativeModel('gemini-1.5-flash')

# ページ設定
st.set_page_config(page_title="商品詳細生成AI", page_icon="🤖", layout="wide")

# チャットページ
st.title("自動商品詳細生成システム・JS3")
st.title("どんな商品について聞きたいでしょう")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "AI"

# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 初回チャットかどうかを判定するフラグを初期化
if "is_first_message" not in st.session_state:
    st.session_state.is_first_message = True

# サイドバー：ダッシュボード表示
with st.sidebar:
    st.header("📋 Chat History")
    if st.session_state.chat_log:
        for idx, chat in enumerate(st.session_state.chat_log):
            if chat["name"] == USER_NAME:
                st.text(f"User: {chat['msg']}")
            elif chat["name"] == ASSISTANT_NAME:
                st.text(f"Assistant: {chat['msg']}")

    # チャットリセットボタン
    if st.button("Reset Chat"):
        if st.sidebar.checkbox("Are you sure?", key="confirm_reset"):
            st.session_state.chat_log = []
            st.session_state.is_first_message = True  # Reset the first message flag
            st.experimental_set_query_params()

# ユーザーからの入力
user_msg = st.chat_input("ここにメッセージを入力")

if user_msg:
    # 初回メッセージに特別な文言を追加
    if st.session_state.is_first_message:
        user_msg += "について商品詳細やお値段を教えてください"
        st.session_state.is_first_message = False  # 次回以降は通常のメッセージ

    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # 最新のメッセージを表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # メモリを利用して会話履歴を作成
    conversation_history = "\n".join(
        [f"{chat['name']}: {chat['msg']}" for chat in st.session_state.chat_log]
    )
    conversation_history += f"\n{USER_NAME}: {user_msg}\n{ASSISTANT_NAME}:"

    # AIモデルに会話履歴を渡して応答を生成
    response = model.generate_content(conversation_history)
    assistant_msg = response.text.strip()

    # アシスタントのメッセージを表示
    with st.chat_message(ASSISTANT_NAME):
        st.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
