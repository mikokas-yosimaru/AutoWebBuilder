import streamlit as st
import os
from datetime import datetime
import sys
import warnings

# Suppress warnings for cleaner output on Streamlit Cloud
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Add the current directory to path to allow imports
if '.' not in sys.path:
    sys.path.insert(0, '.')

# Set up page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="Worker Login Panel Manager",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Auto Website Builder - Professional Domain Management System"
    }
)

# Import components with error handling for Streamlit Cloud
try:
    from components.site_builder import SiteBuilder
    from components.article_manager import ArticleManager
    from components.page_generator import PageGenerator
    from utils.domain_analyzer import DomainAnalyzer
    from utils.cloudflare_api import CloudflareAPI
    from utils.seo_optimizer import SEOOptimizer
    from utils.feed_generator import FeedGenerator
    from utils.gemini_ai import GeminiAI
    from utils.bing_image_scraper import BingImageScraper
    from utils.bing_image_search import BingImageSearch
    from utils.auto_content_manager import AutoContentManager
    from utils.multi_domain_manager import MultiDomainManager
    from utils.api_manager import APIManager
    from utils.keyword_generator import KeywordGenerator
    from utils.pixel_api import PixelAPI
    from utils.domain_config_manager import DomainConfigManager
    from utils.log_manager import LogManager
    from utils.article_formatter import ArticleFormatter
    from utils.template_engine import TemplateEngine
    from utils.adsense_manager import AdSenseManager
    from auth import AuthManager
    
    # Import all functions from main app
    from app import (
        show_worker_dashboard,
        show_add_site,
        show_manage_sites,
        show_articles,
        show_seo_tools,
        show_feed_management,
        show_cloudflare_settings,
        show_domain_management,
        show_domain_panel,
        show_domain_general_settings,
        show_domain_auto_content,
        show_domain_seo_settings,
        show_domain_feed_settings,
        show_domain_cloudflare_settings,
        show_domain_adsense_settings,
        show_domain_analytics,
        show_multi_domain_manager,
        show_domain_settings_modal,
        show_domain_analytics_modal,
        show_api_settings,
        show_auto_content_manager
    )
    
    components_loaded = True
    
except ImportError as e:
    components_loaded = False
    error_message = f"Error loading components: {str(e)}"
    st.error(error_message)
    st.stop()

# Initialize session state - compatible with Streamlit Cloud
def init_session_state():
    """Initialize session state variables for Streamlit Cloud compatibility"""
    if 'sites' not in st.session_state:
        st.session_state.sites = {}
    if 'current_site' not in st.session_state:
        st.session_state.current_site = None
    if 'articles' not in st.session_state:
        st.session_state.articles = {}
    if 'selected_menu' not in st.session_state:
        st.session_state.selected_menu = "Dashboard"
    if 'dashboard_page' not in st.session_state:
        st.session_state.dashboard_page = 0

# Initialize session state
init_session_state()

# CSS for hiding Streamlit Cloud elements
def hide_streamlit_elements():
    """Hide Streamlit Cloud-specific elements for a cleaner interface"""
    st.markdown("""
    <style>
    /* Hide Streamlit Cloud elements */
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom styling for professional appearance */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .status-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        z-index: 1000;
    }
    
    /* Enhanced sidebar styling */
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    /* Error handling styling */
    .error-container {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Loading animation */
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 2s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """, unsafe_allow_html=True)

