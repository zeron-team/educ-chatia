# transcribe_video.py
import warnings
import moviepy.editor as mp
import os
import whisper
import logging
from transformers import pipeline

# Configura el modelo de resumen (BART)
model_name = "facebook/bart-large-cnn"
summarizer = pipeline("summarization", model=model_name)

async def transcribe_audio_from_video(video_path):
    audio_path = "temp_audio.wav"
    
    try:
        # Suppress specific warnings
        warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")

        # Extract audio from video
        logging.info(f"Comenzando extracción de audio de {video_path}")
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, logger=None)
        logging.info("Audio extraction completed successfully.")

        # Load whisper model
        logging.info("Cargando Whisper model")
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        logging.info("Transcripción completada exitosamente.")

        return result['text']
    
    except Exception as e:
        logging.error(f"Error en transcribe_audio_from_video: {e}")
        raise e
    
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

def summarize_text(text):
    # Generar resumen con el modelo de transformers
    logging.info("Generando resumen con el modelo BART")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    summary_text = summary[0]['summary_text']
    logging.info(f"Resumen generado: {summary_text}")
    return summary_text
