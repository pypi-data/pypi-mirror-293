import cv2
import pyzbar.pyzbar as pyzbar
import pyotp
import argparse

class QRDecoder:
    def __init__(self, image_path):
        self.image_path = image_path

    def decode_qr(self):
        gray = cv2.cvtColor(cv2.imread(self.image_path), cv2.COLOR_BGR2GRAY)
        qr_codes = pyzbar.decode(gray)
        for qr_code in qr_codes:
            decoded_data = qr_code.data.decode("utf-8")
            print("Decoded QR Data:", decoded_data)
            return decoded_data
        return None

class OTPGenerator:
    def __init__(self, secret):
        self.secret = secret
        self.otp = pyotp.TOTP(secret)

    def generate_code(self):
        return self.otp.now()

    def display_info(self):
        print("2FA Secret:", self.secret)
        print("2FA Code:", self.generate_code())

class TwoFactorAuthApp:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='QR Code Decoder and OTP Generator.')
        subparsers = self.parser.add_subparsers(dest='command')
        
        qr_parser = subparsers.add_parser('decode', help='Decode QR code from an image')
        qr_parser.add_argument('image_path', type=str, help='Path to the image containing QR code')
        
        otp_parser = subparsers.add_parser('otp', help='Generate OTP from a 2FA secret')
        otp_parser.add_argument('secret', type=str, help='2FA secret')

    def run(self):
        args = self.parser.parse_args()
        
        if args.command == 'decode':
            decoder = QRDecoder(args.image_path)
            decoder.decode_qr()
        elif args.command == 'otp':
            generator = OTPGenerator(args.secret)
            generator.display_info()
        else:
            self.parser.print_help()

if __name__ == "__main__":
    app = TwoFactorAuthApp()
    app.run()
