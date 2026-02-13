import uuid
from PySide2.QtWidgets import (QDialog, QMessageBox, QApplication, QPushButton, 
                               QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame,
                               QStackedWidget, QCalendarWidget, QTabBar)
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QPainter, QColor
from PySide2.QtCharts import QtCharts
from datetime import datetime
from add_account_dialog import AddAccountDialog
from add_transaction_dialog import AddTransactionDialog
from account_card import AccountCard
from stat_card import StatCard
from controllers import MainController
from theme_manager import ThemeManager

class TransactionCalendar(QCalendarWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.daily_summary = {} # { day: {has_income, has_expense} }
        self.currentPageChanged.connect(self.update_summary)
        self.update_summary(self.yearShown(), self.monthShown())

    def update_summary(self, year, month):
        month_str = f"{year}-{month:02d}"
        self.daily_summary = self.controller.get_daily_transaction_summary(month_str)
        self.update() # Trigger repaint

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        
        # Only draw markers for current month being shown
        if date.month() != self.monthShown():
            return

        summary = self.daily_summary.get(date.day())
        if summary is not None:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Marker positions (bottom of the cell)
            dot_size = 4
            space = 2
            start_x = rect.x() + (rect.width() - (dot_size * 2 + space)) / 2
            y = rect.y() + rect.height() - dot_size - 4
            
            # Draw Income Dot (Green)
            if summary.get("has_income"):
                painter.setBrush(QColor("#a6e3a1"))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(start_x, y, dot_size, dot_size))
            
            # Draw Expense Dot (Red)
            if summary.get("has_expense"):
                painter.setBrush(QColor("#f38ba8"))
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(QRectF(start_x + dot_size + space, y, dot_size, dot_size))
            
            painter.restore()

class HomeScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_mode = "grid" # grid or list

        # Initialize Controller
        self.controller = MainController()

        # Main Layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. Sidebar Setup
        self.setup_sidebar()
        main_layout.addWidget(self.sidebarContainer)

        # 2. Content Area Setup
        self.contentArea = QStackedWidget()
        main_layout.addWidget(self.contentArea)

        # 3. Dashboard View (Home)
        self.setup_dashboard_view()
        self.contentArea.addWidget(self.dashboardWidget)

        # 4. Transactions View
        self.setup_transactions_view()
        self.contentArea.addWidget(self.transWidget)

        # 5. Calendar View
        self.setup_calendar_view()
        self.contentArea.addWidget(self.calendarTab)

        # 6. Categories View
        self.setup_categories_view()
        self.contentArea.addWidget(self.categoriesTab)

        # Load Data
        self._load_accounts()
        
        # Resizing & Fullscreen Setup
        self.setMinimumSize(1100, 800)
        self.is_fullscreen = False

    def setup_sidebar(self):
        self.sidebarContainer = QFrame()
        self.sidebarContainer.setObjectName("Sidebar")
        self.sidebarContainer.setFixedWidth(250)
        self.sidebarContainer.setStyleSheet("#Sidebar { background-color: #181825; border-right: 1px solid #2f2f3e; }")
        
        layout = QVBoxLayout(self.sidebarContainer)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # App Title / Logo Area
        title_lbl = QLabel("Budget App")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setStyleSheet("font-size: 24px; font-weight: bold; color: #cdd6f4; padding: 20px 0;")
        layout.addWidget(title_lbl)

        # Navigation Buttons
        self.nav_btns = []
        self.add_nav_btn(layout, "Dashboard", lambda: self.switch_view(0))
        self.add_nav_btn(layout, "Transactions", lambda: self.switch_view(1))
        self.add_nav_btn(layout, "Categories", lambda: self.switch_view(3))
        self.add_nav_btn(layout, "Calendar", lambda: self.switch_view(2))

        layout.addStretch()

        # Theme Support
        self.theme_manager = ThemeManager(QApplication.instance())
        
        self.fullscreenBtn = QPushButton("Fullscreen (F11)")
        self.fullscreenBtn.setObjectName("NavButton")
        self.fullscreenBtn.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(self.fullscreenBtn)

        self.themeBtn = QPushButton("Switch Theme")
        self.themeBtn.setObjectName("NavButton")
        self.themeBtn.clicked.connect(self.theme_manager.toggle_theme)
        layout.addWidget(self.themeBtn)
        
        # Margin at bottom
        layout.addSpacing(20)

    def add_nav_btn(self, layout, text, callback):
        btn = QPushButton(text)
        btn.setObjectName("NavButton")
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        if not self.nav_btns: # First one is active
            btn.setChecked(True)
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        self.nav_btns.append(btn)

    def setup_dashboard_view(self):
        self.dashboardWidget = QWidget()
        layout = QVBoxLayout(self.dashboardWidget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header
        header = QLabel("Dashboard")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(header)

        # 1. Stats Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.netWorthCard = StatCard("Net Worth", 0.0)
        self.incomeCard = StatCard("Monthly Income", 0.0, color="#a6e3a1")
        self.expenseCard = StatCard("Monthly Expenses", 0.0, color="#f38ba8")
        
        stats_layout.addWidget(self.netWorthCard)
        stats_layout.addWidget(self.incomeCard)
        stats_layout.addWidget(self.expenseCard)
        stats_layout.addStretch()
        
        layout.addLayout(stats_layout)

        # 2. Accounts Section Header
        acc_header_layout = QHBoxLayout()
        acc_title = QLabel("Your Accounts")
        acc_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #cdd6f4; margin-top: 10px;")
        acc_header_layout.addWidget(acc_title)
        acc_header_layout.addStretch()
        
        self.addAccBtn = QPushButton("+ Add Account")
        self.addAccBtn.setObjectName("ActionBtn")
        self.addAccBtn.clicked.connect(self.open_add_account_dialog)
        acc_header_layout.addWidget(self.addAccBtn)
        
        layout.addLayout(acc_header_layout)

        # 3. Accounts List (Scroll Area)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        self.accScrollWidget = QWidget()
        self.accScrollWidget.setObjectName("AccountContainer")
        
        # Now permanently a List View (Vertical)
        self.accounts_layout = QVBoxLayout(self.accScrollWidget)
        self.accounts_layout.setAlignment(Qt.AlignTop)
        self.accounts_layout.setSpacing(10)
        
        scroll.setWidget(self.accScrollWidget)
        layout.addWidget(scroll)

    def _refresh_stats(self):
        """Refreshes the summary statistics at the top of the dashboard and charts."""
        summary = self.controller.get_monthly_summary()
        self.netWorthCard.updateValue(summary["net_worth"])
        self.incomeCard.updateValue(summary["income"])
        self.expenseCard.updateValue(summary["expenses"])

    def _refresh_charts(self):
        """Populates the category spending pie chart based on selected month tab."""
        if not hasattr(self, 'categoryMonthTabs'):
            month_str = datetime.now().strftime("%Y-%m")
        else:
            index = self.categoryMonthTabs.currentIndex()
            month_str = self.categoryMonthTabs.tabData(index) if index != -1 else datetime.now().strftime("%Y-%m")
        
        spending_data = self.controller.get_category_spending(month_str)
        
        series = QtCharts.QPieSeries()
        total_expense = sum(spending_data.values())
        
        if not spending_data:
            # Show empty state
            chart = QtCharts.QChart()
            chart.setTitle("No expense data for this month")
            chart.setTitleBrush(QColor("#a6adc8"))
            chart.setBackgroundBrush(Qt.NoBrush)
            self.pie_chart_view.setChart(chart)
            return

        # Color palette (Catppuccin inspired vibrant colors)
        colors = ["#89b4fa", "#a6e3a1", "#f9e2af", "#fab387", "#eba0ac", "#f5c2e7", "#cba6f7", "#94e2d5"]
        
        for i, (cat, amount) in enumerate(spending_data.items()):
            percentage = (amount / total_expense * 100) if total_expense > 0 else 0
            label = f"{cat}: ${amount:,.2f} ({percentage:.1f}%)"
            p_slice = series.append(label, amount)
            p_slice.setLabelVisible(True)
            p_slice.setBrush(QColor(colors[i % len(colors)]))
            p_slice.setLabelColor(QColor("#cdd6f4"))
            
        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitle("Monthly Category Spending")
        chart.setTitleBrush(QColor("#cdd6f4"))
        font = chart.titleFont()
        font.setPointSize(16)
        font.setBold(True)
        chart.setTitleFont(font)
        
        chart.setBackgroundBrush(Qt.NoBrush)
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)
        
        chart.legend().setAlignment(Qt.AlignRight)
        chart.legend().setLabelColor(QColor("#cdd6f4"))
        
        self.pie_chart_view.setChart(chart)

    def _load_accounts(self):
        """Loads accounts and refreshes stats."""
        # 1. Update Stats
        self._refresh_stats()

        # 2. Update Accounts List
        while self.accounts_layout.count():
            item = self.accounts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        accounts = self.controller.get_all_accounts()
        for acc in accounts:
            self._create_account_card(acc.id, acc.name, acc.balance)

    def _create_account_card(self, account_id, name, balance):
        card = AccountCard(account_id, name, balance)
        card.set_view_mode("list") # Always list view now
        card.editRequested.connect(self._edit_account)
        card.deleteRequested.connect(self._delete_account)
        self.accounts_layout.addWidget(card)

    def setup_transactions_view(self):
        self.transWidget = QWidget()
        layout = QVBoxLayout(self.transWidget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        # Header Row
        header_layout = QHBoxLayout()
        title = QLabel("Transactions")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.addTransBtn = QPushButton("+ Add Transaction")
        self.addTransBtn.setObjectName("ActionBtn")
        self.addTransBtn.clicked.connect(self.open_add_transaction_dialog)
        header_layout.addWidget(self.addTransBtn)
        layout.addLayout(header_layout)

        # 1. Month Tabs
        self.monthTabs = QTabBar()
        self.monthTabs.setExpanding(False)
        self.monthTabs.setDrawBase(False)
        self.monthTabs.currentChanged.connect(self._on_month_tab_changed)
        
        # Scroll area for tabs if they get too many
        tabs_scroll = QScrollArea()
        tabs_scroll.setObjectName("MonthTabsScroll")
        tabs_scroll.setFixedHeight(45)
        tabs_scroll.setWidgetResizable(True)
        tabs_scroll.setFrameShape(QFrame.NoFrame)
        tabs_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        tabs_scroll.setWidget(self.monthTabs)
        layout.addWidget(tabs_scroll)

        # 2. Monthly Summary Row
        summary_frame = QFrame()
        summary_frame.setObjectName("TransSummaryRow")
        summary_layout = QHBoxLayout(summary_frame)
        summary_layout.setContentsMargins(20, 10, 20, 10)
        
        self.monthIncomeLbl = QLabel("Income: $0.00")
        self.monthIncomeLbl.setStyleSheet("color: #a6e3a1; font-weight: bold; font-size: 16px;")
        self.monthExpenseLbl = QLabel("Expenses: $0.00")
        self.monthExpenseLbl.setStyleSheet("color: #f38ba8; font-weight: bold; font-size: 16px;")
        self.monthNetLbl = QLabel("Net Income: $0.00")
        self.monthNetLbl.setStyleSheet("color: white; font-weight: bold; font-size: 16px;")
        
        summary_layout.addWidget(self.monthIncomeLbl)
        summary_layout.addSpacing(40)
        summary_layout.addWidget(self.monthExpenseLbl)
        summary_layout.addSpacing(40)
        summary_layout.addWidget(self.monthNetLbl)
        summary_layout.addStretch()
        
        layout.addWidget(summary_frame)

        # 3. Transaction List (Scroll Area)
        self.transList = QScrollArea()
        self.transList.setObjectName("TransactionsScroll")
        self.transList.setWidgetResizable(True)
        self.transList.setFrameShape(QFrame.NoFrame)
        self.transListContent = QWidget()
        self.transListContent.setObjectName("TransactionsContainer")
        self.transListLayout = QVBoxLayout(self.transListContent)
        self.transListLayout.setAlignment(Qt.AlignTop)
        self.transListLayout.setSpacing(10)
        self.transList.setWidget(self.transListContent)
        
        layout.addWidget(self.transList)

    def setup_calendar_view(self):
        self.calendarTab = QWidget()
        layout = QHBoxLayout(self.calendarTab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Left Side: Custom Calendar
        left_layout = QVBoxLayout()
        title = QLabel("Calendar")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4; margin-bottom: 10px;")
        left_layout.addWidget(title)
        
        self.calendar = TransactionCalendar(self.controller)
        self.calendar.setObjectName("MainCalendar")
        self.calendar.selectionChanged.connect(self._on_calendar_date_changed)
        left_layout.addWidget(self.calendar)
        
        layout.addLayout(left_layout, stretch=2)

        # Right Side: Daily Breakdown
        right_panel = QFrame()
        right_panel.setObjectName("CalendarDailyBreakdown")
        right_panel.setFixedWidth(350)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        
        self.dailyTitle = QLabel("Daily Activity")
        self.dailyTitle.setStyleSheet("font-size: 18px; font-weight: bold; color: #89b4fa; margin-bottom: 15px;")
        right_layout.addWidget(self.dailyTitle)
        
        # Daily Transactions Scroll Area
        self.dayTransScroll = QScrollArea()
        self.dayTransScroll.setWidgetResizable(True)
        self.dayTransScroll.setFrameShape(QFrame.NoFrame)
        self.dayTransScroll.setObjectName("CalendarDayTransactionsScroll")
        
        self.dayTransContainer = QWidget()
        self.dayTransContainer.setObjectName("CalendarDayTransactionsContainer")
        self.dayTransLayout = QVBoxLayout(self.dayTransContainer)
        self.dayTransLayout.setAlignment(Qt.AlignTop)
        self.dayTransLayout.setSpacing(10)
        
        self.dayTransScroll.setWidget(self.dayTransContainer)
        right_layout.addWidget(self.dayTransScroll)
        
        layout.addWidget(right_panel, stretch=1)

    def setup_categories_view(self):
        self.categoriesTab = QWidget()
        layout = QVBoxLayout(self.categoriesTab)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        header = QLabel("Category Spending")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(header)

        # Month Tabs (Same style as Transactions)
        self.categoryMonthTabs = QTabBar()
        self.categoryMonthTabs.setExpanding(False)
        self.categoryMonthTabs.setDrawBase(False)
        self.categoryMonthTabs.currentChanged.connect(self._refresh_charts)
        
        tabs_scroll = QScrollArea()
        tabs_scroll.setObjectName("MonthTabsScroll")
        tabs_scroll.setFixedHeight(45)
        tabs_scroll.setWidgetResizable(True)
        tabs_scroll.setFrameShape(QFrame.NoFrame)
        
        tabs_scroll.setWidget(self.categoryMonthTabs)
        layout.addWidget(tabs_scroll)

        # Charts Section
        self.charts_container = QWidget()
        self.charts_layout = QHBoxLayout(self.charts_container)
        self.charts_layout.setContentsMargins(0, 0, 0, 0)
        
        self.pie_chart_view = QtCharts.QChartView()
        self.pie_chart_view.setRenderHint(QPainter.Antialiasing)
        self.pie_chart_view.setStyleSheet("background: transparent;")
        
        self.charts_layout.addWidget(self.pie_chart_view)
        layout.addWidget(self.charts_container)
        
        # Initial chart load
        self._populate_month_tabs(self.categoryMonthTabs)
        self._refresh_charts()

    def _on_calendar_date_changed(self):
        date = self.calendar.selectedDate()
        date_str = date.toString("yyyy-MM-dd")
        display_date = date.toString("MMMM d, yyyy")
        self.dailyTitle.setText(display_date)
        
        # Load transactions for this day
        # Clear existing
        while self.dayTransLayout.count():
            item = self.dayTransLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        transactions = self.controller.get_transactions_for_day(date_str)
        
        if not transactions:
            empty_lbl = QLabel("No transactions for this day.")
            empty_lbl.setStyleSheet("color: #a6adc8; font-style: italic;")
            self.dayTransLayout.addWidget(empty_lbl)
            return

        for t in transactions:
            row = QFrame()
            row.setObjectName("CalendarTransactionRow")
            r_layout = QVBoxLayout(row)
            r_layout.setContentsMargins(15, 12, 15, 12)
            
            top_row = QHBoxLayout()
            cat_lbl = QLabel(t.category)
            cat_lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #cdd6f4;")
            
            amount_str = f"+${t.amount:,.2f}" if t.type == "Income" else f"-${t.amount:,.2f}"
            color = "#a6e3a1" if t.type == "Income" else "#f38ba8"
            amount_lbl = QLabel(amount_str)
            amount_lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
            
            top_row.addWidget(cat_lbl)
            top_row.addStretch()
            top_row.addWidget(amount_lbl)
            
            r_layout.addLayout(top_row)
            
            if t.note:
                note_lbl = QLabel(t.note)
                note_lbl.setWordWrap(True)
                note_lbl.setStyleSheet("color: #a6adc8; font-size: 12px;")
                r_layout.addWidget(note_lbl)
            
            self.dayTransLayout.addWidget(row)

    def switch_view(self, index):
        self.contentArea.setCurrentIndex(index)
        if index == 1: # Transactions
            self._populate_month_tabs(self.monthTabs)
            self._on_month_tab_changed()
        elif index == 2: # Calendar
            self.calendar.update_summary(self.calendar.yearShown(), self.calendar.monthShown()) # Refresh markers
            self._on_calendar_date_changed() # Load transactions for selected day
        elif index == 3: # Categories
            self._populate_month_tabs(self.categoryMonthTabs)
            self._refresh_charts()
        
        # Update Nav State
        for i, btn in enumerate(self.nav_btns):
            btn.setChecked(i == index)

    def _populate_month_tabs(self, tab_bar):
        """Calculates and populates the given tab bar with month options."""
        tab_bar.blockSignals(True)
        # QTabBar does not have clear(), must remove individually
        while tab_bar.count() > 0:
            tab_bar.removeTab(0)
        
        first_date, now = self.controller.get_transaction_date_range()
        
        # Start from the first of the first month
        curr_year = first_date.year
        curr_month = first_date.month
        
        # End 10 months from now
        target_months = (now.year * 12 + now.month) + 10
        
        while (curr_year * 12 + curr_month) <= target_months:
            m_date = datetime(curr_year, curr_month, 1)
            tab_text = m_date.strftime("%b %Y")
            tab_data = m_date.strftime("%Y-%m")
            tab_bar.addTab(tab_text)
            tab_bar.setTabData(tab_bar.count()-1, tab_data)
            
            curr_month += 1
            if curr_month > 12:
                curr_month = 1
                curr_year += 1
        
        # Select current month by default
        current_str = now.strftime("%Y-%m")
        for i in range(tab_bar.count()):
            if tab_bar.tabData(i) == current_str:
                tab_bar.setCurrentIndex(i)
                break
        
        tab_bar.blockSignals(False)

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts."""
        if event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        else:
            super().keyPressEvent(event)

    def toggle_fullscreen(self):
        """Toggles between fullscreen and normal windowed mode for the main window."""
        main_win = self.window()
        if main_win.isFullScreen():
            main_win.showNormal()
            self.is_fullscreen = False
            self.fullscreenBtn.setText("Fullscreen (F11)")
        else:
            main_win.showFullScreen()
            self.is_fullscreen = True
            self.fullscreenBtn.setText("Exit Fullscreen (F11)")

    def _on_month_tab_changed(self):
        index = self.monthTabs.currentIndex()
        if index == -1: return
        month_str = self.monthTabs.tabData(index)
        self._load_transactions(month_str)
        self._refresh_monthly_summary(month_str)

    def _refresh_monthly_summary(self, month_str):
        summary = self.controller.get_monthly_summary(month_str)
        self.monthIncomeLbl.setText(f"Income: ${summary['income']:,.2f}")
        self.monthExpenseLbl.setText(f"Expenses: ${summary['expenses']:,.2f}")
        self.monthNetLbl.setText(f"Net Income: ${summary['net_income']:,.2f}")
        
        color = "#a6e3a1" if summary['net_income'] >= 0 else "#f38ba8"
        self.monthNetLbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")

    def _load_transactions(self, month_str=None):
        # Clear existing
        while self.transListLayout.count():
            item = self.transListLayout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        transactions = self.controller.get_transactions(month_str=month_str)
        
        for t in transactions:
            row = QFrame()
            row.setObjectName("TransactionRow")
            row.setCursor(Qt.PointingHandCursor)
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(15, 10, 15, 10)
            
            # Date
            date_lbl = QLabel(t.date)
            date_lbl.setFixedWidth(100)
            
            # Category & Note
            details_layout = QVBoxLayout()
            cat_lbl = QLabel(t.category)
            cat_lbl.setStyleSheet("font-weight: bold; font-size: 14px;")
            note_lbl = QLabel(t.note)
            note_lbl.setStyleSheet("color: #a6adc8; font-size: 12px;")
            details_layout.addWidget(cat_lbl)
            details_layout.addWidget(note_lbl)
            
            # Amount
            amount_str = f"+${t.amount:,.2f}" if t.type == "Income" else f"-${t.amount:,.2f}"
            color = "#a6e3a1" if t.type == "Income" else "#f38ba8" 
            amount_lbl = QLabel(amount_str)
            amount_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            amount_lbl.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 16px;")
            
            row_layout.addWidget(date_lbl)
            row_layout.addLayout(details_layout)
            row_layout.addStretch()
            row_layout.addWidget(amount_lbl)
            
            # Connect row click to edit
            row.mousePressEvent = lambda e, tid=t.id: self._edit_transaction(tid)
            
            self.transListLayout.addWidget(row)

    def _edit_transaction(self, transaction_id):
        # Find transaction data
        all_t = self.controller.get_transactions()
        t = next((item for item in all_t if item.id == transaction_id), None)
        if not t: return

        # Open Dialog
        accounts = self.controller.get_all_accounts()
        categories = self.controller.get_unique_categories()
        
        initial_data = {
            "account_id": t.account_id,
            "date": t.date,
            "amount": t.amount,
            "type": t.type,
            "category": t.category,
            "note": t.note
        }
        
        dlg = AddTransactionDialog(self, accounts=accounts, categories=categories, initial_data=initial_data)
        if dlg.exec_():
            updated_data = dlg.get_result()
            if updated_data and self.controller.update_transaction(transaction_id, updated_data):
                self._on_month_tab_changed()
                self._refresh_stats() # Update Net Worth on dashboard too
                QMessageBox.information(self, "Success", "Transaction updated!")



    # REMOVED OLD METHODS TO AVOID CONFLICTS
    # show_home_view, show_transactions_view, existing __init__ logic...








    def open_add_account_dialog(self):
        dlg = AddAccountDialog(self)
        if dlg.exec_():
            result = dlg.get_result()
            if result:
                name, balance = result
                self._add_account(name, balance)

    def _add_account(self, name: str, balance: float):
        # Use controller to add to DB
        new_acc = self.controller.add_account(name, balance)
        if new_acc:
            self._create_account_card(new_acc.id, new_acc.name, new_acc.balance)
            self._refresh_stats()

    def _edit_account(self, account_id: str):
        
        all_accs = self.controller.get_all_accounts()
        acc = next((a for a in all_accs if a.id == account_id), None)
        
        if not acc:
            return

        dlg = AddAccountDialog(self, initial_name=acc.name, initial_amount=acc.balance)
        if dlg.exec_():
            name, balance = dlg.get_result()
            if self.controller.update_account(account_id, name, balance):
                # Update UI
                for i in range(self.accounts_layout.count()):
                    item = self.accounts_layout.itemAt(i)
                    if not item: continue
                    widget = item.widget()
                    if isinstance(widget, AccountCard) and widget.account_id == account_id:
                        widget.updateData(name, balance)
                        self._refresh_stats()
                        break

    def open_add_transaction_dialog(self):
        # Pass all accounts to the dialog
        accounts = self.controller.get_all_accounts()
        if not accounts:
            QMessageBox.warning(self, "No Accounts", "Please add an account first.")
            return

        # Fetch Categories
        categories = self.controller.get_unique_categories()

        dlg = AddTransactionDialog(self, accounts=accounts, categories=categories)
        if dlg.exec_():
            data = dlg.get_result()
            if data:
                if self.controller.add_transaction(
                    data["account_id"], 
                    data["date"], 
                    data["amount"], 
                    data["category"], 
                    data["type"], 
                    data["note"]
                ):
                    # Refresh viewing
                    self._load_accounts()
                    self._load_transactions()
                    QMessageBox.information(self, "Success", "Transaction added successfully!")
                else:
                    QMessageBox.critical(self, "Error", "Failed to add transaction.")

    def _delete_account(self, account_id: str):
        confirm = QMessageBox.question(
            self, "Delete account",
            "Are you sure you want to delete this account?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        if self.controller.delete_account(account_id):
            # Remove from UI
            for i in range(self.accounts_layout.count()):
                item = self.accounts_layout.itemAt(i)
                if not item: continue
                widget = item.widget()
                if isinstance(widget, AccountCard) and widget.account_id == account_id:
                    self.accounts_layout.removeWidget(widget)
                    widget.setParent(None)
                    widget.deleteLater()
                    self._refresh_stats()
                    break




