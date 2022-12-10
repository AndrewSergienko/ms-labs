import asyncio
import functools
import sys
import seaborn as sns

from PyQt5 import QtWidgets

import qasync
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qasync import asyncSlot, asyncClose, QApplication

import alg


class MainWindow(QtWidgets.QMainWindow):
    """Main window."""

    _DEF_URL = "https://jsonplaceholder.typicode.com/todos/1"
    """str: Default URL."""

    _SESSION_TIMEOUT = 1.0
    """float: Session timeout."""

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

        params_spinbox_args = [(1000, 50), (1000, 50), (10000, 500), (1000, 20),
                               (10, 3), (10, 3), (10, 3), (10, 3), (10, 2), (1000, 500)]

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

    @asyncSlot()
    async def start_model(self):
        try:
            params = {
                key: param[1].value() for key, param in zip(self.params.keys(), self.params.values())
            }
            print(params)
            canvas = FigureCanvas(await self.seabornplot(params))
            canvas.updateGeometry()
            self.canvas_layout.addWidget(canvas)
            self.setCentralWidget(self.canvas_widget)
            self.resize(1000, 500)
        except Exception as exc:
            print(exc)

    async def seabornplot(self, params):
        model = await alg.create_model(params)
        df = await alg.start(model)
        g = sns.FacetGrid(df)
        g.map_dataframe(sns.lineplot)
        return g.fig


async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    mainWindow = MainWindow()
    mainWindow.show()

    await future
    return True


if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)