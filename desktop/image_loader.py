from PySide6.QtCore import Qt, QSize, QUrl, QStandardPaths, Slot
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkDiskCache
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QLabel, QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QDialog, QScrollArea
from desktop.oss_vm import *

from PySide6.QtCore import Qt, QSize, QUrl, QStandardPaths, Slot
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtNetwork import (
    QNetworkAccessManager, QNetworkRequest, QNetworkDiskCache, QNetworkReply
)
from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QEvent
from pathlib import Path

class ImageLoader(QWidget):
    def __init__(self, parent=None, thumb_size: QSize = QSize(200,150)):
        super().__init__(parent)
        self.thumb_size = thumb_size

        self.list = QListWidget(self)
        self.list.setViewMode(QListWidget.IconMode)
        self.list.setResizeMode(QListWidget.Adjust)
        self.list.setMovement(QListWidget.Static)
        self.list.setSpacing(8)
        self.list.setIconSize(self.thumb_size)
        self.list.setUniformItemSizes(True)
        self.list.setSelectionMode(QListWidget.NoSelection)
        
        self.list.itemClicked.connect(self._on_item_clicked)

        self.nam = QNetworkAccessManager(self)

        cache = QNetworkDiskCache(self)
        cache_dir = QStandardPaths.writableLocation(QStandardPaths.CacheLocation) or "."
        cache.setCacheDirectory(cache_dir)
        self.nam.setCache(cache)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list)
    
    def clear_list(self):
        self.list.clear()

    def load_into(self, oss_keys):
        self.clear_list()
        for key in oss_keys:
            url = get_signed_url_for_key(key)
            qurl = QUrl.fromEncoded(url.encode("utf-8"))
            req = QNetworkRequest(qurl)
            try:
                req.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
            except Exception:
                pass

            reply = self.nam.get(req)
            item = QListWidgetItem("Loading...")
            item.setSizeHint(QSize(self.thumb_size.width() + 16, self.thumb_size.height() + 28))
            item.setData(Qt.UserRole, key)
            self.list.addItem(item)

            reply.finished.connect(lambda r=reply, i=item: self._on_finished(r, i))

            reply.downloadProgress.connect(lambda rec, tot, i=item:
                                           i.setText(f"Loading… {int(rec*100/tot) if tot else 0}%"))
            reply.errorOccurred.connect(
                    lambda err, r=reply, it=item: self._on_error(err, r, it)
                )
    

    def load_local_paths(self, file_paths: list[str]) -> None:
        """Show thumbnails for locally staged files (no network)."""
        self.clear_list()
        for path in file_paths:
            pix = QPixmap(path)
            if pix.isNull():
                continue
            thumb = pix.scaled(self.thumb_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            item = QListWidgetItem(Path(path).name)
            item.setSizeHint(QSize(self.thumb_size.width() + 16,
                                   self.thumb_size.height() + 28))
            item.setData(Qt.UserRole, path)
            item.setIcon(QIcon(thumb))
            item.setData(Qt.UserRole + 1, pix)  # keep full-res for the viewer
            self.list.addItem(item)


    @Slot()
    def _on_error(self, err, reply, item):
        status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)

        # Enum-friendly introspection
        err_code = getattr(err, "value", err)   # number if enum, else the raw int
        err_name = getattr(err, "name", str(err))

        body_preview = bytes(reply.peek(256)).decode("utf-8", "ignore")

        item.setText(f"⚠️ {status or ''} {err_name} | {reply.errorString()}")
        print("[NET] error:",
            "status=", status,
            "qt_err_code=", err_code,
            "qt_err_name=", err_name,
            "errStr=", reply.errorString(),
            "url=", reply.url().toString(),
            "body=", body_preview)

    @Slot()
    def _on_finished(self, reply: QNetworkReply, item: QListWidgetItem, redirected: bool=False):
        status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        reason = reply.attribute(QNetworkRequest.HttpReasonPhraseAttribute)

        # 1) Follow redirects (some OSS/CDN URLs 302/307)
        if status in (301, 302, 303, 307, 308) and not redirected:
            target = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            new_url = reply.url().resolved(target) if target else None
            if new_url:
                reply.deleteLater()
                req = QNetworkRequest(new_url)
                # best-effort follow for all Qt builds
                try: req.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
                except Exception: pass
                r2 = self.nam.get(req)
                r2.errorOccurred.connect(lambda e, r=r2, it=item: self._on_error(e, r, it))
                r2.finished.connect(lambda r=r2, it=item: self._on_finished(r, it, redirected=True))
                return

        # 2) HTTP error handling
        if status is not None and int(status) >= 400:
            body = bytes(reply.readAll())
            err_code = ""
            if b"<Error>" in body:
                import re
                m = re.search(rb"<Code>([^<]+)</Code>", body)
                if m: err_code = m.group(1).decode("utf-8", "ignore")
            preview = body[:200].decode("utf-8", "ignore")
            item.setText(f"⚠️ HTTP {status} {reason or ''} {err_code}")
            print("[HTTP] status=", status, reason or "",
                "| oss_code=", err_code,
                "| url=", reply.url().toString(),
                "| body_preview=", preview)
            reply.deleteLater()
            return

        # 3) Network-level error (DNS/SSL/etc.)
        if reply.error() != QNetworkReply.NetworkError.NoError:
            self._on_error(reply.error(), reply, item)
            reply.deleteLater()
            return

        data = reply.readAll()
        pix = QPixmap()
        if not pix.loadFromData(data):
            item.setText("Invalid image")
        else:
            thumb = pix.scaled(self.thumb_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            item.setIcon(QIcon(thumb))
            item.setData(Qt.UserRole + 1, pix)
        reply.deleteLater()
    
    def _on_item_clicked(self, item: QListWidgetItem):
        pix = item.data(Qt.UserRole + 1)
        if isinstance(pix, QPixmap) and not pix.isNull():
            viewer = ImageViewer(pix, parent=self.window())
            viewer.exec()
        else:
            return


class ImageViewer(QDialog):
    def __init__(self, pix: QPixmap, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Image Viewer")
        self.resize(800,500)
        self._orig = pix
        
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setScaledContents(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self.label)

        self._apply_fit()
        
    def _apply_fit(self):
        if self._orig.isNull():
            self.label.clear()
            return
        target = self.label.size()
        if target.width() <= 0 or target.height() <= 0:
            return
        scaled = self._orig.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(scaled)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._apply_fit()