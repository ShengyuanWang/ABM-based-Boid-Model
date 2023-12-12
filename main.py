from random import randint

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Agents.Boid import Boid
from Agents.Mountain import Mountain
from Agents.Predator import Predator

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, boids, mountains, predators, size):
        super().__init__()
        # setting geometry
        self.setGeometry(0, 0, size*2, size)
        # Create a splitter to arrange plots side by side
        splitter = QSplitter(Qt.Horizontal)
        self.boids = boids
        self.mountains = mountains
        self.predators = predators
        # # # Temperature vs time dynamic plot
        self.plot_graph = pg.PlotWidget()
        self.plot_cohesion = pg.PlotWidget()
        splitter.addWidget(self.plot_graph)
        # splitter.addWidget(self.plot_cohesion)
        splitter.setOrientation(Qt.Horizontal)
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")
        self.plot_graph.setTitle("Boid", color="b", size="20pt")
        styles = {"color": "red", "font-size": "18px"}
        self.plot_graph.setLabel("left", "Y-Position", **styles)
        self.plot_graph.setLabel("bottom", "X-Position", **styles)
        self.plot_graph.addLegend()
        self.plot_graph.showGrid(x=True, y=True)
        self.plot_graph.setYRange(0, size)
        self.plot_graph.setXRange(0, size)
        self.time = list(range(10))
        self.temperature = [randint(20, 40) for _ in range(10)]
        self.size = size
        self.scatter_boids = pg.ScatterPlotItem()
        self.scatter_mountains = pg.ScatterPlotItem(size=20)
        self.scatter_predators = pg.ScatterPlotItem(brush=pg.mkBrush(0, 255, 255))
        self.plot_graph.addItem(self.scatter_boids)
        self.plot_graph.addItem(self.scatter_mountains)
        self.plot_graph.addItem(self.scatter_predators)





        # Add a timer to simulate new temperature measurements
        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        # self.UiComponents()
        # self.s1 = QScrollBar(Qt.Horizontal, self)
        # method for components
    def UiComponents(self):
        scroll = QScrollBar(self)

        # setting geometry of the scroll bar
        scroll.setGeometry(100, 50, 30, 200)

        # setting value of scroll bar
        scroll.setValue(25)

        # making its background color to green
        scroll.setStyleSheet("background : lightgrey;")

        # creating a label
        label = QLabel("GeeksforGeeks", self)

        # setting geometry to the label
        label.setGeometry(200, 100, 300, 80)

        # making label multi line
        label.setWordWrap(True)

        # getting value changed signal
        scroll.valueChanged.connect(lambda: do_action())

        # method called when signal is emitted
        def do_action():

            # getting current value
            value = scroll.value()

            # setting text to the label
            label.setText("Current Value : " + str(value))




    def update_plot(self):
        self.update()


    def update(self):
        for i in range(1):
            for boid in self.boids:
                boid.updateBoid(self.boids, self.predators, self.mountains, boid.xstr, boid.xlim, boid.ystr, boid.xlim, 1)
            for predator in self.predators:
                predator.updatePredator(self.boids, 0, self.size, 0, self.size)
        boid_pen = pg.mkPen(color=(0, 0, 255))
        mountain_pen = pg.mkPen(color=(0, 255, 0))
        self.x_data = [boid.x for boid in self.boids]
        self.y_data = [boid.y for boid in self.boids]
        self.scatter_boids.setData(self.x_data, self.y_data, pen=boid_pen)
        self.x_data = [mountain.x for mountain in self.mountains]
        self.y_data = [mountain.y for mountain in self.mountains]
        self.scatter_mountains.setData(self.x_data, self.y_data, pen=mountain_pen)
        self.x_data = [predator.x for predator in self.predators]
        self.y_data = [predator.y for predator in self.predators]
        self.scatter_predators.setData(self.x_data, self.y_data)



size = 1000
app = QtWidgets.QApplication([])
boids = [Boid(xstr=size/3, ystr=size/3,xlim=size/2, ylim=size/2) for _ in range(40)]
mountains = [Mountain(xlim=size, ylim=size) for _ in range(20)]
predators = [Predator(xstr=size/3, ystr=size/3,xlim=size/2, ylim=size/2) for _ in range(4)]
main = MainWindow(boids, mountains, predators, size)
main.show()
app.exec()
