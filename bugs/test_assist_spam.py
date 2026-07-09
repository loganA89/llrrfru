import sys, os, time, logging
import threading
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))
from fruitcraft_client import FruitClient

def setup_logger(name):
    os.makedirs('logs', exist_ok=True)
    log_file = f"logs/test_{name}_{int(time.time())}.log"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers = []
    fh = logging.FileHandler(log_file)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger, log_file

def run_test(recovery_code):
    logger, log_file = setup_logger('assist_spam')
    client = FruitClient()
    success, data = client.login(recovery_code, "android_exp_spam")
    
    if not success:
        logger.error("Login failed. Cannot proceed.")
        return "LOGIN_FAILED"
        
    logger.info("Testing Bug 5: Assist Spam (Concurrent help requests)")
    payload = {'battle_id': 999999} # Dummy ID
    results = []
    
    def send_req():
        try:
            resp = client.post('/live-battle/help', payload)
            results.append(resp)
        except Exception as e:
            results.append({"error": str(e)})
            
    threads = []
    for _ in range(5): # Send 5 concurrent requests
        t = threading.Thread(target=send_req)
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    if not results:
        res = "FAILED (No Response)"
    else:
        successes = [r for r in results if isinstance(r, dict) and r.get('status') is True]
        errors = [r for r in results if isinstance(r, dict) and not r.get('status')]
        
        logger.info(f"Concurrent requests resulted in {len(successes)} successes.")
        if len(successes) > 1:
            res = "VULNERABLE (Race condition allowed multiple assists)"
        elif len(successes) == 1:
            res = "PATCHED (Only 1 success allowed)"
        else:
            err_strs = str([e.get('error', '') for e in errors])
            if "already" in err_strs.lower():
                res = "PATCHED (Server tracks duplicate requests)"
            else:
                res = "PATCHED / FAILED (Invalid battle ID or general error)"
                
    logger.info(f"Bug 5: [{res}]")
    logger.info(f"Details: {results}")
    return res

def main():
    code = input("Enter recovery code: ").strip()
    if code:
        run_test(code)

if __name__ == '__main__':
    main()
