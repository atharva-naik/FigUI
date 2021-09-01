import re, sys
import untangle
from PyQt5.QtQml import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPositioning import *
from PyQt5.QtQuickWidgets import *
import xml.etree.ElementTree as ET


class MarkerItem():
    def __init__(self, position, title):
        self._position = position
        self._title = title

    def position(self):
        return self._position

    def setPosition(self, value):
        self._position = value

    def title(self):
        return self._title

    def setTitle(self, value):
        self._title = value


class MarkerModel(QAbstractListModel):
    PositionRole = Qt.UserRole
    TitleRole = Qt.UserRole + 1

    _roles = {PositionRole: QByteArray(
        b"markerPosition"), TitleRole: QByteArray(b"markerTitle")}

    def __init__(self, parent=None):
        QAbstractListModel.__init__(self, parent)
        self._markers = []

    def rowCount(self, index=QModelIndex()):
        return len(self._markers)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        marker = self._markers[index.row()]

        if role == MarkerModel.PositionRole:
            return marker.position()

        elif role == MarkerModel.TitleRole:
            return marker.title()

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            marker = self._markers[index.row()]
            if role == MarkerModel.PositionRole:
                marker.setPosition(value)

            if role == MarkerModel.TitleRole:
                marker.setTitle(value)

            self.dataChanged.emit(index, index)
            return True
        return QAbstractListModel.setData(self, index, value, role)

    def addMarker(self, marker):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable


