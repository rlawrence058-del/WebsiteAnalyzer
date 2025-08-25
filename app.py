import streamlit as st
import os
from dotenv import load_dotenv
import json
import time
import streamlit.components.v1 as components
from analyzer_utils import (
    analyze_website_comprehensive,
    generate_lead_qualification,
    generate_replit_prompt,
    generate_outreach_email,
    generate_outreach_dm
)
from authorized_users import AUTHORIZED_EMAILS

# Load environment variables
load_dotenv()

# Disable login requirement - go straight to API key screen
LOGIN_REQUIRED = False

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = not LOGIN_REQUIRED
    if 'api_key_validated' not in st.session_state:
        st.session_state.api_key_validated = False
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'current_url' not in st.session_state:
        st.session_state.current_url = ""

def login_screen():
    """Display login screen for authorized access"""
    st.markdown("### 🔒 Authorized Access Only")
    
    email = st.text_input("Email address", key="login_email")
    
    if st.button("Login", use_container_width=True):
        if email.lower().strip() in [e.lower() for e in AUTHORIZED_EMAILS]:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Email address not authorized.")
    
    st.caption("We don't store your API key. It's only used in your session.")

def api_key_screen():
    """Display API key input screen"""
    st.markdown("### 🔑 Enter Your OpenAI API Key")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            key="api_key_input"
        )
    
    with col2:
        st.write("")  # Spacer
        if st.button("Continue", use_container_width=True):
            if api_key.startswith("sk-") and len(api_key) > 20:
                st.session_state.openai_api_key = api_key
                st.session_state.api_key_validated = True
                st.rerun()
            else:
                st.error("Please enter a valid OpenAI API key.")

def analysis_screen():
    """Display website analysis input screen"""
    st.markdown("### 📊 Website Analysis")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        website_url = st.text_input(
            "Website URL",
            placeholder="example.com or https://example.com",
            key="website_url_input"
        )
    
    with col2:
        st.write("")  # Spacer
        analyze_button = st.button("Analyze Website", use_container_width=True)
    
    if analyze_button and website_url.strip():
        with st.spinner("Running analysis..."):
            try:
                # Store the current URL
                st.session_state.current_url = website_url.strip()
                
                # Run comprehensive analysis
                results = analyze_website_comprehensive(
                    website_url.strip(), 
                    st.session_state.openai_api_key
                )
                
                # Generate additional content
                lead_qual = generate_lead_qualification(results, st.session_state.openai_api_key)
                replit_prompt = generate_replit_prompt(results)
                outreach_email = generate_outreach_email(results, st.session_state.openai_api_key)
                outreach_dm = generate_outreach_dm(results, st.session_state.openai_api_key)
                
                # Store all results
                st.session_state.analysis_results = {
                    'analysis': results,
                    'lead_qualification': lead_qual,
                    'replit_prompt': replit_prompt,
                    'outreach_email': outreach_email,
                    'outreach_dm': outreach_dm
                }
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
    
    elif analyze_button:
        st.error("Please enter a website URL.")

def get_score_color(score):
    """Return color based on score"""
    if score >= 7:
        return "#28a745"  # Green
    elif score >= 4:
        return "#ffc107"  # Yellow
    else:
        return "#dc3545"  # Red

def copy_to_clipboard(text, button_id):
    """Create a copy button that actually works"""
    # Escape backticks and quotes in the text
    escaped_text = text.replace('`', '\\`').replace('"', '\\"').replace("'", "\\'")
    
    html_code = f"""
    <div>
        <button onclick="copyToClipboard{button_id}()" 
                style="background-color: #0066cc; color: white; border: none; 
                       padding: 8px 16px; border-radius: 4px; cursor: pointer;
                       font-size: 14px; width: 100%;">
            Copy
        </button>
    </div>
    
    <script>
    async function copyToClipboard{button_id}() {{
        try {{
            const text = `{escaped_text}`;
            await navigator.clipboard.writeText(text);
            
            // Show success message
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = 'Copied!';
            button.style.backgroundColor = '#28a745';
            
            setTimeout(() => {{
                button.innerHTML = originalText;
                button.style.backgroundColor = '#0066cc';
            }}, 2000);
            
        }} catch (err) {{
            console.error('Failed to copy: ', err);
            // Fallback - select text for manual copy
            const textArea = document.createElement('textarea');
            textArea.value = `{escaped_text}`;
            document.body.appendChild(textArea);
            textArea.select();
            textArea.setSelectionRange(0, 99999);
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            const button = event.target;
            const originalText = button.innerHTML;
            button.innerHTML = 'Copied!';
            button.style.backgroundColor = '#28a745';
            
            setTimeout(() => {{
                button.innerHTML = originalText;
                button.style.backgroundColor = '#0066cc';
            }}, 2000);
        }}
    }}
    </script>
    """
    
    components.html(html_code, height=50)

