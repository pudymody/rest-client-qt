from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from requests import request

from widgets.DictionaryEditor import DictionaryEditor
from widgets.LocationWidget import LocationWidget 

class TabbedDockWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setTabPosition(Qt.AllDockWidgetAreas, QTabWidget.North)

    def addWidget(self, label, widget):
        tab = QDockWidget(label)
        tab.setFeatures(QDockWidget.DockWidgetMovable)
        tab.setWidget(widget)

        self.addDockWidget(Qt.TopDockWidgetArea, tab)

def makeRequest():
    method = RequestLocation.getMethod()
    url = RequestLocation.getURL()
    headers = HeadersEditor.getValues()
    params = QueryEditor.getValues()
    data = {}

    if method == "POST":
        data = BodyEditor.getValues()

    try:
        r = request( method=method, url=url, headers=headers, params=params, data=data, allow_redirects=False )

        r_headers = r.headers;

        response_headers.setRowCount( len(r_headers)+1 )
        response_headers.setItem(0,0, QTableWidgetItem("Status") )
        response_headers.setItem(0,1, QTableWidgetItem( str(r.status_code) ) )

        i = 1
        for key, value in r_headers.items():
            response_headers.setItem(i,0, QTableWidgetItem(key) )
            response_headers.setItem(i,1, QTableWidgetItem(value) )
            i = i + 1

        response_body.setPlainText( r.text )

        response_cookies.setRowCount( len(r.cookies) )
        i = 0
        for c in r.cookies:
            response_cookies.setItem(i,0, QTableWidgetItem(c.name) )
            response_cookies.setItem(i,1, QTableWidgetItem(c.value) )
            response_cookies.setItem(i,2, QTableWidgetItem(c.expires) )
            response_cookies.setItem(i,3, QTableWidgetItem(c.path) )
            i = i + 1
    except BaseException as e:
        print(e)
        msg = QMessageBox(QMessageBox.Critical,"Request error", "Im sorry, there was an error performing the request. For more information check the console.")
        msg.open()


app = QApplication([])
window = QWidget()

windowLayout = QVBoxLayout()

RequestLocation = LocationWidget()
RequestLocation.request.connect(makeRequest)
windowLayout.addWidget( RequestLocation )

RequestParams = TabbedDockWidget()
HeadersEditor = DictionaryEditor()
QueryEditor = DictionaryEditor()
BodyEditor = DictionaryEditor()
RequestParams.addWidget("Request Headers", HeadersEditor )
RequestParams.addWidget("Request Query", QueryEditor )
RequestParams.addWidget("Request Body", BodyEditor )
windowLayout.addWidget(RequestParams)

ResponseParams = TabbedDockWidget()

response_headers = QTableWidget(1,2)
response_headers.setHorizontalHeaderLabels(["Header", "Value"])
response_headers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
response_headers.verticalHeader().hide()

response_cookies = QTableWidget(1,4)
response_cookies.setHorizontalHeaderLabels(["Name", "Value", "Expires", "Path"])
response_cookies.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
response_cookies.verticalHeader().hide()

response_body = QTextEdit()
response_body.setReadOnly(True)

ResponseParams.addWidget("Response Headers", response_headers)
ResponseParams.addWidget("Response Cookies", response_cookies)
ResponseParams.addWidget("Response Body", response_body)
windowLayout.addWidget(ResponseParams)

window.setLayout(windowLayout)
window.show()
app.exec()
