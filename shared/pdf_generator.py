# shared/pdf_generator.py

import os
from fpdf import FPDF

class InvoicePDF(FPDF):
    """A custom PDF class to define a consistent header and footer for all invoices."""
    def __init__(self, company_details, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_name = company_details.get('company_name', 'Your Company Name')
        self.company_address = company_details.get('company_address', '123 Main St, Anytown')
        self.logo_path = company_details.get('logo_path')
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Logo: Check if path is valid before trying to render
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                self.image(self.logo_path, 10, 8, 33)
            except Exception as e:
                print(f"Warning: Could not load logo image. Error: {e}")
        
        # Company Details
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, self.company_name, 0, 1, 'R')
        self.set_font('Helvetica', '', 11)
        self.cell(0, 6, self.company_address, 0, 1, 'R')
        
        # Line break
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Thank you for your business! - Page {self.page_no()}', 0, 0, 'C')

def create_invoice_pdf(invoice_data, line_items, client_data, company_details):
    """
    Generates a professional invoice PDF using dynamically provided details.
    
    This is the primary function to be called from other parts of the application.
    """
    
    # 1. Initialize our custom PDF class with company details
    pdf = InvoicePDF(company_details)
    pdf.add_page()
    
    # 2. Client & Invoice Info Section
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(100, 8, "BILL TO:", 0, 0, 'L')
    pdf.cell(0, 8, f"INVOICE #: {invoice_data.get('invoice_number', 'N/A')}", 0, 1, 'R')

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(100, 6, client_data.get('name', 'N/A'), 0, 0, 'L')
    pdf.cell(0, 6, f"Issue Date: {invoice_data.get('issue_date', 'N/A')}", 0, 1, 'R')
    if client_data.get('address'):
        pdf.cell(100, 6, client_data.get('address', ''), 0, 0, 'L')
    pdf.cell(0, 6, f"Due Date: {invoice_data.get('due_date', 'N/A')}", 0, 1, 'R')
    
    # 3. Line Items Table
    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(224, 224, 224) # A light grey for the header
    pdf.set_text_color(0) # Black text for the header
    
    pdf.cell(100, 10, 'DESCRIPTION', 1, 0, 'L', 1)
    pdf.cell(30, 10, 'QUANTITY', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'RATE', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'AMOUNT', 1, 1, 'C', 1)

    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0)
    
    for item in line_items:
        # Improved, more flexible quantity formatting
        qty_str = f"{item['quantity']:.2f}" if isinstance(item['quantity'], float) else str(int(item['quantity']))
        
        pdf.cell(100, 10, item['description'], 1, 0, 'L')
        pdf.cell(30, 10, qty_str, 1, 0, 'R')
        pdf.cell(30, 10, f"${item.get('rate', 0):.2f}", 1, 0, 'R')
        pdf.cell(30, 10, f"${item.get('amount', 0):.2f}", 1, 1, 'R')
        
    # 4. Totals Section
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(130, 12, 'TOTAL:', 0, 0, 'R')
    pdf.cell(60, 12, f"${invoice_data.get('total_amount', 0.0):.2f}", 1, 1, 'R')
    
    # 5. Save the PDF file
    output_dir = os.path.join(os.getcwd(), 'data', 'invoices')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a clean filename to prevent errors
    safe_client_name = "".join(c for c in client_data.get('name', '') if c.isalnum() or c in (' ',)).rstrip()
    file_name = f"{invoice_data.get('invoice_number', 'INV-000')}_{safe_client_name}.pdf".replace(' ', '_')
    pdf_path = os.path.join(output_dir, file_name)
    
    try:
        pdf.output(pdf_path)
        print(f"✅ Invoice PDF created at: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"❌ Error while saving PDF: {e}")
        return None