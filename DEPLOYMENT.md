# 🚀 SmartSDLC Deployment Guide

This guide covers multiple deployment options for the SmartSDLC application.

## 📋 Prerequisites

- Python 3.8+ installed
- Git repository with your SmartSDLC code
- IBM Watsonx API credentials
- Account on your chosen deployment platform

## 🔐 Security Setup

Before deploying, ensure your credentials are secure:

1. **Update `.streamlit/secrets.toml`:**
   ```toml
   [watsonx]
   api_key = "your_actual_api_key_here"
   project_id = "your_actual_project_id_here"
   url = "https://eu-de.ml.cloud.ibm.com"
   model_id = "ibm/granite-3-3-8b-instruct"
   ```

2. **Never commit credentials to version control**
3. **Use environment variables in production**

---

## 🌐 Deployment Options

### **1. Streamlit Cloud (Recommended - Free)**

**Best for:** Quick deployment, free hosting, easy setup

#### Setup Steps:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial SmartSDLC deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [https://share.streamlit.io/](https://share.streamlit.io/)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Secrets:**
   - In your app dashboard, go to "Settings" → "Secrets"
   - Add your Watsonx credentials:
   ```toml
   [watsonx]
   api_key = "your_api_key"
   project_id = "your_project_id"
   url = "https://eu-de.ml.cloud.ibm.com"
   model_id = "ibm/granite-3-3-8b-instruct"
   ```

4. **Redeploy** - Your app will automatically redeploy with the new secrets

**Pros:** Free, automatic deployments, built-in secrets management
**Cons:** Limited customization, Streamlit branding

---

### **2. Docker Deployment**

**Best for:** Full control, containerized deployment, production environments

#### Setup Steps:

1. **Build the Docker image:**
   ```bash
   docker build -t smartsdlc .
   ```

2. **Run with environment variables:**
   ```bash
   docker run -d \
     -p 8501:8501 \
     -e WATSONX_APIKEY="your_api_key" \
     -e WATSONX_PROJECT_ID="your_project_id" \
     -e WATSONX_URL="https://eu-de.ml.cloud.ibm.com" \
     -e MODEL_ID="ibm/granite-3-3-8b-instruct" \
     --name smartsdlc-app \
     smartsdlc
   ```

3. **Using Docker Compose:**
   ```bash
   # Create .env file
   echo "WATSONX_APIKEY=your_api_key" > .env
   echo "WATSONX_PROJECT_ID=your_project_id" >> .env
   echo "WATSONX_URL=https://eu-de.ml.cloud.ibm.com" >> .env
   echo "MODEL_ID=ibm/granite-3-3-8b-instruct" >> .env
   
   # Deploy
   docker-compose up -d
   ```

**Pros:** Full control, portable, production-ready
**Cons:** Requires Docker knowledge, manual server management

---

### **3. Heroku Deployment**

**Best for:** Easy cloud deployment, good free tier

#### Setup Steps:

1. **Install Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-smartsdlc-app
   ```

3. **Set environment variables:**
   ```bash
   heroku config:set WATSONX_APIKEY="your_api_key"
   heroku config:set WATSONX_PROJECT_ID="your_project_id"
   heroku config:set WATSONX_URL="https://eu-de.ml.cloud.ibm.com"
   heroku config:set MODEL_ID="ibm/granite-3-3-8b-instruct"
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open the app:**
   ```bash
   heroku open
   ```

**Pros:** Easy deployment, good free tier, automatic scaling
**Cons:** Limited free tier, requires credit card for verification

---

### **4. Railway Deployment**

**Best for:** Simple deployment, good free tier, automatic HTTPS

#### Setup Steps:

