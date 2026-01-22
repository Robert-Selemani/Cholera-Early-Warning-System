# Deployment Guide - Cholera Early Warning System

## Streamlit Cloud Deployment (Recommended)

Streamlit Cloud is the best platform for deploying this application. It's free, easy to use, and optimized for Streamlit apps.

### Prerequisites

1. **GitHub Account**: https://github.com/Robert-Selemani
2. **Repository**: https://github.com/Robert-Selemani/Cholera-Early-Warning-System
3. **Streamlit Cloud Account**: Sign up at https://share.streamlit.io/

### Deployment Steps

#### 1. Sign Up for Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign up" and authenticate with your GitHub account
3. Authorize Streamlit Cloud to access your repositories

#### 2. Deploy Your App

1. Click "New app" on Streamlit Cloud dashboard
2. Fill in the deployment form:
   - **Repository**: `Robert-Selemani/Cholera-Early-Warning-System`
   - **Branch**: `master`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain like `cholera-ews`

3. Click "Deploy!"

#### 3. Wait for Deployment

- Initial deployment takes 2-5 minutes
- Streamlit Cloud will:
  - Clone your repository
  - Install dependencies from `requirements.txt`
  - Install system packages from `packages.txt`
  - Configure settings from `.streamlit/config.toml`
  - Start your app

#### 4. Access Your App

Your app will be available at:
```
https://[your-app-name].streamlit.app
```

Example: `https://cholera-ews.streamlit.app`

### Configuration Files

The following files are configured for Streamlit Cloud:

#### 1. `requirements.txt`
- Lists all Python dependencies
- Automatically installed during deployment

#### 2. `packages.txt`
- System-level dependencies (apt packages)
- Required for geospatial operations

#### 3. `.streamlit/config.toml`
- Streamlit configuration
- Theme settings (CSIDNET colors)
- Server settings

#### 4. `.streamlit/secrets.toml` (Optional)
- Sensitive configuration (API keys, credentials)
- **Not** committed to GitHub
- Add secrets via Streamlit Cloud dashboard

### Adding Secrets (Optional)

If you need to add API keys or credentials:

1. Go to your app on Streamlit Cloud
2. Click "Settings" → "Secrets"
3. Add your secrets in TOML format:

```toml
[dhis2]
server_url = "https://your-dhis2-instance.org"
username = "your_username"
password = "your_password"

[api_keys]
climate_api_key = "your_key_here"
```

4. Click "Save"

Access secrets in code:
```python
import streamlit as st

# Access secrets
dhis2_url = st.secrets["dhis2"]["server_url"]
api_key = st.secrets["api_keys"]["climate_api_key"]
```

### Automatic Updates

Streamlit Cloud automatically redeploys when you push to GitHub:

1. Make changes to your code
2. Commit and push to the `master` branch
3. Streamlit Cloud detects the change
4. Automatically redeploys (takes 1-2 minutes)

### Managing Your Deployment

#### View Logs
1. Go to Streamlit Cloud dashboard
2. Click on your app
3. Click "Manage app" → "Logs"
4. View real-time application logs

#### Restart App
1. Go to your app settings
2. Click "Reboot app"
3. Wait for restart (30 seconds)

#### Delete App
1. Go to app settings
2. Click "Delete app"
3. Confirm deletion

### Resource Limits (Free Tier)

Streamlit Cloud free tier includes:
- **1 GB RAM** per app
- **1 CPU** core
- **Unlimited** apps (public repositories)
- **Sleep after inactivity**: Apps sleep after 7 days of no traffic

If your app needs more resources, consider upgrading to a paid plan.

### Troubleshooting

#### Issue: App Won't Start

**Solution:**
1. Check logs for errors
2. Verify `requirements.txt` has all dependencies
3. Ensure `app.py` is in the repository root
4. Check Python version compatibility (3.8+)

#### Issue: Import Errors

**Solution:**
1. Add missing packages to `requirements.txt`
2. Add system packages to `packages.txt`
3. Reboot the app

#### Issue: Out of Memory

**Solution:**
1. Reduce data size
2. Optimize code for memory usage
3. Consider upgrading to paid tier

#### Issue: Slow Performance

**Solution:**
1. Use `@st.cache_data` for data loading
2. Use `@st.cache_resource` for model loading
3. Optimize database queries
4. Reduce visualization complexity

### Performance Optimization

Add caching to improve performance:

```python
import streamlit as st

@st.cache_data
def load_data():
    """Cache data loading"""
    return pd.read_csv('data.csv')

@st.cache_resource
def load_model():
    """Cache model loading"""
    return joblib.load('model.pkl')
```

### Custom Domain (Optional)

To use a custom domain:

1. Go to app settings
2. Click "Custom domain"
3. Follow instructions to configure DNS
4. Add CNAME record to your domain

### Monitoring

Monitor your app:
- **Analytics**: View usage stats on Streamlit Cloud
- **Uptime**: Streamlit provides 99.9% uptime SLA
- **Alerts**: Set up email alerts for app issues

### Security Best Practices

1. **Never commit secrets** to GitHub
2. **Use secrets management** for API keys
3. **Validate user input** in forms
4. **Enable XSRF protection** (already configured)
5. **Keep dependencies updated** regularly

### Scaling Options

If you need more resources:

1. **Streamlit Cloud Teams**: $250/month
   - 4 GB RAM
   - Dedicated resources
   - Priority support

2. **Streamlit Cloud Enterprise**: Custom pricing
   - Custom resources
   - On-premises deployment
   - Advanced security

## Alternative: Self-Hosted Deployment

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t cholera-ews .
docker run -p 8501:8501 cholera-ews
```

### AWS Deployment

Use EC2 or Elastic Beanstalk:

1. Create EC2 instance (Ubuntu 22.04)
2. Install Python and dependencies
3. Clone repository
4. Run with `streamlit run app.py`
5. Use nginx as reverse proxy
6. Configure SSL certificate

### Heroku Deployment (Alternative)

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
port = $PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create cholera-ews
git push heroku master
```

## Post-Deployment Checklist

- [ ] App is accessible via URL
- [ ] All pages load correctly
- [ ] Data upload works
- [ ] Model training functions
- [ ] Predictions generate successfully
- [ ] Visualizations render properly
- [ ] Settings save correctly
- [ ] No error messages in logs
- [ ] Performance is acceptable
- [ ] Mobile responsive (check on phone)

## Support

For deployment help:
- **Streamlit Docs**: https://docs.streamlit.io/
- **Community Forum**: https://discuss.streamlit.io/
- **GitHub Issues**: https://github.com/Robert-Selemani/Cholera-Early-Warning-System/issues

## Update Schedule

Recommended update frequency:
- **Dependencies**: Monthly security updates
- **Features**: Quarterly releases
- **Bug fixes**: As needed
- **Data**: Weekly/monthly depending on sources

## Backup Strategy

Regular backups recommended:
1. **Code**: Already on GitHub
2. **Data**: Export CSV files monthly
3. **Models**: Download trained models
4. **Configurations**: Save YAML files

## Monitoring Checklist

Monitor these metrics:
- [ ] App uptime (aim for >99%)
- [ ] Response time (<3 seconds)
- [ ] Memory usage (<80% of limit)
- [ ] Error rate (<1%)
- [ ] User sessions
- [ ] Page load times

---

**Last Updated**: January 2026
**Version**: 1.0.0
