# TOPSIS Web Service

A Flask-based web application for performing TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) analysis.

## Features

✅ Upload CSV files for TOPSIS analysis  
✅ Input weights and impacts via web form  
✅ Email validation  
✅ Input validation (weights, impacts, file format)  
✅ Results sent via email  
✅ Beautiful responsive UI  
✅ Drag-and-drop file upload  

---

## Setup Instructions

### 1. Create Conda Environment

```bash
conda create -n topsis-web python=3.9 -y
conda activate topsis-web
```

### 2. Install Dependencies

```bash
cd web-service
pip install -r requirements.txt
```

### 3. Configure Email (IMPORTANT!)

Open `app.py` and update these lines (around line 100):

```python
sender_email = "your-email@gmail.com"      # Your Gmail address
sender_password = "your-app-password"       # Your Gmail app password
```

**How to get Gmail App Password:**
1. Go to your Google Account settings
2. Security → 2-Step Verification (enable if not enabled)
3. App passwords → Generate new app password
4. Select "Mail" and your device
5. Copy the 16-character password
6. Use this password in `app.py`

### 4. Run Locally

```bash
python app.py
```

Open browser: http://localhost:5000

---

## Usage

1. **Upload CSV File**
   - First column: Names/IDs
   - Remaining columns: Numeric criteria
   
2. **Enter Weights**
   - Comma-separated numeric values
   - Example: `0.25,0.25,0.25,0.25`

3. **Enter Impacts**
   - Comma-separated + or - values
   - `+` for benefit criteria (higher is better)
   - `-` for cost criteria (lower is better)
   - Example: `+,+,-,+`

4. **Enter Email**
   - Valid email address
   - Results will be sent here

5. **Click "Analyze with TOPSIS"**
   - Wait for processing
   - Check your email for results

---

## Input Validation

The application validates:
- ✅ File format (CSV only)
- ✅ Email format
- ✅ Number of weights = number of impacts = number of criteria
- ✅ Weights are numeric
- ✅ Impacts are + or -
- ✅ Criteria columns are numeric

---

## Example Input

**CSV File (sample.csv):**
```
Model,Storage,Camera,Price,Rating
M1,16,12,250,5
M2,16,8,200,3
M3,32,16,300,4
M4,32,8,275,4
M5,16,16,225,2
```

**Weights:** `0.25,0.25,0.25,0.25`  
**Impacts:** `+,+,-,+`  
**Email:** `your.email@example.com`

---

## Deployment

### Option 1: Render.com (Recommended - FREE)

1. Create account on https://render.com
2. New → Web Service
3. Connect your GitHub repository
4. Select `web-service` folder
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `gunicorn app:app`
7. Add `gunicorn` to requirements.txt
8. Deploy!

### Option 2: Railway.app (FREE)

1. Create account on https://railway.app
2. New Project → Deploy from GitHub
3. Select repository
4. Railway auto-detects Flask app
5. Deploy!

### Option 3: PythonAnywhere (FREE)

1. Create account on https://www.pythonanywhere.com
2. Upload your code
3. Configure web app
4. Set working directory to web-service
5. Reload web app

---

## File Structure

```
web-service/
├── app.py                 # Flask application
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary file storage (auto-created)
├── requirements.txt      # Dependencies
└── README.md            # This file
```

---

## Troubleshooting

**Email not sending:**
- Check Gmail credentials in `app.py`
- Enable "Less secure app access" or use App Password
- Check spam folder

**Module not found:**
- Activate conda environment: `conda activate topsis-web`
- Install dependencies: `pip install -r requirements.txt`

**File upload error:**
- Check file is CSV format
- File size under 16MB
- CSV has at least 3 columns

**Validation errors:**
- Weights count = impacts count = criteria columns count
- Impacts only + or -
- Weights must be numeric

---

## Security Notes

⚠️ **Before deploying to production:**
1. Change `app.secret_key` to a random string
2. Don't commit email credentials to GitHub
3. Use environment variables for sensitive data
4. Enable HTTPS in production

---

## Technologies Used

- **Flask** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical calculations
- **SMTP** - Email sending
- **HTML/CSS/JavaScript** - Frontend

---

## Author

**Prabhsimar Singh**  
Roll Number: 102483078  
Course: UCS654 – Prescriptive Analytics

---

## License

MIT License