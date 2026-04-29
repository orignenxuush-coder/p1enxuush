import streamlit as st
import google.generativeai as genai

# Апп-ын тохиргоо
st.set_page_config(page_title="Төслийн Үйлдвэр", page_icon="🏭", layout="wide")

# Secrets-ээс API Key унших
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Файл боловсруулах чадвартай модель
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ API Key олдсонгүй!")
    st.stop()

# --- SIDEBAR: ФАЙЛ ОРУУЛАХ ХЭСЭГ ---
with st.sidebar:
    st.title("📂 Мэдээллийн сан")
    uploaded_file = st.file_uploader("Файл оруулах (Зураг, PDF, Текст)", type=['png', 'jpg', 'jpeg', 'pdf', 'txt'])
    
    if uploaded_file is not None:
        st.success(f"✅ {uploaded_file.name} амжилттай орлоо.")
        # Зургийг харах боломжтой
        if uploaded_file.type.startswith('image/'):
            st.image(uploaded_file, caption='Оруулсан зураг', use_container_width=True)

st.title("🏭 Төслийн Үйлдвэр: Удирдлагын Систем")

# ... (өмнөх товчлууртай код хэвээрээ байна) ...
# Даалгавар илгээх хэсэгт дараах логикийг нэмнэ:
if prompt:
    input_data = [full_command]
    if uploaded_file:
        # Хэрэв файл оруулсан бол түүнийг модельд илгээхээр бэлдэнэ
        import PIL.Image
        if uploaded_file.type.startswith('image/'):
            img = PIL.Image.open(uploaded_file)
            input_data.append(img)
            
    with st.chat_message("assistant"):
        # Файлтай болон файлгүй хүсэлтийг явуулна
        response = model.generate_content(input_data)
        st.markdown(response.text)
