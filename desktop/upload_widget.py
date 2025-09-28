from re import S
from PySide6.QtWidgets import QFileDialog, QVBoxLayout, QLabel
from PySide6.QtCore import QObject, QThread, Signal, Slot
from desktop.view_models import *
from desktop.ui_pm import *
from desktop.oss_vm import *
from pathlib import Path
from PIL import Image, ImageOps
from uuid import uuid4
from typing import Callable, Optional
import tempfile


class UploadWorker(QObject):
    finished = Signal(str) # emits oss_key
    failed = Signal(str)
    progress = Signal(int) # 0-100

    def __init__(self, file_path: str, product_id: int, key_name: str):
        super().__init__()
        self.file_path = file_path
        self.product_id = product_id
        self.key_name = key_name

    @Slot()
    def run(self):
        try:
            oss_key = select_and_upload_image(self.file_path, self.product_id,
                                              self.key_name)
            self.finished.emit(oss_key)
        except Exception as e:
            self.failed.emit(str(e))
        finally:
            try:
                os.remove(self.file_path)
            except OSError:
                pass


class UploadWidget(QWidget):
    def __init__(self, product_id: int | None = None, on_uploaded:  Optional[Callable[[str], None]] = None, on_staged:  Optional[Callable[[str, str], None]] = None,):
        super().__init__()
        self.pm = ProductManager()
        self.product_id = product_id
        self.init_ui()
        self._on_uploaded = on_uploaded
        self._on_staged = on_staged

    def init_ui(self):
        self.setWindowTitle("Upload Image")
        self.resize(300, 150)

        self.label = QLabel("Select an image to upload", self)
        self.button = QPushButton("Upload Image")
        self.button.clicked.connect(self.open_file_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self._thread = None
        self._worker = None

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            shrinked_path, key_name = self.shrink_if_needed(file_path)
            if self.product_id:
                self.start_upload(shrinked_path, key_name)
            else:
                self._on_staged(shrinked_path, key_name)
                

    def shrink_if_needed(self, path, max_side=1600, quality=85):
        if not isinstance(path, (str, os.PathLike, Path)):
            raise TypeError(f"Expected a file path, got {type(path).__name__}: {path!r}")

        # open + auto-rotate from EXIF
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            img.thumbnail((max_side, max_side))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            fd, out = tempfile.mkstemp(suffix=".jpg"); os.close(fd)
            img.save(out, format="JPEG", quality=quality, optimize=True, progressive=True)

            original = Path(path)
            key_name = f"{Path(original).stem}-{uuid4().hex[:6]}.jpg"
        
        return out, key_name
    
    def start_upload(self, file_path:str, key_name:str):
        self.button.setEnabled(False)
        self.label.setText("Uploading...")

        self._thread = QThread(self)
        self._worker = UploadWorker(file_path, self.product_id, key_name)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self.on_success)
        self._worker.failed.connect(self.on_failed)

        self._worker.finished.connect(self._thread.quit)
        self._worker.failed.connect(self._thread.quit)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()
    
    @Slot(str)
    def on_success(self, oss_key: str):
        self.button.setEnabled(True)
        self.label.setText(f"✅ Uploaded: {Path(oss_key).name}")
        if self._on_uploaded:
            self._on_uploaded(oss_key)
    
    @Slot(str)
    def on_failed(self, msg:str):
        self.button.setEnabled(True)
        self.label.setText(f"❌ Upload failed: {str(msg)}")

