import pandas as pd
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import seaborn as sns
import matplotlib.pyplot as plt

import methods


def seabornplot(df):
    g = sns.FacetGrid(df)
    g.map_dataframe(sns.barplot, x="group", y="count")
    return g.fig


class MainWindow(QtWidgets.QMainWindow):
    send_fig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.main_widget = QtWidgets.QWidget(self)

        self.canvas_list = []
        random_list = [pd.DataFrame(data={'group': [], 'count': []}),
                       pd.DataFrame(data={'group': [], 'count': []}),
                       pd.DataFrame(data={'group': [], 'count': []})]
        for random_df in random_list:
            canvas = FigureCanvas(seabornplot(random_df))
            canvas.updateGeometry()
            self.canvas_list.append(canvas)

        self.canvas_label_list = [QtWidgets.QLabel('Метод середини квадрата'),
                                  QtWidgets.QLabel('Конкурентно лінійний метод'),
                                  QtWidgets.QLabel('Метод генерації Python')]

        self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)

        self.canvas_layout = QtWidgets.QVBoxLayout(self.main_widget)
        for label, canvas in zip(self.canvas_label_list, self.canvas_list):
            self.canvas_layout.addWidget(label)
            self.canvas_layout.addWidget(canvas)

        self.main_layout.addLayout(self.canvas_layout)

        self.button = QtWidgets.QPushButton("Згенерувати")
        self.label1 = QtWidgets.QLabel("Інтевал від 0 до")
        self.label2 = QtWidgets.QLabel("Кількість проміжків")
        self.label3 = QtWidgets.QLabel("Кільіксть випробувань")
        self.spinBox1 = QtWidgets.QSpinBox()
        self.spinBox2 = QtWidgets.QSpinBox()
        self.spinBox3 = QtWidgets.QSpinBox()
        self.spinBox1.setMaximum(1000)
        self.spinBox2.setMaximum(10)
        self.spinBox3.setMaximum(100)

        self.numbers_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.numbers_area_list = []
        for _ in range(3):
            textarea = QtWidgets.QTextBrowser()
            textarea.setMaximumWidth(50)
            self.numbers_area_list.append(textarea)
            self.numbers_layout.addWidget(textarea)
        self.main_layout.addLayout(self.numbers_layout)

        params = [self.button, self.label1, self.spinBox1, self.label2, self.spinBox2,
                  self.label3, self.spinBox3]
        self.button.clicked.connect(self.update)
        self.params_layout = QtWidgets.QVBoxLayout(self.main_widget)
        for param in params:
            self.params_layout.addWidget(param)

        self.params_layout.addStretch()
        self.params_layout.setSpacing(1)

        self.main_layout.addLayout(self.params_layout)

        self.setCentralWidget(self.main_widget)
        self.show()

    def update(self):
        m = self.spinBox1.value()
        p = self.spinBox2.value()
        n = self.spinBox3.value()
        numbers = [
                    methods.random_square_center(m, n, p),
                    methods.random_linear_concurent(m, n, p),
                    methods.random_system(m, n, p)]
        random_stats = [pd.read_csv("square_center.csv", sep='\t'),
                        pd.read_csv("linear_concurent.csv", sep='\t'),
                        pd.read_csv("system.csv", sep='\t')]
        for i, canvas in enumerate(self.canvas_list):
            canvas.figure = seabornplot(random_stats[i])
            canvas.draw()
            canvas.resize(300, 210)

            self.numbers_area_list[i].setText("\n".join(numbers[i]))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
