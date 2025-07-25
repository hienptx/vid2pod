from fastapi import FastAPI, BackgroundTasks
from pipeline import downloader, transcriber, translator, podcaster

app = FastAPI()

@app.post("/process/")
def process_video(url: str, target_lang: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_pipeline, url, target_lang)
    return {"status": "processing started"}

def run_pipeline(url: str, lang: str):
    audio_path = downloader.download_audio(url)
    transcript = transcriber.transcribe(audio_path)
    translated = translator.translate(transcript, lang)
    podcast_path = podcaster.generate_audio(translated)
    # Save podcast or notify user