class Minimap():
    def __init__(self):
        self.setupUi()
        self.connect()
        self.createLayout()
        self.createQml()
        self.addWidgets()
        self.createColors()

    def setupUi(self):
        self.searchLabel = QLabel("Search for coordinate")
        self.searchLabel.setFixedWidth(160)
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedWidth(285)
        self.searchButton = QPushButton()
        self.searchButton.setFixedWidth(30)
        self.searchButton.resize(self.searchButton.sizeHint())
        icon = QIcon()
        icon.addPixmap(QPixmap(
            "icons/searchIcon.png"), QIcon.Normal, QIcon.Off)
        self.searchButton.setIcon(icon)
        self.listLabel = QLabel("Import XML-coordinates \nand pin them on Map")
        self.listLabel.setFixedWidth(160)
        self.listEdit = QLineEdit()
        self.listEdit.setFixedWidth(285)
        self.listButton = QPushButton()
        self.searchButton.setFixedWidth(30)
        self.listButton.resize(self.listButton.sizeHint())
        icon = QIcon()
        icon.addPixmap(QPixmap(
            "icons/listsearchIcon.png"), QIcon.Normal, QIcon.Off)
        self.listButton.setIcon(icon)
        self.colorLabel = QLabel("Change color of Line")
        self.colorLabel.setFixedWidth(160)
        self.comboBox = QComboBox()
        self.comboBox.setFixedWidth(285)
        self.selectColorBtn = QPushButton()
        self.selectColorBtn.resize(self.selectColorBtn.sizeHint())
        icon = QIcon()
        icon.addPixmap(QPixmap(
            "icons/changecolorIcon.png"), QIcon.Normal, QIcon.Off)
        self.selectColorBtn.setIcon(icon)

    def connect(self):
        self.searchButton.clicked.connect(self.search)
        self.lineEdit.returnPressed.connect(self.search)
        self.listButton.clicked.connect(self.openList)
        self.selectColorBtn.clicked.connect(self.selectColor)

    def createLayout(self):
        self.window = QWidget()
        self.window.setLayout(QVBoxLayout())
        self.controlS = QWidget()
        self.controlS.setLayout(QHBoxLayout())
        self.controlS.setMaximumSize(495, 50)
        self.controlX = QWidget()
        self.controlX.setLayout(QHBoxLayout())
        self.controlX.setMaximumSize(495, 50)
        self.jsonLine = QWidget()
        self.jsonLine.setLayout(QHBoxLayout())
        self.jsonLine.setMaximumSize(495, 50)

    def addWidgets(self):
        self.controlS.layout().addWidget(self.searchLabel)
        self.controlS.layout().addWidget(self.lineEdit)
        self.controlS.layout().addWidget(self.searchButton)
        self.controlX.layout().addWidget(self.listLabel)
        self.controlX.layout().addWidget(self.listEdit)
        self.controlX.layout().addWidget(self.listButton)
        self.jsonLine.layout().addWidget(self.colorLabel)
        self.jsonLine.layout().addWidget(self.comboBox)
        self.jsonLine.layout().addWidget(self.selectColorBtn)
        self.window.layout().addWidget(self.controlS)
        self.window.layout().addWidget(self.controlX)
        self.window.layout().addWidget(self.jsonLine)
        self.window.layout().addWidget(self.view)
        self.window.setMinimumSize(500, 500)
        self.window.setWindowTitle("Minimap")
        self.window.show()

    def createQml(self):
        self.view = QQuickWidget()
        self.model = MarkerModel()
        self.context = self.view.rootContext()
        self.context.setContextProperty('markerModel', self.model)
        self.view.setSource(QUrl('map.qml'))
        self.view.setMinimumSize(200, 200)
        self.view.setResizeMode(self.view.SizeRootObjectToView)
        self.rootObject = self.view.rootObject()

    def createColors(self):
        self.colors = []
        self.colors.append("blue")
        self.colors.append("red")
        self.colors.append("yellow")
        self.colors.append("black")
        self.colors.append("white")
        self.comboBox.addItems(self.colors)

    def selectColor(self):
        self.selected = self.comboBox.currentText()
        paintObject = self.rootObject.findChild(QObject, "paint")
        paintObject.setProperty("lineColor", self.selected)

    def openList(self):
        fileName = QFileDialog.getOpenFileName(
            None, "Open", "/home", "Only Xml(*.xml)")
        self.listEdit.setText(fileName[0])
        url = self.listEdit.text()
        tree = ET.parse(url)
        root = tree.getroot()
        r = root.find('item')
        if r:
            for elem in root.findall('item'):
                titl = elem.find('title').text
                lati = elem.find('latitude').text
                longi = elem.find('longitude').text
                self.model.addMarker(MarkerItem(QPointF(
                    float(lati), float(longi)), titl))
                self.mapObject = self.rootObject.findChild(QObject, "mapboxgl")
                self.mapObject.setProperty("zoomLevel", 2)
        else:
            i = 0
            titl = []
            tree = ET.parse(url)
            root = tree.getroot()
            for elem in root.findall('.//{'
                                     'http://ogr.maptools.org/}Name'):
                titl.append(elem.text)
            for elem in root.findall('.//{'
                                     'http://www.opengis.net/gml}'
                                     'coordinates'):
                coord = []
                coord.append(elem.text)
                for elem in coord:
                    part = elem.split(",")
                    lati = part[0]
                    longi = part[1]
                    self.model.addMarker(
                        MarkerItem(QPointF(
                            float(lati), float(longi)), titl[i]))
                    self.mapObject = self.rootObject.findChild(
                        QObject, "mapboxgl")
                    self.mapObject.setProperty("zoomLevel", 2)
                    i = i + 1

    def search(self):
        try:
            f = re.match(
                r'^([+-]?\d+\.?\d*),?\s+([+-]?\d+\.?\d*)$',
                self.lineEdit.text())
            if abs(float(f[1])) <= 90 and abs(float(f[2])) <= 180:
                lat = float(f[1])
                lon = float(f[2])
            self.mapObject = self.rootObject.findChild(QObject, "mapboxgl")
            self.markerObject = self.rootObject.findChild(QObject, "marker")
            self.mapObject.setProperty("lat", lat)
            self.mapObject.setProperty("lon", lon)
            self.markerObject.setProperty("coordinate", QGeoCoordinate(
                lat, lon))
            self.markerObject.setProperty("visible", True)
        except Exception:
            QMessageBox.warning(
                None, "Invalid Coordinate", "Invalid coordinate")
            self.lineEdit.selectAll()


if __name__ == "__main__":
    myApp = QApplication(sys.argv)
    GUI = Minimap()
    sys.exit(myApp.exec_())
