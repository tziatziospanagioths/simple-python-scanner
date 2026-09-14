import requests
import urllib3

# Suppress the warning that Python prints when we intentionally ignore SSL errors
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# A list of critical security headers we want to check for
SECURITY_HEADERS = [
    'Strict-Transport-Security', # Enforces HTTPS
    'X-Frame-Options',           # Prevents Clickjacking
    'X-Content-Type-Options',    # Prevents MIME-sniffing
    'Content-Security-Policy',   # Prevents XSS attacks
    'Referrer-Policy'            # Controls information sent in the Referer header
]

def check_headers(url):
    """
    Scans the target URL, retrieves headers, and analyzes them.
    Now configured to bypass invalid SSL certificates (useful for shady sites).
    """
    scan_results = {
        'target': url,
        'status_code': None,
        'security_report': {
            'secure': [],      
            'vulnerable': []   
        },
        'error': None
    }
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        scan_results['target'] = url

    try:
        # Added verify=False to force the connection even if the SSL certificate is invalid/fake
        response = requests.get(url, timeout=5, verify=False)
        scan_results['status_code'] = response.status_code
        
        if response.status_code == 200:
            headers_lower = {k.lower(): v for k, v in response.headers.items()}
            
            for header in SECURITY_HEADERS:
                if header.lower() in headers_lower:
                    scan_results['security_report']['secure'].append({
                        'name': header,
                        'value': headers_lower[header.lower()]
                    })
                else:
                    scan_results['security_report']['vulnerable'].append(header)
                    
    except requests.exceptions.RequestException as e:
        # We only catch actual connection drops now, not SSL mismatches
        scan_results['error'] = str(e)
        
    return scan_results