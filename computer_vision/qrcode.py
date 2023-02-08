# This contains the library calls to read QR code from image
import cv2
import pyzbar
from pyzbar.pyzbar import decode

def read_qr_code(image):
    # Read the image
    img = cv2.imread(image)
    # Create a QRCodeDetector Object
    detector = cv2.QRCodeDetector()
    # Detect and decode the QR code
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    return data

# Use this to detect multiple QR codes in a single image
def read_qr_code_pyzbar(image):
    # Read the image
    img = cv2.imread(image)
    # Find the barcodes in the image and decode each of the barcodes
    decodedObjects = decode(img)
    # Loop over all decoded objects
    decoded_data = []
    for obj in decodedObjects:
        decoded_data.append(obj.data.decode("ascii"))
    return decoded_data

# def main():
#     # Read the QR code
#     data = read_qr_code("images/qr4.jpg")
#     print("QR Code Data:", data)
#     # Read the QR code using pyzbar
#     data = read_qr_code_pyzbar("images/qr4.jpg")
#     print("QR Code Data:", data)
    
# if __name__ == "__main__":
#     main()