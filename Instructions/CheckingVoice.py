from elevenlabs import voices, generate,play,save,set_api_key
set_api_key("32363b1aa61a9bdf1a852a054981ec61")
 
audio = generate(
  text="Get ready... you got 5...... 4...... 3...... 2....... 1.....",
  voice="Arnold",
  model="eleven_monolingual_v1",
  
  
)
play(audio)
save( audio,"./next.wav")

# voices = voices()

# audio = generate(text="Hello there!", voice=voices[0])

# print(voices)