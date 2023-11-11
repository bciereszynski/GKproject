from PyQt5 import QtCore
from PyQt5.QtChart import QChartView, QValueAxis, QBarSeries, QBarSet
from PyQt5.QtWidgets import QDialog, QVBoxLayout


class PlotDialog(QDialog):
    def __init__(self, x, y, parent=None):
        super().__init__(parent)

        self.resize(800, 600)

        set = QBarSet("")
        for i in range(len(x)):
            if y[i] != 0:
                set.append(y[i])

        series = QBarSeries()
        series.append(set)

        y_axis = QValueAxis()
        y_axis.setRange(min(y), max(y))
        y_axis.setLabelFormat("%d")

        x_axis = QValueAxis()
        x_axis.setRange(0, len(x))
        x_axis.setLabelFormat("%d")

        view = QChartView()

        chart = view.chart()
        chart.addSeries(series)
        chart.addAxis(x_axis, QtCore.Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(y_axis, QtCore.Qt.AlignmentFlag.AlignLeft)
        chart.legend().markers(series)[0].setVisible(False)

        self.lay = QVBoxLayout()
        self.lay.addWidget(view)

        self.setLayout(self.lay)
