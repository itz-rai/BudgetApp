import sys
from PySide2.QtWidgets import QApplication, QStackedWidget, QFrame
from home import HomeScreen
from theme_manager import ThemeManager

def test_redesign():
    # 1. Initialize App
    print("Initializing App...")
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 2. Initialize Controller & Home
    print("Loading HomeScreen...")
    try:
        home = HomeScreen()
    except Exception as e:
        print(f"FAILED to instantiate HomeScreen: {e}")
        raise e

    # 3. Verify Layout Structure
    print("Verifying Layout...")
    
    # Check Sidebar
    sidebar = getattr(home, "sidebarContainer", None)
    assert sidebar is not None, "Sidebar container not found"
    assert isinstance(sidebar, QFrame)
    print("Sidebar found.")

    # Check Content Area
    content = getattr(home, "contentArea", None)
    assert content is not None, "Content Area not found"
    assert isinstance(content, QStackedWidget)
    print("Content Area found.")
    
    # Check Views
    assert content.count() >= 2, f"Expected at least 2 views, got {content.count()}"
    print("Views setup correctly.")

    print("UI Redesign Instantiation Successful!")

if __name__ == "__main__":
    try:
        test_redesign()
    except Exception as e:
        print(f"Test Failed: {e}")
        sys.exit(1)
