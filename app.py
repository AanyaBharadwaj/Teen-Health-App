import google.generativeai as genai
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from guardrails import get_system_prompt, is_crisis_situation, CRISIS_RESOURCES

# Initialize session state for user information
if "user_info_submitted" not in st.session_state:
    st.session_state.user_info_submitted = False
if "user_age" not in st.session_state:
    st.session_state.user_age = None
if "user_nickname" not in st.session_state:
    st.session_state.user_nickname = None
if "user_context" not in st.session_state:
    st.session_state.user_context = None

if "gemini_model" not in st.session_state:
    st.session_state["gemini_model"] = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversation_history = []

genai.configure(api_key='AIzaSyD1z-CSUfH_ms0DoMSkELL2xvODPVuYMdo')

# Define context options
CONTEXT_OPTIONS = [
    "Mental Health",
    "Physical Health",
    "Family Issues",
    "Relationships & Social",
    "Academics & School",
    "Career & Future Planning",
    "Substance & Wellness",
    "Self-Esteem & Identity"
]

# FRONTPAGE - User Information Form
if not st.session_state.user_info_submitted:
    st.set_page_config(page_title="Health Education Assistant", layout="centered")
    st.title("Welcome to Health Education Assistant")
    st.markdown("---")
    st.markdown("### Let's Get to Know You!")
    st.markdown("Please provide some information so we can personalize your experience.")
    
    with st.form("user_info_form", clear_on_submit=False):
        # Age dropdown
        age = st.selectbox(
            "How old are you?",
            options=list(range(13, 20)),
            help="Select your age to get age-appropriate information"
        )
        
        # Nickname input
        nickname = st.text_input(
            "What should we call you? (nickname)",
            placeholder="Enter a nickname",
            help="We'll use this to personalize our conversations"
        )
        
        # Context selection
        st.markdown("### What brings you here today?")
        st.markdown("Select the main topic you'd like to discuss:")
        
        selected_context = st.radio(
            "Choose your primary concern:",
            options=CONTEXT_OPTIONS,
            horizontal=False,
            help="This helps us provide more relevant guidance"
        )
        
        # Submit button
        submitted = st.form_submit_button("Start Chatting 💬", use_container_width=True)
        
        if submitted:
            if nickname.strip() == "":
                st.error("Please enter a nickname to continue.")
            else:
                st.session_state.user_age = age
                st.session_state.user_nickname = nickname.strip()
                st.session_state.user_context = selected_context
                st.session_state.user_info_submitted = True
                st.rerun()
else:
    # CHATBOT INTERFACE - After user information is submitted
    st.set_page_config(page_title="Health Education Assistant", layout="wide")
    st.title(f"Health Education Assistant")
    
    # Display user info at top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Age", st.session_state.user_age)
    with col2:
        st.metric("Nickname", st.session_state.user_nickname)
    with col3:
        st.metric("Focus Area", st.session_state.user_context)
    
    # Button to change user info
    if st.button("Change User Info"):
        st.session_state.user_info_submitted = False
        st.rerun()
    
    st.markdown("---")
    
    # Display conversation history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What would you like to know?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Check for crisis keywords
            if is_crisis_situation(prompt):
                crisis_message = "I'm really glad you reached out. It sounds like you're going through something very heavy, and you don't deserve to handle it alone. I can't help with anything that could hurt you, but your safety matters a lot.\n\n"
                crisis_message += "**Please reach out to someone who can help:**\n"
                for country, resource in CRISIS_RESOURCES.items():
                    crisis_message += f"- {country}: {resource}\n"
                crisis_message += "\nPlease also reach out to a trusted adult as soon as you can."
                response_text = crisis_message
            else:
                try:
                    model = genai.GenerativeModel(st.session_state["gemini_model"])
                    # Get personalized system prompt with user information
                    system_prompt = get_system_prompt(
                        age=st.session_state.user_age,
                        nickname=st.session_state.user_nickname,
                        context=st.session_state.user_context
                    )
                    # Build conversation history from previous messages
                    history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages[:-1]])
                    prompt_with_context = f"System Instructions:\n{system_prompt}\n\nConversation history:\n{history_text}\n\nUser: {prompt}" if history_text else f"System Instructions:\n{system_prompt}\n\nUser: {prompt}"
                    
                    response_text = ""
                    placeholder = st.empty()
                    
                    try:
                        stream = model.generate_content(prompt_with_context, stream=True)
                        for chunk in stream:
                            if chunk and hasattr(chunk, 'text') and chunk.text:
                                response_text += chunk.text
                                placeholder.markdown(response_text)
                    except Exception as e:
                        # Fallback to non-streaming if streaming fails
                        st.warning("Switching to non-streaming mode...")
                        response = model.generate_content(prompt_with_context, stream=False)
                        if hasattr(response, 'text'):
                            response_text = response.text
                        else:
                            response_text = "I apologize, but I encountered an error generating a response. Please try again."
                        placeholder.markdown(response_text)
                
                except Exception as e:
                    response_text = f"I apologize, but I encountered an error: {str(e)}"
                    st.error(response_text)
            
            # If crisis situation, display the message without streaming
            if is_crisis_situation(prompt):
                st.markdown(response_text)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})