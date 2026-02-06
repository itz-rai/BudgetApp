import sys
import os
from PySide2.QtWidgets import QApplication
from theme_manager import ThemeManager

def test_themes():
    app = QApplication.instance() or QApplication(sys.argv)
    
    manager = ThemeManager(app)
    
    # Check default
    assert manager.current_theme == "dark"
    print("Default theme is dark.")

    # Check file checks
    dark_path = os.path.join("themes", "dark.qss")
    light_path = os.path.join("themes", "light.qss")
    
    assert os.path.exists(dark_path), "Dark theme file missing"
    assert os.path.exists(light_path), "Light theme file missing"
    print("Theme files exist.")

    # Test toggling
    manager.toggle_theme()
    assert manager.current_theme == "light", f"Expected light, got {manager.current_theme}"
    try:
        manager.toggle_theme()
    except Exception as e:
        print(f"Error toggling theme: {e}")
        
    assert manager.current_theme == "dark", f"Expected dark, got {manager.current_theme}"
    print("Theme toggling logic verified.")
    print("Phase 2 Test Successful!")

if __name__ == "__main__":
    try:
        test_themes()
    except Exception as e:
        print(f"Test Failed: {e}")