def results_screen():
    """Display analysis results screen"""
    results = st.session_state.analysis_results
    
    # Top action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        # Create comprehensive text for copying
        all_text = f"""Website Analysis Results for {st.session_state.current_url}

IS THIS A GOOD LEAD?
{results['lead_qualification']}

PLAIN-ENGLISH REPORT:
{results['analysis']['report']}

REPLIT PROMPT:
{results['replit_prompt']}

OUTREACH EMAIL:
{results['outreach_email']}

OUTREACH DM:
{results['outreach_dm']}
"""
        copy_to_clipboard(all_text, "all")
    
    with col2:
        # Generate text file content
        report_text = f"""Website Analysis Report
Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
Website: {st.session_state.current_url}

OVERALL SCORE: {results['analysis']['score']}/10

IS THIS A GOOD LEAD?
{results['lead_qualification']}

PLAIN-ENGLISH REPORT:
{results['analysis']['report']}

REPLIT SITE BUILDER PROMPT:
{results['replit_prompt']}

OUTREACH EMAIL:
{results['outreach_email']}

OUTREACH DM:
{results['outreach_dm']}
"""
        
        st.download_button(
            label="📄 Download Report",
            data=report_text,
            file_name=f"website_analysis_{st.session_state.current_url.replace('https://', '').replace('http://', '').replace('/', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("Reset", use_container_width=True):
            st.session_state.analysis_results = None
            st.session_state.current_url = ""
            st.rerun()
    
    st.markdown(f"### 📊 Results for [{st.session_state.current_url}]")
    
    # Lead Qualification - prominent display
    lead_answer = "Yes" if "yes" in results['lead_qualification'].lower() else "No"
    lead_color = "#28a745" if lead_answer == "Yes" else "#dc3545"  # Green for Yes, Red for No
    
    st.markdown("#### Is This a Good Lead?")
    st.markdown(f'<div style="background-color: {lead_color}; color: white; padding: 20px; border-radius: 5px; text-align: center; font-size: 36px; font-weight: bold; margin-bottom: 10px;">{lead_answer}</div>', unsafe_allow_html=True)
    st.write(results['lead_qualification'])
    
    # Plain-English Report
    st.markdown("#### Plain-English Report")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_area("Report Content", value=results['analysis']['report'], height=150, disabled=True, key="report_text", label_visibility="collapsed")
    with col2:
        st.write("")  # Spacer
        copy_to_clipboard(results['analysis']['report'], "report")
    

    
    # Replit Prompt
    st.markdown("#### Replit Prompt")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_area("Replit Prompt Content", value=results['replit_prompt'], height=200, disabled=True, key="replit_prompt_text", label_visibility="collapsed")
    with col2:
        st.write("")  # Spacer
        copy_to_clipboard(results['replit_prompt'], "replit")
    
    # Outreach Email
    st.markdown("#### Outreach Email")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_area("Email Content", value=results['outreach_email'], height=150, disabled=True, key="email_text", label_visibility="collapsed")
    with col2:
        st.write("")  # Spacer
        copy_to_clipboard(results['outreach_email'], "email")
    
    # Outreach DM
    st.markdown("#### Outreach DM")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_area("DM Content", value=results['outreach_dm'], height=100, disabled=True, key="dm_text", label_visibility="collapsed")
    with col2:
        st.write("")  # Spacer
        copy_to_clipboard(results['outreach_dm'], "dm")

def main():
    """Main application logic"""
    st.set_page_config(
        page_title="5MM Website Analyzer",
        page_icon="📊",
        layout="wide"
    )
    
    # Initialize session state
    init_session_state()
    
    # Main title
    st.title("5MM Website Analyzer & Site Builder")
    
    # Determine which screen to show
    if LOGIN_REQUIRED and not st.session_state.logged_in:
        login_screen()
    elif not st.session_state.api_key_validated:
        api_key_screen()
    elif st.session_state.analysis_results is None:
        analysis_screen()
    else:
        results_screen()

if __name__ == "__main__":
    main()