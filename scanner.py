import requests

def check_headers(url):
    print(f"[*] Starting scan on: {url}\n")
    try:
       
        response = requests.get(url, timeout=5)
        
        
        if response.status_code == 200:
            print("[+] Target is online! Checking headers...\n")
            
            
            for header, value in response.headers.items():
                print(f" - {header}: {value}")
        else:
            print(f"[-] Target returned status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection error: {e}")

if __name__ == "__main__":
    target_url = "http://example.com"
    check_headers(target_url)