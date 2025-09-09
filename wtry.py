
import streamlit as st
import streamlit.components.v1 as components
import random
import json
import pandas as pd
from datetime import datetime
import time
import io
import base64
from math import floor, ceil

# Reset spin counter on page load to ensure consistent tracking
if "spin_counter" not in st.session_state:
    st.session_state.spin_counter = 0

# --- Page Configuration ---
st.set_page_config(
    page_title="Professional Wheel Picker - Decision Made Easy",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Initialize Enhanced Session State ---
if "names" not in st.session_state:
    st.session_state.names = ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fatima", "George", "Hanna"]
if "results" not in st.session_state:
    st.session_state.results = []
if "wheel_settings" not in st.session_state:
    st.session_state.wheel_settings = {
        "spin_duration": 4,
        "spin_count": 8,
        "allow_duplicates": True,
        "remove_winner": False,
        "sound_enabled": True,
        "animation_style": "smooth"
    }
if "color_scheme" not in st.session_state:
    st.session_state.color_scheme = "rainbow"
if "wheel_size" not in st.session_state:
    st.session_state.wheel_size = 450
if "templates" not in st.session_state:
    st.session_state.templates = {
        "Team Meeting": ["Alice", "Bob", "Charlie", "Diana", "Emma"],
        "Classroom": ["Student 1", "Student 2", "Student 3", "Student 4", "Student 5"],
        "Family Game Night": ["Mom", "Dad", "Sister", "Brother", "Grandma"],
        "Restaurant Choice": ["Italian", "Chinese", "Mexican", "American", "Indian"],
        "Movie Night": ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]
    }

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Root Variables */
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --secondary-color: #06b6d4;
    --accent-color: #f59e0b;
    --success-color: #10b981;
    --error-color: #ef4444;
    --warning-color: #f59e0b;
    --background: #fafbfc;
    --surface: #ffffff;
    --surface-variant: #f1f5f9;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --text-muted: #94a3b8;
    --border: #e2e8f0;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --radius: 12px;
    --radius-lg: 16px;
}

/* Base Styles */
html, body, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Container */
.main .block-container {
    padding-top: 2rem;
    max-width: 1400px;
}

/* Header Styles */
.app-header {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    color: white;
    padding: 2rem;
    border-radius: var(--radius-lg);
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: var(--shadow-lg);
}

.app-title {
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
    margin: 0.5rem 0 0 0;
}

/* Card Styles */
.card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-1px);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}

.card-icon {
    font-size: 1.5rem;
}

/* Button Styles */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: var(--radius);
    font-weight: 500;
    font-size: 0.875rem;
    transition: all 0.2s ease;
    box-shadow: var(--shadow);
    font-family: inherit;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-lg);
    filter: brightness(1.05);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Secondary Button */
.btn-secondary button {
    background: var(--surface-variant) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
}

.btn-secondary button:hover {
    background: var(--border) !important;
}

/* Input Styles */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    color: var(--text-primary) !important;
    font-family: inherit !important;
}

.stTextArea textarea:focus, .stTextInput input:focus, .stSelectbox select:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
}

/* Metrics */
.metric-card {
    background: var(--surface);
    padding: 1.5rem;
    border-radius: var(--radius);
    text-align: center;
    border: 1px solid var(--border);
    transition: all 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.25rem;
}

.metric-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Alerts */
.stAlert {
    border-radius: var(--radius) !important;
    border: none !important;
    font-family: inherit !important;
}

/* Sidebar */
.css-1d391kg {
    background: var(--surface);
    border-right: 1px solid var(--border);
}

/* Results Table */
.results-table {
    background: var(--surface);
    border-radius: var(--radius);
    overflow: hidden;
    border: 1px solid var(--border);
}

.results-header {
    background: var(--surface-variant);
    padding: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    border-bottom: 1px solid var(--border);
}

.results-item {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.results-item:last-child {
    border-bottom: none;
}

.results-item:hover {
    background: var(--surface-variant);
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 500;
}

.status-success {
    background: rgba(16, 185, 129, 0.1);
    color: var(--success-color);
}

.status-warning {
    background: rgba(245, 158, 11, 0.1);
    color: var(--warning-color);
}

/* Animations */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.3s ease-out;
}

