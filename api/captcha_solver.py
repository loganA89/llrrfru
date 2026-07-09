import base64
import os
import io
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
import logging

class CaptchaSolver:
    def __init__(self, save_dir="."):
        self.save_dir = save_dir
        self.logger = logging.getLogger("CaptchaSolver")

    def solve(self, b64_string: str) -> str:
        """Solves a base64 encoded CAPTCHA image."""
        try:
            # Remove data URI prefix if present
            if "," in b64_string:
                b64_string = b64_string.split(",")[1]
            
            img_data = base64.b64decode(b64_string)
            img_path = os.path.join(self.save_dir, "captcha.png")
            
            with open(img_path, "wb") as f:
                f.write(img_data)
                
            self.logger.info(f"Saved CAPTCHA to {img_path}")
            
            if OCR_AVAILABLE:
                try:
                    img = Image.open(io.BytesIO(img_data))
                    text = pytesseract.image_to_string(img, config='--psm 8 -c tessedit_char_whitelist=0123456789').strip()
                    if text:
                        self.logger.info(f"OCR solved CAPTCHA: {text}")
                        return text
                except Exception as e:
                    self.logger.error(f"OCR failed: {e}")
            
            # Fallback to manual input
            print(f"Please open {img_path} and read the CAPTCHA.")
            return input("Enter CAPTCHA: ").strip()
            
        except Exception as e:
            self.logger.error(f"Failed to process CAPTCHA: {e}")
            return ""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    solver = CaptchaSolver()
    # Dummy test
    print("Captcha solver initialized. OCR Available:", OCR_AVAILABLE)
