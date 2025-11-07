"""The module defines the ContactList class.

This window allows users to add and remove contacts using a simple table.
"""

__author__ = "ACE Faculty"
__version__ = "1.0.0"
__credits__ = ""

from PySide6.QtWidgets import (
    QMainWindow, QLineEdit, QPushButton, QTableWidget, QLabel,
    QVBoxLayout, QWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Slot


class ContactList(QMainWindow):
    """Represents a window that provides the UI to manage contacts."""

    def __init__(self):
        """Initializes a new instance of the ContactList class."""
        super().__init__()
        self.__initialize_widgets()

        # Step 1: connect Add button (signal) to private slot (handler).
        self.add_button.clicked.connect(self.__on_add_contact)

        # Step 2: connect Remove button (signal) to private slot (handler).
        self.remove_button.clicked.connect(self.__on_remove_contact)

    def __initialize_widgets(self):
        """Initializes the widgets on this Window.

        DO NOT EDIT (given design).
        """
        self.setWindowTitle("Contact List")

        # Inputs
        self.contact_name_input = QLineEdit(self)
        self.contact_name_input.setPlaceholderText("Contact Name")

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone Number")

        # Buttons
        self.add_button = QPushButton("Add Contact", self)
        self.remove_button = QPushButton("Remove Contact", self)

        # Table
        self.contact_table = QTableWidget(self)
        self.contact_table.setColumnCount(2)
        self.contact_table.setHorizontalHeaderLabels(["Name", "Phone"])

        # Status label
        self.status_label = QLabel(self)

        # Layout (matches the screenshot order)
        layout = QVBoxLayout()
        layout.addWidget(self.contact_name_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.contact_table)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # -----------------------------
    # Step 1: Add Contact
    # -----------------------------
    @Slot()
    def __on_add_contact(self):
        """
        Adds a contact to the table if both inputs contain text.
        Otherwise, displays the required message in the status label.

        Messages:
            - Success: "Added contact: {name}"
            - Missing input: "Please enter a contact name and phone number."
        """
        name = self.contact_name_input.text().strip()
        phone = self.phone_input.text().strip()

        if name and phone:
            row = self.contact_table.rowCount()
            self.contact_table.insertRow(row)
            self.contact_table.setItem(row, 0, QTableWidgetItem(name))
            self.contact_table.setItem(row, 1, QTableWidgetItem(phone))
            self.status_label.setText(f"Added contact: {name}")
        else:
            self.status_label.setText("Please enter a contact name and phone number.")

    # -----------------------------
    # Step 2: Remove Contact
    # -----------------------------
    @Slot()
    def __on_remove_contact(self):
        """
        Removes the currently selected contact (after confirmation).
        If nothing is selected, shows a guidance message.

        Messages:
            - No selection: "Please select a contact to remove."
            - Confirm dialog: "Remove contact: {name}?"
            - Success: "Removed contact: {name}"
            - Canceled: "Removal canceled."
        """
        row = self.contact_table.currentRow()

        if row < 0:
            self.status_label.setText("Please select a contact to remove.")
            return

        name_item = self.contact_table.item(row, 0)
        name = name_item.text() if name_item is not None else "selected contact"

        reply = QMessageBox.question(
            self,
            "Confirm Remove",
            f"Remove contact: {name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.contact_table.removeRow(row)
            self.status_label.setText(f"Removed contact: {name}")
        else:
            self.status_label.setText("Removal canceled.")
