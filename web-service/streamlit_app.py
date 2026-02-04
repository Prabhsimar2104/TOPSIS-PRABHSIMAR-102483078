import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re
import os
import tempfile
import subprocess

# Page configuration
st.set_page_config(
    page_title="TOPSIS Web Service",
    page_icon="📊",
    layout="centered"
)

# Custom CSS for better UI - FIXED VISIBILITY
st.markdown("""
    <style>
    /* Main app background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Form container */
    div[data-testid="stForm"] {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Make all form labels dark and visible */
    div[data-testid="stForm"] label {
        color: #333 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Make subheaders dark */
    div[data-testid="stForm"] h3 {
        color: #333 !important;
        font-weight: 600 !important;
    }
    
    /* Title */
    h1 {
        color: white !important;
        text-align: center;
        font-size: 2.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Info box */
    .info-box {
        background-color: rgba(255, 255, 255, 0.95);
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    
    .info-box h3 {
        color: #667eea !important;
        margin-bottom: 10px;
    }
    
    .info-box ul, .info-box li {
        color: #333 !important;
    }
    
    .info-box strong {
        color: #333 !important;
    }
    
    /* Input fields - better visibility */
    input, textarea {
        color: #fff !important;
        background-color: #2d3748 !important;
    }
    
    /* Placeholder text */
    input::placeholder, textarea::placeholder {
        color: #a0aec0 !important;
    }
    
    /* When input is focused */
    input:focus, textarea:focus {
        background-color: #374151 !important;
        color: #fff !important;
    }
    
    /* File uploader text */
    .uploadedFileName {
        color: #333 !important;
    }
    
    /* Better spacing for mobile */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        div[data-testid="stForm"] {
            padding: 1.5rem;
        }
        h1 {
            font-size: 2rem !important;
        }
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 0.9rem !important;
    }
    
    /* Success/Error messages - better contrast */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_inputs(weights_str, impacts_str, num_criteria):
    """Validate weights and impacts"""
    try:
        # Split and validate weights
        weights = weights_str.split(',')
        if len(weights) != num_criteria:
            return False, f"Number of weights ({len(weights)}) must equal number of criteria ({num_criteria})"
        
        # Check if all weights are numeric
        for w in weights:
            float(w.strip())
        
        # Split and validate impacts
        impacts = impacts_str.split(',')
        if len(impacts) != num_criteria:
            return False, f"Number of impacts ({len(impacts)}) must equal number of criteria ({num_criteria})"
        
        # Check if all impacts are + or -
        for i in impacts:
            if i.strip() not in ['+', '-']:
                return False, "Impacts must be either '+' or '-'"
        
        return True, "Valid"
    except ValueError:
        return False, "Weights must be numeric values"

def perform_topsis_with_package(data, weights_str, impacts_str):
    """
    Perform TOPSIS calculation using Topsis-Prabhsimar-102483078 package
    Uses the CLI command: topsis input.csv weights impacts output.csv
    """
    input_path = None
    output_path = None
    
    try:
        if data.shape[1] < 3:
            return None, "Input file must contain at least 3 columns"
        
        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp_input:
            data.to_csv(tmp_input.name, index=False)
            input_path = tmp_input.name
        
        # Create output file path
        output_path = input_path.replace('.csv', '_output.csv')
        
        # Run TOPSIS package as CLI command
        # Command: topsis input.csv "weights" "impacts" output.csv
        cmd = [
            'topsis',
            input_path,
            weights_str,
            impacts_str,
            output_path
        ]
        
        # Execute the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Check if command was successful
        if result.returncode == 0:
            # Read the output file
            if os.path.exists(output_path):
                result_data = pd.read_csv(output_path)
                
                # Clean up temp files
                try:
                    os.unlink(input_path)
                    os.unlink(output_path)
                except:
                    pass
                
                return result_data, "✅ TOPSIS analysis completed using Topsis-Prabhsimar-102483078 package!"
            else:
                raise Exception("Output file not created by TOPSIS package")
        else:
            # Command failed, show error
            error_msg = result.stderr if result.stderr else result.stdout
            raise Exception(f"TOPSIS package error: {error_msg}")
            
    except subprocess.TimeoutExpired:
        return None, "❌ TOPSIS calculation timed out"
    except FileNotFoundError:
        # TOPSIS package not installed, show helpful error
        return None, "❌ TOPSIS package not found. Please ensure 'Topsis-Prabhsimar-102483078' is installed."
    except Exception as e:
        return None, f"❌ Error: {str(e)}"
    finally:
        # Clean up temp files
        try:
            if input_path and os.path.exists(input_path):
                os.unlink(input_path)
            if output_path and os.path.exists(output_path):
                os.unlink(output_path)
        except:
            pass

def send_email(recipient_email, result_df):
    """Send email with result file"""
    try:
        # Email configuration
        sender_email = st.secrets.get("SENDER_EMAIL", os.getenv('SENDER_EMAIL', 'simarprabh095@gmail.com'))
        sender_password = st.secrets.get("SENDER_PASSWORD", os.getenv('SENDER_PASSWORD', 'wods spdg mvfq dsnx'))
        
        # Create temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp_file:
            result_df.to_csv(tmp_file.name, index=False)
            temp_filepath = tmp_file.name
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "TOPSIS Analysis Results"
        
        # Email body
        body = """
        Hello,
        
        Your TOPSIS analysis has been completed successfully using the Topsis-Prabhsimar-102483078 package!
        
        Please find the results attached to this email.
        
        Thank you for using our TOPSIS Web Service.
        
        Best regards,
        TOPSIS Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file
        filename = "topsis_results.csv"
        with open(temp_filepath, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        # Clean up temp file
        os.unlink(temp_filepath)
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

# Main App
st.title("📊 TOPSIS Web Service")
st.markdown("<p style='text-align: center; color: white; font-size: 1.2em;'>Multi-Criteria Decision Making</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white; font-size: 0.9em;'>Powered by 📦 <strong>Topsis-Prabhsimar-102483078</strong></p>", unsafe_allow_html=True)

# Main form
with st.form("topsis_form"):
    st.subheader("📁 Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="First column should contain names, remaining columns should be numeric criteria"
    )
    
    st.subheader("⚖️ Weights")
    weights = st.text_input(
        "Enter weights (comma-separated)",
        placeholder="0.25,0.25,0.25,0.25",
        help="Comma-separated numeric values"
    )
    
    st.subheader("📈 Impacts")
    impacts = st.text_input(
        "Enter impacts (comma-separated)",
        placeholder="+,+,-,+",
        help="Comma-separated + or - values (+ for benefit, - for cost)"
    )
    
    st.subheader("📧 Email Address")
    email = st.text_input(
        "Enter your email",
        placeholder="your.email@example.com",
        help="Results will be sent to this email address"
    )
    
    submitted = st.form_submit_button("🚀 Analyze with TOPSIS", use_container_width=True)

if submitted:
    # Validation
    if uploaded_file is None:
        st.error("❌ Please upload a CSV file")
    elif not weights:
        st.error("❌ Please provide weights")
    elif not impacts:
        st.error("❌ Please provide impacts")
    elif not email:
        st.error("❌ Please provide an email address")
    elif not validate_email(email):
        st.error("❌ Please provide a valid email address")
    else:
        try:
            # Read CSV
            data = pd.read_csv(uploaded_file)
            num_criteria = data.shape[1] - 1
            
            # Validate inputs
            valid, message = validate_inputs(weights, impacts, num_criteria)
            
            if not valid:
                st.error(f"❌ {message}")
            else:
                with st.spinner('🔄 Performing TOPSIS analysis using your PyPI package...'):
                    # Perform TOPSIS using package
                    result_data, topsis_message = perform_topsis_with_package(data, weights, impacts)
                    
                    if result_data is None:
                        st.error(topsis_message)
                    else:
                        st.success(topsis_message)
                        
                        # Display results
                        st.subheader("📊 Results Preview")
                        st.dataframe(result_data, use_container_width=True)
                        
                        # Download button
                        csv = result_data.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="⬇️ Download Results CSV",
                            data=csv,
                            file_name="topsis_results.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                        
                        # Send email
                        with st.spinner('📧 Sending email...'):
                            email_success, email_message = send_email(email, result_data)
                            
                            if email_success:
                                st.success(f"✅ {email_message}")
                            else:
                                st.warning(f"⚠️ Results generated but email failed: {email_message}")
                                st.info("💡 You can still download the results using the button above")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Information box
st.markdown("""
<div class="info-box">
    <h3>📌 Instructions</h3>
    <ul style="color: #333;">
        <li>Number of weights must equal number of impacts</li>
        <li>Both must match the number of criteria columns in your CSV</li>
        <li>Weights must be numeric values separated by commas</li>
        <li>Impacts must be either '+' (benefit) or '-' (cost)</li>
        <li>CSV file must have at least 3 columns</li>
    </ul>
    <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-top: 10px; font-family: monospace; color: #333;">
        <strong style="color: #333;">Example:</strong><br>
        <span style="color: #333;">Weights: 0.25,0.25,0.25,0.25</span><br>
        <span style="color: #333;">Impacts: +,+,-,+</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: white;">
    <p>Developed by <strong>Prabhsimar Singh (102483078)</strong></p>
    <p>Course: UCS654 – Prescriptive Analytics</p>
    <p style="margin-top: 10px;">
        <a href="https://pypi.org/project/Topsis-Prabhsimar-102483078/" target="_blank" style="color: white;">📦 View Package on PyPI</a>
    </p>
</div>
""", unsafe_allow_html=True)