from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator
from langdetect import detect

def detect_language(text):
    try:
        language_code = detect(text)
        return language_code
    except:
        # If language detection fails, return text or handle the exception as needed
        return text

def get_text_from_video(link):
    a = link.split("=")
    video_id = a[-1]
    try:
        raw_text = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
    except:
        raw_text = YouTubeTranscriptApi.get_transcript(video_id)

    text = '. '.join([line['text'] for line in raw_text])
    if detect_language(text)=='hi':
        # Break text into smaller chunks to prevent translation errors
        chunk_size = 500  # You can adjust this value based on your needs
        text_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

        # Translate each chunk separately
        translated_chunks = []
        translator = Translator()
        for chunk in text_chunks:
            translated_chunk = translator.translate(chunk, src='hi', dest='en')
            translated_chunks.append(translated_chunk.text)
        
        translated_text = '. '.join(translated_chunks)

        return translated_text
    else:
        return text

   
