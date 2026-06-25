# Troubleshooting Guide

## 🔧 Common Issues and Solutions

### 1. Port Already in Use
**Error**: `Port 8501 is already in use`

**Solutions**:
```bash
# Option 1: Use different port
streamlit run streamlit_app.py --server.port 8502

# Option 2: Kill existing process (Windows)
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F

# Option 3: Kill existing process (macOS/Linux)
lsof -ti:8501 | xargs kill -9
```

### 2. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solutions**:
```bash
# Check if in correct environment
which python
which pip

# Install requirements
pip install -r requirements.txt

# If still failing, install individually
pip install streamlit pandas plotly wordcloud matplotlib numpy
```

### 3. Virtual Environment Issues
**Error**: Environment not activating or wrong Python version

**Solutions**:
```bash
# Create new virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify activation
where python  # Windows
which python  # macOS/Linux
```

### 4. Permission Errors
**Error**: `Permission denied` or `Access denied`

**Solutions**:
```bash
# Windows: Run as Administrator
# Right-click Command Prompt → Run as Administrator

# macOS/Linux: Use sudo (if necessary)
sudo streamlit run streamlit_app.py

# Check file permissions
ls -la streamlit_app.py  # Unix
icacls streamlit_app.py  # Windows
```

### 5. Browser Issues
**Error**: Browser doesn't open or shows connection error

**Solutions**:
```bash
# Manually open browser
# Go to: http://localhost:8501

# Try different browser
# Chrome, Firefox, Edge, Safari

# Check firewall settings
# Allow Python/Streamlit through firewall

# Use different address
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### 6. Memory/Performance Issues
**Error**: App runs slowly or crashes

**Solutions**:
```python
# Clear cache in app
st.cache_data.clear()

# Optimize data loading
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# Reduce data size
df = df.head(1000)  # Limit rows for testing
```

### 7. File Upload Issues
**Error**: File upload fails or shows errors

**Solutions**:
```python
# Check file size (default limit: 200MB)
# Increase in .streamlit/config.toml:
[server]
maxUploadSize = 400

# Validate file type
if uploaded_file.type != 'text/csv':
    st.error("Please upload a CSV file")

# Handle encoding issues
try:
    df = pd.read_csv(uploaded_file, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(uploaded_file, encoding='latin-1')
```

### 8. Model Loading Errors
**Error**: Cannot load trained model

**Solutions**:
```python
# Check file path
import os
if os.path.exists('model.pkl'):
    print("Model file found")
else:
    print("Model file not found")

# Handle missing model gracefully
try:
    model = load_model('model.pkl')
except FileNotFoundError:
    st.warning("Model not found. Using demo mode.")
    model = None
```

### 9. Data Processing Errors
**Error**: DataFrame or data manipulation errors

**Solutions**:
```python
# Check data types
st.write(df.dtypes)

# Handle missing columns
if 'text' not in df.columns:
    st.error("CSV must contain 'text' column")
    st.stop()

# Handle empty data
if df.empty:
    st.warning("No data to analyze")
    st.stop()
```

### 10. Configuration Issues
**Error**: Streamlit configuration problems

**Solutions**:
```bash
# Reset configuration
rm -rf ~/.streamlit/  # macOS/Linux
rmdir /s ~/.streamlit/  # Windows

# Create new config
mkdir .streamlit
# Add config.toml file

# Check config location
streamlit config show
```

## 🐛 Debug Mode

### Enable Debug Logging
```bash
streamlit run streamlit_app.py --logger.level debug
```

### Add Debug Prints
```python
# In your code
st.write("Debug: Variable value =", variable)
print(f"Debug: {variable}")  # Console output
```

### Check System Requirements
```python
import sys
st.write(f"Python version: {sys.version}")
st.write(f"Streamlit version: {st.__version__}")
```

## 📞 Getting Help

### 1. Check Logs
- Terminal output for error messages
- Browser developer console (F12)

### 2. Community Resources
- Streamlit Community Forum
- Stack Overflow (tag: streamlit)
- GitHub Issues

### 3. Documentation
- Official Streamlit Docs
- API Reference
- Component Gallery

### 4. Local Debugging
```python
# Add to your code for debugging
import traceback

try:
    # Your code here
    pass
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.text(traceback.format_exc())
```

---

**Note**: If none of these solutions work, try creating a minimal test app to isolate the issue:

```python
import streamlit as st
st.title("Test App")
st.write("If you see this, Streamlit is working!")
```

Save as `test_app.py` and run with `streamlit run test_app.py`.
