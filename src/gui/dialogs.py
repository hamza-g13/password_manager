import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QGroupBox, QFormLayout,
                             QLineEdit, QCheckBox, QHBoxLayout, QLabel,
                             QSlider, QPushButton, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from src.core import generator

class LoginDialog(QDialog):
    def __init__(self, storage, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.setWindowTitle("Login - Secure Vault")
        self.setFixedSize(400, 180)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        is_setup = not os.path.exists(str(self.storage.master_hash_file))
        title_text = "Create Master Password" if is_setup else "Enter Master Password"

        lbl_info = QLabel(title_text)
        lbl_info.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(lbl_info)

        self.pwd_input = QLineEdit()
        self.pwd_input.setEchoMode(QLineEdit.Password)
        self.pwd_input.setPlaceholderText("Master Password")
        self.pwd_input.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.pwd_input)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.verify_password)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def verify_password(self):
        pwd = self.pwd_input.text()
        if not pwd: return
        try:
            self.storage.set_master_password(pwd)
            self.accept()
        except ValueError:
            QMessageBox.critical(self, "Error", "Incorrect Master Password!")
            self.pwd_input.clear()
            self.pwd_input.setFocus()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


class AddEntryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Entry")
        self.setMinimumWidth(450)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # --- Form Section ---
        form_group = QGroupBox("Entry Details")
        form_layout = QFormLayout()

        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("e.g. Netflix, Gmail")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("email@example.com")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Generated password will appear here")

        form_layout.addRow("Service:", self.service_input)
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_group.setLayout(form_layout)

        # --- Generator Section ---
        gen_group = QGroupBox("Password Generator")
        gen_layout = QVBoxLayout()

        options_layout = QHBoxLayout()
        self.cb_upper = QCheckBox("A-Z")
        self.cb_upper.setChecked(True)
        self.cb_lower = QCheckBox("a-z")
        self.cb_lower.setChecked(True)
        self.cb_digits = QCheckBox("0-9")
        self.cb_digits.setChecked(True)
        self.cb_symbols = QCheckBox("@#$")
        self.cb_symbols.setChecked(True)

        options_layout.addWidget(self.cb_upper)
        options_layout.addWidget(self.cb_lower)
        options_layout.addWidget(self.cb_digits)
        options_layout.addWidget(self.cb_symbols)

        slider_layout = QHBoxLayout()
        self.lbl_length = QLabel("Length: 16")
        self.lbl_length.setFixedWidth(80)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(8, 64)
        self.slider.setValue(16)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(lambda v: self.lbl_length.setText(f"Length: {v}"))

        self.btn_generate = QPushButton("Generate")
        self.btn_generate.setProperty("class", "primary")
        self.btn_generate.clicked.connect(self.generate_new_password)

        slider_layout.addWidget(self.lbl_length)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.btn_generate)

        gen_layout.addLayout(options_layout)
        gen_layout.addLayout(slider_layout)
        gen_group.setLayout(gen_layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(form_group)
        layout.addWidget(gen_group)
        layout.addWidget(self.buttons)
        self.setLayout(layout)

    def generate_new_password(self):
        try:
            pwd = generator.generate_password(
                length=self.slider.value(),
                use_lower=self.cb_lower.isChecked(),
                use_upper=self.cb_upper.isChecked(),
                use_digits=self.cb_digits.isChecked(),
                use_symbols=self.cb_symbols.isChecked()
            )
            self.password_input.setText(pwd)
            self.password_input.setFocus()
        except ValueError:
            self.password_input.setText("")
            self.password_input.setPlaceholderText("Select at least one option!")

    def get_data(self):
        return {
            "service": self.service_input.text(),
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }

    def set_data(self, service, username, password):
        self.service_input.setText(service)
        self.service_input.setReadOnly(True)
        self.username_input.setText(username)
        self.password_input.setText(password)
        self.setWindowTitle(f"Edit {service}")
