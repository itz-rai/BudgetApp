import os
from PySide2.QtWidgets import QApplication

class ThemeManager:
    def __init__(self, app: QApplication):
        self.app = app
        self.current_theme = "dark" # Default

    def load_theme(self, theme_name: str):
        """Loads the .qss file for the given theme name."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        theme_path = os.path.join(base_dir, "themes", f"{theme_name}.qss")
        
        if os.path.exists(theme_path):
            with open(theme_path, "r") as f:
                style_sheet = f.read()
                self.app.setStyleSheet(style_sheet)
                self.current_theme = theme_name
        else:
            print(f"Theme file not found: {theme_path}")

    def toggle_theme(self):
        """Switches between light and dark themes."""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.load_theme(new_theme)
