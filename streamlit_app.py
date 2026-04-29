import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Төслийн Үйлдвэр", page_icon="🏭", layout="wide")

# Нууц шургуулганаас түлхүүр унших
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Secrets хэсэгт API Key хадгалагдаагүй байна!")
    st.stop()

st.title("🏭 Төслийн Үйлдвэр")
st.caption("Баруун-Урт сум | Төсөл боловсруулах төв")

# Ажилчдын жагсаалт
agents = ["АНХАА", "СУГАР", "МӨНХӨӨ", "ТОГТОХ", "ТУЯА", "БАТ-ОД", "НАРАА", "ЗӨВЛӨХ", "БҮГД"]

# --- АГЕНТ ДУУДАХ ТОВЧЛУУРУУД ---
st.write("📢 Ажилтан дуудах:")
cols = st.columns(len(agents))
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

for i, agent in enumerate(agents):
    if cols[i].button(agent):
        st.session_state.input_text = f"@{agent} "

# Чатны түүх
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Чат бичих хэсэг
prompt = st.chat_input("Даалгавраа бичнэ үү...", key="chat_input")

# Хэрэв товчлуур дарсан бол эсвэл текст бичсэн бол
final_prompt = prompt if prompt else ""
if st.session_state.input_text and not prompt:
    st.info(f"Сонгосон ажилтан: {st.session_state.input_text}. Одоо даалгавраа бичээд Enter дарна уу.")

if prompt:
    full_command = st.session_state.input_text + prompt
    st.session_state.messages.append({"role": "user", "content": full_command})
    with st.chat_message("user"):
        st.markdown(full_command)

    with st.chat_message("assistant"):
        response = model.generate_content(full_command)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    
    # Текстийг цэвэрлэх
    st.session_state.input_text = ""
