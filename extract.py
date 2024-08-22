import pdfplumber
import re
import requests

# Path to your PDF file
pdf_path = "2911576WEM SBC Labels.pdf"

# Example regex for tracking numbers (you may need to adjust this)
# tracking_number_pattern = r"\b\d{12}\b"
sscc_pattern = r"SSCC:.*?\n(.*)"
vendor_number_pattern = r"VENDOR#: (\d+)"
sku_pattern = r"SKU: (\d+)"
description_pattern = r"DES: (.*)"
case_qty_pattern = r"CASE QTY: (\d+)"
po_number_pattern = r"PO#: (\w+)"
case_number_pattern = r"CASE:(\d+) OF (\d+)"
po_number = None
total_cases = None
vendor_number = None

cases = []

# api endpoint
api_url = "https://8h9qv4gh1b.execute-api.us-east-2.amazonaws.com/default/ShipmentTrackingAddNewPO"

print("Extracting data from PDF...")

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not po_number:
            po_number = re.findall(po_number_pattern, text)[0]
        case_number = re.findall(case_number_pattern, text)
        if not total_cases:
            total_cases = int(case_number[0][1])
        vendor_numbers = re.findall(vendor_number_pattern, text)
        if not vendor_number:
            vendor_number = vendor_numbers[0]

        barcode_numbers = re.findall(sscc_pattern, text)
        barcode_numbers = [re.sub(r"[\(\)\s]", "", bn) for bn in barcode_numbers]
        sku_numbers = re.findall(sku_pattern, text)
        description = re.findall(description_pattern, text)
        case_qty = re.findall(case_qty_pattern, text)
        print(f"------------- Page {i+1} -------------")
        # print(f"SSCC: {barcode_numbers[0]}")
        # print(f"Vendor Number: {vendor_number}")
        # print(f"SKU Number: {sku_numbers[0]}")
        # print(f"Description: {description[0]}")
        # print(f"Case Quantity: {case_qty[0]}")
        # print(f"PO Number: {po_number}")
        # print(f"Case Number: {case_number[0][0]} of {total_cases}")
        # print()

        cases.append(
            {
                "barcode": barcode_numbers[0],
                "SKU": sku_numbers[0],
                "description": description[0],
                "case_number": case_number[0][0],
                "current_location": "PPC",
            }
        )

        # make PO object and make a POST request to the API
    po = {
        "PO_number": po_number,
        "vendor_number": vendor_number,
        "total_cases": total_cases,
        "cases": cases,
    }

    # make a POST request to the API
    response = requests.post(api_url, json=po)
    print(response.json())
