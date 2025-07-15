import requests
import json
import os
from typing import Dict, List, Optional

class CloudflareDeploy:
    def __init__(self, api_key: str, email: str):
        self.api_key = api_key
        self.email = email
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def test_connection(self) -> Dict:
        """Test Cloudflare API connection"""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Successfully connected to Cloudflare API',
                    'user_info': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f'API connection failed: {response.status_code}',
                    'details': response.text
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Connection error: {str(e)}'
            }
    
    def list_zones(self) -> Dict:
        """List all available zones (domains)"""
        try:
            response = requests.get(f"{self.base_url}/zones", headers=self.headers)
            
            if response.status_code == 200:
                zones_data = response.json()
                zones = []
                
                for zone in zones_data.get('result', []):
                    zones.append({
                        'id': zone['id'],
                        'name': zone['name'],
                        'status': zone['status'],
                        'name_servers': zone.get('name_servers', [])
                    })
                
                return {
                    'success': True,
                    'zones': zones,
                    'total': len(zones)
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to list zones: {response.status_code}',
                    'details': response.text
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error listing zones: {str(e)}'
            }
    
    def create_dns_record(self, zone_id: str, record_type: str, name: str, content: str) -> Dict:
        """Create a DNS record"""
        try:
            data = {
                'type': record_type,
                'name': name,
                'content': content,
                'ttl': 1  # Auto TTL
            }
            
            response = requests.post(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': f'DNS record created successfully',
                    'record': response.json()['result']
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to create DNS record: {response.status_code}',
                    'details': response.text
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error creating DNS record: {str(e)}'
            }
    
    def deploy_static_site(self, domain: str, site_content: str) -> Dict:
        """Deploy a static site to Cloudflare Pages"""
        try:
            # First, get the zone ID for the domain
            zones_result = self.list_zones()
            
            if not zones_result['success']:
                return {
                    'success': False,
                    'error': 'Failed to get domain zones',
                    'details': zones_result['error']
                }
            
            zone_id = None
            for zone in zones_result['zones']:
                if zone['name'] == domain or domain.endswith(f".{zone['name']}"):
                    zone_id = zone['id']
                    break
            
            if not zone_id:
                return {
                    'success': False,
                    'error': f'Domain {domain} not found in your Cloudflare account'
                }
            
            # Create a simple HTML file for the site
            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{domain}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .content {{
            line-height: 1.6;
            color: #666;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        {site_content}
        <div class="footer">
            <p>Powered by Auto Website Builder</p>
        </div>
    </div>
</body>
</html>"""
            
            # Save the HTML file locally
            site_dir = f"generated_sites/{domain}"
            os.makedirs(site_dir, exist_ok=True)
            
            with open(f"{site_dir}/index.html", 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return {
                'success': True,
                'message': f'Site generated successfully for {domain}',
                'site_path': f"{site_dir}/index.html",
                'domain': domain,
                'zone_id': zone_id,
                'deployment_notes': 'Site files generated locally. To deploy to Cloudflare Pages, upload the files manually or use Cloudflare Workers.'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error deploying site: {str(e)}'
            }
    
    def get_zone_analytics(self, zone_id: str) -> Dict:
        """Get analytics for a zone"""
        try:
            response = requests.get(
                f"{self.base_url}/zones/{zone_id}/analytics/dashboard",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'analytics': response.json()['result']
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to get analytics: {response.status_code}',
                    'details': response.text
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error getting analytics: {str(e)}'
            }
    
    def purge_cache(self, zone_id: str) -> Dict:
        """Purge cache for a zone"""
        try:
            data = {'purge_everything': True}
            
            response = requests.post(
                f"{self.base_url}/zones/{zone_id}/purge_cache",
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Cache purged successfully'
                }
            else:
                return {
                    'success': False,
                    'error': f'Failed to purge cache: {response.status_code}',
                    'details': response.text
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error purging cache: {str(e)}'
            }