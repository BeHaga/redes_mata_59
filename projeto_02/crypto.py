# TODO
# - criar codigo para criptografar as conexoes
# - voce pode usar criptografia simetrica ou assimetrica (AES ou RSA)
from cryptography.fernet import Fernet
import base64

class AES:
    def __init__(self, key=None):
        if key is None:
            self.key = self.generate_key()
        else:
            self.key = key

    def generate_key(self):
        return Fernet.generate_key()

    def encrypt(self, message):
        f = Fernet(self.key)
        # Codifica a mensagem para bytes antes de criptografar
        message_bytes = message.encode('utf-8')
        encrypted_message = f.encrypt(message_bytes)
        # Codifica a mensagem criptografada para base64
        return base64.b64encode(encrypted_message)

    def decrypt(self, encrypted_message):
        f = Fernet(self.key)
        # Decodifica a mensagem criptografada de base64
        encrypted_message_bytes = base64.b64decode(encrypted_message)
        decrypted_message_bytes = f.decrypt(encrypted_message_bytes)
        # Decodifica a mensagem descriptografada para string
        return decrypted_message_bytes.decode('utf-8')