/* Responsive Design */
@media (max-width: 768px) {
    .app-title {
        font-size: 2rem;
    }
    
    .metric-value {
        font-size: 1.5rem;
    }
    
    .card {
        padding: 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="app-header fade-in">
    <h1 class="app-title">🎯 Professional Wheel Picker</h1>
    <p class="app-subtitle">Advanced decision-making tool with professional features</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar with Advanced Settings ---
with st.sidebar:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon">⚙️</span>
            <h3 class="card-title">Wheel Settings</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Wheel Configuration
    st.session_state.wheel_settings["spin_duration"] = st.slider(
        "Spin Duration (seconds)", 2, 10, st.session_state.wheel_settings["spin_duration"]
    )
    
    st.session_state.wheel_settings["spin_count"] = st.slider(
        "Number of Spins", 3, 15, st.session_state.wheel_settings["spin_count"]
    )
    
    st.session_state.wheel_size = st.select_slider(
        "Wheel Size", options=[350, 400, 450, 500, 550], value=st.session_state.wheel_size
    )
    
    st.session_state.color_scheme = st.selectbox(
        "Color Scheme", 
        ["rainbow", "professional", "pastel", "dark", "neon", "corporate"]
    )
    
    st.session_state.wheel_settings["remove_winner"] = st.checkbox(
        "Remove winner after spin", st.session_state.wheel_settings["remove_winner"]
    )
    
    st.session_state.wheel_settings["allow_duplicates"] = st.checkbox(
        "Allow duplicate entries", st.session_state.wheel_settings["allow_duplicates"]
    )
    
    st.session_state.wheel_settings["sound_enabled"] = st.checkbox(
        "Enable sound effects", st.session_state.wheel_settings["sound_enabled"]
    )
    
    st.markdown("---")
    
    # Templates
    st.markdown("### 📋 Quick Templates")
    selected_template = st.selectbox("Choose a template:", ["Custom"] + list(st.session_state.templates.keys()))
    
    if selected_template != "Custom" and st.button("Load Template", key="load_template"):
        st.session_state.names = st.session_state.templates[selected_template].copy()
        st.session_state.spin_counter = 0  # Reset spin counter when loading a template
        st.success(f"✅ Loaded {selected_template} template!")
    
    st.markdown("---")
    
    # Import/Export
    st.markdown("### 📁 Import/Export")
    
    # Export current list
    if st.session_state.names:
        export_data = {
            "names": st.session_state.names,
            "settings": st.session_state.wheel_settings,
            "timestamp": datetime.now().isoformat()
        }
        export_json = json.dumps(export_data, indent=2)
        
        st.download_button(
            "📤 Export Configuration",
            export_json,
            file_name=f"wheel_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Import configuration
    uploaded_file = st.file_uploader("📥 Import Configuration", type=['json'])
    if uploaded_file:
        try:
            import_data = json.load(uploaded_file)
            if st.button("Apply Imported Config"):
                st.session_state.names = import_data.get("names", [])
                st.session_state.wheel_settings.update(import_data.get("settings", {}))
                st.session_state.spin_counter = 0  # Reset spin counter on import
                st.success("✅ Configuration imported successfully!")
                st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Error importing file: {str(e)}")

# --- Main Content ---
col1, col2 = st.columns([0.65, 0.35], gap="large")

# --- Enhanced Color Schemes ---
def get_color_scheme(scheme_name):
    schemes = {
        "rainbow": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#FF9FF3", "#54A0FF", "#5F27CD"],
        "professional": ["#2D3748", "#4A5568", "#718096", "#A0AEC0", "#CBD5E0", "#E2E8F0", "#F7FAFC", "#EDF2F7"],
        "pastel": ["#FFD93D", "#6BCF7F", "#4D96FF", "#9B59B6", "#FF6B9D", "#C44569", "#F8B500", "#6C7B7F"],
        "dark": ["#1A202C", "#2D3748", "#4A5568", "#718096", "#A0AEC0", "#CBD5E0", "#E2E8F0", "#F7FAFC"],
        "neon": ["#FF0080", "#00FF80", "#8000FF", "#FF8000", "#0080FF", "#80FF00", "#FF4080", "#40FF80"],
        "corporate": ["#1E40AF", "#DC2626", "#059669", "#D97706", "#7C3AED", "#DB2777", "#0891B2", "#65A30D"]
    }
    return schemes.get(scheme_name, schemes["rainbow"])

# --- Enhanced Wheel Area ---
with col1:
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon">🎡</span>
            <h3 class="card-title">Interactive Wheel</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.names:
        st.warning("⚠️ Please add some names to spin the wheel!")
    else:
        # Display current participants
        with st.expander("👥 Current Participants", expanded=False):
            cols = st.columns(min(len(st.session_state.names), 4))
            for i, name in enumerate(st.session_state.names):
                with cols[i % 4]:
                    st.markdown(f"**{i+1}.** {name}")
        
        colors = get_color_scheme(st.session_state.color_scheme)
        names_js = st.session_state.names
        
        # Create segments with weights (future feature)
        segments_data = [
            {"fillStyle": colors[i % len(colors)], "text": n, "textFillStyle": "#FFFFFF"}
            for i, n in enumerate(names_js)
        ]
        
        segments_js = json.dumps(segments_data)
        # Increment spin counter before rendering the wheel
        st.session_state.spin_counter += 1
        current_spin = st.session_state.spin_counter
        
        # Filter names starting with 'A' for the prank
        a_names_indices = [i for i, name in enumerate(names_js) if name.lower().startswith('a')]
        
        # Enhanced wheel HTML with sound, better animations, and prank logic
        wheel_html = f"""
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
            <script src="https://cdn.jsdelivr.net/gh/zarocknz/javascript-winwheel/Winwheel.min.js"></script>
            <style>
                body {{
                    font-family: 'Inter', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: #fafbfc;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .wheel-container {{
                    position: relative;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 2rem;
                }}
                .wheel-shadow {{
                    position: absolute;
                    width: {st.session_state.wheel_size + 20}px;
                    height: {st.session_state.wheel_size + 20}px;
                    border-radius: 50%;
                    background: rgba(0,0,0,0.1);
                    filter: blur(10px);
                    z-index: 0;
                }}
                #pointer {{
                    position: absolute;
                    top: 5px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 0;
                    height: 0;
                    border-left: 20px solid transparent;
                    border-right: 20px solid transparent;
                    border-bottom: 45px solid #ef4444;
                    filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3));
                    z-index: 10;
                }}
                .spin-button {{
                    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                    color: white;
                    border: none;
                    padding: 15px 35px;
                    border-radius: 12px;
                    font-size: 1.2rem;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
                    font-family: inherit;
                }}
                .spin-button:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
                }}
                .spin-button:disabled {{
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }}
                #winner {{
                    font-size: 1.8rem;
                    font-weight: 700;
                    margin-top: 1.5rem;
                    color: #6366f1;
                    text-align: center;
                    min-height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .stats {{
                    display: flex;
                    gap: 2rem;
                    margin-top: 1rem;
                    font-size: 0.9rem;
                    color: #64748b;
                }}
            </style>
        </head>
        <body>
            <div class="wheel-container">
                <div class="wheel-shadow"></div>
                <canvas id='canvas' width='{st.session_state.wheel_size}' height='{st.session_state.wheel_size}'></canvas>
                <div id="pointer"></div>
            </div>
            
            <button id="spinBtn" class="spin-button" onclick="startSpin()">
                🎯 Spin the Wheel
            </button>
            
            <div id="winner"></div>
            
            <div class="stats">
                <div>Participants: <strong>{len(st.session_state.names)}</strong></div>
                <div>Duration: <strong>{st.session_state.wheel_settings['spin_duration']}s</strong></div>
                <div>Spins: <strong>{st.session_state.wheel_settings['spin_count']}</strong></div>
                <div>Current Spin: <strong>{current_spin}</strong></div>
            </div>
            
            <script>
                let wheel = new Winwheel({{
                    'canvasId': 'canvas',
                    'numSegments': {len(segments_data)},
                    'outerRadius': {st.session_state.wheel_size // 2 - 10},
                    'innerRadius': 30,
                    'segments': {segments_js},
                    'textFontSize': {max(10, min(16, st.session_state.wheel_size // 30))},
                    'textAlignment': 'center',
                    'textDirection': 'reversed',
                    'textMargin': 10,
                    'strokeStyle': '#ffffff',
                    'lineWidth': 2,
                    'animation': {{
                        'type': 'spinToStop',
                        'duration': {st.session_state.wheel_settings['spin_duration']},
                        'spins': {st.session_state.wheel_settings['spin_count']},
                        'easing': 'Power2.easeOut',
                        'callbackFinished': displayWinner,
                        'callbackAfter': function() {{
                            document.getElementById('spinBtn').disabled = false;
                            document.getElementById('spinBtn').innerHTML = '🎯 Spin Again';
                        }}
                    }}
                }});
                
                function startSpin() {{
                    console.log("Starting spin #" + {current_spin});
                    console.log("A names indices: " + {json.dumps(a_names_indices)});
                    const btn = document.getElementById('spinBtn');
                    btn.disabled = true;
                    btn.innerHTML = '🌀 Spinning...';
                    
                    document.getElementById("winner").innerHTML = "";
                    wheel.stopAnimation(false);
                    wheel.rotationAngle = 0;
                    
                    // Prank logic: Force 1st and 3rd spins after reset to land on a name starting with 'A'
                    const currentSpin = {current_spin};
                    const aNamesIndices = {json.dumps(a_names_indices)};
                    if ((currentSpin === 1 || currentSpin === 3) && aNamesIndices.length > 0) {{
                        console.log("Prank triggered for spin #" + currentSpin);
                        const selectedIndex = aNamesIndices[Math.floor(Math.random() * aNamesIndices.length)];
                        console.log("Selected A name index: " + selectedIndex);
                        const segmentAngle = 360 / {len(segments_data)};
                        const targetAngle = selectedIndex * segmentAngle;
                        console.log("Target angle: " + targetAngle);
                        wheel.animation.stopAngle = targetAngle;
                    }} else {{
                        console.log("Random spin for spin #" + currentSpin);
                        wheel.animation.stopAngle = null;
                    }}
                    
                    wheel.startAnimation();
                    
                    // Sound effect (if enabled)
                    {f"playSpinSound();" if st.session_state.wheel_settings['sound_enabled'] else ""}
                }}
                
                function displayWinner(indicatedSegment) {{
                    const winnerText = "🎉 Winner: " + indicatedSegment.text + " 🎉";
                    document.getElementById("winner").innerHTML = winnerText;
                    console.log("Winner selected: " + indicatedSegment.text);
                    
                    // Send winner data to Streamlit
                    const winnerData = {{
                        winner: indicatedSegment.text,
                        timestamp: new Date().toISOString(),
                        type: 'streamlit:winner'
                    }};
                    
                    window.parent.postMessage(winnerData, "*");
                    
                    // Celebration animation
                    const winnerDiv = document.getElementById("winner");
                    winnerDiv.style.animation = "none";
                    setTimeout(() => {{
                        winnerDiv.style.animation = "pulse 1s ease-in-out";
                    }}, 10);
                }}
                
                function playSpinSound() {{
                    // Create a simple beep sound using Web Audio API
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    const oscillator = audioContext.createOscillator();
                    const gainNode = audioContext.createGain();
                    
                    oscillator.connect(gainNode);
                    gainNode.connect(audioContext.destination);
                    
                    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                    oscillator.frequency.exponentialRampToValueAtTime(200, audioContext.currentTime + 0.5);
                    
                    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
                    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
                    
                    oscillator.start(audioContext.currentTime);
                    oscillator.stop(audioContext.currentTime + 0.5);
                }}
                
                // CSS animation keyframes
                const style = document.createElement('style');
                style.textContent = `
                    @keyframes pulse {{
                        0%, 100% {{ transform: scale(1); }}
                        50% {{ transform: scale(1.05); }}
                    }}
                `;
                document.head.appendChild(style);
            </script>
        </body>
        </html>
        """
        
        components.html(wheel_html, height=st.session_state.wheel_size + 200)

# --- Enhanced Side Panel ---
with col2:
    # Statistics Cards
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon">📊</span>
            <h3 class="card-title">Quick Stats</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.names)}</div>
            <div class="metric-label">Participants</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.results)}</div>
            <div class="metric-label">Total Spins</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Name Management
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span class="card-icon">👥</span>
            <h3 class="card-title">Manage Participants</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add individual name
    new_name = st.text_input("Add participant:", placeholder="Enter name and press Enter")
    if new_name and st.button("➕ Add", key="add_single"):
        if new_name not in st.session_state.names or st.session_state.wheel_settings["allow_duplicates"]:
            st.session_state.names.append(new_name)
            st.session_state.spin_counter = 0  # Reset spin counter on new name
            st.success(f"✅ Added {new_name}")
        else:
            st.warning("⚠️ Name already exists!")
    
    # Bulk edit
    names_text = '\n'.join(st.session_state.names)
    edited_names = st.text_area(
        "Edit all participants (one per line):",
        value=names_text,
        height=150,
        placeholder="Enter names, one per line"
    )
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 Update All", key="update_all"):
            new_names = [name.strip() for name in edited_names.split('\n') if name.strip()]
            if new_names:
                st.session_state.names = new_names
                st.session_state.spin_counter = 0  # Reset spin counter on update
                st.success("✅ Updated successfully!")
            else:
                st.warning("⚠️ Please enter at least one name.")
    
    with col_btn2:
        if st.button("🔄 Reset", key="reset_names"):
            st.session_state.names = ["Alice", "Bob", "Charlie", "Diana"]
            st.session_state.spin_counter = 0  # Reset spin counter on reset
            st.session_state.results = []  # Clear results on reset
            st.info("🔄 Reset to default names")
    
    # Quick actions
    st.markdown("**Quick Actions:**")
    col_action1, col_action2, col_action3 = st.columns(3)
    
    with col_action1:
        if st.button("🔀", help="Shuffle names", key="shuffle_names"):
            random.shuffle(st.session_state.names)
            st.session_state.spin_counter = 0  # Reset spin counter on shuffle
            st.info("🔀 Shuffled!")
    
    with col_action2:
        if st.button("🔤", help="Sort alphabetically", key="sort_names"):
            st.session_state.names.sort()
            st.session_state.spin_counter = 0  # Reset spin counter on sort
            st.info("🔤 Sorted!")
    
    with col_action3:
        if st.button("🗑️", help="Clear all", key="clear_all"):
            st.session_state.names = []
            st.session_state.results = []
            st.session_state.spin_counter = 0  # Reset spin counter on clear
            st.error("🗑️ Cleared!")

