# ChatWatsonx

Simple Streamlit Chat Interface for IBM watsonx.ai Foundation Models

> Adapted from <https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps>

## Local 

### Build

```bash
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

## Image 

### Build

```bash
podman build -f Containerfile -t chatwatsonx
```

### Run

```bash
podman run -p 8501:8501 chatwatsonx:latest
```
