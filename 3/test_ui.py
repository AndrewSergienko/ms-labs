from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import seaborn as sns

import alg


def seabornplot(params):
    model = alg.create_model(params)
    df = alg.start(model)
    g = sns.FacetGrid(df)
    g.map_dataframe(sns.lineplot)
    return g.fig


class MainWindow(QtWidgets.QMainWindow):
    send_fig = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        # self.main_widget = QtWidgets.QWidget(self)

        self.params_widget = QtWidgets.QWidget(self)
        self.params_layout = QtWidgets.QVBoxLayout(self.params_widget)

        self.params = {
            "x": (QtWidgets.QLabel("Розмір сітки по Х"), QtWidgets.QSpinBox()),
            "y": (QtWidgets.QLabel("Розмір сітки по Y"), QtWidgets.QSpinBox()),
            "victim_num": (QtWidgets.QLabel("Кількість жертв"), QtWidgets.QSpinBox()),
            "predator_num": (QtWidgets.QLabel("Кількість хижаків"), QtWidgets.QSpinBox()),
            "victim_repr_age": (QtWidgets.QLabel("Поч. вік розмноження жертв"), QtWidgets.QSpinBox()),
            "predator_repr_age": (QtWidgets.QLabel("Поч. вік розмноження хижаків"), QtWidgets.QSpinBox()),
            "victim_repr_period": (QtWidgets.QLabel("Період розмноження жертв"), QtWidgets.QSpinBox()),
            "predator_repr_period": (QtWidgets.QLabel("Період розмноження хижаків"), QtWidgets.QSpinBox()),
            "predator_lifetime": (QtWidgets.QLabel("Хижак живе без їжі"), QtWidgets.QSpinBox()),
            "tacts": (QtWidgets.QLabel("Кількість тактів"), QtWidgets.QSpinBox()),
        }

        params_spinbox_args = [(1000, 20), (1000, 20), (10000, 500), (1000, 20),
                               (10, 3), (10, 3), (10, 3), (10, 3), (10, 3), (1000, 200)]

        for (label, input_w), (maximum, value) in zip(self.params.values(), params_spinbox_args):
            self.params_layout.addWidget(label)
            self.params_layout.addWidget(input_w)
            input_w.setMaximum(maximum)
            input_w.setValue(value)

        self.start_button = QtWidgets.QPushButton("Згенерувати")
        self.start_button.clicked.connect(self.start_model)
        self.params_layout.addWidget(self.start_button)

        # self.canvas_list = []
        # random_list = [pd.DataFrame(data={'group': [], 'count': []})]
        # for random_df in random_list:
        #     canvas = FigureCanvas(seabornplot(random_df))
        #     canvas.updateGeometry()
        #     self.canvas_list.append(canvas)
        #
        # self.main_layout = QtWidgets.QHBoxLayout(self.main_widget)
        #
        # self.canvas_layout = QtWidgets.QVBoxLayout(self.main_widget)
        # for canvas in self.canvas_list:
        #     self.canvas_layout.addWidget(canvas)
        #
        # self.main_layout.addLayout(self.canvas_layout)

        self.canvas_widget = QtWidgets.QWidget(self)
        self.canvas_layout = QtWidgets.QVBoxLayout(self.canvas_widget)

        self.setCentralWidget(self.params_widget)
        self.show()

    def start_model(self):
        try:
            params = {
                key: param[1].value() for key, param in zip(self.params.keys(), self.params.values())
            }
            canvas = FigureCanvas(seabornplot(params))
            canvas.updateGeometry()
            self.canvas_layout.addWidget(canvas)
            self.setCentralWidget(self.canvas_widget)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())