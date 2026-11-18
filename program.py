import sys
from PySide6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
	QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QCheckBox, QFileDialog, QComboBox,
)
from PySide6.QtCore import Qt, QRunnable, QThreadPool, Slot, Signal, QObject
import pandas as pd
from pipeline import gooey_loader

US_STATES = {
	"Alabama": "AL",
	"Alaska": "AK",
	"Arizona": "AZ",
	"Arkansas": "AR",
	"California": "CA",
	"Colorado": "CO",
	"Connecticut": "CT",
	"Delaware": "DE",
	"Florida": "FL",
	"Georgia": "GA",
	"Hawaii": "HI",
	"Idaho": "ID",
	"Illinois": "IL",
	"Indiana": "IN",
	"Iowa": "IA",
	"Kansas": "KS",
	"Kentucky": "KY",
	"Louisiana": "LA",
	"Maine": "ME",
	"Maryland": "MD",
	"Massachusetts": "MA",
	"Michigan": "MI",
	"Minnesota": "MN",
	"Mississippi": "MS",
	"Missouri": "MO",
	"Montana": "MT",
	"Nebraska": "NE",
	"Nevada": "NV",
	"New Hampshire": "NH",
	"New Jersey": "NJ",
	"New Mexico": "NM",
	"New York": "NY",
	"North Carolina": "NC",
	"North Dakota": "ND",
	"Ohio": "OH",
	"Oklahoma": "OK",
	"Oregon": "OR",
	"Pennsylvania": "PA",
	"Rhode Island": "RI",
	"South Carolina": "SC",
	"South Dakota": "SD",
	"Tennessee": "TN",
	"Texas": "TX",
	"Utah": "UT",
	"Vermont": "VT",
	"Virginia": "VA",
	"Washington": "WA",
	"West Virginia": "WV",
	"Wisconsin": "WI",
	"Wyoming": "WY",
	"Washington D.C.": "DC",
	"Puerto Rico": "PR",
}

class WorkerSignals(QObject):
	finished = Signal()
	progress = Signal(str)

class GooeyWorker(QRunnable):
	def __init__(self, input_file, output_dir, region):
		super().__init__()
		self.input_file = input_file
		self.output_dir = output_dir
		self.region = region
		self.signals = WorkerSignals()

	@Slot()
	def run(self):
		gooey_loader(self.input_file, self.output_dir, self.region)
		self.signals.finished.emit()

class DataProcessorApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.threadpool = QThreadPool() # for processing later

		self.setWindowTitle("Contractor Data Template Creation")
		self.setMinimumSize(500, 350)

		# Main Layout Container
		main_layout = QVBoxLayout()
		main_layout.setSpacing(15)

		###
		# File & Directory Selection
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

		###
		# Export options & demographic selection
		options_group = QGroupBox("Export Configuration")

		horizontal_layout = QHBoxLayout() # Holds both layouts
		chk_layout = QVBoxLayout()
		chk_layout.setSpacing(8)

		demo_layout = QVBoxLayout()
		demo_layout.setSpacing(0)

		self.chk_census = QCheckBox("Save Census Data")
		self.chk_powerbi = QCheckBox("Save Data for Power BI")

		self.combo_label = QLabel("US Census Demographic Region")
		self.combo = QComboBox()
		self.combo.addItem("United States")
		self.combo.addItems(list(US_STATES.keys()))
		self.combo.setCurrentText("United States")

		# Set default states if desired
		#self.chk_census.setChecked(True)
		self.chk_powerbi.setChecked(True)

		chk_layout.addWidget(self.chk_census)
		chk_layout.addWidget(self.chk_powerbi)

		demo_layout.addWidget(self.combo_label, alignment=Qt.AlignmentFlag.AlignVCenter)
		demo_layout.addWidget(self.combo, alignment=Qt.AlignmentFlag.AlignVCenter)
		demo_layout.addStretch()

		horizontal_layout.addLayout(demo_layout)
		horizontal_layout.addLayout(chk_layout)

		options_group.setLayout(horizontal_layout)
		main_layout.addWidget(options_group)

		# For dropdown box demographic changes
		def set_region(region):
			if region != "United States":
				self.region = US_STATES[region] # set to shorthand code
			else:
				self.region = "USA"
			print(region)

		self.region = "USA"
		self.combo.currentTextChanged.connect(
			lambda text: set_region(text)
		)

		###
		# Button processing
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

	def run_gooey_process(self, input_file, output_dir):
		self.lbl_status.setText(f"Processing {input_file}...")
		worker = GooeyWorker(input_file, output_dir, self.region)
		self.btn_process.setEnabled(False)
		worker.signals.finished.connect(lambda: self.btn_process.setEnabled(True))
		worker.signals.finished.connect(lambda: self.lbl_status.setText(f"Processing complete, files saved to {output_dir}"))
		worker.signals.finished.connect(lambda: self.lbl_status.setStyleSheet("color: green;"))
		
		self.threadpool.start(worker)

	@Slot(str)

	def run_processing(self):
		# Retrieve the parameters selected by the user
		input_file = self.txt_input.text()
		output_dir = self.txt_output.text()
		save_census = self.chk_census.isChecked()
		save_powerbi = self.chk_powerbi.isChecked()

		# Validation Check
		if not input_file or not output_dir:
			self.lbl_status.setText("Error: Please select both an input file and output directory.")
			self.lbl_status.setStyleSheet("color: red;")
			return

		# Gooey loading
		self.run_gooey_process(input_file, output_dir)
		
		# Example print to show captured states in the console
		print(f"Processing: {input_file} -> {output_dir}")
		print(f"Options chosen -> Census: {save_census}, Power BI: {save_powerbi}")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	
	# Modern clean styling layout helper
	app.setStyle('Fusion')
	
	window = DataProcessorApp()
	window.show()
	
	sys.exit(app.exec())
