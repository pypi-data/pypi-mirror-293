# condy/condy.py
import requests

def get_embeddings(text):
    url = "api.condy.ai/embeddings*with*tokens"
    params = {"text": text}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    return response.json()