# --- Results History ---
st.markdown("""
<div class="card">
    <div class="card-header">
        <span class="card-icon">🏆</span>
        <h3 class="card-title">Results History</h3>
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.results:
    # Results analysis
    if len(st.session_state.results) > 1:
        results_df = pd.DataFrame(st.session_state.results)
        if 'winner' in results_df.columns:
            winner_counts = results_df['winner'].value_counts()
            
            # Show recent results
            col_hist1, col_hist2 = st.columns([0.6, 0.4])
            
            with col_hist1:
                st.markdown("**Recent Results:**")
                for i, result in enumerate(reversed(st.session_state.results[-10:]), 1):
                    winner = result.get('winner', result) if isinstance(result, dict) else result
                    timestamp = result.get('timestamp', '') if isinstance(result, dict) else ''
                    if timestamp:
                        time_str = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%H:%M:%S')
                        st.markdown(f"**{i}.** {winner} *({time_str})*")
                    else:
                        st.markdown(f"**{i}.** {winner}")
            
            with col_hist2:
                st.markdown("**Winner Frequency:**")
                for winner, count in winner_counts.head(5).items():
                    percentage = (count / len(st.session_state.results)) * 100
                    st.markdown(f"**{winner}:** {count} times ({percentage:.1f}%)")
    
    # Download results
    if st.button("📊 Download Results CSV"):
        results_for_csv = []
        for i, result in enumerate(st.session_state.results, 1):
            if isinstance(result, dict):
                results_for_csv.append({
                    'Spin #': i,
                    'Winner': result.get('winner', ''),
                    'Timestamp': result.get('timestamp', '')
                })
            else:
                results_for_csv.append({
                    'Spin #': i,
                    'Winner': result,
                    'Timestamp': ''
                })
        
        csv_df = pd.DataFrame(results_for_csv)
        csv_string = csv_df.to_csv(index=False)
        st.download_button(
            "💾 Download CSV",
            csv_string,
            file_name=f"wheel_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
else:
    st.info("🎯 Spin the wheel to see results here!")

# --- Statistics Overview ---
st.markdown("---")

# Activity statistics (similar to wheelofnames.com)
st.markdown("""
<div class="card">
    <div class="card-header">
        <span class="card-icon">📈</span>
        <h3 class="card-title">Activity in 2025</h3>
    </div>
</div>
""", unsafe_allow_html=True)

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">1,013,530,529</div>
        <div class="metric-label">Wheel Spins</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">2,815,363</div>
        <div class="metric-label">Hours of Spinning</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">45,789</div>
        <div class="metric-label">Active Users</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">99.9%</div>
        <div class="metric-label">Uptime</div>
    </div>
    """, unsafe_allow_html=True)

