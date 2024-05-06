import os
from litellm import completion
import streamlit as st
import requests

watsonx_url = "https://us-south.ml.cloud.ibm.com"
model_spec_endpt = "/ml/v1/foundation_model_specs"
version = "version=2024-05-06"
default_model = "meta-llama/llama-3-70b-instruct"


def get_models():
    url = f"{watsonx_url}{model_spec_endpt}?{version}"
    res = requests.get(url).json()
    models = res["resources"]
    filtered_models = (
        model
        for model in models
        if any(func["id"] == "text_generation" for func in model["functions"])
    )
    for model in filtered_models:
        yield model


def get_model_ids():
    return (model["model_id"] for model in get_models())


st.title("ChatWatsonx")

with st.sidebar:
    os.environ["WATSONX_URL"] = watsonx_url

    if not os.environ.get("WATSONX_API_KEY"):
        watsonx_api_key = st.text_input("Watsonx API Key", type="password")
        os.environ["WATSONX_API_KEY"] = watsonx_api_key

    if not os.environ.get("WATSONX_PROJECT_ID"):
        watsonx_project_id = st.text_input("Watsonx Project ID", type="password")
        os.environ["WATSONX_PROJECT_ID"] = watsonx_project_id

    model_ids = list(get_model_ids())
    model_id = st.selectbox(
        "Select a model:",
        model_ids,
        index=model_ids.index(default_model),
    )

    st.header("Hyperparameters")
    max_tokens = st.slider("Max New Tokens", min_value=2, max_value=2000, value=500)
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0, step=0.05, value=0.5
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is IBM?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = completion(
            model=f"watsonx/{model_id}",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
        stream = (chunk.choices[0].delta.content for chunk in stream)
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": str(response)})
