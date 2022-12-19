import subprocess
import os
from PyQt5 import QtWidgets, QtGui

class DebloatWindow(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()

    # Set up the user interface
    self.setupUi()

  def setupUi(self):
    # Create a widget to hold the checkboxes
    self.checkbox_widget = QtWidgets.QWidget(self)
    self.checkbox_layout = QtWidgets.QVBoxLayout(self.checkbox_widget)

    # Create a list of checkboxes for the user to select the applications to uninstall
    self.app_checkboxes = []
    for app in self.getInstalledApps():
        checkbox = QtWidgets.QCheckBox(app, self.checkbox_widget)
        self.app_checkboxes.append(checkbox)
        self.checkbox_layout.addWidget(checkbox)

    # Create a scroll area to hold the checkboxes
    self.scroll_area = QtWidgets.QScrollArea(self)
    self.scroll_area.setWidget(self.checkbox_widget)
    self.scroll_area.setWidgetResizable(True)

    # Create a button to trigger the debloat process
    self.debloat_button = QtWidgets.QPushButton("Debloat", self)
    self.debloat_button.clicked.connect(self.debloat)

    # Create a layout to hold the scroll area and button
    layout = QtWidgets.QVBoxLayout(self)
    layout.addWidget(self.scroll_area)
    layout.addWidget(self.debloat_button)

    # Set the window properties
    self.setWindowTitle("Debloat Windows 11")
    self.setGeometry(500, 500, 300, 300)


  def debloat(self):
    # Elevate privileges to run as an administrator
    os.setuid(0)

    # Iterate through the list of checkboxes and uninstall the selected applications using the wmic command
    for checkbox in self.app_checkboxes:
      if checkbox.isChecked():
        app = checkbox.text()
        subprocess.run(["wmic", "product", "where", f"name='{app}'", "call", "uninstall"])

    # Print a message to confirm that the applications have been uninstalled
    print("Selected applications have been uninstalled.")

  def getInstalledApps(self):
    # Use the wmic command to get the list of installed applications
    installed_apps = subprocess.run(["wmic", "product", "get", "name"], capture_output=True).stdout.decode("utf-8").split("\n")[1:-1]
    return installed_apps

if __name__ == "__main__":
  app = QtWidgets.QApplication([])
  window = DebloatWindow()
  window.show()
  app.exec_()
