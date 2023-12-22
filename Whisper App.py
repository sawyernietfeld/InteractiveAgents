import torch
import whisper

def transcribe_audio(file_path):
    # Check if GPU is available
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load the Whisper model on the specified device
    model = whisper.load_model("large-v3", device=device)

    # Load the audio file and transcribe it
    result = model.transcribe(file_path)

    # Print the transcription
    print(result["text"])

# Replace 'path_to_your_audio_file' with the path to your audio file
audio_file_path = r"C:\Users\..."
transcribe_audio(audio_file_path)