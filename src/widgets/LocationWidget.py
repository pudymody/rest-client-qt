from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QLineEdit 
from PyQt5.QtCore import Qt, pyqtSignal

class LocationWidget(QWidget):
    request = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        requestLayout = QHBoxLayout()
        requestLayout.setContentsMargins(0,0,0,0)

        method = QComboBox()
        method.addItems(["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
        self.method = method

        url = QLineEdit()
        url.setText("https://httpbin.org/get")
        url.returnPressed.connect( self._fireRequest )

        self.url = url

        submit = QPushButton("Send")
        submit.clicked.connect( self._fireRequest )

        requestLayout.addWidget(method)
        requestLayout.addWidget(url)
        requestLayout.addWidget(submit)
        requestLayout.setAlignment(Qt.AlignTop)

        self.setLayout(requestLayout)

    def getMethod(self):
        return self.method.currentText()

    def getURL(self):
        url = self.url.text()
        if url[0:7] != "http://" and url[0:8] != "https://":
            url = "https://" + url

        return url 

    def _fireRequest(self):
        self.request.emit()
