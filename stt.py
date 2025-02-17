"""
Handles voice input using microphone and converts to text using Google Speech Recognition.
"""
import speech_recognition as sr
import streamlit as st


def speech_to_text():
    # Captures audio input and converts to text. 
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.session_state.chat_active = True
        try:
            audio = recognizer.listen(source, timeout=8)
            try:
                text = recognizer.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                st.warning("Could not understand audio")
                return None
        except sr.WaitTimeoutError:
            return None
        except Exception as e:  # Added general exception handling
            st.error(f"Microphone error: {str(e)}")
            return None