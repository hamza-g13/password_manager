from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton,
                             QHeaderView, QLabel, QApplication, QMessageBox)
from PyQt5.QtCore import Qt
from .dialogs import AddEntryDialog

class MainWindow(QMainWindow):
    def __init__(self, storage_manager):
        super().__init__()
        self.storage = storage_manager
        self.setWindowTitle("Secure Pass Manager")
        self.resize(1000, 600)
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # --- Header ---
        header_layout = QHBoxLayout()
        title_label = QLabel("My Vault")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")

        self.btn_add = QPushButton("+ Add Password")
        self.btn_add.setFixedSize(160, 45)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setProperty("class", "primary")
        self.btn_add.clicked.connect(self.show_add_dialog)

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_add)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Service", "Username", "Password", "Actions"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.table.setColumnWidth(3, 280)  # Ökad bredd för extra knapp
        self.table.verticalHeader().setDefaultSectionSize(55)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setAlternatingRowColors(True)

        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.table)

    def show_add_dialog(self):
        dialog = AddEntryDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            if data["service"] and data["password"]:
                try:
                    self.storage.save_entry(data["service"], data["username"], data["password"])
                    self.refresh_table()
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"Could not save entry: {e}")

    def refresh_table(self):
        try:
            entries = self.storage.load_entries()
        except Exception as e:
            print(f"Error loading entries: {e}")
            entries = []

        self.table.setRowCount(0)

        for entry in entries:
            row = self.table.rowCount()
            self.table.insertRow(row)

            try:
                decrypted_pwd = self.storage.crypto.decrypt(entry["password"])
            except Exception:
                decrypted_pwd = entry["password"]

            self.table.setItem(row, 0, QTableWidgetItem(str(entry.get("service", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(entry.get("username", ""))))

            pwd_item = QTableWidgetItem("********")
            pwd_item.setData(Qt.UserRole, decrypted_pwd)
            self.table.setItem(row, 2, pwd_item)

            # --- Action Buttons ---
            btn_widget = QWidget()
            layout = QHBoxLayout(btn_widget)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.setSpacing(8)

            btn_eye = QPushButton("👁")
            btn_eye.setFixedSize(35, 35)
            btn_eye.setCursor(Qt.PointingHandCursor)
            btn_eye.setToolTip("Toggle Visibility")
            btn_eye.clicked.connect(lambda _, r=row: self.toggle_password_visibility(r))

            btn_copy = QPushButton("Copy")
            btn_copy.setCursor(Qt.PointingHandCursor)
            btn_copy.setFixedHeight(35)
            btn_copy.clicked.connect(lambda _, p=decrypted_pwd: self.copy_to_clipboard(p))

            btn_edit = QPushButton("Edit")
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setFixedHeight(35)
            btn_edit.clicked.connect(
                lambda _, s=entry.get("service"), u=entry.get("username"), p=decrypted_pwd:
                self.edit_entry(s, u, p)
            )

            # Delete Button
            btn_del = QPushButton("Delete")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setFixedHeight(35)
            btn_del.setProperty("class", "danger")
            btn_del.clicked.connect(lambda _, s=entry.get("service"): self.delete_entry(s))

            layout.addWidget(btn_eye)
            layout.addWidget(btn_copy)
            layout.addWidget(btn_edit)
            layout.addWidget(btn_del)

            self.table.setCellWidget(row, 3, btn_widget)

    def toggle_password_visibility(self, row):
        item = self.table.item(row, 2)
        if item.text() == "********":
            real_pwd = item.data(Qt.UserRole)
            item.setText(real_pwd)
        else:
            item.setText("********")

    def copy_to_clipboard(self, password):
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

    def edit_entry(self, service, username, current_password):
        dialog = AddEntryDialog(self)
        dialog.set_data(service, username, current_password)

        if dialog.exec_():
            data = dialog.get_data()
            try:
                self.storage.update_entry(data["service"], data["username"], data["password"])
                self.refresh_table()
                QMessageBox.information(self, "Success", f"Updated {data['service']}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not update entry: {e}")

    def delete_entry(self, service_name):
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{service_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                self.storage.delete_entry(service_name)
                self.refresh_table()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {e}")
