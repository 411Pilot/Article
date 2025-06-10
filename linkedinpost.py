import streamlit as st
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Gemini API configuration (replace with your Gemini API key)
GEMINI_API_KEY = "AIzaSyAqmaBl29_KRPEABlKKnpemlpV8jF9pxlY"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Custom CSS for AI-themed gradient
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #6b48ff 100%);
        color: white;
    }
    .stButton>button {
        background-color: #4e54c8;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stTextInput>div>input, .stSelectbox>div>select {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 8px;
    }
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 8px;
    }
    h1, h2, h3, label {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "generated_post" not in st.session_state:
    st.session_state.generated_post = None

# Function to generate LinkedIn post using Gemini API
def generate_linkedin_post(topic, tone):
    prompt = f"""
    Create a polished LinkedIn post about the topic: '{topic}' in a {tone} tone.
    Keep it concise (under 300 words), include 3-5 relevant hashtags, and end with a call-to-action.
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 500
            }
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating post: {e}")
        return None

# Function to generate PDF
def generate_pdf(post_content):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 12)
    lines = post_content.split("\n")
    y = 750
    for line in lines:
        if y < 50:  # Start new page if running out of space
            c.showPage()
            y = 750
        c.drawString(50, y, line[:100])  # Truncate long lines
        y -= 15
    c.save()
    buffer.seek(0)
    return buffer

# Main UI
st.title("🚀 LinkedIn Post Generator")
st.write("Enter a topic, choose a tone, and generate a professional LinkedIn post!")

# User Input
topic = st.text_input("Enter the topic for your LinkedIn post", value=st.session_state.topic)
tone = st.selectbox("Select Tone", ["Professional", "Casual", "Inspirational", "Humorous"])

# Generate Post
if st.button("Generate Post"):
    if topic:
        st.session_state.topic = topic
        post = generate_linkedin_post(topic, tone)
        if post:
            st.session_state.generated_post = post
            st.markdown("### Generated Post")
            st.write(post)

# Regenerate Post
if st.session_state.generated_post and st.button("Regenerate Post"):
    post = generate_linkedin_post(st.session_state.topic, tone)
    if post:
        st.session_state.generated_post = post
        st.markdown("### Generated Post")
        st.write(post)

# Download PDF
if st.session_state.generated_post:
    pdf_buffer = generate_pdf(st.session_state.generated_post)
    st.download_button(
        label="Download Post as PDF",
        data=pdf_buffer,
        file_name="linkedin_post.pdf",
        mime="application/pdf"
    )