# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'product_manager.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QTabWidget, QTableWidget, QTableWidgetItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1808, 1275)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout_10 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.edit_mode = QWidget()
        self.edit_mode.setObjectName(u"edit_mode")
        self.edit_mode.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.edit_mode.sizePolicy().hasHeightForWidth())
        self.edit_mode.setSizePolicy(sizePolicy1)
        self.edit_mode.setMaximumSize(QSize(1697, 1041))
        self.verticalLayout_7 = QVBoxLayout(self.edit_mode)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.edit_mode)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout_11 = QFormLayout(self.groupBox)
        self.formLayout_11.setObjectName(u"formLayout_11")
        self.ref_num_label = QLabel(self.groupBox)
        self.ref_num_label.setObjectName(u"ref_num_label")

        self.formLayout_11.setWidget(2, QFormLayout.ItemRole.LabelRole, self.ref_num_label)

        self.ref_num_LineEdit = QLineEdit(self.groupBox)
        self.ref_num_LineEdit.setObjectName(u"ref_num_LineEdit")

        self.formLayout_11.setWidget(2, QFormLayout.ItemRole.FieldRole, self.ref_num_LineEdit)

        self.name_label = QLabel(self.groupBox)
        self.name_label.setObjectName(u"name_label")

        self.formLayout_11.setWidget(6, QFormLayout.ItemRole.LabelRole, self.name_label)

        self.name_LineEdit = QLineEdit(self.groupBox)
        self.name_LineEdit.setObjectName(u"name_LineEdit")

        self.formLayout_11.setWidget(6, QFormLayout.ItemRole.FieldRole, self.name_LineEdit)

        self.barcode_label = QLabel(self.groupBox)
        self.barcode_label.setObjectName(u"barcode_label")

        self.formLayout_11.setWidget(8, QFormLayout.ItemRole.LabelRole, self.barcode_label)

        self.barcode_LineEdit = QLineEdit(self.groupBox)
        self.barcode_LineEdit.setObjectName(u"barcode_LineEdit")

        self.formLayout_11.setWidget(8, QFormLayout.ItemRole.FieldRole, self.barcode_LineEdit)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.edit_mode)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout_12 = QFormLayout(self.groupBox_2)
        self.formLayout_12.setObjectName(u"formLayout_12")
        self.pcs_innerbox_label = QLabel(self.groupBox_2)
        self.pcs_innerbox_label.setObjectName(u"pcs_innerbox_label")

        self.formLayout_12.setWidget(1, QFormLayout.ItemRole.LabelRole, self.pcs_innerbox_label)

        self.pcs_innerbox_LineEdit = QLineEdit(self.groupBox_2)
        self.pcs_innerbox_LineEdit.setObjectName(u"pcs_innerbox_LineEdit")

        self.formLayout_12.setWidget(1, QFormLayout.ItemRole.FieldRole, self.pcs_innerbox_LineEdit)

        self.pcs_ctn_label = QLabel(self.groupBox_2)
        self.pcs_ctn_label.setObjectName(u"pcs_ctn_label")

        self.formLayout_12.setWidget(3, QFormLayout.ItemRole.LabelRole, self.pcs_ctn_label)

        self.pcs_ctn_LineEdit = QLineEdit(self.groupBox_2)
        self.pcs_ctn_LineEdit.setObjectName(u"pcs_ctn_LineEdit")

        self.formLayout_12.setWidget(3, QFormLayout.ItemRole.FieldRole, self.pcs_ctn_LineEdit)

        self.weight_label = QLabel(self.groupBox_2)
        self.weight_label.setObjectName(u"weight_label")

        self.formLayout_12.setWidget(5, QFormLayout.ItemRole.LabelRole, self.weight_label)

        self.weight_lineEdit = QLineEdit(self.groupBox_2)
        self.weight_lineEdit.setObjectName(u"weight_lineEdit")

        self.formLayout_12.setWidget(5, QFormLayout.ItemRole.FieldRole, self.weight_lineEdit)

        self.packing_label = QLabel(self.groupBox_2)
        self.packing_label.setObjectName(u"packing_label")

        self.formLayout_12.setWidget(7, QFormLayout.ItemRole.LabelRole, self.packing_label)

        self.packing_LineEdit = QLineEdit(self.groupBox_2)
        self.packing_LineEdit.setObjectName(u"packing_LineEdit")

        self.formLayout_12.setWidget(7, QFormLayout.ItemRole.FieldRole, self.packing_LineEdit)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.edit_mode)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.formLayout_13 = QFormLayout(self.groupBox_3)
        self.formLayout_13.setObjectName(u"formLayout_13")
        self.price_usd_label = QLabel(self.groupBox_3)
        self.price_usd_label.setObjectName(u"price_usd_label")

        self.formLayout_13.setWidget(0, QFormLayout.ItemRole.LabelRole, self.price_usd_label)

        self.price_usd_LineEdit = QLineEdit(self.groupBox_3)
        self.price_usd_LineEdit.setObjectName(u"price_usd_LineEdit")

        self.formLayout_13.setWidget(0, QFormLayout.ItemRole.FieldRole, self.price_usd_LineEdit)

        self.price_rmb_label = QLabel(self.groupBox_3)
        self.price_rmb_label.setObjectName(u"price_rmb_label")

        self.formLayout_13.setWidget(1, QFormLayout.ItemRole.LabelRole, self.price_rmb_label)

        self.price_rmb_LineEdit = QLineEdit(self.groupBox_3)
        self.price_rmb_LineEdit.setObjectName(u"price_rmb_LineEdit")

        self.formLayout_13.setWidget(1, QFormLayout.ItemRole.FieldRole, self.price_rmb_LineEdit)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.edit_mode)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.formLayout = QFormLayout(self.groupBox_4)
        self.formLayout.setObjectName(u"formLayout")
        self.remarks_TextEdit = QTextEdit(self.groupBox_4)
        self.remarks_TextEdit.setObjectName(u"remarks_TextEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.remarks_TextEdit)


        self.verticalLayout.addWidget(self.groupBox_4)


        self.gridLayout_4.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.groupBox_8 = QGroupBox(self.edit_mode)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.image_container = QWidget(self.groupBox_8)
        self.image_container.setObjectName(u"image_container")
        sizePolicy.setHeightForWidth(self.image_container.sizePolicy().hasHeightForWidth())
        self.image_container.setSizePolicy(sizePolicy)
        self.gridLayout = QGridLayout(self.image_container)
        self.gridLayout.setObjectName(u"gridLayout")

        self.horizontalLayout_8.addWidget(self.image_container)

        self.upload_img_pushButton = QPushButton(self.groupBox_8)
        self.upload_img_pushButton.setObjectName(u"upload_img_pushButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.upload_img_pushButton.sizePolicy().hasHeightForWidth())
        self.upload_img_pushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_8.addWidget(self.upload_img_pushButton)


        self.gridLayout_4.addWidget(self.groupBox_8, 0, 2, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_7 = QGroupBox(self.edit_mode)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.add_tag_pushButton = QPushButton(self.groupBox_7)
        self.add_tag_pushButton.setObjectName(u"add_tag_pushButton")
        icon = QIcon()
        iconThemeName = u"plus"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Mode.Normal, QIcon.State.Off)

        self.add_tag_pushButton.setIcon(icon)

        self.horizontalLayout_7.addWidget(self.add_tag_pushButton)

        self.scrollArea = QScrollArea(self.groupBox_7)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(120, 0))
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 450, 69))
        self.horizontalLayout_3 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tag_container = QWidget(self.scrollAreaWidgetContents)
        self.tag_container.setObjectName(u"tag_container")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tag_container.sizePolicy().hasHeightForWidth())
        self.tag_container.setSizePolicy(sizePolicy3)
        self.tag_container.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.horizontalLayout = QHBoxLayout(self.tag_container)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.horizontalLayout_3.addWidget(self.tag_container)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_7.addWidget(self.scrollArea)


        self.verticalLayout_2.addWidget(self.groupBox_7)

        self.groupBox_5 = QGroupBox(self.edit_mode)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.add_customer_pushButton = QPushButton(self.groupBox_5)
        self.add_customer_pushButton.setObjectName(u"add_customer_pushButton")
        self.add_customer_pushButton.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.add_customer_pushButton)

        self.scrollArea_2 = QScrollArea(self.groupBox_5)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 450, 69))
        self.horizontalLayout_4 = QHBoxLayout(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.customer_container = QWidget(self.scrollAreaWidgetContents_2)
        self.customer_container.setObjectName(u"customer_container")
        self.horizontalLayout_2 = QHBoxLayout(self.customer_container)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.horizontalLayout_4.addWidget(self.customer_container)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.horizontalLayout_5.addWidget(self.scrollArea_2)


        self.verticalLayout_2.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.edit_mode)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.add_quote_pushButton = QPushButton(self.groupBox_6)
        self.add_quote_pushButton.setObjectName(u"add_quote_pushButton")
        self.add_quote_pushButton.setIcon(icon)

        self.horizontalLayout_6.addWidget(self.add_quote_pushButton)

        self.quote_tableWidget = QTableWidget(self.groupBox_6)
        if (self.quote_tableWidget.columnCount() < 3):
            self.quote_tableWidget.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.quote_tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.quote_tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.quote_tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.quote_tableWidget.setObjectName(u"quote_tableWidget")

        self.horizontalLayout_6.addWidget(self.quote_tableWidget)


        self.verticalLayout_2.addWidget(self.groupBox_6)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_10 = QGroupBox(self.edit_mode)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_10)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.comboBox = QComboBox(self.groupBox_10)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_9.addWidget(self.comboBox)

        self.search_LineEdit = QLineEdit(self.groupBox_10)
        self.search_LineEdit.setObjectName(u"search_LineEdit")

        self.horizontalLayout_9.addWidget(self.search_LineEdit)

        self.search_PushButton = QPushButton(self.groupBox_10)
        self.search_PushButton.setObjectName(u"search_PushButton")

        self.horizontalLayout_9.addWidget(self.search_PushButton)


        self.verticalLayout_4.addWidget(self.groupBox_10)

        self.groupBox_9 = QGroupBox(self.edit_mode)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.productlist_ListWidget = QListWidget(self.groupBox_9)
        self.productlist_ListWidget.setObjectName(u"productlist_ListWidget")

        self.verticalLayout_3.addWidget(self.productlist_ListWidget)


        self.verticalLayout_4.addWidget(self.groupBox_9)


        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.scrollArea_3 = QScrollArea(self.edit_mode)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 553, 419))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.add_product_label = QLabel(self.scrollAreaWidgetContents_3)
        self.add_product_label.setObjectName(u"add_product_label")

        self.gridLayout_3.addWidget(self.add_product_label, 1, 0, 1, 1)

        self.last_updated_at_label = QLabel(self.scrollAreaWidgetContents_3)
        self.last_updated_at_label.setObjectName(u"last_updated_at_label")

        self.gridLayout_3.addWidget(self.last_updated_at_label, 0, 0, 1, 1)

        self.edit_pushButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.edit_pushButton.setObjectName(u"edit_pushButton")

        self.gridLayout_3.addWidget(self.edit_pushButton, 2, 1, 1, 1)

        self.edit_product_label = QLabel(self.scrollAreaWidgetContents_3)
        self.edit_product_label.setObjectName(u"edit_product_label")

        self.gridLayout_3.addWidget(self.edit_product_label, 2, 0, 1, 1)

        self.add_PushButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.add_PushButton.setObjectName(u"add_PushButton")

        self.gridLayout_3.addWidget(self.add_PushButton, 1, 2, 1, 1)

        self.delete_pushButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.delete_pushButton.setObjectName(u"delete_pushButton")

        self.gridLayout_3.addWidget(self.delete_pushButton, 3, 1, 1, 1)

        self.newform_PushButton = QPushButton(self.scrollAreaWidgetContents_3)
        self.newform_PushButton.setObjectName(u"newform_PushButton")

        self.gridLayout_3.addWidget(self.newform_PushButton, 1, 1, 1, 1)

        self.delete_product_label = QLabel(self.scrollAreaWidgetContents_3)
        self.delete_product_label.setObjectName(u"delete_product_label")

        self.gridLayout_3.addWidget(self.delete_product_label, 3, 0, 1, 1)

        self.last_updated_Label = QLabel(self.scrollAreaWidgetContents_3)
        self.last_updated_Label.setObjectName(u"last_updated_Label")

        self.gridLayout_3.addWidget(self.last_updated_Label, 0, 1, 1, 1)

        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.gridLayout_4.addWidget(self.scrollArea_3, 1, 0, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_4)

        self.tabWidget.addTab(self.edit_mode, "")
        self.display_mode = QWidget()
        self.display_mode.setObjectName(u"display_mode")
        sizePolicy.setHeightForWidth(self.display_mode.sizePolicy().hasHeightForWidth())
        self.display_mode.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.display_mode)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_11 = QGroupBox(self.display_mode)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_11)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.comboBox_2 = QComboBox(self.groupBox_11)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.horizontalLayout_11.addWidget(self.comboBox_2)

        self.search_LineEdit_2 = QLineEdit(self.groupBox_11)
        self.search_LineEdit_2.setObjectName(u"search_LineEdit_2")

        self.horizontalLayout_11.addWidget(self.search_LineEdit_2)

        self.search_PushButton_2 = QPushButton(self.groupBox_11)
        self.search_PushButton_2.setObjectName(u"search_PushButton_2")

        self.horizontalLayout_11.addWidget(self.search_PushButton_2)


        self.verticalLayout_5.addWidget(self.groupBox_11)

        self.groupBox_12 = QGroupBox(self.display_mode)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.horizontalLayout_12 = QHBoxLayout(self.groupBox_12)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.listWidget_2 = QListWidget(self.groupBox_12)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.horizontalLayout_12.addWidget(self.listWidget_2)


        self.verticalLayout_5.addWidget(self.groupBox_12)


        self.gridLayout_5.addLayout(self.verticalLayout_5, 1, 0, 1, 1)

        self.groupBox_13 = QGroupBox(self.display_mode)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_13)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.image_container_2 = QWidget(self.groupBox_13)
        self.image_container_2.setObjectName(u"image_container_2")
        sizePolicy.setHeightForWidth(self.image_container_2.sizePolicy().hasHeightForWidth())
        self.image_container_2.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.image_container_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.verticalLayout_6.addWidget(self.image_container_2)


        self.gridLayout_5.addWidget(self.groupBox_13, 1, 1, 1, 1)

        self.groupBox_14 = QGroupBox(self.display_mode)
        self.groupBox_14.setObjectName(u"groupBox_14")
        self.formLayout_2 = QFormLayout(self.groupBox_14)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.ref_num_label_2 = QLabel(self.groupBox_14)
        self.ref_num_label_2.setObjectName(u"ref_num_label_2")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.ref_num_label_2)

        self.ref_num_LineEdit_2 = QLineEdit(self.groupBox_14)
        self.ref_num_LineEdit_2.setObjectName(u"ref_num_LineEdit_2")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.ref_num_LineEdit_2)

        self.name_label_2 = QLabel(self.groupBox_14)
        self.name_label_2.setObjectName(u"name_label_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.name_label_2)

        self.name_LineEdit_2 = QLineEdit(self.groupBox_14)
        self.name_LineEdit_2.setObjectName(u"name_LineEdit_2")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.name_LineEdit_2)

        self.price_usd_label_2 = QLabel(self.groupBox_14)
        self.price_usd_label_2.setObjectName(u"price_usd_label_2")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.LabelRole, self.price_usd_label_2)

        self.price_usd_LineEdit_2 = QLineEdit(self.groupBox_14)
        self.price_usd_LineEdit_2.setObjectName(u"price_usd_LineEdit_2")

        self.formLayout_2.setWidget(2, QFormLayout.ItemRole.FieldRole, self.price_usd_LineEdit_2)


        self.gridLayout_5.addWidget(self.groupBox_14, 0, 1, 1, 1)


        self.verticalLayout_8.addLayout(self.gridLayout_5)

        self.tabWidget.addTab(self.display_mode, "")

        self.horizontalLayout_13.addWidget(self.tabWidget)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_13)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1808, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Product Identity", None))
        self.ref_num_label.setText(QCoreApplication.translate("MainWindow", u"Reference #", None))
        self.name_label.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.barcode_label.setText(QCoreApplication.translate("MainWindow", u"Barcode", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Packaging", None))
        self.pcs_innerbox_label.setText(QCoreApplication.translate("MainWindow", u"Pcs/inner box", None))
        self.pcs_ctn_label.setText(QCoreApplication.translate("MainWindow", u"Pcs/ctn", None))
        self.weight_label.setText(QCoreApplication.translate("MainWindow", u"Weight", None))
        self.packing_label.setText(QCoreApplication.translate("MainWindow", u"Packing", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Pricing", None))
        self.price_usd_label.setText(QCoreApplication.translate("MainWindow", u"Price (USD)", None))
        self.price_rmb_label.setText(QCoreApplication.translate("MainWindow", u"Price (RMB)", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Remarks", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Images", None))
        self.upload_img_pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload Image", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Tags", None))
        self.add_tag_pushButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Customers", None))
        self.add_customer_pushButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Quotes", None))
        self.add_quote_pushButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        ___qtablewidgetitem = self.quote_tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Customer", None));
        ___qtablewidgetitem1 = self.quote_tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Quote", None));
        ___qtablewidgetitem2 = self.quote_tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Remark", None));
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Search Bar", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Reference number", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Name", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Tag", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", u"Customer", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("MainWindow", u"Barcode", None))

        self.search_PushButton.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Product List", None))
        self.add_product_label.setText(QCoreApplication.translate("MainWindow", u"Add Product", None))
        self.last_updated_at_label.setText(QCoreApplication.translate("MainWindow", u"Last Updated at", None))
        self.edit_pushButton.setText(QCoreApplication.translate("MainWindow", u"Confirm edit", None))
        self.edit_product_label.setText(QCoreApplication.translate("MainWindow", u"Edit Product", None))
        self.add_PushButton.setText(QCoreApplication.translate("MainWindow", u"Confirm addition", None))
        self.delete_pushButton.setText(QCoreApplication.translate("MainWindow", u"Delete product", None))
        self.newform_PushButton.setText(QCoreApplication.translate("MainWindow", u"New form", None))
        self.delete_product_label.setText(QCoreApplication.translate("MainWindow", u"Delete Product", None))
        self.last_updated_Label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.edit_mode), QCoreApplication.translate("MainWindow", u"Edit mode", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Search Bar", None))
        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Reference number", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"Name", None))
        self.comboBox_2.setItemText(2, QCoreApplication.translate("MainWindow", u"Tag", None))
        self.comboBox_2.setItemText(3, QCoreApplication.translate("MainWindow", u"Customer", None))
        self.comboBox_2.setItemText(4, QCoreApplication.translate("MainWindow", u"Barcode", None))

        self.search_PushButton_2.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Product List", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Images", None))
        self.groupBox_14.setTitle(QCoreApplication.translate("MainWindow", u"Product Details", None))
        self.ref_num_label_2.setText(QCoreApplication.translate("MainWindow", u"Reference number", None))
        self.name_label_2.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.price_usd_label_2.setText(QCoreApplication.translate("MainWindow", u"Price (USD)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.display_mode), QCoreApplication.translate("MainWindow", u"Display Mode", None))
    # retranslateUi

