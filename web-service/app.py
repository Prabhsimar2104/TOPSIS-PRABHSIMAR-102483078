from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import pandas as pd
from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

def perform_topsis(input_file, weights_str, impacts_str, output_file):
    """Perform TOPSIS calculation"""
    try:
        import numpy as np
        
        # Read input file
        data = pd.read_csv(input_file)
        
        if data.shape[1] < 3:
            return False, "Input file must contain at least 3 columns"
        
        # Extract criteria (all columns except first)
        try:
            criteria = data.iloc[:, 1:].astype(float)
        except:
            return False, "Criteria columns must be numeric"
        
        # Parse weights and impacts
        weights = np.array([float(w.strip()) for w in weights_str.split(',')])
        impacts = [i.strip() for i in impacts_str.split(',')]
        
        # Normalize the decision matrix
        norm = np.sqrt((criteria ** 2).sum())
        normalized = criteria / norm
        
        # Apply weights
        weighted = normalized * weights
        
        # Determine ideal best and ideal worst
        ideal_best = []
        ideal_worst = []
        
        for i in range(weighted.shape[1]):
            if impacts[i] == "+":
                ideal_best.append(weighted.iloc[:, i].max())
                ideal_worst.append(weighted.iloc[:, i].min())
            else:
                ideal_best.append(weighted.iloc[:, i].min())
                ideal_worst.append(weighted.iloc[:, i].max())
        
        ideal_best = np.array(ideal_best)
        ideal_worst = np.array(ideal_worst)
        
        # Calculate distances
        dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
        dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))
        
        # Calculate TOPSIS score
        score = dist_worst / (dist_best + dist_worst)
        rank = score.rank(ascending=False, method="dense")
        
        # Add score and rank to dataframe
        data["Topsis Score"] = score
        data["Rank"] = rank.astype(int)
        
        # Save output file
        data.to_csv(output_file, index=False)
        
        return True, "TOPSIS calculation successful"
    except Exception as e:
        return False, f"Error in TOPSIS calculation: {str(e)}"

def send_email(recipient_email, output_file):
    """Send email with result file"""
    try:
        # Email configuration - UPDATE THESE WITH YOUR CREDENTIALS
        sender_email = "simarprabh095@gmail.com"  # Change this
        sender_password = "wods spdg mvfq dsnx"   # Change this (use app password for Gmail)
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "TOPSIS Analysis Results"
        
        # Email body
        body = """
        Hello,
        
        Your TOPSIS analysis has been completed successfully!
        
        Please find the results attached to this email.
        
        Thank you for using our TOPSIS Web Service.
        
        Best regards,
        TOPSIS Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file
        filename = os.path.basename(output_file)
        attachment = open(output_file, "rb")
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        
        msg.attach(part)
        attachment.close()
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            file = request.files.get('file')
            weights = request.form.get('weights', '').strip()
            impacts = request.form.get('impacts', '').strip()
            email = request.form.get('email', '').strip()
            
            # Validate file
            if not file or file.filename == '':
                flash('Please select a CSV file', 'error')
                return redirect(request.url)
            
            if not allowed_file(file.filename):
                flash('Only CSV files are allowed', 'error')
                return redirect(request.url)
            
            # Validate email
            if not email:
                flash('Please provide an email address', 'error')
                return redirect(request.url)
            
            if not validate_email(email):
                flash('Please provide a valid email address', 'error')
                return redirect(request.url)
            
            # Validate weights and impacts
            if not weights:
                flash('Please provide weights', 'error')
                return redirect(request.url)
            
            if not impacts:
                flash('Please provide impacts', 'error')
                return redirect(request.url)
            
            # Save uploaded file
            filename = secure_filename(file.filename)
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_path)
            
            # Read file to get number of criteria
            try:
                df = pd.read_csv(input_path)
                num_criteria = df.shape[1] - 1  # Exclude first column
            except Exception as e:
                flash(f'Error reading CSV file: {str(e)}', 'error')
                os.remove(input_path)
                return redirect(request.url)
            
            # Validate inputs
            valid, message = validate_inputs(weights, impacts, num_criteria)
            if not valid:
                flash(message, 'error')
                os.remove(input_path)
                return redirect(request.url)
            
            # Perform TOPSIS
            output_filename = 'result_' + filename
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            success, message = perform_topsis(input_path, weights, impacts, output_path)
            
            if not success:
                flash(message, 'error')
                os.remove(input_path)
                return redirect(request.url)
            
            # Send email
            email_success, email_message = send_email(email, output_path)
            
            # Clean up files
            os.remove(input_path)
            os.remove(output_path)
            
            if email_success:
                flash('TOPSIS analysis completed! Results sent to your email.', 'success')
            else:
                flash(f'TOPSIS analysis completed but email failed: {email_message}', 'warning')
            
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)