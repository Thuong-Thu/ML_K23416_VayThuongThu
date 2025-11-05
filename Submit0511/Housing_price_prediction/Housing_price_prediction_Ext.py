import sys
import pickle
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class HousePredictor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dự đoán giá nhà bằng mô hình Machine Learning")
        self.setGeometry(100, 100, 600, 450)
        self.initUI()

    def initUI(self):
        y = 40
        label_width = 200
        input_width = 200
        height = 30
        spacing = 50

        # --- Các nhãn và ô nhập dữ liệu ---
        self.labels = []
        self.inputs = []
        fields = [
            "Avg. Area Income:",
            "Avg. Area House Age:",
            "Avg. Area Number of Rooms:",
            "Avg. Area Number of Bedrooms:",
            "Area Population:"
        ]

        for i, field in enumerate(fields):
            lbl = QLabel(field, self)
            lbl.setGeometry(50, y + i * spacing, label_width, height)
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.labels.append(lbl)

            inp = QLineEdit(self)
            inp.setGeometry(270, y + i * spacing, input_width, height)
            self.inputs.append(inp)

        # --- Nút dự đoán ---
        self.btnPredict = QPushButton("Dự đoán giá nhà", self)
        self.btnPredict.setGeometry(200, y + len(fields) * spacing, 180, 40)
        self.btnPredict.clicked.connect(self.predict_price)

        # --- Hàng hiển thị giá nhà dự đoán ---
        lbl_price = QLabel("Giá nhà dự đoán:", self)
        lbl_price.setGeometry(50, y + (len(fields) + 1) * spacing, label_width, height)
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.predicted_price = QLineEdit(self)
        self.predicted_price.setGeometry(270, y + (len(fields) + 1) * spacing, input_width, height)
        self.predicted_price.setReadOnly(True)
        self.predicted_price.setStyleSheet("color: blue; font-weight: bold; font-size: 14px;")

    def predict_price(self):
        try:
            import pandas as pd

            # Lấy dữ liệu từ giao diện
            values = [float(inp.text()) for inp in self.inputs]

            # Nạp model đã huấn luyện
            with open("housingmodel.zip", "rb") as f:
                model = pickle.load(f)

            # Tạo DataFrame với đúng tên cột
            columns = [
                'Avg. Area Income',
                'Avg. Area House Age',
                'Avg. Area Number of Rooms',
                'Avg. Area Number of Bedrooms',
                'Area Population'
            ]
            features = pd.DataFrame([values], columns=columns)

            # Dự đoán
            prediction = model.predict(features)[0]

            # Xuất kết quả ra ô hiển thị
            self.predicted_price.setText(f"${prediction:,.2f}")

        except ValueError:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng nhập đầy đủ và đúng định dạng số!")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy file 'housingmodel.zip'!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi hệ thống", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HousePredictor()
    window.show()
    sys.exit(app.exec())