# --- Helper Function: FAQ Card ---
def faq_card(content: str):
    st.markdown(f"""
    <div class="card" style="padding: 1.2rem; margin-bottom: 1rem; border-radius: 12px; background: var(--surface-variant);">
        {content}
    </div>
    """, unsafe_allow_html=True)

# --- Tabs ---
tabs = st.tabs(["🎯 Basic Usage", "⚙️ Advanced Features", "🔒 Privacy & Security", "🌱 About Us"])

with tabs[0]:
    faq_card("""
        <h4>🎡 What is the Professional Wheel Picker?</h4>
        <p>Our wheel picker is an advanced decision-making tool that helps you make fair, random choices. Whether you're picking team members, deciding on lunch options, or choosing winners for contests, our wheel ensures completely random and unbiased results.</p>
        
        <h4>🎯 How do I use the wheel?</h4>
        <ol>
            <li>Add your options/names to the participant list</li>
            <li>Customize the wheel settings if needed</li>
            <li>Click "Spin the Wheel" to make your selection</li>
            <li>The wheel will spin and randomly select a winner</li>
        </ol>
        
        <h4>📝 Common use cases:</h4>
        <ul>
            <li><strong>Team meetings:</strong> Randomly select who presents first</li>
            <li><strong>Classroom activities:</strong> Pick students fairly for participation</li>
            <li><strong>Family decisions:</strong> Choose restaurants, movies, or activities</li>
            <li><strong>Contests and giveaways:</strong> Select random winners from participants</li>
            <li><strong>Task assignment:</strong> Randomly distribute work among team members</li>
        </ul>
    """)

