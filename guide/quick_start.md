# Quick Start Guide

## 🚀 Run Streamlit App in 3 Steps

### Step 1: Open Terminal/Command Prompt
Navigate to the project directory:
```bash
cd "c:\Users\Sushruth M S\OneDrive\文档\Projects\Aspect-based-Sentimental-Analysis"
```

### Step 2: Activate Environment (if using virtual environment)
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Run the App
```bash
streamlit run streamlit_app.py
```

## 🌐 Access the App
Open your browser and go to: **http://localhost:8501**

## 🎯 What You Can Do
- **Single Text Analysis**: Analyze individual reviews
- **Batch Processing**: Analyze multiple texts at once
- **File Upload**: Upload CSV files for bulk analysis

## 🔧 Common Commands
```bash
# Run on different port
streamlit run streamlit_app.py --server.port 8502

# Stop the app
Ctrl + C (in terminal)

# Check if running
netstat -an | findstr 8501
```

## ❗ Troubleshooting
- **Port busy**: Use `--server.port 8502`
- **Module error**: Run `pip install -r requirements.txt`
- **Browser won't open**: Manually go to `http://localhost:8501`

---
**That's it! Your Streamlit app should now be running. 🎉**
