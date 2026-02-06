import sys
from PySide2.QtWidgets import(QApplication,QMainWindow,QDialog,QStackedWidget,QLabel)
from PySide2.QtCore import Qt, Signal
from ui.ui_main import Ui_MainWindow
from home import HomeScreen
from theme_manager import ThemeManager

class Login(QMainWindow):
    def __init__(self,stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.loginbutton.clicked.connect(self.loginfunction)
        self.ui.guest.clicked.connect(self.goToHome)

    def goToHome(self):
        home = HomeScreen()
        self.stacked_widget.addWidget(home)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()+1)


    def loginfunction(self):
        userName = self.ui.userNameInput.text()
        password = self.ui.passwordInput.text()
        print("Successfully logged in with username : ",userName," and password", password)
        self.goToHome()


class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self,parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
    
    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self.clicked.emit()
        super.mouseReleaseEvent(ev)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Initialize Theme
    theme_manager = ThemeManager(app)
    theme_manager.load_theme("dark") # Set default to dark

    stack = QStackedWidget()
    login = Login(stacked_widget=stack) 
    stack.addWidget(login)
    stack.setFixedSize(1000,600)
    stack.show()
    sys.exit(app.exec_())
    
    
