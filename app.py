from dotenv import load_dotenv
from config.config import Config
from groq import Groq
import streamlit as st


# Cargar las variables de entorno
load_dotenv()

# Obtener todos los valores de configuración
config = Config.get_all()

# Client
client = Groq()


def ai_request(messages):
    completion = client.chat.completions.create(
        model=config["model"],
        messages=messages,
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        stream=True,
    )
    response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
    print("Respuesta de Groq:\n", response)

    return response


def main():
    st.title(f"Chat con Memoria - {config['model']}")
    st.write(
        "! Bienvenido al Chat con ElysIA...!, escribe 'end' para terminar la conversacion."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def submit():
        user_input = st.session_state.user_input
        if user_input.lower() == "end":
            st.write("Nos vemos, bye...!")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Consultando a ElysIA..."):
            ai_answer = ai_request(st.session_state.messages)
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_answer}
            )

        st.session_state.user_input = ""

    for m in st.session_state.messages:
        role = "Tu " if m["role"] == "user" else "Bot "
        st.write(f"**{role}:** {m['content']}")

    with st.form(key="chat_form", clear_on_submit=True):
        st.text_input("Tu: ", key="user_input")
        submit_button = st.form_submit_button(label="Enviar", on_click=submit)


if __name__ == "__main__":
    main()
