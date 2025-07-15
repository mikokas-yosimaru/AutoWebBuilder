import streamlit as st

def show_api_settings(api_manager, pixel_api):
    """Simplified API settings with only Gemini and Cloudflare API"""
    st.header("🔐 API Settings")
    
    # Custom CSS for cPanel-like appearance
    st.markdown("""
    <style>
    .api-status-card {
        background: #f0f2f6;
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .api-key-input {
        background: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 4px;
        padding: 8px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get API status
    api_status = api_manager.get_api_status()
    
    # API Status Overview
    st.subheader("📊 API Status Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        gemini_status = "✅ Connected" if api_status['gemini']['success'] else "❌ Disconnected"
        st.metric("Gemini Status", gemini_status)
    
    with col2:
        cloudflare_status = "✅ Connected" if api_status['cloudflare']['success'] else "❌ Disconnected"
        st.metric("Cloudflare Status", cloudflare_status)
    
    # Gemini API Configuration
    st.subheader("🤖 Gemini AI Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_gemini_key = api_manager.get_api_key('GEMINI_API_KEY') or ''
        new_gemini_key = st.text_input(
            "Gemini API Key",
            value=current_gemini_key[:20] + "..." if len(current_gemini_key) > 20 else current_gemini_key,
            type="password",
            help="Get your API key from Google AI Studio"
        )
        
        if st.button("Update Gemini API Key"):
            if new_gemini_key and not new_gemini_key.endswith("..."):
                if api_manager.update_api_key('GEMINI_API_KEY', new_gemini_key):
                    st.success("✅ Gemini API key updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update Gemini API key")
            else:
                st.warning("Please enter a valid API key")
    
    with col2:
        if st.button("Test Gemini API"):
            test_result = api_manager.test_gemini_api()
            if test_result['success']:
                st.success("✅ Gemini API working!")
            else:
                st.error(f"❌ {test_result['error']}")
    
    # Cloudflare API Configuration
    st.subheader("☁️ Cloudflare Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        current_cloudflare_key = api_manager.get_api_key('CLOUDFLARE_API_KEY') or ''
        new_cloudflare_key = st.text_input(
            "Cloudflare API Key",
            value=current_cloudflare_key[:20] + "..." if len(current_cloudflare_key) > 20 else current_cloudflare_key,
            type="password",
            help="Get your API key from Cloudflare Dashboard"
        )
        
        # Cloudflare email
        current_cloudflare_email = api_manager.get_api_key('CLOUDFLARE_EMAIL') or ''
        new_cloudflare_email = st.text_input(
            "Cloudflare Email",
            value=current_cloudflare_email,
            help="Your Cloudflare account email"
        )
        
        col1a, col1b = st.columns(2)
        
        with col1a:
            if st.button("Update Cloudflare API Key"):
                if new_cloudflare_key and not new_cloudflare_key.endswith("..."):
                    if api_manager.update_api_key('CLOUDFLARE_API_KEY', new_cloudflare_key):
                        st.success("✅ Cloudflare API key updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update Cloudflare API key")
                else:
                    st.warning("Please enter a valid API key")
        
        with col1b:
            if st.button("Update Cloudflare Email"):
                if new_cloudflare_email:
                    if api_manager.update_api_key('CLOUDFLARE_EMAIL', new_cloudflare_email):
                        st.success("✅ Cloudflare email updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update Cloudflare email")
                else:
                    st.warning("Please enter a valid email")
    
    with col2:
        if st.button("Test Cloudflare API"):
            test_result = api_manager.test_cloudflare_api()
            if test_result['success']:
                st.success("✅ Cloudflare API working!")
            else:
                st.error(f"❌ {test_result['error']}")
    
    # API Usage Guidelines
    st.subheader("📋 API Usage Guidelines")
    
    st.markdown("""
    **Gemini API:**
    - Free tier: 15 requests per minute
    - Used for: Article generation, keyword research, SEO optimization
    - Get your key: [Google AI Studio](https://ai.google.dev/)
    
    **Cloudflare API:**
    - Used for: Domain management, DNS configuration, site deployment
    - Get your key: [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens)
    - Requires: API key + account email
    
    **API Key Security:**
    - Keys are stored locally in `apikey.txt`
    - Never share your API keys publicly
    - Rotate keys regularly for security
    """)
    
    # Load API keys from file
    if st.button("🔄 Reload API Keys from File"):
        api_manager.load_api_keys()
        st.success("✅ API keys reloaded from apikey.txt")
        st.rerun()
    
    # Show current API file content
    with st.expander("View apikey.txt Content"):
        try:
            with open("apikey.txt", "r") as f:
                content = f.read()
                st.code(content, language="text")
        except FileNotFoundError:
            st.warning("apikey.txt file not found. It will be created automatically.")
        except Exception as e:
            st.error(f"Error reading apikey.txt: {str(e)}")