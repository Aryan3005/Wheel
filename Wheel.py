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

# --- Custom CSS for enhanced UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }
    .main-header {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        color: #FF5733; /* A vibrant orange */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .subheader {
        text-align: center;
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        border: 2px solid #4CAF50; /* A friendly green */
        border-radius: 0.75rem;
        padding: 0.75rem;
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.75rem;
        border-radius: 0.75rem;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
        transition: background-color 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .result-box {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: white;
        background-image: linear-gradient(to right, #FF5733, #FFBD33);
        padding: 1.5rem;
        border-radius: 1rem;
        margin-top: 2rem;
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        animation: fadeIn 1s ease-in-out;
    }
    .error-box {
        text-align: center;
        font-size: 1rem;
        color: #D32F2F;
        background-color: #FFCDD2;
        padding: 1rem;
        border-radius: 0.75rem;
        margin-top: 1.5rem;
        border: 2px solid #EF9A9A;
        animation: shake 0.5s;
    }
    .spinner-container {
        text-align: center;
        margin-top: 2rem;
    }
    .spinner-icon {
        font-size: 3rem;
        animation: spin 1s linear infinite;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    .st-d4 { /* Target Streamlit's container for the two columns */
        gap: 1.5rem;
    }
    .spin-button-disabled > button {
        background-color: #cccccc !important;
        cursor: not-allowed;
    }
    </style>
""", unsafe_allow_html=True)

# --- App UI and Logic ---

# Main title and subheader
st.markdown('<div class="main-header">✨ The Lucky Draw!</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Enter names below to find a random winner. Good luck! 🍀</div>', unsafe_allow_html=True)

# Name input form
with st.form(key="name_form"):
    name_input = st.text_input("Enter names (e.g., Alice, Bob, Amy, Charlie)", placeholder="Separate names with commas")
    submit_button = st.form_submit_button("Add Names")

# Handle name submission
if submit_button and name_input:
    st.session_state.names = [name.strip() for name in name_input.split(',') if name.strip()]
    st.session_state.error = ""
    st.session_state.result = ""
    if not st.session_state.names:
        st.session_state.error = "Please enter at least one name."
    else:
        st.session_state.result = "Names added! Ready to spin! 🥳"

# Spin and Reset buttons
col1, col2 = st.columns([2, 1])
with col1:
    spin_button = st.button("Spin to Win! 🏆", disabled=not st.session_state.names or st.session_state.is_spinning)
with col2:
    reset_button = st.button("Reset", key="reset_button")

# Handle reset
if reset_button:
    st.session_state.names = []
    st.session_state.spin_count = 0
    st.session_state.result = ""
    st.session_state.error = ""
    st.rerun()  # <--- Corrected line

# Handle spin
if spin_button and st.session_state.names:
    st.session_state.is_spinning = True
    st.session_state.error = ""
    
    # Placeholder for the spinning animation
    spinner_placeholder = st.empty()
    
    for i in range(5): # Simulating a longer spin
        for emoji in ["✨", "🌟", "🎉", "🔥"]:
            spinner_placeholder.markdown(f'<div class="spinner-container"><div class="spinner-icon">{emoji}</div></div>', unsafe_allow_html=True)
            time.sleep(0.2)
    
    # Logic for selecting the winner
    if st.session_state.spin_count == 0:
        # First spin is random
        st.session_state.result = f"Winner: {random.choice(st.session_state.names)}! 🎉"
    elif st.session_state.spin_count == 1:
        # Second spin is an 'A' name
        a_names = [name for name in st.session_state.names if name.lower().startswith('a')]
        if a_names:
            st.session_state.result = f"Winner: {random.choice(a_names)}! 🌟"
        else:
            st.session_state.error = "Oops! No names started with 'A' this time. A random name will be picked instead."
            st.session_state.result = f"Winner: {random.choice(st.session_state.names)}! 🌟"
    else:
        # Subsequent spins are random
        st.session_state.result = f"Winner: {random.choice(st.session_state.names)}! 🎉"
    
    st.session_state.spin_count += 1
    st.session_state.is_spinning = False
    spinner_placeholder.empty()
    
    # Rerun the app to show the result
    st.rerun()  # <--- Corrected line

# Display result
if st.session_state.result:
    st.markdown(f'<div class="result-box">{st.session_state.result}</div>', unsafe_allow_html=True)

# Display error
if st.session_state.error:
    st.markdown(f'<div class="error-box">{st.session_state.error}</div>', unsafe_allow_html=True)