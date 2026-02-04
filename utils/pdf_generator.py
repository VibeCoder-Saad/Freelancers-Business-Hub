from fpdf import FPDF
import os

class InvoicePDF(FPDF):
    def header(self):
        # Logo (if exists) or Title
        self.set_font('helvetica', 'B', 20)
        self.cell(0, 10, 'INVOICE', align='R', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def generate(self, invoice_data, output_path):
        self.add_page()
        self.set_font('helvetica', '', 12)
        
        # Billed To
        self.set_font('helvetica', 'B', 12)
        self.cell(0, 10, 'Billed To:', new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', '', 12)
        self.cell(0, 10, f"Client: {invoice_data.get('client_name', 'Unknown')}", new_x="LMARGIN", new_y="NEXT")
        self.ln(5)
        
        # Invoice Details
        self.cell(0, 10, f"Invoice #: {invoice_data.get('number', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 10, f"Date: {invoice_data.get('date', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 10, f"Due Date: {invoice_data.get('due_date', 'N/A')}", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)
        
        # Table Header
        self.set_fill_color(200, 220, 255)
        self.set_font('helvetica', 'B', 12)
        self.cell(100, 10, 'Description', border=1, fill=True)
        self.cell(30, 10, 'Hours', border=1, fill=True, align='C')
        self.cell(30, 10, 'Rate', border=1, fill=True, align='R')
        self.cell(30, 10, 'Total', border=1, fill=True, align='R', new_x="LMARGIN", new_y="NEXT")
        
        # Table Body
        self.set_font('helvetica', '', 12)
        total = 0.0
        
        items = invoice_data.get('items', [])
        # If no explicit items, maybe we have a summary? 
        # For this MVP, let's assume 'items' list with desc, hours, rate, amount
        
        if not items:
            # Fallback if just a total amount is known
             self.cell(100, 10, "Service Rendered", border=1)
             self.cell(30, 10, "-", border=1, align='C')
             self.cell(30, 10, "-", border=1, align='R')
             amount = float(invoice_data.get('amount', 0))
             self.cell(30, 10, f"${amount:.2f}", border=1, align='R', new_x="LMARGIN", new_y="NEXT")
             total = amount
        else:
            for item in items:
                desc = item.get('description', 'Service')
                hours = float(item.get('hours', 0))
                rate = float(item.get('rate', 0))
                amount = hours * rate
                total += amount
                
                self.cell(100, 10, desc, border=1)
                self.cell(30, 10, f"{hours:.1f}", border=1, align='C')
                self.cell(30, 10, f"${rate:.2f}", border=1, align='R')
                self.cell(30, 10, f"${amount:.2f}", border=1, align='R', new_x="LMARGIN", new_y="NEXT")
        
        self.ln(5)
        
        # Total
        self.set_font('helvetica', 'B', 14)
        self.cell(160, 10, 'Total Amount:', align='R')
        self.cell(30, 10, f"${total:.2f}", border=1, align='R', new_x="LMARGIN", new_y="NEXT")
        
        self.output(output_path)
