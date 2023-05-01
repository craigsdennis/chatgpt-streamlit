# ChatGPT Streamlit

A version of the [OpenAI ChatGPT UI](https://chat.openai.com/) written in [streamlit](https://streamlit.io). This is handy for workshops.

## Installation

Requires Python > 3.8 [Install](https://python.org)

You're going to need an [OpenAI API Key](https://platform.openai.com/account/api-keys)

If you are at an event, we'll share the key with you.

Copy `.env.example` to `.env` and update with the key.

```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the app

```
streamlit run explore.py
```
