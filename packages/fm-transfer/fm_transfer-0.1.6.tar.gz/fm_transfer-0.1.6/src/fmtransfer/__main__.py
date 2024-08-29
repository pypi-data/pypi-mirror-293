import sys
from PyQt6.QtWidgets import QApplication, QStyle, QStyleFactory
import fmtransfer
# import importlib.metadata
# import requests

def _main() -> None:
    app = QApplication(sys.argv)
    style: QStyle = app.style()
    if style.name() == "windows11":
        app.setStyle(QStyleFactory.create('Fusion'))
    fm_transfer = fmtransfer.FmTransfer()
    fm_transfer.show()
    sys.exit(app.exec())

def _check_versions() -> None:
    # url = "https://pypi.org/pypi/gg-transfer/json"
    # res = requests.get(url)
    # json_data = res.json()
    # print("gg-transfer", json_data["info"]["version"], importlib.metadata.version("gg-transfer"))
    # url = "https://pypi.org/pypi/quiet-transfer/json"
    # res = requests.get(url)
    # json_data = res.json()
    # print("quiet-transfer", json_data["info"]["version"], importlib.metadata.version("quiet-transfer"))
    # url = "https://pypi.org/pypi/ggwave-wheels/json"
    # res = requests.get(url)
    # json_data = res.json()
    # print("ggwave-wheels", json_data["info"]["version"], importlib.metadata.version("ggwave-wheels"))
    # url = "https://pypi.org/pypi/fm-transfer/json"
    # res = requests.get(url)
    # json_data = res.json()
    # print("fm_transfer", json_data["info"]["version"], fmtransfer.__version__)
    pass


if __name__ == "__main__":
    _main()
