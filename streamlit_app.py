import streamlit as st
import google.generativeai as genai

# Апп-ын үндсэн тохиргоо
st.set_page_config(page_title="Төслийн Үйлдвэр", page_icon="🏭", layout="wide")

# Зүүн талын цэс (Sidebar)
with st.sidebar:
    st.title("⚙️ Тохиргоо")
    api_key = st.text_input("Үйлдвэрийн түлхүүрээ (API Key) оруулна уу:", type="password")
    st.info("AI Studio-оос авсан түлхүүрээ энд оруулж үйлдвэрээ асаана уу.")
    st.markdown("---")
    st.write("Үйлдвэрийн төлөв: " + ("🟢 Ажиллахад бэлэн" if api_key else "🔴 Түлхүүр хүлээж байна"))

st.title("🏭 Төслийн Үйлдвэр: Удирдлагын Систем")
st.caption("Сүхбаатар аймаг, Баруун-Урт сум | Төсөл боловсруулах нэгдсэн төв")

# AI-тай холбогдох хэсэг
if api_key:
    try:
        genai.configure(api_key=api_key)
        # Таны Playground дээр сонгосон хамгийн шилдэг загвар
        model = genai.GenerativeModel('gemini-3.0-flash-preview') 
        
        # Чатны түүхийг хадгалах
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Хуучин чатуудыг харуулах
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Захирлын тушаал авах хэсэг
        if prompt := st.chat_input("Захирал аа, даалгавраа энд бичнэ үү..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Ажилчид тооцоолол хийж байна... ⏳")
                
                # AI-аас хариу авах
                response = model.generate_content(prompt)
                full_response = response.text
                
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
    except Exception as e:
        st.error(f"Алдаа гарлаа: {e}")
else:
    st.warning("⚠️ Захирал аа, үйлдвэрээ ажиллуулахын тулд зүүн талын цэсэнд 'Үйлдвэрийн түлхүүр'-ээ оруулна уу.")
    st.image("https://images.unsplash.com/photo-1518186285589-2f7649de83e0?auto=format&fit=crop&q=80&w=1000", caption="Төслийн үйлдвэр таны тушаалыг хүлээж байна.")