1. **Go to [Railway.app](https://railway.app/)**
2. **Connect your GitHub repository**
3. **Set environment variables:**
   - `WATSONX_APIKEY`
   - `WATSONX_PROJECT_ID`
   - `WATSONX_URL`
   - `MODEL_ID`
4. **Deploy automatically**

**Pros:** Very simple, good free tier, automatic HTTPS
**Cons:** Limited customization

---

### **5. Vercel Deployment**

**Best for:** Fast deployment, global CDN, automatic HTTPS

#### Setup Steps:

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel --prod
   ```

3. **Set environment variables in Vercel dashboard**

**Pros:** Fast, global CDN, automatic HTTPS
**Cons:** Limited Python support, may have issues with Streamlit

---

### **6. Google Cloud Run**

**Best for:** Scalable, pay-per-use, enterprise-ready

#### Setup Steps:

1. **Enable Cloud Run API:**
   ```bash
   gcloud services enable run.googleapis.com
   ```

2. **Build and deploy:**
   ```bash
   gcloud run deploy smartsdlc \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars WATSONX_APIKEY="your_key"
   ```

**Pros:** Highly scalable, pay-per-use, enterprise features
**Cons:** More complex setup, requires Google Cloud account

---

### **7. AWS Elastic Beanstalk**

**Best for:** Enterprise deployment, AWS integration

#### Setup Steps:

1. **Install AWS CLI and EB CLI**
2. **Initialize EB application:**
   ```bash
   eb init smartsdlc --platform python-3.9
   ```

3. **Set environment variables:**
   ```bash
   eb setenv WATSONX_APIKEY="your_key"
   eb setenv WATSONX_PROJECT_ID="your_project_id"
   ```

4. **Deploy:**
   ```bash
   eb create smartsdlc-env
   eb deploy
   ```

**Pros:** Enterprise features, AWS integration, auto-scaling
**Cons:** Complex setup, requires AWS knowledge

---

## 🔧 Environment Variables

All deployment methods use these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `WATSONX_APIKEY` | IBM Watsonx API key | `89B_QQncoXf53DaBc89zWwMpEvJ5lGfUoZ15eJuI7LaA` |
| `WATSONX_PROJECT_ID` | Watsonx project ID | `f7f03912-3bc3-43b1-9c1f-bcfb805ec438` |
| `WATSONX_URL` | Watsonx API URL | `https://eu-de.ml.cloud.ibm.com` |
| `MODEL_ID` | Model identifier | `ibm/granite-3-3-8b-instruct` |

## 📊 Performance Optimization

### **For Production Deployments:**

1. **Enable caching:**
   ```python
   @st.cache_data(ttl=3600)  # Cache for 1 hour
   def expensive_function():
       # Your expensive computation
       pass
   ```

2. **Optimize imports:**
   ```python
   # Use lazy imports for heavy libraries
   if st.button("Use PDF Feature"):
       import PyPDF2
   ```

3. **Set resource limits:**
   ```python
   # In .streamlit/config.toml
   [server]
   maxUploadSize = 200
   ```

## 🔍 Monitoring and Logging

### **Add logging to your app:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log important events
logger.info("User generated code")
logger.error("API call failed")
```

### **Health check endpoint:**
```python
if st.sidebar.button("Health Check"):
    try:
        # Test API connection
        watsonx_ai = get_watsonx_ai()
        st.success("✅ All systems operational")
    except Exception as e:
        st.error(f"❌ System error: {e}")
```

## 🚨 Troubleshooting

### **Common Issues:**

1. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **API Connection Issues:**
   - Verify credentials are correct
   - Check network connectivity
   - Ensure Watsonx service is available

3. **Memory Issues:**
   - Optimize code for memory usage
   - Use streaming for large responses
   - Implement proper cleanup

4. **Timeout Issues:**
   - Increase timeout settings
   - Implement retry logic
   - Use async operations where possible

## 📈 Scaling Considerations

### **For High Traffic:**

1. **Use load balancers**
2. **Implement caching (Redis)**
3. **Use CDN for static assets**
4. **Monitor resource usage**
5. **Set up auto-scaling**

### **Cost Optimization:**

1. **Use spot instances where possible**
2. **Implement request throttling**
3. **Cache expensive operations**
4. **Monitor API usage**

## 🔐 Security Best Practices

1. **Never commit secrets to version control**
2. **Use environment variables for all credentials**
3. **Implement rate limiting**
4. **Add input validation**
5. **Use HTTPS in production**
6. **Regular security updates**

---

## 🎯 Quick Start Recommendation

**For beginners:** Use **Streamlit Cloud**
**For developers:** Use **Docker + Cloud Run**
**For enterprises:** Use **AWS Elastic Beanstalk**

Choose the deployment method that best fits your needs, technical expertise, and budget! 