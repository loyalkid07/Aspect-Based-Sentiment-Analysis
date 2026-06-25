# Streamlit App Setup and Execution Guide

## Prerequisites

Before running the Streamlit app, ensure you have the following installed:

### 1. Python Environment
- Python 3.8 or higher
- Virtual environment (recommended)

### 2. Required Dependencies
All dependencies are listed in `requirements.txt`. Make sure your environment has them installed.

## Step-by-Step Setup

### Step 1: Navigate to Project Directory
```bash
cd "c:\Users\Sushruth M S\OneDrive\文档\Projects\Aspect-based-Sentimental-Analysis"
```

### Step 2: Activate Virtual Environment (if using one)
```bash
# For Windows
venv\Scripts\activate

# For macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
streamlit --version
```

## Running the Streamlit App

### Method 1: Basic Execution
```bash
streamlit run streamlit_app.py
```

### Method 2: Run with Custom Port
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Method 3: Run in Headless Mode (for servers)
```bash
streamlit run streamlit_app.py --server.headless true
```

### Method 4: Run with Custom Configuration
```bash
streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
```

## Accessing the Application

After running the command, you'll see output similar to:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

- **Local URL**: Access from the same machine
- **Network URL**: Access from other devices on the same network

## Application Features

### 1. Single Text Analysis
- Enter individual text for aspect-based sentiment analysis
- View results in table and chart format
- Real-time analysis with interactive visualizations

### 2. Batch Analysis
- Analyze multiple texts simultaneously
- Compare sentiment across different inputs
- Aggregate results and statistics

### 3. File Upload Analysis
- Upload CSV files with text data
- Bulk processing capabilities
- Export results for further analysis

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Port Already in Use
```bash
# Error: Port 8501 is already in use
# Solution: Use a different port
streamlit run streamlit_app.py --server.port 8502
```

#### Issue 2: Module Not Found
```bash
# Error: ModuleNotFoundError
# Solution: Install missing dependencies
pip install -r requirements.txt
```

#### Issue 3: Permission Denied
```bash
# Error: Permission denied
# Solution: Run as administrator or check file permissions
```

#### Issue 4: Browser Doesn't Open Automatically
- Manually navigate to `http://localhost:8501`
- Check firewall settings
- Try different browser

### Performance Optimization

#### 1. Enable Caching
The app uses `@st.cache_data` for better performance. Ensure your functions are properly cached.

#### 2. Memory Management
For large files:
- Process data in chunks
- Use memory-efficient data types
- Clear cache when needed: `st.cache_data.clear()`

#### 3. Configuration Tuning
Modify `.streamlit/config.toml` for optimal performance:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false
```

## Development Mode

### Hot Reloading
Streamlit automatically reloads when you save changes to your Python files.

### Debug Mode
```bash
streamlit run streamlit_app.py --logger.level debug
```

### Environment Variables
Set environment variables for different configurations:
```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=false
```

## Deployment Options

### 1. Local Network Sharing
```bash
streamlit run streamlit_app.py --server.address 0.0.0.0
```

### 2. Cloud Deployment
- **Streamlit Cloud**: Connect GitHub repository
- **Heroku**: Use Procfile for deployment
- **AWS/GCP**: Use Docker containers

### 3. Docker Deployment
Create a Dockerfile:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## Security Considerations

### 1. CORS Configuration
```toml
[server]
enableCORS = false
enableXsrfProtection = false
```

### 2. File Upload Security
- Validate file types
- Limit file sizes
- Sanitize file content

### 3. Data Privacy
- Don't log sensitive information
- Implement secure data handling
- Use HTTPS in production

## Monitoring and Logging

### 1. Application Logs
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 2. Performance Monitoring
- Monitor memory usage
- Track response times
- Log user interactions

### 3. Error Handling
```python
try:
    # Your code here
    pass
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    logging.error(f"Error: {str(e)}")
```

## Next Steps

1. **Model Integration**: Connect your trained ABSA model
2. **Data Pipeline**: Implement real-time data processing
3. **User Authentication**: Add login/logout functionality
4. **Database Integration**: Store analysis results
5. **API Integration**: Connect external services

## Support and Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: Report bugs and feature requests
- **Tutorials**: https://streamlit.io/gallery

---

**Note**: This guide assumes you have basic knowledge of Python and command-line operations. For additional help, refer to the Streamlit official documentation.
