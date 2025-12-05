import os
from pdf2image import convert_from_path

FILE_PATH = "data/report.pdf"
PAGE_INDEX = 79  # Python Index (Page 63 in viewer)

print(f"SNAPSHOT TEST: Extracting Page {PAGE_INDEX}...")

try:
    images = convert_from_path(FILE_PATH, first_page=PAGE_INDEX+1, last_page=PAGE_INDEX+1)

    if not images:
        print("Error: No images extracted. Check PAGE_INDEX.")
        exit()

    output_file = "debug_balance_sheet.jpg"
    images[0].save(output_file, "JPEG")

    print(f"Success! Image saved to: {output_file}")
    print("Run this command to view it:  xdg-open debug_balance_sheet.jpg")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    print("Tip: Did you install poppler-utils? (sudo apt install poppler-utils)")