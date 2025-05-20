import sys
import json
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel, QMessageBox

class ModelFTDialog(QDialog):
    def __init__(self, parent=None):
        super(ModelFTDialog, self).__init__(parent)
        self.setWindowTitle("Diffss ModelFT Dialog")

        self.layout = QVBoxLayout()

        # Pretrained Model
        self.pretrained_model_layout = QHBoxLayout()
        self.pretrained_model_label = QLabel("Pretrained Model:")
        self.pretrained_model_edit = QLineEdit("path/to/pretrained/model")
        self.pretrained_model_browse = QPushButton("Browse")
        self.pretrained_model_browse.clicked.connect(lambda: self.browse_folder(self.pretrained_model_edit))
        self.pretrained_model_layout.addWidget(self.pretrained_model_label)
        self.pretrained_model_layout.addWidget(self.pretrained_model_edit)
        self.pretrained_model_layout.addWidget(self.pretrained_model_browse)
        self.layout.addLayout(self.pretrained_model_layout)

        # Train Data
        self.train_data_layout = QHBoxLayout()
        self.train_data_label = QLabel("Train Data (image_dir, label_dir, class_nums):")
        self.train_image_dir_edit = QLineEdit("path/to/train/images")
        self.train_image_dir_browse = QPushButton("Browse")
        self.train_image_dir_browse.clicked.connect(lambda: self.browse_folder(self.train_image_dir_edit))
        self.train_label_dir_edit = QLineEdit("path/to/train/labels")
        self.train_label_dir_browse = QPushButton("Browse")
        self.train_label_dir_browse.clicked.connect(lambda: self.browse_folder(self.train_label_dir_edit))
        self.train_class_nums_edit = QLineEdit("10")
        self.train_data_layout.addWidget(self.train_data_label)
        self.train_data_layout.addWidget(self.train_image_dir_edit)
        self.train_data_layout.addWidget(self.train_image_dir_browse)
        self.train_data_layout.addWidget(self.train_label_dir_edit)
        self.train_data_layout.addWidget(self.train_label_dir_browse)
        self.train_data_layout.addWidget(self.train_class_nums_edit)
        self.layout.addLayout(self.train_data_layout)

        # Save Directory
        self.save_dir_layout = QHBoxLayout()
        self.save_dir_label = QLabel("Save Directory:")
        self.save_dir_edit = QLineEdit("path/to/save/directory")
        self.save_dir_browse = QPushButton("Browse")
        self.save_dir_browse.clicked.connect(lambda: self.browse_folder(self.save_dir_edit))
        self.save_dir_layout.addWidget(self.save_dir_label)
        self.save_dir_layout.addWidget(self.save_dir_edit)
        self.save_dir_layout.addWidget(self.save_dir_browse)
        self.layout.addLayout(self.save_dir_layout)

        # Test Data
        self.test_data_layout = QHBoxLayout()
        self.test_data_label = QLabel("Test Data (image_dir, label_dir, class_nums):")
        self.test_image_dir_edit = QLineEdit("path/to/test/images")
        self.test_image_dir_browse = QPushButton("Browse")
        self.test_image_dir_browse.clicked.connect(lambda: self.browse_folder(self.test_image_dir_edit))
        self.test_label_dir_edit = QLineEdit("path/to/test/labels")
        self.test_label_dir_browse = QPushButton("Browse")
        self.test_label_dir_browse.clicked.connect(lambda: self.browse_folder(self.test_label_dir_edit))
        self.test_class_nums_edit = QLineEdit("10")
        self.test_data_layout.addWidget(self.test_data_label)
        self.test_data_layout.addWidget(self.test_image_dir_edit)
        self.test_data_layout.addWidget(self.test_image_dir_browse)
        self.test_data_layout.addWidget(self.test_label_dir_edit)
        self.test_data_layout.addWidget(self.test_label_dir_browse)
        self.test_data_layout.addWidget(self.test_class_nums_edit)
        self.layout.addLayout(self.test_data_layout)

        # Predict Directory
        self.predict_dir_layout = QHBoxLayout()
        self.predict_dir_label = QLabel("Predict Directory:")
        self.predict_dir_edit = QLineEdit("path/to/predict/directory")
        self.predict_dir_browse = QPushButton("Browse")
        self.predict_dir_browse.clicked.connect(lambda: self.browse_folder(self.predict_dir_edit))
        self.predict_dir_layout.addWidget(self.predict_dir_label)
        self.predict_dir_layout.addWidget(self.predict_dir_edit)
        self.predict_dir_layout.addWidget(self.predict_dir_browse)
        self.layout.addLayout(self.predict_dir_layout)

        # Load and Save Config Buttons
        self.config_layout = QHBoxLayout()
        self.load_config_button = QPushButton("Load Config")
        self.load_config_button.clicked.connect(self.load_config)
        self.save_config_button = QPushButton("Save Config")
        self.save_config_button.clicked.connect(self.save_config)
        self.config_layout.addWidget(self.load_config_button)
        self.config_layout.addWidget(self.save_config_button)
        self.layout.addLayout(self.config_layout)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.start_training_button = QPushButton("Start Training")
        self.start_training_button.clicked.connect(self.on_start_training)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.button_layout.addWidget(self.start_training_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            line_edit.setText(folder)

    def load_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    config = json.load(file)
                    self.pretrained_model_edit.setText(config.get('pretrained_model', ''))
                    self.train_image_dir_edit.setText(config.get('train_image_dir', ''))
                    self.train_label_dir_edit.setText(config.get('train_label_dir', ''))
                    self.train_class_nums_edit.setText(str(config.get('train_class_nums', 10)))
                    self.save_dir_edit.setText(config.get('save_dir', ''))
                    self.test_image_dir_edit.setText(config.get('test_image_dir', ''))
                    self.test_label_dir_edit.setText(config.get('test_label_dir', ''))
                    self.test_class_nums_edit.setText(str(config.get('test_class_nums', 10)))
                    self.predict_dir_edit.setText(config.get('predict_dir', ''))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load configuration: {str(e)}")

    def save_config(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            try:
                config = {
                    'pretrained_model': self.pretrained_model_edit.text(),
                    'train_image_dir': self.train_image_dir_edit.text(),
                    'train_label_dir': self.train_label_dir_edit.text(),
                    'train_class_nums': int(self.train_class_nums_edit.text()),
                    'save_dir': self.save_dir_edit.text(),
                    'test_image_dir': self.test_image_dir_edit.text(),
                    'test_label_dir': self.test_label_dir_edit.text(),
                    'test_class_nums': int(self.test_class_nums_edit.text()),
                    'predict_dir': self.predict_dir_edit.text()
                }
                with open(file_name, 'w') as file:
                    json.dump(config, file, indent=4)
                QMessageBox.information(self, "Success", "Configuration saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")
                
    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder:
            line_edit.setText(folder)

    def on_start_training(self):
        pretrained_model = self.pretrained_model_edit.text()
        train_image_dir = self.train_image_dir_edit.text()
        train_label_dir = self.train_label_dir_edit.text()
        train_class_nums = int(self.train_class_nums_edit.text())
        save_dir = self.save_dir_edit.text()
        test_image_dir = self.test_image_dir_edit.text()
        test_label_dir = self.test_label_dir_edit.text()
        test_class_nums = int(self.test_class_nums_edit.text())
        predict_dir = self.predict_dir_edit.text()

        print(f"Pretrained Model: {pretrained_model}")
        print(f"Train Data (image_dir, label_dir, class_nums): {train_image_dir}, {train_label_dir}, {train_class_nums}")
        print(f"Save Directory: {save_dir}")
        print(f"Test Data (image_dir, label_dir, class_nums): {test_image_dir}, {test_label_dir}, {test_class_nums}")
        print(f"Predict Directory: {predict_dir}")

        # 这里可以调用训练模型的函数
        self.accept()

def run_dialog():
    app = QApplication(sys.argv)
    dialog = ModelFTDialog()
    dialog.exec_()
    app.quit()
