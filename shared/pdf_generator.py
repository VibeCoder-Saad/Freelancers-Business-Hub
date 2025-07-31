# shared/pdf_generator.py

from fpdf import FPDF
import os

class PDF(FPDF):
    def __init__(self, company_name="Your Company", company_address="123 Business Rd", logo_path=None):
        super().__init__()
        self.company_name = company_name
        self.company_address = company_address
        self.logo_path = logo_path
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Logo
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        
        # Company Name
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, self.company_name, 0, 1, 'R')
        
        # Company Address
        self.set_font('Helvetica', '', 11)
        self.cell(0, 6, self.company_address, 0, 1, 'R')
        
        self.ln(20) # Line break

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Thank you for your business! - Page {self.page_no()}', 0, 0, 'C')

def create_invoice_pdf(invoice_data, line_items, client_data, company_details):
    """
    Generates a professional invoice PDF using dynamically provided company details.
    
    Args:
        invoice_data (dict): Contains invoice details like number, dates, total.
        line_items (list of dicts): Contains all line items for the invoice.
        client_data (dict): Contains the client's name and address.
        company_details (dict): Contains your company name, address, and logo path.
    """
    
    pdf = PDF(
        company_name=company_details.get('company_name', 'Your Company Name'),
        company_address=company_details.get('company_address', '123 Main St, Anytown'),
        logo_path=company_details.get('logo_path')
    )
    pdf.add_page()
    
    # --- Client & Invoice Details Section ---
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(100, 8, "BILL TO:", 0, 0, 'L')
    pdf.cell(0, 8, f"INVOICE #: {invoice_data['invoice_number']}", 0, 1, 'R')

    pdf.set_font('Helvetica', '', 11)
    pdf.cell(100, 6, client_data['name'], 0, 0, 'L')
    pdf.cell(0, 6, f"Issue Date: {invoice_data['issue_date']}", 0, 1, 'R')

    if client_data.get('address'):
        pdf.cell(100, 6, client_data['address'], 0, 0, 'L')
        
    pdf.cell(0, 6, f"Due Date: {invoice_data['due_date']}", 0, 1, 'R')
    
    # --- Line Items Table ---
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
        # Check if quantity is a float (like hours) for specific formatting
        qty_str = f"{item['quantity']:.2f}" if isinstance(item['quantity'], float) else str(item['quantity'])
        pdf.cell(100, 10, item['description'], 1, 0, 'L')
        pdf.cell(30, 10, qty_str, 1, 0, 'R')
        pdf.cell(30, 10, f"${item['rate']:.2f}", 1, 0, 'R')
        pdf.cell(30, 10, f"${item['amount']:.2f}", 1, 1, 'R')
        
    # --- Totals Section ---
    pdf.ln(10)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(130, 12, 'Total:', 0, 0, 'R')
    pdf.cell(60, 12, f"${invoice_data['total_amount']:.2f}", 1, 1, 'R')
    
    # --- Save the PDF ---
    output_dir = os.path.join(os.getcwd(), 'data', 'invoices')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a clean filename
    safe_client_name = "".join(c for c in client_data['name'] if c.isalnum() or c in (' ',)).rstrip()
    file_name = f"{invoice_data['invoice_number']}_{safe_client_name}.pdf".replace(' ', '_')
    pdf_path = os.path.join(output_dir, file_name)
    
    try:
        pdf.output(pdf_path)
        print(f"✅ Invoice PDF created at: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return None