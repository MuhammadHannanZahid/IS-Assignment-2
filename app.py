from flask import Flask, render_template, request, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import os

app = Flask(__name__)

SECRET_KEY = b'mySuperSecret123' 

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process():
    data = request.get_json()
    
    if not data or 'text' not in data or 'algorithm' not in data or 'action' not in data:
        return jsonify({"error": "Missing required fields."}), 400
        
    text = data['text']
    algorithm = data['algorithm']
    action = data['action']
    
    try:
        shift = int(data.get('shift', 3))
    except ValueError:
        shift = 3

    result = ""

    try:
        if action == 'encrypt':
            if algorithm == 'aes':
                iv = os.urandom(16)
                cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
                ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
                result = base64.b64encode(iv + ct_bytes).decode('utf-8')
            
            elif algorithm == 'base64':
                result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
            
            elif algorithm == 'caesar':
                result = caesar_cipher(text, shift) # Uses custom shift
            
            elif algorithm == 'sha256':
                result = hashlib.sha256(text.encode('utf-8')).hexdigest()
            else:
                return jsonify({"error": "Invalid algorithm."}), 400

        elif action == 'decrypt':
            if algorithm == 'aes':
                try:
                    ct = base64.b64decode(text)
                    iv = ct[:16]
                    ct_bytes = ct[16:]
                    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
                    pt = unpad(cipher.decrypt(ct_bytes), AES.block_size)
                    result = pt.decode('utf-8')
                except ValueError:
                    return jsonify({"error": "Decryption failed. Invalid ciphertext or key."}), 400
            
            elif algorithm == 'base64':
                result = base64.b64decode(text).decode('utf-8')
            
            elif algorithm == 'caesar':
                result = caesar_cipher(text, -shift) # Uses reverse custom shift
            
            elif algorithm == 'sha256':
                return jsonify({"error": "SHA-256 cannot be decrypted."}), 400
            else:
                return jsonify({"error": "Invalid algorithm."}), 400

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": "Processing error. Please check your inputs."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)