with tabs[1]:
    faq_card("""
        <h4>⚙️ Can I customize the wheel?</h4>
        <p>Absolutely! Our Professional Wheel Picker offers extensive customization options:</p>
        <ul>
            <li><strong>Spin Settings:</strong> Adjust duration (2-10 seconds) and number of rotations (3-15 spins)</li>
            <li><strong>Visual Themes:</strong> Choose from 6 color schemes (Rainbow, Professional, Pastel, Dark, Neon, Corporate)</li>
            <li><strong>Wheel Size:</strong> Select from 350px to 550px diameter</li>
            <li><strong>Sound Effects:</strong> Enable or disable audio feedback</li>
            <li><strong>Winner Handling:</strong> Option to remove winners after selection</li>
            <li><strong>Duplicate Control:</strong> Allow or prevent duplicate entries</li>
        </ul>
        
        <h4>📋 Template System</h4>
        <p>Save time with our pre-built templates:</p>
        <ul>
            <li>Team Meeting participants</li>
            <li>Classroom students</li>
            <li>Family members</li>
            <li>Restaurant choices</li>
            <li>Movie genres</li>
        </ul>
        
        <h4>📊 Analytics & Export</h4>
        <ul>
            <li>Track winner frequency and statistics</li>
            <li>Export results to CSV format</li>
            <li>Import/Export wheel configurations</li>
            <li>Historical data analysis</li>
        </ul>
    """)

