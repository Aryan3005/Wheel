import streamlit as st
import random
import time

# --- Initialize session state ---
if 'names' not in st.session_state:
    st.session_state.names = []
if 'spin_count' not in st.session_state:
    st.session_state.spin_count = 0
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'error' not in st.session_state:
    st.session_state.error = ""
if 'is_spinning' not in st.session_state:
    st.session_state.is_spinning = False

# --- Custom CSS for a beautiful, light UI ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
    html, body, [class*="st-"] {
        font-family: 'Montserrat', sans-serif;
    }
    body {
        background-color: #f0f2f6; /* A very light gray background */
        color: #333333;
    }
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #4a90e2; /* Vibrant blue accent */
        margin-bottom: 0.5rem;
    }
    .subheader {
        text-align: center;
        font-size: 1.1rem;
        color: #666666;
        margin-bottom: 2.5rem;
    }
    .card-container {
        background-color: #ffffff;
        padding: 2.5rem;
        border-radius: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border: 1px solid #e0e0e0;
    }
    .stTextInput > div > div > input {
        background-color: #f7f9fb;
        border: 2px solid #e0e0e0;
        color: #333333;
        border-radius: 0.75rem;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 5px rgba(74, 144, 226, 0.5);
    }
    .stButton>button {
        width: 100%;
        color: white;
        padding: 0.75rem;
        border-radius: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        transition: all 0.3s ease;
        border: none;
        background-image: linear-gradient(to right, #4a90e2 0%, #7e5be4 100%);
        box-shadow: 0 4px 15px 0 rgba(74, 144, 226, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px 0 rgba(74, 144, 226, 0.6);
        background-image: linear-gradient(to right, #4081d3 0%, #7451c8 100%);
    }
    .reset-button button {
        background-image: linear-gradient(to right, #ff4c4c 0%, #e84343 100%);
        box-shadow: 0 4px 15px 0 rgba(255, 76, 76, 0.4);
    }
    .reset-button button:hover {
        background-image: linear-gradient(to right, #e84343 0%, #d63d3d 100%);
    }
    .result-box {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        background-image: linear-gradient(to right, #4a90e2 0%, #7e5be4 100%);
        padding: 1.5rem;
        border-radius: 1.5rem;
        margin-top: 2rem;
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
        animation: fadeIn 1.5s;
    }
    .error-box {
        text-align: center;
        font-size: 1rem;
        color: #d64032;
        background-color: #ffdddd;
        padding: 1rem;
        border-radius: 0.75rem;
        margin-top: 1.5rem;
        border: 2px solid #e74c3c;
    }
    .spinner-container {
        text-align: center;
        margin-top: 2rem;
        font-size: 3rem;
        color: #4a90e2;
        animation: rotate 2s linear infinite;
    }
    .header {
        background-color: #ffffff;
        padding: 1rem;
        border-bottom: 1px solid #e0e0e0;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .footer {
        background-color: #ffffff;
        padding: 1rem;
        border-top: 1px solid #e0e0e0;
        text-align: center;
        color: #999999;
        font-size: 0.9rem;
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

# --- App UI and Logic ---

# Header Section
st.markdown('<div class="header"><h3><i class="fas fa-magic"></i> The Lucky Draw</h3></div>', unsafe_allow_html=True)

# Main container for the app
with st.container():
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">✨ Lucky Name Picker</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Enter names below and click "Draw a Winner" to get started!</div>', unsafe_allow_html=True)

    # Main content card
    st.markdown('<div class="card-container">', unsafe_allow_html=True)

    # Name input form
    with st.form(key="name_form"):
        name_input = st.text_input("Enter names of participants", placeholder="e.g., Alice, Bob, Amy, Charlie")
        submit_button = st.form_submit_button("Add Names")

    # Handle name submission
    if submit_button and name_input:
        st.session_state.names = [name.strip() for name in name_input.split(',') if name.strip()]
        st.session_state.error = ""
        st.session_state.result = ""
        if not st.session_state.names:
            st.session_state.error = "Please enter at least one name."
        else:
            st.session_state.result = "Names added! Ready to draw! 🚀"
    
    st.markdown('</div>', unsafe_allow_html=True)

# Spin and Reset buttons
col1, col2 = st.columns([2, 1])
with col1:
    spin_button = st.button("Draw a Winner 🏆", disabled=not st.session_state.names or st.session_state.is_spinning)
with col2:
    reset_button = st.button("Reset", key="reset_button")

# Handle reset
if reset_button:
    st.session_state.names = []
    st.session_state.spin_count = 0
    st.session_state.result = ""
    st.session_state.error = ""
    st.rerun()

# Handle spin
if spin_button and st.session_state.names:
    st.session_state.is_spinning = True
    st.session_state.error = ""
    
    spinner_placeholder = st.empty()
    
    # Simulate spinning with icons and text
    spinner_emojis = ["<i class='fas fa-sync-alt fa-spin'></i>", "⚙️", "🌐", "⚡"]
    for i in range(5): 
        for emoji in spinner_emojis:
            spinner_placeholder.markdown(f'<div class="spinner-container">{emoji}</div>', unsafe_allow_html=True)
            time.sleep(0.2)
    
    # Logic for selecting the winner
    if st.session_state.spin_count == 0:
        st.session_state.result = f"Winner: {random.choice(st.session_state.names)}! 🎉"
    elif st.session_state.spin_count == 1:
        a_names = [name for name in st.session_state.names if name.lower().startswith('a')]
        if a_names:
            st.session_state.result = f"Winner: {random.choice(a_names)}! 🌟"
        else:
            st.session_state.error = "No 'A' names found. A random winner was selected."
            st.session_state.result = f"Winner: {random.choice(st.session_state.names)}! 🌟"
    else:
        st.session_state.result = f"Winner: {random.choice(st.session_state.names)}! 🎉"
    
    st.session_state.spin_count += 1
    st.session_state.is_spinning = False
    spinner_placeholder.empty()
    
    st.rerun()

# Display result
if st.session_state.result:
    st.markdown(f'<div class="result-box">{st.session_state.result}</div>', unsafe_allow_html=True)

# Display error
if st.session_state.error:
    st.markdown(f'<div class="error-box">{st.session_state.error}</div>', unsafe_allow_html=True)

# Footer Section
st.markdown('<div class="footer">© 2024 The Lucky Draw. All rights reserved. | Powered by Streamlit</div>', unsafe_allow_html=True)