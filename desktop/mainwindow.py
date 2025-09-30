from ast import List
from re import S
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPoint, QEvent, QObject, QTimer
from PySide6.QtWidgets import QSizePolicy, QLineEdit, QTableWidgetItem
from PySide6.QtCore import QSize
from desktop.view_models import *
from desktop.ui_pm import *
from desktop.oss_vm import *
from pathlib import Path
import copy
from desktop.upload_widget import *
from desktop.image_loader import *
from desktop.login_dialog import login

import os
import sys
from importlib import resources
from io import StringIO
from dotenv import load_dotenv

def resource_path(relative_path: str):
    """Get absolute path to resource (for dev and PyInstaller)"""
    base_path = getattr(sys, "_MEIPASS", None)
    if not base_path:
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, relative_path)


def _load_env_file() -> bool:
    env_path = resource_path(".env")
    loaded = False

    if os.path.exists(env_path):
        loaded = load_dotenv(env_path)

    if not loaded:
        exe_env = None
        if getattr(sys, "frozen", False):
            exe_env = os.path.join(os.path.dirname(sys.executable), ".env")
        else:
            exe_env = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), ".env")
        if exe_env and os.path.exists(exe_env):
            loaded = load_dotenv(exe_env, override=False)

    if not loaded:
        try:
            with resources.files("desktop").joinpath(".env").open("r", encoding="utf-8") as handle:
                loaded = load_dotenv(stream=StringIO(handle.read()), override=False)
        except (FileNotFoundError, ModuleNotFoundError, AttributeError):
            loaded = False

    if not loaded:
        import pkgutil

        try:
            data = pkgutil.get_data("desktop", ".env")
        except Exception:
            data = None
        if data:
            loaded = load_dotenv(stream=StringIO(data.decode("utf-8")), override=False)

    if not loaded:
        loaded = load_dotenv()

    return loaded


_load_env_file()

