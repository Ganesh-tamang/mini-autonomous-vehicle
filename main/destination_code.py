
# find route using openroute services
# show map using folium and displaying it using pyqt5

# Note: change client api key by your api key. YOU CAN CREATE YOUR API KEY IN OPENROUTE Service for free
# see here for details: https://api.openrouteservice.org/

import sys
import io
import folium 
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine
from PyQt5 import QtCore, QtGui, QtWidgets
from main import main_process
import openrouteservice as ors
import folium
import geocoder

# I will change my api key on april 1, 2023. 
client = ors.Client(key="5b3ce3597851110001cf6248a2eff3cc63f54301b86eb4e6720d4420")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.run_main_code =False
        self.directions = []
        self.locations = []
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 0, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 10, 251, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda : self.pressed_it())
        self.pushButton.setGeometry(QtCore.QRect(380, 10, 31, 23))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(29, 59, 700, 541))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        
        self.webView = QWebEngineView()
        self.verticalLayout.addWidget(self.webView)
        self.showmap()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Destination:"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Destination Name"))
        self.pushButton.setText(_translate("MainWindow", "Go"))

    # show the map 
    def showmap(self, end = ""):
        start_loc = geocoder.ip("me")
        map_directions = folium.Map(location=[start_loc.lat, start_loc.lng], zoom_start=18)
        map_directions.add_child(folium.Marker(location=[start_loc.lat,start_loc.lng],popup = "your location",icon = folium.Icon(color = 'blue')))
        if end !="":
            end = self.lineEdit.text()
            end_loc = geocoder.osm(end)
            coordinates = [[start_loc.lng, start_loc.lat], [end_loc.lng, end_loc.lat]]
            route = client.directions(coordinates=coordinates,
                                profile='driving-car',
                                format='geojson') 
                

            # add geojson to map
            folium.GeoJson(route, name='route').add_to(map_directions)
            map_directions.add_child(folium.Marker(location=[end_loc.lat,end_loc.lng],popup = "destination",icon = folium.Icon(color = 'red')))

            self.show_directions(route)
            self.run_main_code = True
            
        # add layer control to map (allows layer to be turned on or off)
        folium.LayerControl().add_to(map_directions)

        # save map data to data object
        data = io.BytesIO()
        map_directions.save(data, close_file=False)
        self.webView.setHtml(data.getvalue().decode())
        
        if self.run_main_code:
            main_process( self.directions, self.locations)
            
       

    def pressed_it(self):
        self.directions = []
        self.locations = []
        self.showmap(self.lineEdit.text())
        
    
    def show_directions(self, route):
        for index, i in enumerate(route['features'][0]['properties']['segments'][0]['steps']):
            # print(index+1, i, '\n')
            self.directions.append(i["instruction"])
            self.locations.append(i["name"])


        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