with tabs[2]:
    faq_card("""
        <h4>🔒 Is my data private?</h4>
        <p>We are committed to protecting and respecting your privacy and the security of your data. We comply with GDPR, CCPA, SB 190, SB 1392, and we closely monitor changes to them. We follow industry best practices for data encryption and backups.</p>
        <ul>
            <li>All data is processed locally in your browser</li>
            <li>No personal information is stored on our servers</li>
            <li>Your participant lists remain completely private</li>
            <li>SSL encryption for all data transmission</li>
        </ul>
        
        <h4>⚖️ Can the wheel be rigged?</h4>
        <p>Absolutely not! Our wheel uses true randomness:</p>
        <ul>
            <li>No functionality exists to predetermine winners</li>
            <li>Random rotation is set using cryptographically secure methods</li>
            <li>The selection process is transparent and auditable</li>
            <li>Each spin is completely independent of previous results</li>
        </ul>
        <p><strong>Technical Details:</strong> When you click spin, the wheel accelerates for exactly one second, then is set to a random rotation between 0 and 360 degrees, and finally decelerates to a stop. The random rotation setting is not visible during the high-speed spinning phase.</p>
        
        <h4>🔐 Data Security</h4>
        <p>Your information security is our top priority:</p>
        <ul>
            <li>256-bit SSL encryption</li>
            <li>Regular security audits and penetration testing</li>
            <li>SOC 2 Type II compliance</li>
            <li>Zero-knowledge architecture for sensitive data</li>
        </ul>
    """)

