import hashlib
import os.path
from os import path

from PyQt5.QtSql import userName, password

from src.core.crypto import crypto


class storage:
    def __init__(self, storage_file: str = "vault.txt"):
        base_dir = path(__file__).parents[1]
        base_dir = base_dir.parent
        data_dir = base_dir/ 'data'

        data_dir.mkdir(exist_ok=True)

        self.storage_file = str(data_dir / storage_file)
        self.master_hash_file = str(data_dir / "master.hash")
        self.crypto = crypto()

    def set_master_password(self,master_password: str):
        password_hash = hashlib.sha256(master_password.encode()).hexdigest()

        if os.path.exists(self.master_hash_file):
            with open(self.master_hash_file, 'r') as key:
                stored_hash = key.read()

            if password_hash != stored_hash:
                raise ValueError("Wrong Master_Password")

        else:
            with open(self.master_hash_file, 'w') as key:
                key.write(password_hash)

        self.crypto.initialize_master_password(master_password)

    def save_entry(self, service: str, username: str, new_password: str):
        entries = self.load_entries()
        entry = {
            "id":self.generate_id(),
            "service":service,
            "username":username,
            "password":self.crypto.encrypt(new_password)
        }

        entries.append(entry)
        self.save_entries(entries)

    def get_entry(self, service: str):
        entries = self.load_entries()
        for entry in entries:
            if entry["service"]== service:
                entry["password"] = self.crypto.decrypt(entry["password"])
                return entry

        return None

    def delete_entry(self):

    def update_entry(self):

    def generate_id(self):

    def load_entries(self):

    def save_entries(self):

