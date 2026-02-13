import os
from PySide2.QtWidgets import QTextEdit
from PySide2.QtGui import QTextDocument
from PySide2.QtPrintSupport import QPrinter
from PySide2.QtCore import QSizeF

class PDFExporter:
    @staticmethod
    def export_monthly_report(data, file_path):
        """Generates a PDF report from the provided data."""
        doc = QTextDocument()
        
        # HTML Template with internal CSS
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: sans-serif; color: #333; }}
                h1 {{ color: #5288c1; text-align: center; margin-bottom: 5px; }}
                .subtitle {{ text-align: center; color: #666; margin-bottom: 20px; font-size: 16px; font-weight: bold; }}
                
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th {{ background-color: #f2f2f2; border: 1px solid #ddd; padding: 10px; text-align: left; font-weight: bold; }}
                td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; }}
                
                .summary-box {{ background-color: #f9f9f9; border: 1px solid #ddd; padding: 15px; text-align: center; }}
                .amount {{ font-size: 18px; font-weight: bold; display: block; margin-top: 5px; }}
                .income {{ color: #2e7d32; }}
                .expense {{ color: #c62828; }}
                
                h2 {{ border-bottom: 2px solid #5288c1; color: #5288c1; padding-bottom: 5px; margin-top: 30px; font-size: 18px; }}
                .text-right {{ text-align: right; }}
            </style>
        </head>
        <body>
            <h1>Budget App Report</h1>
            <div class="subtitle">Monthly Summary: {data['month']}</div>

            <table style="width: 100%; border: none;">
                <tr>
                    <td style="border: none; width: 25%;">
                        <div class="summary-box">
                            <b>Net Worth</b><br/>
                            <span class="amount">${data['summary']['net_worth']:,.2f}</span>
                        </div>
                    </td>
                    <td style="border: none; width: 25%;">
                        <div class="summary-box">
                            <b>Income</b><br/>
                            <span class="amount income">+${data['summary']['income']:,.2f}</span>
                        </div>
                    </td>
                    <td style="border: none; width: 25%;">
                        <div class="summary-box">
                            <b>Expenses</b><br/>
                            <span class="amount expense">-${data['summary']['expenses']:,.2f}</span>
                        </div>
                    </td>
                    <td style="border: none; width: 25%;">
                        <div class="summary-box">
                            <b>Net Income</b><br/>
                            <span class="amount {'income' if data['summary']['net_income'] >= 0 else 'expense'}">
                                {'+$' if data['summary']['net_income'] >= 0 else '-$'}{abs(data['summary']['net_income']):,.2f}
                            </span>
                        </div>
                    </td>
                </tr>
            </table>

            <h2>Category Breakdown</h2>
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th class="text-right">Amount</th>
                        <th class="text-right">Percentage</th>
                    </tr>
                </thead>
                <tbody>
        """

        total_expense = sum(data['categories'].values())
        for cat, amount in sorted(data['categories'].items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_expense * 100) if total_expense > 0 else 0
            html += f"""
                <tr>
                    <td>{cat}</td>
                    <td class="text-right">${amount:,.2f}</td>
                    <td class="text-right">{percentage:.1f}%</td>
                </tr>
            """
        
        if not data['categories']:
            html += "<tr><td colspan='3' style='text-align:center;'>No expense data found.</td></tr>"

        html += """
                </tbody>
            </table>

            <h2>Transaction Log</h2>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Category</th>
                        <th>Note</th>
                        <th class="text-right">Amount</th>
                    </tr>
                </thead>
                <tbody>
        """

        for t in data['transactions']:
            amount_str = f"+${t.amount:,.2f}" if t.type == "Income" else f"-${t.amount:,.2f}"
            amount_style = 'color: #2e7d32;' if t.type == "Income" else 'color: #c62828;'
            html += f"""
                <tr>
                    <td>{t.date}</td>
                    <td>{t.category}</td>
                    <td>{t.note}</td>
                    <td class="text-right" style="{amount_style} font-weight: bold;">{amount_str}</td>
                </tr>
            """

        if not data['transactions']:
            html += "<tr><td colspan='4' style='text-align:center;'>No transactions found.</td></tr>"

        html += """
                </tbody>
            </table>

            <div style="margin-top: 50px; text-align: center; color: #999; font-size: 12px;">
                Generated by Budget App
            </div>
        </body>
        </html>
        """
        
        # Debug: Save HTML for internal verification
        debug_html_path = file_path.replace(".pdf", ".debug.html")
        try:
            with open(debug_html_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"Debug HTML saved to {debug_html_path}")
        except Exception as e:
            print(f"Could not save debug HTML: {e}")

        doc.setHtml(html)
        
        # Setup Printer
        printer = QPrinter(QPrinter.ScreenResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_path)
        printer.setPageSize(QPrinter.A4)
        
        from PySide2.QtGui import QPainter
        painter = QPainter()
        if not painter.begin(printer):
            print("ERROR: Failed to begin painting on printer.")
            return False
            
        # Draw the document onto the printer
        doc.drawContents(painter)
        painter.end()
        
        print(f"PDF Exported successfully to {file_path}")
        return True
