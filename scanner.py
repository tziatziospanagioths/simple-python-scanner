import requests

def check_headers(url):
    """
    Scans the target URL and returns a dictionary with the results.
    Instead of printing to the terminal, it packages the data for the Flask app.
    """

    scan_results = {
        'target': url,
        'status_code': None,
        'headers': {},
        'error': None
    }
    
   
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
        scan_results['target'] = url

    try:
       
        response = requests.get(url, timeout=5)
        scan_results['status_code'] = response.status_code
        
      
        if response.status_code == 200:
          
            scan_results['headers'] = dict(response.headers)
            
    except requests.exceptions.RequestException as e:
        
        scan_results['error'] = str(e)
        
    return scan_results

