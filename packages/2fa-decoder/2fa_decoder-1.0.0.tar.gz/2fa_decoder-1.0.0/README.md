**The Project is used To Extract Raw Data From a QR Code & Generate an OTP From Secret Code Entered Via The keyboard.**

Installation
```
# pip install opencv-python pyzbar pyotp
# pip install 2fa_decoder
```

How To Use
```
# 2fa_decoder [-h] {decode,otp} INPUT
# QR Code Decoder and OTP Generator
# Arguments:
# decode		Decode QR Code With <INPUT> - Path To QR Code
# otp			Generate OTP From Secret Code
# -h, --help	Show This Help Message and Exit
```

Example
| Command	    | Output 		|
| :-------------: |:-------------:|
| # 2fa_decoder decode C:\Users\Test\QR-Code.png	| This-Is-Raw-Data-From-QR-Code
| # 2fa_decoder otp 1233214566547899870				| 123456