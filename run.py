from dotenv import load_dotenv
from config.config import Config

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.llms import Ollama
import streamlit as st

# Cargar las variables de entorno
load_dotenv()

# Obtener todos los valores de configuración
config = Config.get_all()

llm = Ollama(model=config["model_ollama"])


def main():
    st.title(f"Chat con Memoria - {config['model_ollama']}")
    boot_name = st.text_input("Ingrese el nombre del Bot:", value="Jarvis")
    prompt = f"Erres un asistente virtual inteligente, te llamas {boot_name}, respondes a con respuestas cortas, ademas debes de conocer a tu usuario por ello debes de preguntarles cosas basicas al usuario de acorde al contexto"
    bot_description = st.text_area("Prompt del asistente virtual: ", value=prompt)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    chain = prompt_template | llm
    user_input = st.text_input("Escriba su pregunta:", key="user_input")

    if st.button("Enviar"):
        if user_input.lower() == "bye":
            st.stop()
        else:
            response = chain.invoke(
                {"input": user_input, "chat_history": st.session_state.chat_history}
            )
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(AIMessage(content=response))

    chat_show = ""
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            chat_show += f"Humano: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            chat_show += f"{boot_name}: {msg.content}\n"

    st.text_area("Chat", value=chat_show, height=400, key="chat_area")


if __name__ == "__main__":
    main()
