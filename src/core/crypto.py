from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class crypto:
    def __init__(self):
        self.cipher = None
        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir/ 'data'
        data_dir.mkdir(exist_ok=True)

        self.salt_file = data_dir/ "salt.key"

    def initialize_master_password(self, master_password: str):
        salt = self._load_or_create_salt()
        key = self._derive_key(master_password, salt)
        self.cipher = Fernet(key)

    def _load_or_create_salt(self):
        if self.salt_file.exists():
            with open(self.salt_file, 'rb') as f:
                return f.read()
        else:
            salt_byte = os.urandom(16)
            with open(self.salt_file, 'wb') as f:
                f.write(salt_byte)
            return salt_byte

    def _derive_key(self, password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def encrypt(self, text: str):
        if not self.cipher:
            raise ValueError("Master_password not initialised")
        encrypted = self.cipher.encrypt(text.encode())
        return encrypted.decode()

    def decrypt(self,encrypted_text: str):
        if not self.cipher:
            raise ValueError("Master_password not initialised")
        decrypted = self.cipher.decrypt(encrypted_text.encode())
        return decrypted.decode()