import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog
)
from PySide6.QtCore import Qt
from pipeline import gooey_loader

class DataProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contractor Data Template Creation")
        self.setMinimumSize(500, 350)

        # Main Layout Container
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # -------------------------------------------------------------
        # 1. FILE & DIRECTORY SELECTION GROUP
        # -------------------------------------------------------------
        io_group = QGroupBox("File & Folder Settings")
        io_layout = QGridLayout()
        io_layout.setSpacing(10)

        # Input File Selection
        self.lbl_input = QLabel("Input File:")
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Select a data file to process...")
        self.btn_browse_input = QPushButton("Browse...")
        self.btn_browse_input.clicked.connect(self.select_input_file)

        io_layout.addWidget(self.lbl_input, 0, 0)
        io_layout.addWidget(self.txt_input, 0, 1)
        io_layout.addWidget(self.btn_browse_input, 0, 2)

        # Output Directory Selection
        self.lbl_output = QLabel("Output Directory:")
        self.txt_output = QLineEdit()
        self.txt_output.setPlaceholderText("Select where to save generated files...")
        self.btn_browse_output = QPushButton("Choose Output Folder...")
        self.btn_browse_output.clicked.connect(self.select_output_directory)

        io_layout.addWidget(self.lbl_output, 1, 0)
        io_layout.addWidget(self.txt_output, 1, 1)
        io_layout.addWidget(self.btn_browse_output, 1, 2)

        io_group.setLayout(io_layout)
        main_layout.addWidget(io_group)

        # -------------------------------------------------------------
        # 2. EXPORT OPTIONS GROUP (Checkboxes)
        # -------------------------------------------------------------
        options_group = QGroupBox("Export Configuration")
        options_layout = QVBoxLayout()
        options_layout.setSpacing(8)

        self.chk_census = QCheckBox("Save Census Data")
        self.chk_csv = QCheckBox("Save as Word Document")
        self.chk_powerbi = QCheckBox("Save Data for Power BI")

        # Set default states if desired
        self.chk_csv.setChecked(True)
        #self.chk_census.setChecked(True)
        self.chk_powerbi.setChecked(True)

        options_layout.addWidget(self.chk_census)
        options_layout.addWidget(self.chk_csv)
        options_layout.addWidget(self.chk_powerbi)

        options_group.setLayout(options_layout)
        main_layout.addWidget(options_group)

        # -------------------------------------------------------------
        # 3. ACTION BUTTON (Run / Process)
        # -------------------------------------------------------------
        self.btn_process = QPushButton("Process Data")
        self.btn_process.setStyleSheet("font-weight: bold; font-size: 13px; padding: 6px;")
        self.btn_process.clicked.connect(self.run_processing)
        main_layout.addWidget(self.btn_process)

        # Status Label for User Feedback
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet("color: gray;")
        main_layout.addWidget(self.lbl_status)

        # Set Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Slot functions for handling events
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Input Data File", "", "All Files (*);;CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        if file_path:
            self.txt_input.setText(file_path)

    def select_output_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", "")
        if dir_path:
            self.txt_output.setText(dir_path)

    def run_processing(self):
        # Retrieve the parameters selected by the user
        input_file = self.txt_input.text()
        output_dir = self.txt_output.text()
        save_census = self.chk_census.isChecked()
        save_csv = self.chk_csv.isChecked()
        save_powerbi = self.chk_powerbi.isChecked()

        # Validation Check
        if not input_file or not output_dir:
            self.lbl_status.setText("Error: Please select both an input file and output directory.")
            self.lbl_status.setStyleSheet("color: red;")
            return

        # Place your pandas or processing logic here!
        gooey_loader(input_file, output_dir)

        # Finished
        self.lbl_status.setText("Processing complete!")
        self.lbl_status.setStyleSheet("color: green;")
        
        # Example print to show captured states in the console
        print(f"Processing: {input_file} -> {output_dir}")
        print(f"Options chosen -> Census: {save_census}, CSV: {save_csv}, Power BI: {save_powerbi}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Modern clean styling layout helper
    app.setStyle('Fusion')
    
    window = DataProcessorApp()
    window.show()
    
    sys.exit(app.exec())
