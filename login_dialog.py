from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class login(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.name_edit = QLineEdit(self)
        ok = QPushButton("Confirm", self)
        ok.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Enter your display name:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(ok)
    
    def user_name(self) -> str:
        return self.name_edit.text().strip()