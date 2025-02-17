"""
Manages conversation flow with enhanced error handling and user feedback. 
Supports emergency termination and auto-timeout features.
"""

from stt import speech_to_text
from tts import text_to_speech
from gemini_integration import generate_response
import streamlit as st
import time

# Constants
SILENCE_TIMEOUT = 15  # Seconds of inactivity before auto-close

def chatbot():
    """
    Main conversation loop handling voice input, AI responses, and system states.
    """
    # Session state initialization
    st.session_state.chat_active = True
    st.session_state.force_terminate = False
    last_activity_time = time.time()

    try:
        while True:
            # Priority 1: Check for emergency termination
            if st.session_state.force_terminate:
                _handle_termination()
                break

            # Priority 2: Check for normal stop or timeout
            if not st.session_state.chat_active or _check_timeout(last_activity_time):
                break

            # Voice input handling with progress indicator
            with st.spinner("🔄 Processing voice input..."):
                user_input = _get_voice_input()

            if user_input:
                # Update activity timer and handle response
                last_activity_time = time.time()
                _process_user_input(user_input)

                # Stop listening after successful response
                st.session_state.chat_active = False  # Add this line
                break  # Add this line to exit loop

    except SystemExit:
        # Clean exit for termination requests
        pass
    finally:
        # Removed audio cleanup, kept state cleanup
        if 'force_terminate' in st.session_state:
            del st.session_state.force_terminate
        # Always deactivate after processing
        st.session_state.chat_active = False

def _handle_termination():
    """Emergency termination procedure with user feedback"""
    st.toast("🚨 Emergency termination activated!", icon="💀")
    st.session_state.chat_active = False
    st.rerun()

def _check_timeout(last_activity):
    """Handles auto-close functionality with visual feedback"""
    elapsed = time.time() - last_activity
    if elapsed > SILENCE_TIMEOUT:
        st.warning(f"Session closed after {SILENCE_TIMEOUT}s of inactivity")
        st.session_state.chat_active = False
        st.rerun()
        return True
    return False

def _get_voice_input():
    """Safe voice input acquisition with error suppression"""
    try:
        if text := speech_to_text():
            return text.strip()
        st.info("No speech detected - try speaking louder")
    except Exception as e:
        st.error(f"Input error: {str(e)}")
        return None

def _process_user_input(user_input):
    """Handles AI response generation and output"""
    try:
        # Generate response with loading indicator
        with st.spinner("🤖 Generating AI response..."):
            response = generate_response(user_input)
        
        # Validate response before processing
        if not response.strip():
            raise ValueError("Empty response from AI")

        # Generate audio URI AND file into the pc
        audio_uri, audio_file = text_to_speech(response)
        
        # Update history with audio
        st.session_state.chat_history.extend([
            {"type": "user", "content": user_input},
            {
                "type": "bot", 
                "content": response,
                "audio_uri": audio_uri,
                "audio_file": audio_file
            }
        ])

        # Audio output with error handling
        with st.spinner("🔊 Generating voice response..."):
            text_to_speech(response)
        
        st.rerun()

    except Exception as e:
        st.error(f"Response error: {str(e)}")
        st.session_state.chat_active = False