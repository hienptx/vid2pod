import subprocess
import os

WHISPER_CPP_PATH = "/app/whisper.cpp"
MODEL_NAME = "ggml-base.en.bin"  # or "ggml-base.bin" for multilingual

def transcribe(audio_path: str, model_dir: str = "./models") -> str:
    model_path = os.path.join(model_dir, MODEL_NAME)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    command = [
        os.path.join(WHISPER_CPP_PATH, "main"),
        "-m", model_path,
        "-f", audio_path,
        "-otxt",  # Output .txt file
    ]

    print("Running:", " ".join(command))
    subprocess.run(command, check=True)

    txt_file = os.path.splitext(audio_path)[0] + ".txt"
    if not os.path.exists(txt_file):
        raise RuntimeError("Transcription failed: output file not found.")

    with open(txt_file, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    audio_file = "/home/mafalda/Projects/video2podcast/storage/Funniest Leadership Speech ever!.mp3"  # replace with your file
    result = transcribe(audio_file)
    print("Transcription result:\n", result)
