import pdfplumber

# Path to your PDF file
pdf_path = "21301049PBR SBC Labels.pdf"

# Open the PDF file
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        # Extract text from the current page
        text = page.extract_text()
        print(f"--- Page {i+1} ---")
        print(text)

        # You can further process the `text` variable to extract specific information
