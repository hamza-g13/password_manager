import hashlib
from pathlib import Path

from src.core.crypto import crypto


class storage:
    def __init__(self, storage_file: str = "vault.txt"):
        base_dir = Path(__file__).resolve().parents[2]
        data_dir = base_dir/ 'data'

        data_dir.mkdir(exist_ok=True)

        self.storage_file = data_dir / storage_file
        self.master_hash_file = data_dir / "master.hash"
        self.crypto = crypto()

    def set_master_password(self,master_password: str):
        password_hash = hashlib.sha256(master_password.encode()).hexdigest()

        if self.master_hash_file.exists():
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
                entry_copy = entry.copy()
                entry_copy["password"] = self.crypto.decrypt(entry["password"])
                return entry_copy

        return None

    def delete_entry(self, service: str):
        entries = self.load_entries()
        new_entries = []

        removed = False

        for entry in entries:
            if entry["service"] == service:
                removed = True
                continue  # hoppa över denna → den tas bort
            new_entries.append(entry)

        if removed:
            self.save_entries(new_entries)

        return removed

    def update_entry(self, service: str, new_username: str , new_password: str ):
        entries = self.load_entries()
        updated = False

        for entry in entries:
            if entry["service"] == service:
                if new_username is not None:
                    entry["username"] = new_username

                if new_password is not None:
                    entry["password"] = self.crypto.encrypt(new_password)

                updated = True
                break

        if updated:
            self.save_entries(entries)

        return updated

    def generate_id(self):

        entries = self.load_entries()

        if not entries:
            return 1

        return max(entry["id"] for entry in entries) + 1

    def load_entries(self):
        if not self.storage_file.exists():
            return []

        entries = []
        with self.storage_file.open("r", encoding="utf-8") as storage:
            for line in storage:
                line = line.strip()
                if not line:
                    continue

                id_, service, username, password =line.split(";")

                entries.append({
                    "id":int(id_),
                    "service":service,
                    "username":username,
                    "password":password
                })
            return entries



    def save_entries(self, entries: list):
        with self.storage_file.open("w", encoding="utf-8") as storage:
            for entry in entries:
                line = f"{entry['id']};{entry['service']};{entry['username']};{entry['password']}\n"
                storage.write(line)
