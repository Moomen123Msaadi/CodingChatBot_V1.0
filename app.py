"""
Main Streamlit application interface for the chatbot
Handles UI layout and state management
"""

import streamlit as st
from chatbot import chatbot

# UI Layout
st.title("Voice Chatbot for Coding")
st.write("Ask a coding question and the chatbot will respond!")

# Initialize session states
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'time_left' not in st.session_state:
    st.session_state.time_left = 0

# Real-time timer display
timer_placeholder = st.empty()
if st.session_state.chat_active:
    timer_placeholder.markdown(
        f"⏳ **Auto-close in:** {st.session_state.time_left}s | "
        f"Click Stop Chat button to end session immediately"
    )
else:
    timer_placeholder.empty()

# Chat history display
with st.expander("Conversation History", expanded=True):

    if not st.session_state.chat_history:
        st.info("No conversation history yet")

    for entry in st.session_state.chat_history:
        if entry["type"] == "user":
            st.markdown(f"**You:**\n {entry['content']}")
        else:
            st.markdown(f"**Bot:**\n {entry['content']}")

            if entry.get("audio_uri"):
                # Browser player
                st.audio(entry["audio_uri"], format="audio/mp3")
                
            if entry.get("audio_file"):
                # File location info
                st.caption(f"Audio saved at: `{entry['audio_file']}`")

col1, col2 = st.columns(2)

# Add to session state initialization
if 'force_terminate' not in st.session_state:
    st.session_state.force_terminate = False

# Add this button AFTER the existing columns
st.markdown("---")  # Visual separator
if st.button("☢️ TERMINATE", 
            type="primary", 
            disabled=not st.session_state.chat_active,
            help="Nuclear option - stops ALL operations immediately"):
    # Set termination flags
    st.session_state.chat_active = False
    st.session_state.force_terminate = True
    
    # Force immediate refresh
    st.rerun()

with col1:
    if st.button("Start Chat", disabled=st.session_state.chat_active) and not st.session_state.chat_active:
        st.session_state.chat_active = True
        st.session_state.force_terminate = False
        st.session_state.chat_history = []
        #st.rerun()
        chatbot()
        
with col2:
    if st.button("Stop Chat") and st.session_state.chat_active:
        st.session_state.chat_active = False
        st.rerun()

# Start chatbot logic if active
if st.session_state.chat_active:
    chatbot()