# Main application function
def main():
    """Main application function optimized for Streamlit Cloud"""
    
    # Hide Streamlit elements
    hide_streamlit_elements()
    
    # Show loading indicator
    if not components_loaded:
        st.markdown('<div class="loading-spinner"></div>', unsafe_allow_html=True)
        st.error("Failed to load application components. Please refresh the page.")
        return
    
    # Online status indicator
    st.markdown("""
    <div class="status-indicator">
        🟢 Online
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize authentication with error handling
    try:
        auth_manager = AuthManager()
        
        # Check authentication
        if not auth_manager.is_session_valid():
            auth_manager.show_login_form()
            return
            
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.info("Please refresh the page to try again.")
        return
    
    # Initialize managers with error handling
    try:
        api_manager = APIManager()
        domain_config_manager = DomainConfigManager()
        log_manager = LogManager()
        article_formatter = ArticleFormatter()
        
        # Auto-clean logs with error handling
        try:
            log_manager.auto_clean_all_logs(24)
        except Exception as e:
            st.warning(f"Log cleanup warning: {str(e)}")
        
        # Initialize components with API manager
        site_builder = SiteBuilder()
        article_manager = ArticleManager()
        page_generator = PageGenerator()
        domain_analyzer = DomainAnalyzer()
        cloudflare_api = CloudflareAPI()
        seo_optimizer = SEOOptimizer()
        feed_generator = FeedGenerator()
        gemini_ai = GeminiAI(api_manager)
        bing_image_scraper = BingImageScraper(api_manager)
        bing_image_search = BingImageSearch()
        auto_content_manager = AutoContentManager(api_manager)
        multi_domain_manager = MultiDomainManager(api_manager)
        keyword_generator = KeywordGenerator(api_manager)
        pixel_api = PixelAPI(api_manager)
        adsense_manager = AdSenseManager()
        
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.info("Some features may not work properly. Please check your configuration.")
        return
    
    # Professional sidebar navigation
    with st.sidebar:
        st.markdown("""
        <style>
        .nav-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .nav-item {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .nav-item:hover {
            background: #e9ecef;
            border-color: #6c757d;
        }
        .nav-item.active {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border-color: #28a745;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # User info section
        try:
            current_user = auth_manager.get_current_user()
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
                <h4>👤 {current_user}</h4>
                <p>Worker Login Panel Manager</p>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"User info error: {str(e)}")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            try:
                auth_manager.logout()
                st.rerun()
            except Exception as e:
                st.error(f"Logout error: {str(e)}")
        
        st.markdown("---")
        
        # Navigation menu items (simplified for stability)
        nav_items = [
            ("🏠 Dashboard", "Dashboard"),
            ("🔐 API Settings", "API Settings"),
            ("➕ Add Site", "Add New Site")
        ]
        
        # Create navigation buttons
        for display_name, menu_value in nav_items:
            if st.button(display_name, key=f"nav_{menu_value}", use_container_width=True):
                st.session_state.selected_menu = menu_value
                st.rerun()
        
        # System status overview with error handling
        st.markdown("---")
        st.subheader("🔧 System Status")
        
        try:
            # Get domain status overview
            domain_status = log_manager.get_all_domain_status()
            
            if domain_status:
                healthy_count = sum(1 for status in domain_status.values() if status.get('status') == 'healthy')
                warning_count = sum(1 for status in domain_status.values() if status.get('status') == 'warning')
                error_count = sum(1 for status in domain_status.values() if status.get('status') == 'error')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("✅", healthy_count)
                with col2:
                    st.metric("⚠️", warning_count)
                with col3:
                    st.metric("❌", error_count)
                
                # Show status messages
                if error_count > 0:
                    st.error(f"🚨 {error_count} domain(s) have errors")
                    if st.button("🔍 View Error Logs"):
                        st.session_state.show_error_logs = True
                elif warning_count > 0:
                    st.warning(f"⚠️ {warning_count} domain(s) have warnings")
                else:
                    st.success("✅ All systems operational")
            else:
                st.info("No domains to monitor")
        
        except Exception as e:
            st.warning(f"Status check error: {str(e)}")
            st.info("System status temporarily unavailable")
        
        # User management panel with error handling
        try:
            auth_manager.show_user_management_panel()
        except Exception as e:
            st.warning(f"User management error: {str(e)}")
        
        menu_option = st.session_state.selected_menu
    
    # Main content area with error handling
    try:
        if menu_option == "Dashboard":
            show_worker_dashboard(multi_domain_manager, keyword_generator, pixel_api, 
                                log_manager, domain_config_manager, auto_content_manager, 
                                gemini_ai, bing_image_scraper, article_formatter)
        elif menu_option == "API Settings":
            show_api_settings(api_manager, pixel_api)
        elif menu_option == "Add New Site":
            show_add_site(site_builder, domain_analyzer, seo_optimizer, 
                         multi_domain_manager, domain_config_manager)
        else:
            st.error(f"Unknown menu option: {menu_option}")
            
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please try refreshing the page or contact support if the problem persists.")
        
        # Debug information for development
        if st.checkbox("Show debug information"):
            st.code(f"Error details: {str(e)}")
            st.code(f"Menu option: {menu_option}")

# Error handling for imports and execution
def run_app():
    """Run the application with comprehensive error handling"""
    try:
        main()
    except Exception as e:
        st.error(f"Critical application error: {str(e)}")
        st.info("Please refresh the page to restart the application.")
        
        # Show restart button
        if st.button("🔄 Restart Application"):
            st.rerun()

# Entry point for Streamlit Cloud
if __name__ == "__main__":
    run_app()