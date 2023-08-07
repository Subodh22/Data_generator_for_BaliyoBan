import os
import threading
from tqdm import tqdm
from elevenlabs import voices, generate, play, save, set_api_key

set_api_key("32363b1aa61a9bdf1a852a054981ec61")

# Specify the folder containing your text files
folder_path = './TextFolder'

# Get a list of all text files in the specified directory
text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Function to generate audio and save it
def process_file(text_file, pbar):
    # Read the content of the text file
    with open(os.path.join(folder_path, text_file), 'r') as file:
        exercise_text = file.read()

    # Generate audio
    audio = generate(
      text=exercise_text,
      voice="Arnold",
      model="eleven_monolingual_v1"
    )
    
    # Save the audio file
    save(audio, f"{text_file.replace('.txt', '')}.wav")
    
    # Update the progress bar
    pbar.update(1)

# Create a progress bar
with tqdm(total=len(text_files)) as pbar:
    # List to keep track of threads
    threads = []

    # Start a new thread for each text file
    for text_file in text_files:
        thread = threading.Thread(target=process_file, args=(text_file, pbar))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()
