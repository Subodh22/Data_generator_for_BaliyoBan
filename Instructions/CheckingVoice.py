from elevenlabs import voices, generate,play,save,set_api_key
set_api_key("32363b1aa61a9bdf1a852a054981ec61")
audio = generate(
  text="Lie flat on a bench with your feet firmly planted on the floor. Position your body so that your eyes are directly under the barbell when it's racked.Grip the barbell with both hands slightly wider than shoulder-width apart, using either a pronated grip (palms facing away from you) or a neutral grip (palms facing each other).",
  voice="Arnold",
  model="eleven_monolingual_v1"
)
play(audio)
save( audio,"kyle.wav")

# voices = voices()

# audio = generate(text="Hello there!", voice=voices[0])

# print(voices)