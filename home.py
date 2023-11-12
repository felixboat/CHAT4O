import streamlit as st
# import openai
from openai import OpenAI
from datetime import datetime
import usrauth
import downchatpdf
import downchattxt
import string
import trsfjson
import base64

# User authentication
if not usrauth.check_password():
    st.stop()


# Setup variables
user_chat = string.capwords(st.session_state['user_chat'])
usr_api_key = st.session_state['api_key']
OPENAI_API_KEY = usr_api_key
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL_NAME = ['gpt-3.5-turbo', 'gpt-3.5-turbo-1106', 'gpt-4', 'gpt-4-0613', 'gpt-4-1106-preview']

# Main Streamlit app starts here
st.title("Chatbot Current Session")

# Sidebar options
st.sidebar.title("AI Model & Configuration")
llm_model = st.sidebar.selectbox("Select LLM Model", MODEL_NAME, index=4)
temperature_model = st.sidebar.slider("Select Temperature", min_value=0.0, max_value=1.0, value=0.1, step=0.1)
# print(llm_model)
# print(temperature_model)

# Define states for refresh of the main page
if "page" not in st.session_state:
    st.session_state.page = 0


# def nextpage():
#     st.session_state.page += 1

def restart():
    st.session_state.page = 0


if st.sidebar.button("New Chat Session", on_click=restart):
    # Reset the chat history
    st.session_state.messages = []
    st.session_state["messages"] = [{"role": "assistant", "content": f"Hello {user_chat}! How can I help you?"}]

if st.sidebar.button("Download Current Session"):
    current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    txt_name = "Conversation" + "_" + current_date + ".txt"
    chat_log_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    buffer = downchattxt.get_text_file_buffer(chat_log_str)
    b64 = base64.b64encode(buffer.getvalue().encode()).decode()
    st.sidebar.markdown(f'<a href="data:file/txt;base64,{b64}" download={txt_name}>Download Chat Log</a>',
                        unsafe_allow_html=True)
    # pdf_name = "Conversation" + "_" + current_date + ".pdf"
    #
    # all_messages = trsfjson.transform_msg_json(st.session_state.messages)
    # output_text = ""
    # for message in all_messages:
    #     output_text += f"{message['role']}: {message['content']}\n"
    #
    # output_text_strp = output_text.strip()
    #
    # downchatpdf.download_messages(output_text_strp, pdf_name)

# Prepare placeholder to clear all the messages
placeholder = st.empty()

if st.session_state.page == 0:
    with placeholder.container():
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": f"Hello {user_chat}! How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            # Integrate with the OpenAI API to get the response
            response = client.chat.completions.create(model=llm_model, messages=st.session_state.messages,
                                                      temperature=temperature_model)

            msg = response.choices[0].message
            msg_content = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg_content})
            st.chat_message("assistant").write(msg.content)
# else:
#     with placeholder:
#         st.sidebar.button("New Chat Session", on_click=restart)