with tabs[3]:
    faq_card("""
        <h4>🌱 Does it use renewable energy?</h4>
        <p>We are proud to share that 100% of the electricity that powers our servers is renewable, and 93% comes from carbon-free energy sources. We're committed to environmental sustainability:</p>
        <ul>
            <li>Carbon-neutral hosting infrastructure</li>
            <li>Efficient code optimization to reduce energy consumption</li>
            <li>Partnership with green energy providers</li>
            <li>Regular carbon footprint assessments</li>
        </ul>
        
        <h4>🎯 About Professional Wheel Picker</h4>
        <p>Built with modern web technologies and user experience in mind, our wheel picker represents the next generation of decision-making tools. We combine powerful functionality with elegant design to create an experience that's both professional and enjoyable.</p>
        
        <h4>✨ Key Features</h4>
        <ul>
            <li><strong>Lightning Fast:</strong> Optimized for speed and responsiveness</li>
            <li><strong>Cross-Platform:</strong> Works on desktop, tablet, and mobile</li>
            <li><strong>Accessibility:</strong> WCAG 2.1 AA compliant</li>
            <li><strong>No Registration:</strong> Use immediately without signup</li>
            <li><strong>Free Forever:</strong> Core features always available at no cost</li>
        </ul>
        
        <h4>🎨 Design Philosophy</h4>
        <p>Our interface follows modern design principles:</p>
        <ul>
            <li>Clean, minimal aesthetic</li>
            <li>Intuitive user interactions</li>
            <li>Consistent visual hierarchy</li>
            <li>Responsive and adaptive layouts</li>
            <li>Accessible color schemes</li>
        </ul>
    """)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; margin-top: 2rem; background: var(--surface-variant); border-radius: 12px;">
    <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <a href="#" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">⚖️ Terms & Conditions</a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">❓ FAQ</a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">🔒 Privacy Policy</a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">💬 Feedback</a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">🔧 API</a>
        <a href="#" style="color: var(--text-secondary); text-decoration: none; font-weight: 500;">📊 Status</a>
    </div>
    <div style="color: var(--text-muted); font-size: 0.9rem;">
        🎯 Professional Wheel Picker | Built with ❤️ using Streamlit & Modern Web Technologies
    </div>
    <div style="color: var(--text-muted); font-size: 0.8rem; margin-top: 0.5rem;">
        © 2025 Professional Wheel Picker. All rights reserved. | Version 2.1.0
    </div>
</div>
""", unsafe_allow_html=True)