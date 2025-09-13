from re import S
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow, QMessageBox, QMenu
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QPoint, QEvent, QObject, QTimer
from desktop.view_models import *
from desktop.ui_pm import *
from desktop.oss_vm import *
from pathlib import Path
import copy
from desktop.upload_widget import *
from desktop.image_loader import *
from desktop.login_dialog import login

import os, sys
from dotenv import load_dotenv

def resource_path(relative_path: str):
    """Get absolute path to resource (for dev and PyInstaller)"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Load .env once at startup
env_path = resource_path(".env")
load_dotenv(env_path)


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
        # Make sure centralwidget has no limits
        self.centralWidget().setMaximumSize(QSize(16777215, 16777215))
        self.centralWidget().setMinimumSize(QSize(0, 0))

        # Force tabWidget to expand
        self.ui.tabWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.tabWidget.setMinimumSize(QSize(0, 0))
        self.ui.tabWidget.setMaximumSize(QSize(16777215, 16777215))

        # Same for edit_mode tab
        self.ui.edit_mode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.edit_mode.setMinimumSize(QSize(0, 0))
        self.ui.edit_mode.setMaximumSize(QSize(16777215, 16777215))

        # And display_mode tab for consistency
        self.ui.display_mode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.display_mode.setMinimumSize(QSize(0, 0))
        self.ui.display_mode.setMaximumSize(QSize(16777215, 16777215))

        print("Central:", self.centralWidget().sizeHint())
        print("TabWidget:", self.ui.tabWidget.sizeHint())
        print("Edit mode:", self.ui.edit_mode.sizeHint())

        # Finally, launch maximized
        self.showMaximized()
        self.setMinimumSize(1000, 700)

        self.setWindowTitle("Product Manager")
        self.pm = ProductManager()

        self.user = self.ask_user_name()

        self._uploader = None
    
        self.ui.search_PushButton.clicked.connect(self.search_tab1)
        self.ui.search_PushButton_2.clicked.connect(self.search_tab2)
        self.ui.productlist_ListWidget.itemClicked.connect(self.display_selected)
        self.ui.listWidget_2.itemClicked.connect(self.display_tab2)

        self.blocker = BlockVerticalWheel()

        self.tag_layout = self.ui.tag_container.layout()

        #tag_layout settings
        self.tag_layout.setAlignment(Qt.AlignLeft)
        self.tag_layout.setContentsMargins(5, 0, 5, 50)
        self.tag_layout.setSpacing(8)
        self.ui.tag_container.setMinimumHeight(40)
        self.ui.tag_container.setMaximumHeight(40)
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.scrollArea.viewport().installEventFilter(self.blocker)

        self.customer_layout = self.ui.customer_container.layout()

        #customer_layout settings
        self.customer_layout.setAlignment(Qt.AlignLeft)
        self.customer_layout.setContentsMargins(5, 0, 5, 50)
        self.customer_layout.setSpacing(8)
        self.ui.customer_container.setMinimumHeight(40)
        self.ui.customer_container.setMaximumHeight(40)
        self.ui.scrollArea_2.setWidgetResizable(True)
        self.ui.scrollArea_2.viewport().installEventFilter(self.blocker)

        self.ui.edit_pushButton.clicked.connect(self.edit_product)
        self.ui.newform_PushButton.clicked.connect(self.clear_fields)
        self.ui.add_PushButton.clicked.connect(self.add_product)
        self.ui.add_customer_pushButton.clicked.connect(self.add_customer)
        self.ui.add_tag_pushButton.clicked.connect(self.add_tag)
        self.ui.add_quote_pushButton.clicked.connect(self.add_quote)
        self.ui.delete_pushButton.clicked.connect(self.delete_product)
        self.ui.upload_img_pushButton.clicked.connect(self.open_uploader)

        self.ui.quote_tableWidget.setColumnCount(4)
        self.ui.quote_tableWidget.setHorizontalHeaderLabels(["Customer", "Quote", "Remark", "ID"])
        self.ui.quote_tableWidget.setColumnHidden(3, True)
        self.ui.quote_tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.quote_tableWidget.customContextMenuRequested.connect(self.show_quote_menu)
        
        self.img_loader = ImageLoader(self, thumb_size=QSize(220, 160))
        self.image_layout = self.ui.image_container.layout()
        self.image_layout.addWidget(self.img_loader)
        self.img_loader.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.img_loader.list.customContextMenuRequested.connect(self.show_image_menu)

        self.img_loader_2 = ImageLoader(self, thumb_size=QSize(220, 160))
        self.image_layout_2 = self.ui.image_container_2.layout()
        self.image_layout_2.addWidget(self.img_loader_2)
        self.img_loader_2.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.img_loader_2.list.customContextMenuRequested.connect(self.show_image_menu)

        self.ui.ref_num_LineEdit_2.setReadOnly(True)
        self.ui.name_LineEdit_2.setReadOnly(True)
        self.ui.price_usd_LineEdit_2.setReadOnly(True)
        
        self.original_vm = None

    def ask_user_name(self) -> str:
        dialog = login(self)
        if dialog.exec():
            name = dialog.user_name()
            if not name:
                name = "Anonymous"
            return name

    def open_uploader(self):
        if self._uploader is None:
            self._uploader = UploadWidget(self.original_vm.id)
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
            self.ui.barcode_LineEdit.setText(f"{current_obj.barcode}")
            self.ui.pcs_innerbox_LineEdit.setText(f"{current_obj.pcs_innerbox}")
            self.ui.pcs_ctn_LineEdit.setText(f"{current_obj.pcs_ctn}")
            self.ui.weight_lineEdit.setText(f"{current_obj.weight}")
            self.ui.price_usd_LineEdit.setText(f"{current_obj.price_usd}")
            self.ui.price_rmb_LineEdit.setText(f"{current_obj.price_rmb}")
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
        current_obj.barcode = self.ui.barcode_LineEdit.text()
        current_obj.pcs_innerbox = self.ui.pcs_innerbox_LineEdit.text()
        current_obj.pcs_ctn = self.ui.pcs_ctn_LineEdit.text()
        current_obj.weight = self.ui.weight_lineEdit.text()
        current_obj.price_usd = self.ui.price_usd_LineEdit.text()
        current_obj.price_rmb = self.ui.price_rmb_LineEdit.text()
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
        return quote_vm
    
    @staticmethod
    def safe_int(text: str) -> int | None:
        return int(text) if text.strip() else None

    @staticmethod
    def safe_float(text: str) -> float | None:
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
            "imgs": [],  # populate from image selector or OSS hook
            "tags": self.get_all_tags(),
            "locked_by": None,
            "locked_timestamp": None,
            "last_updated": None,
        }

        new_vm = self.pm.create_product(data)
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
        sender_widget = self.sender()
        menu = QMenu()
        delete_action = menu.addAction("Delete Customer")
        action = menu.exec(sender_widget.mapToGlobal(position))
        if action == delete_action:
            customer = sender_widget.text()
            self.pm.delete_customer(self.original_vm, customer)
            self.remove_widget_from_layout(self.customer_layout, sender_widget)

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
        sender_widget = self.sender()
        menu = QMenu()
        delete_action = menu.addAction("Delete Tag")
        action = menu.exec(sender_widget.mapToGlobal(position))
        if action == delete_action:
            tag = sender_widget.text()
            self.pm.delete_tag(self.original_vm, tag)
            self.remove_widget_from_layout(self.tag_layout, sender_widget)


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
        if action == delete_action:
            index = self.ui.quote_tableWidget.indexAt(position)
            selected_row = index.row()
            if selected_row >= 0:
                quote_id_item = self.ui.quote_tableWidget.item(selected_row, 3)
                quote_id = int(quote_id_item.text())
                self.pm.delete_quote(self.original_vm, quote_id)
                self.ui.quote_tableWidget.removeRow(selected_row)
    
    def show_image_menu(self, position):
        item = self.img_loader.list.itemAt(position)
        if not item:
            return
        menu = QMenu(self.img_loader.list)
        delete_action = menu.addAction("Delete Image")
        action = menu.exec(self.img_loader.list.viewport().mapToGlobal(position))
        if action == delete_action:
            image_path = item.data(Qt.UserRole)
            if image_path:
                self.pm.delete_img(self.original_vm, image_path)
            row = self.img_loader.list.row(item)
            self.img_loader.list.takeItem(row)

app = QApplication([])
window = MainWindow()

window.show()

app.exec()
