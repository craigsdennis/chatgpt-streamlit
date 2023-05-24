from dotenv import load_dotenv

load_dotenv()

import json
import os
import requests
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)

"""
# HackGPT Playground

Dive in and get your hands dirty with OpenAI. Don't worry you won't break anything.
"""

with st.expander("📚 Learn more"):
    """
    - [OpenAI Completion Introduction](https://platform.openai.com/docs/guides/completion/introduction)
    - [Learn Prompting](https://learnprompting.org)
    - [Awesome Prompts](https://prompts.chat)
    """

@st.cache_resource
def get_chat(model_name, temperature=0.7):
    return ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=None)


model_name = st.sidebar.selectbox(
    label="Which model OpenAI should be used?",
    options=["gpt-3.5-turbo", "gpt-4"],
    key="model_name",
)
temperature = st.sidebar.number_input(
    "What temperature should we set things",
    min_value=0.0,
    max_value=2.0,
    value=0.7,
    step=0.1,
    help="""
    What sampling temperature to use, between 0 and 2.
    
    Higher values like 0.8 will make the output more random, 
    while lower values like 0.2 will make it more focused and deterministic.
    """
)
chat = get_chat(model_name, temperature)


if "system_locked" not in st.session_state:
    st.session_state["system_locked"] = False

system_prompter = st.sidebar.text_area(
    "How should the system behave?",
    key="system_prompter",
    help="""
    This is the ChatGPT System Prompt. 
    
    For inspiration checkout [Awesome Prompts](https://prompts.chat)
    """,
    disabled=st.session_state["system_locked"],
)


def reset():
    st.session_state["system_locked"] = False
    st.session_state["history"] = []
    st.balloons()


if st.session_state["system_locked"]:
    with st.sidebar:
        st.button(label="Reset Chat ❌", on_click=reset)
if "history" not in st.session_state:
    st.session_state["history"] = []
else:
    st.markdown("### Chat History")


def remove_response_and_prompt(response_index):
    prompt_index = response_index - 1
    prompt = st.session_state["history"].pop(prompt_index)
    print(f"Removing prompt {prompt}")
    # Note since the list has shifted up we are using the same index
    ai = st.session_state["history"].pop(prompt_index)
    print(f"Removing ai result: {ai}")


for index, message in enumerate(st.session_state["history"]):
    if isinstance(message, HumanMessage):
        st.markdown(f"#### {message.content}")
    elif isinstance(message, AIMessage):
        st.markdown(message.content)
        st.button(
            "Remove this prompt",
            key=f"remove_{index}",
            on_click=remove_response_and_prompt,
            args=(index,),
        )


if st.session_state["history"]:
    number_of_tokens = chat.get_num_tokens_from_messages(st.session_state["history"])
    st.markdown(
        f"**Number of Tokens used in current conversation**: {number_of_tokens}"
    )


def submit_chat():
    messages = st.session_state["history"]
    if not messages:
        messages.append(SystemMessage(content=system_prompter))
    messages.append(HumanMessage(content=st.session_state.chat_prompter))
    ai_message = chat(messages)
    messages.append(ai_message)
    st.session_state["history"] = messages
    st.session_state["system_locked"] = True
    st.session_state.chat_prompter = ""


with st.form("chat_prompt"):
    chat_prompter = st.text_area(
        "What would you like to ask your assistant?", key="chat_prompter"
    )
    st.form_submit_button("Ask", on_click=submit_chat)


def import_json(json_obj):
    messages = messages_from_dict(json_obj)
    st.session_state["history"] = messages
    st.session_state["system_prompter"] = messages[0].content
    st.session_state["system_locked"] = True
    st.balloons()


def import_json_url():
    url = st.session_state["json_url"]
    response = requests.get(url)
    json = response.json()
    return import_json(json)


with st.sidebar:
    with st.expander("Additional storage and retrieval options"):
        with st.form("import_json_url"):
            json_url = st.text_input("Import from JSON URL", key="json_url")
            st.form_submit_button("Import", on_click=import_json_url)

        st.markdown("#### Raw JSON")
        st.code(json.dumps(messages_to_dict(st.session_state["history"])))
