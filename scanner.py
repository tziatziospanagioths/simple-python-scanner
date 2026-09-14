import requests
import urllib3

# Suppress the warning for bypassing invalid SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SECURITY_HEADERS = [
    'Strict-Transport-Security', 
    'X-Frame-Options',           
    'X-Content-Type-Options',    
    'Content-Security-Policy',   
    'Referrer-Policy'            
]

def check_headers(url):
    """
    Scans the URL, retrieves headers, and calculates a Safeness Score.
    """
    scan_results = {
        'target': url,
        'status_code': None,
        'security_report': {
            'secure': [],      
            'vulnerable': []   
        },
        'score': 0, # Added a new field to hold our safeness percentage
        'error': None
    }
    
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        scan_results['target'] = url

    try:
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
            
            # Calculate the Safeness Score based on how many headers were found
            total_headers = len(SECURITY_HEADERS)
            secure_count = len(scan_results['security_report']['secure'])
            # (Secure / Total) * 100 to get the percentage
            scan_results['score'] = int((secure_count / total_headers) * 100)
                    
    except requests.exceptions.RequestException as e:
        scan_results['error'] = str(e)
        
    return scan_results