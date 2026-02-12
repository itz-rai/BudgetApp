import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from account_card import AccountCard
from controllers import MainController
import unittest

# Mock DB for controller test (or just check attribute existence)
class TestFixes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)

    def test_controller_has_delete_method(self):
        controller = MainController()
        # attributes are often added in init or are methods of class
        self.assertTrue(hasattr(controller, 'delete_account'), "MainController missing delete_account method")

    def test_account_card_sizing(self):
        card = AccountCard("test_id", "Test Account", 1000.0)
        
        # Test Grid Mode (Default)
        card.set_view_mode("grid")
        min_w = card.minimumWidth()
        max_w = card.maximumWidth()
        min_h = card.minimumHeight()
        max_h = card.maximumHeight()
        
        # Fixed size 220x120 implies min=max=220 and min=max=120
        self.assertEqual(min_w, 220)
        self.assertEqual(max_w, 220)
        self.assertEqual(min_h, 120)
        self.assertEqual(max_h, 120)

        # Test List Mode
        card.set_view_mode("list")
        min_w = card.minimumWidth()
        max_w = card.maximumWidth()
        
        self.assertEqual(min_w, 0)
        self.assertGreater(max_w, 220) # Should be expanding
        
        min_h = card.minimumHeight()
        max_h = card.maximumHeight()
        self.assertEqual(min_h, 60)
        self.assertEqual(max_h, 80)

if __name__ == '__main__':
    unittest.main()
