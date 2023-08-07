import requests

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/<voice-id>"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": "32363b1aa61a9bdf1a852a054981ec61"
}

data = {
  "text": "Hi! My name is Bella, nice Anything elses to meet you!",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

response = requests.post(url, json=data, headers=headers)
with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
