from gtts import gTTS
import base64
from io import BytesIO
import os
from datetime import datetime

def text_to_speech(text) -> tuple:
    """Convert text to speech, save as MP3, and return data URI"""
    try:
        # Create directory if needed
        os.makedirs("audio_history", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_history/response_{timestamp}.mp3"
        
        # Create in-memory and file versions
        tts = gTTS(text=text, lang='en')
        
        # Save to file
        tts.save(filename)
        
        # Create data URI for browser
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        data_uri = f"data:audio/mp3;base64,{audio_base64}"
        
        return data_uri, filename
        
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return None, None