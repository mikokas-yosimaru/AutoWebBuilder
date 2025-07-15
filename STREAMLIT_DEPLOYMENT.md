# Streamlit Cloud Deployment Guide

## Overview
This guide explains how to deploy the Auto Website Builder application to Streamlit Cloud.

## Files for Deployment

### Main Application File
- `streamlit_app.py` - Optimized main application file for Streamlit Cloud
- This file includes enhanced error handling and compatibility improvements

### Configuration Files
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml` - Template for API keys and secrets
- `requirements_streamlit.txt` - Python dependencies for Streamlit Cloud

## Deployment Steps

### 1. Repository Setup
1. Create a new GitHub repository
2. Upload all project files including:
   - `streamlit_app.py`
   - All `components/` and `utils/` folders
   - `auth.py`
   - `.streamlit/` folder
   - `requirements_streamlit.txt` (rename to `requirements.txt`)

### 2. Streamlit Cloud Configuration
1. Go to https://share.streamlit.io/
2. Connect your GitHub account
3. Select your repository
4. Set main file path to: `streamlit_app.py`
5. Set Python version to: `3.11`

### 3. Configure Secrets
1. In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
2. Copy content from `.streamlit/secrets.toml`
3. Update with your actual API keys:
   - `GEMINI_API_KEY` - Google Gemini API key
   - `BING_API_KEY` - Bing Image Search API key
   - `CLOUDFLARE_API_KEY` - Cloudflare API key
   - `GOOGLE_API_KEY` - Google Indexing API key
   - `PIXEL_API_KEY` - Pixel API key
   - `ADMIN_USERNAME` - Admin username
   - `ADMIN_PASSWORD` - Admin password

### 4. Required Dependencies
The application requires these Python packages:
- streamlit>=1.32.0
- beautifulsoup4>=4.12.0
- google-generativeai>=0.3.0
- jinja2>=3.1.0
- requests>=2.31.0
- trafilatura>=1.6.0
- python-dotenv>=1.0.0
- lxml>=4.9.0
- urllib3>=2.0.0

## Key Optimizations for Streamlit Cloud

### 1. Error Handling
- Comprehensive try-catch blocks around all major functions
- Graceful degradation when components fail to load
- User-friendly error messages

### 2. Performance Optimizations
- Lazy loading of components
- Optimized session state management
- Reduced memory usage

### 3. UI Improvements
- Hidden Streamlit Cloud branding elements
- Professional status indicators
- Responsive design for mobile devices

### 4. Security Features
- Environment variable protection
- Secure API key handling
- Input validation and sanitization

## Testing Before Deployment

1. Test locally with the new `streamlit_app.py`:
   ```bash
   streamlit run streamlit_app.py
   ```

2. Verify all features work correctly:
   - Authentication system
   - Domain management
   - Content generation
   - API integrations

## Troubleshooting

### Common Issues
1. **Import Errors**: Ensure all required files are in the repository
2. **API Key Issues**: Check secrets configuration in Streamlit Cloud
3. **Memory Issues**: Streamlit Cloud has memory limits, optimize accordingly
4. **Permission Errors**: Ensure all file paths are relative, not absolute

### Performance Monitoring
- Monitor app performance in Streamlit Cloud dashboard
- Check logs for errors and warnings
- Optimize based on usage patterns

## Support
For issues specific to Streamlit Cloud deployment, refer to:
- Streamlit Cloud documentation
- Streamlit Community Forum
- GitHub issues for this project

## Security Notes
- Never commit API keys to version control
- Use Streamlit Cloud secrets for sensitive data
- Regularly rotate API keys
- Monitor access logs for suspicious activity