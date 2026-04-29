import streamlit as st
import google.generativeai as genai

# Апп-ын үндсэн тохиргоо
st.set_page_config(page_title="Төслийн Үйлдвэр", page_icon="🏭", layout="wide")

# Secrets-ээс түлхүүр унших
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = None

st.title("🏭 Төслийн Үйлдвэр: Удирдлагын Систем")
st.caption("Сүхбаатар аймаг, Баруун-Урт сум | Төсөл боловсруулах нэгдсэн төв")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Квот бага иддэг, хурдан Flash загвар
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Захирал аа, даалгавраа энд бичнэ үү..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Ажилчид тооцоолол хийж байна... ⏳")
                
                response = model.generate_content(prompt)
                full_response = response.text
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
    except Exception as e:
        st.error(f"Алдаа гарлаа: {e}")
else:
    st.warning("⚠️ Streamlit Settings -> Secrets хэсэгт GEMINI_API_KEY-ээ оруулна уу.")