class BlockVerticalWheel(QObject):
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel and event.angleDelta().y() != 0:
            return True  # Block vertical scroll
        return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._configure_window()

        self.pm = ProductManager()
        self.user = self.ask_user_name()

        self._uploader = None
        self.staged_image: list[dict[str, str]] = []
        self.original_vm = None

        self.blocker = BlockVerticalWheel()
        self._setup_scroll_containers()
        self._setup_image_loaders()
        self._configure_read_only_fields()
        self._configure_quote_table()
        self._connect_signals()

    def _configure_window(self) -> None:
        max_size = QSize(16777215, 16777215)
        min_size = QSize(0, 0)

        central = self.centralWidget()
        if central is not None:
            central.setMaximumSize(max_size)
            central.setMinimumSize(min_size)

        for widget in (self.ui.tabWidget, self.ui.edit_mode, self.ui.display_mode):
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            widget.setMinimumSize(min_size)
            widget.setMaximumSize(max_size)

        self.setWindowTitle("Product Manager")
        self.setMinimumSize(1000, 700)
        self.showMaximized()

    def _setup_scroll_containers(self) -> None:
        self.tag_layout = self._configure_flow_container(
            self.ui.tag_container,
            self.ui.scrollArea,
        )
        self.customer_layout = self._configure_flow_container(
            self.ui.customer_container,
            self.ui.scrollArea_2,
        )

    def _configure_flow_container(self, container, scroll_area):
        layout = container.layout()
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(5, 0, 5, 50)
        layout.setSpacing(8)
        container.setMinimumHeight(40)
        container.setMaximumHeight(40)
        scroll_area.setWidgetResizable(True)
        scroll_area.viewport().installEventFilter(self.blocker)
        return layout

    def _setup_image_loaders(self) -> None:
        thumb_size = QSize(220, 160)

        self.img_loader = ImageLoader(self, thumb_size=thumb_size)
        self.image_layout = self.ui.image_container.layout()
        self.image_layout.addWidget(self.img_loader)
        self.img_loader.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.img_loader.list.customContextMenuRequested.connect(self.show_image_menu)

        self.img_loader_2 = ImageLoader(self, thumb_size=thumb_size)
        self.image_layout_2 = self.ui.image_container_2.layout()
        self.image_layout_2.addWidget(self.img_loader_2)
        self.img_loader_2.list.setContextMenuPolicy(Qt.NoContextMenu)

    def _configure_read_only_fields(self) -> None:
        for widget in (
            self.ui.ref_num_LineEdit_2,
            self.ui.name_LineEdit_2,
            self.ui.price_usd_LineEdit_2,
        ):
            widget.setReadOnly(True)

    def _configure_quote_table(self) -> None:
        self.ui.quote_tableWidget.setColumnCount(4)
        self.ui.quote_tableWidget.setHorizontalHeaderLabels(
            ["Customer", "Quote", "Remark", "ID"]
        )
        self.ui.quote_tableWidget.setColumnHidden(3, True)
        self.ui.quote_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.quote_tableWidget.customContextMenuRequested.connect(self.show_quote_menu)

    def _connect_signals(self) -> None:
        self.ui.search_PushButton.clicked.connect(self.search_tab1)
        self.ui.search_PushButton_2.clicked.connect(self.search_tab2)
        self.ui.productlist_ListWidget.itemClicked.connect(self.display_selected)
        self.ui.listWidget_2.itemClicked.connect(self.display_tab2)
        self.ui.edit_pushButton.clicked.connect(self.edit_product)
        self.ui.newform_PushButton.clicked.connect(self.new_form)
        self.ui.add_PushButton.clicked.connect(self.add_product)
        self.ui.add_customer_pushButton.clicked.connect(self.add_customer)
        self.ui.add_tag_pushButton.clicked.connect(self.add_tag)
        self.ui.add_quote_pushButton.clicked.connect(self.add_quote)
        self.ui.delete_pushButton.clicked.connect(self.delete_product)
        self.ui.upload_img_pushButton.clicked.connect(self.open_uploader)

    def ask_user_name(self) -> str:
        dialog = login(self)
        if dialog.exec():
            name = dialog.user_name()
            if not name:
                name = "Anonymous"
            return name

    def open_uploader(self):
        if self._uploader is None:
            self._uploader = UploadWidget(product_id=self.original_vm.id if self.original_vm else None,
                                          on_uploaded=self.handle_uploaded_image, on_staged=self.handle_staged_image)
            self._uploader.setAttribute(Qt.WA_DeleteOnClose, True)
            self._uploader.destroyed.connect(lambda: setattr(self, "_uploader", None))

        self._uploader.show()
        self._uploader.raise_()
        self._uploader.activateWindow() 

    def search(self, text: str, selected: str):
        # text = search text entered; selected = comboBox selection
        if not text:
            return
        
        if selected == "Reference number":
            result = self.pm.search_products(ref_num=text)
        elif selected == "Name":
            result = self.pm.search_products(name=text)
        elif selected == "Tag":
            result = self.pm.search_products(tag=text)
        elif selected == "Customer":
            result = self.pm.search_products(customer=text)
        elif selected == "Barcode":
            result = self.pm.search_products(barcode=text)
        
        return result #list of VM
    
    def search_tab1(self):
        selected = self.ui.comboBox.currentText()
        text = self.ui.search_LineEdit.text()
        self.ui.search_LineEdit.clear()
        self.ui.productlist_ListWidget.clear()
        self.ui.listWidget_2.clear()

        result = self.search(text, selected)
        if not result:
            return
        for vm in result:
            self.ui.productlist_ListWidget.addItem(f"{vm.name} [{vm.ref_num}]")
            self.ui.listWidget_2.addItem(f"{vm.name} [{vm.ref_num}]")
        
        return result #list of VM
    
    def search_tab2(self):
        selected = self.ui.comboBox_2.currentText()
        text = self.ui.search_LineEdit_2.text()
        self.ui.search_LineEdit_2.clear()
        self.ui.listWidget_2.clear()

        result = self.search(text, selected)
        if not result:
            return

        for vm in result:
            self.ui.listWidget_2.addItem(f"{vm.name} [{vm.ref_num}]")
        
        return result
    
    def display_selected(self):
        """Display a content when selected"""
        item = self.ui.productlist_ListWidget.currentItem()
        if item:
            text = item.text()
            ref_num = text.split("[")[-1].rstrip("]")
            current_obj = self.pm.find_by_ref_num(ref_num)
            self.original_vm = copy.deepcopy(current_obj)

            self.ui.ref_num_LineEdit.setText(ref_num)
            self.ui.name_LineEdit.setText(current_obj.name)
            self.set_text_if_not_none(self.ui.barcode_LineEdit, current_obj.barcode)
            self.set_text_if_not_none(self.ui.pcs_innerbox_LineEdit, current_obj.pcs_innerbox)
            self.set_text_if_not_none(self.ui.pcs_ctn_LineEdit, current_obj.pcs_ctn)
            self.set_text_if_not_none(self.ui.weight_lineEdit, current_obj.weight)
            self.set_text_if_not_none(self.ui.price_usd_LineEdit, current_obj.price_usd)
            self.set_text_if_not_none(self.ui.price_rmb_LineEdit, current_obj.price_rmb)
            self.ui.remarks_TextEdit.setText(current_obj.remarks)
            self.ui.packing_LineEdit.setText(current_obj.packing)
            self.display_tags(current_obj)
            self.display_customers(current_obj)
            self.display_quotes(current_obj)
            self.ui.last_updated_Label.setText(current_obj.last_updated)
            
            oss_keys = []
            for image in current_obj.imgs:
                oss_keys.append(image['img'])
            self.img_loader.clear_list()
            self.display_product_images(oss_keys)

            self.img_loader_2.clear_list()
            self.display_tab2(ref_num, current_obj, oss_keys)
    
    def set_text_if_not_none(self, line_edit: QLineEdit, value: Any) -> None:
        if value is not None:
            line_edit.setText(str(value))
        else:
            line_edit.clear()
    
    def display_tab2(self, ref_num = None, current_obj = None, oss_keys = None):
        if current_obj is None:
            item = self.ui.listWidget_2.currentItem()
            if not item:
                return
            text = item.text()
            ref_num = text.split("[")[-1].rstrip("]")
            current_obj = self.pm.find_by_ref_num(ref_num)

        if oss_keys is None:
            oss_keys = []
            for image in current_obj.imgs:
                oss_keys.append(image['img'])

        self.ui.ref_num_LineEdit_2.setText(ref_num)
        self.ui.name_LineEdit_2.setText(current_obj.name)
        self.ui.price_usd_LineEdit_2.setText(f"{current_obj.price_usd}")
        self.display_product_images(oss_keys, tab2 = True)
    
    def display_product_images(self, oss_keys: list[str], tab2 = False):
        if not oss_keys:
            self.img_loader.clear_list()
            self.img_loader_2.clear_list()
            self.staged_image = []
            return
        if tab2:
            self.img_loader_2.load_into(oss_keys)
        else:
            self.img_loader.load_into(oss_keys)

    def clear_layout(self, layout_name):
        while layout_name.count():
            child = layout_name.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def display_tags(self, current_obj):
        # Empty container
        self.clear_layout(self.tag_layout)

        # Put tags in container
        for tag in current_obj.tags:
            tag_text = tag.get("tag_name")
            line_edit = QLineEdit()
            line_edit.setText(tag_text)
            line_edit.setFixedWidth(80)
            line_edit.setFixedHeight(28)
            line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
            line_edit.customContextMenuRequested.connect(self.show_tag_menu)
            self.tag_layout.addWidget(line_edit, alignment=Qt.AlignVCenter)
        
    def display_customers(self, current_obj):
        # Empty container
        self.clear_layout(self.customer_layout)

        # Put customers in container
        for customer in current_obj.customers:
            customer_text = customer.get("customer_name")
            line_edit = QLineEdit()
            line_edit.setText(customer_text)
            line_edit.setFixedWidth(80)
            line_edit.setFixedHeight(28)
            line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
            line_edit.customContextMenuRequested.connect(self.show_customer_menu)
            self.customer_layout.addWidget(line_edit, alignment=Qt.AlignVCenter)
    
    def display_quotes(self, current_obj):
        self.ui.quote_tableWidget.setRowCount(0)

        for quote in current_obj.quotes:
            customer_text = quote.get("customer_name")
            quote_text = str(quote.get("quote"))
            remark_text = quote.get("quote_remark")

            row_position = self.ui.quote_tableWidget.rowCount()
            self.ui.quote_tableWidget.insertRow(row_position)
            self.ui.quote_tableWidget.setItem(row_position, 0, QTableWidgetItem(customer_text))
            self.ui.quote_tableWidget.setItem(row_position, 1, QTableWidgetItem(quote_text))
            self.ui.quote_tableWidget.setItem(row_position, 2, QTableWidgetItem(remark_text))
    
            # Store quote id, retrieve in column 3
            quote_id_item = QTableWidgetItem(str(quote.get("quote_id")))
            self.ui.quote_tableWidget.setItem(row_position, 3, quote_id_item)
            
            

    def edit_product(self):
        # For editing existing product
        ref_num = self.ui.ref_num_LineEdit.text()
        current_obj = self.pm.find_by_ref_num(ref_num)
        current_obj.name = self.ui.name_LineEdit.text()
        current_obj.barcode = self.safe_int(self.ui.barcode_LineEdit.text())
        current_obj.pcs_innerbox = self.safe_int(self.ui.pcs_innerbox_LineEdit.text())
        current_obj.pcs_ctn = self.safe_int(self.ui.pcs_ctn_LineEdit.text())
        current_obj.weight = self.safe_float(self.ui.weight_lineEdit.text())
        current_obj.price_usd = self.safe_float(self.ui.price_usd_LineEdit.text())
        current_obj.price_rmb = self.safe_float(self.ui.price_rmb_LineEdit.text())
        current_obj.remarks = self.ui.remarks_TextEdit.toPlainText()
        current_obj.packing = self.ui.packing_LineEdit.text()

        flatfield_vm = self.pm.update_product(current_obj)
        old_tags = [t["tag_name"] for t in self.original_vm.tags]
        new_tags = [self.tag_layout.itemAt(i).widget().text() for i in range(self.tag_layout.count())]
        tag_vm = self.pm.bulk_update_tag(flatfield_vm, old_tags, new_tags)

        old_customers = [c["customer_name"] for c in self.original_vm.customers]
        new_customers = [self.customer_layout.itemAt(i).widget().text() for i in range(self.customer_layout.count())]
        customer_vm = self.pm.bulk_update_customer(tag_vm, old_customers, new_customers)

        old_quotes = self.original_vm.quotes
        new_quotes = self.get_all_quotes()
        quote_vm = self.pm.bulk_update_quote(customer_vm, old_quotes, new_quotes)
        self.original_vm = copy.deepcopy(quote_vm)
        return self.original_vm
    
    @staticmethod
    def safe_int(text: str) -> int | None:
        if text:
            return int(text) if text.strip() else None

    @staticmethod
    def safe_float(text: str) -> float | None:
        if text:
            return float(text) if text.strip() else None

    def add_product(self):
        data = {
            "ref_num": self.ui.ref_num_LineEdit.text(),
            "name": self.ui.name_LineEdit.text(),
            "barcode": self.safe_int(self.ui.barcode_LineEdit.text()),
            "pcs_innerbox": self.safe_int(self.ui.pcs_innerbox_LineEdit.text()),
            "pcs_ctn": self.safe_int(self.ui.pcs_ctn_LineEdit.text()),
            "weight": self.safe_float(self.ui.weight_lineEdit.text()),
            "price_usd": self.safe_float(self.ui.price_usd_LineEdit.text()),
            "price_rmb": self.safe_float(self.ui.price_rmb_LineEdit.text()),
            "remarks": self.ui.remarks_TextEdit.toPlainText(),
            "packing": self.ui.packing_LineEdit.text(),
            "customers": self.get_all_customers(),
            "quote": self.get_all_quotes(),
            "tags": self.get_all_tags(),
            "locked_by": None,
            "locked_timestamp": None,
            "last_updated": None,
        }

        new_vm = self.pm.create_product(data)

        for img in self.staged_image:
            select_and_upload_image(img["temp"], new_vm.id, img["key_name"])
            os.remove(img["temp"])
        return new_vm
    
    def remove_widget_from_layout(self, layout, widget):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item.widget() == widget:
                widget.deleteLater()
                layout.takeAt(i)
                return
            
    def add_customer(self):
        line_edit = QLineEdit()
        line_edit.setFixedWidth(80)
        line_edit.setFixedHeight(28)
        line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        line_edit.customContextMenuRequested.connect(self.show_customer_menu)
        self.customer_layout.addWidget(line_edit, alignment=Qt.AlignVCenter)

    def get_all_customers(self):
        customer_names = []
        for i in range(self.customer_layout.count()):
            item = self.customer_layout.itemAt(i)
            widget = item.widget()
            if isinstance (widget, QLineEdit):
                customer_names.append(widget.text())
        return customer_names

    def show_customer_menu(self, position):
        if not self.original_vm:
            return

        sender = self.sender()
        if not isinstance(sender, QLineEdit):
            return

        menu = QMenu()
        delete_action = menu.addAction("Delete Customer")
        action = menu.exec(sender.mapToGlobal(position))
        if action != delete_action:
            return

        name = sender.text().strip()
        if not name:
            self.display_customers(self.original_vm)
            return

        current_names = {c["customer_name"] for c in (self.original_vm.customers or [])}
        if name not in current_names:
            self.remove_widget_from_layout(self.customer_layout, sender)
            return

        self.original_vm = self.pm.delete_customer(self.original_vm, name)
        self.display_customers(self.original_vm)


    def add_tag(self):
        line_edit = QLineEdit()
        line_edit.setFixedWidth(80)
        line_edit.setFixedHeight(28)
        line_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        line_edit.customContextMenuRequested.connect(self.show_tag_menu)
        self.tag_layout.addWidget(line_edit, alignment=Qt.AlignVCenter)

    def get_all_tags(self):
        tag_names = []
        for i in range(self.tag_layout.count()):
            item = self.tag_layout.itemAt(i)
            widget = item.widget()
            if isinstance (widget, QLineEdit):
                tag_names.append(widget.text())
        return tag_names

    def show_tag_menu(self, position):
        if not self.original_vm:
            return

        sender = self.sender()
        if not isinstance(sender, QLineEdit):
            return

        menu = QMenu()
        delete_action = menu.addAction("Delete Tag")
        action = menu.exec(sender.mapToGlobal(position))
        if action != delete_action:
            return

        tag = sender.text().strip()
        if not tag:
            self.display_tags(self.original_vm)
            return

        current_tags = {t["tag_name"] for t in (self.original_vm.tags or [])}
        if tag not in current_tags:
            self.remove_widget_from_layout(self.tag_layout, sender)
            return

        self.original_vm = self.pm.delete_tag(self.original_vm, tag)
        self.display_tags(self.original_vm)

    def add_quote(self):
        row_position = self.ui.quote_tableWidget.rowCount()
        self.ui.quote_tableWidget.insertRow(row_position)

    def get_all_quotes(self):
        quote_list = []
        row_count = self.ui.quote_tableWidget.rowCount()

        for i in range(row_count):
            customer_item = self.ui.quote_tableWidget.item(i, 0)
            quote_item = self.ui.quote_tableWidget.item(i, 1)
            remark_item = self.ui.quote_tableWidget.item(i, 2)
            quote_id_item = self.ui.quote_tableWidget.item(i, 3)

            customer_name = customer_item.text() if customer_item else ""
            quote_str = quote_item.text() if quote_item else ""
            try:
                quote = float(quote_str)
            except ValueError:
                quote = None

            remark = remark_item.text() if remark_item else ""

            quote_dict = {"customer_name": customer_name,
                          "quote": quote,
                          "remark": remark}
            
            if quote_id_item:
                quote_id_str = quote_id_item.text()
                try:
                    quote_id = int(quote_id_str)
                    quote_dict["quote_id"] = quote_id
                except (ValueError, TypeError):
                    pass
            
            quote_list.append(quote_dict)

        return quote_list

    def new_form(self):
        self.clear_fields()
        self.staged_image = []
        self.original_vm = None
    
    def handle_uploaded_image(self, oss_key: str) -> None:
        """Existing product: upload already succeeded, so pull fresh data."""
        if not oss_key or not self.original_vm:
            return

        # Re-fetch the product so caches and galleries stay in sync.
        self.original_vm = self.pm.fetch_product(self.original_vm)
        self.display_selected()

    def handle_staged_image(self, temp_path: str, key_name: str) -> None:
        """New product: keep the resized file + future OSS key until we have an ID."""
        if not temp_path or not key_name:
            return

        if self.staged_image is None:
            self.staged_image = []

        self.staged_image.append({"temp": temp_path, "key_name": key_name})

        local_paths = [img["temp"] for img in self.staged_image if img.get("temp")]
        self.img_loader.load_local_paths(local_paths)


    def clear_fields(self):
        self.ui.ref_num_LineEdit.clear()
        self.ui.name_LineEdit.clear()
        self.ui.barcode_LineEdit.clear()
        self.ui.pcs_innerbox_LineEdit.clear()
        self.ui.pcs_ctn_LineEdit.clear()
        self.ui.weight_lineEdit.clear()
        self.ui.price_usd_LineEdit.clear()
        self.ui.price_rmb_LineEdit.clear()
        self.ui.remarks_TextEdit.clear()
        self.ui.packing_LineEdit.clear()
        self.ui.last_updated_Label.clear()

        self.clear_layout(self.tag_layout)
        self.clear_layout(self.customer_layout)
        self.ui.quote_tableWidget.setRowCount(0)

    def delete_product(self):
        item = self.ui.productlist_ListWidget.currentItem()
        if item:
            text = item.text()
            ref_num = text.split("[")[-1].rstrip("]")
            current_obj = self.pm.find_by_ref_num(ref_num)
            self.pm.delete_product(current_obj)
        self.clear_fields()
        self.delete_selected_list_item()
    
    def delete_selected_list_item(self):
        row = self.ui.productlist_ListWidget.currentRow()
        if row >= 0:
            self.ui.productlist_ListWidget.takeItem(row)
    
    def show_quote_menu(self, position: QPoint):
        menu = QMenu()
        delete_action = menu.addAction("Delete Quote")
        action = menu.exec(self.ui.quote_tableWidget.viewport().mapToGlobal(position))
        if not self.original_vm:
            return
        if action == delete_action:
            index = self.ui.quote_tableWidget.indexAt(position)
            selected_row = index.row()
            if selected_row >= 0:
                quote_id_item = self.ui.quote_tableWidget.item(selected_row, 3)
                if not quote_id_item or not quote_id_item.text():
                    self.display_quotes(self.original_vm)
                    return
                quote_id = int(quote_id_item.text())
                self.original_vm = self.pm.delete_quote(self.original_vm, quote_id)
                self.display_quotes(self.original_vm)
    
    def show_image_menu(self, position):
        sender = self.sender()
        if not isinstance(sender, QListWidget):
            return

        item = sender.itemAt(position)
        if not item:
            return

        menu = QMenu(sender)
        delete_action = menu.addAction("Delete Image")
        action = menu.exec(sender.viewport().mapToGlobal(position))
        if action != delete_action:
            return

        path = item.data(Qt.UserRole)
        if not path:
            sender.takeItem(sender.row(item))
            return

        if self.original_vm:
            self.original_vm = self.pm.delete_img(self.original_vm, path)
            oss_keys = [img["img"] for img in (self.original_vm.imgs or [])]
            self.display_product_images(oss_keys)
        else:
            self._drop_staged_image(path)
            staged = [img["temp"] for img in self.staged_image if img.get("temp")]
            self.img_loader.load_local_paths(staged)

    def _drop_staged_image(self, path: str) -> None:
        if not self.staged_image or not path:
            return

        remaining = []
        for entry in self.staged_image:
            if entry.get("temp") == path:
                try:
                    os.remove(path)
                except OSError:
                    pass
            else:
                remaining.append(entry)
        self.staged_image = remaining

app = QApplication([])
window = MainWindow()

window.show()

app.exec()
