import time
from pypdf import PdfReader
import pdfplumber
import pymupdf4llm

FILE_PATH = "data/report.pdf"
PAGE_INDEX = 62  # The Balance Sheet page (Page in the pdf file = 63)

print(f"BENCHMARKING LOCAL PDF EXTRACTION (Page {PAGE_INDEX})")
print("="*60)

# --- MODEL 1: pypdf (The Stream) ---
print(f"RUNNING: pypdf...")
start_time = time.time()
reader = PdfReader(FILE_PATH)
page = reader.pages[PAGE_INDEX]
text_pypdf = page.extract_text()
end_time = time.time()

print(f"TIME: {end_time - start_time:.4f} seconds")
print(f"PREVIEW: {text_pypdf[:100].replace(chr(10), ' ')}...")
print("-" * 20)

# --- MODEL 2: pdfplumber (The Detective) ---
print(f"2️⃣RUNNING: pdfplumber...")
start_time = time.time()
with pdfplumber.open(FILE_PATH) as pdf:
    page = pdf.pages[PAGE_INDEX]
    text_plumber = page.extract_text()
    tables = page.extract_tables()
end_time = time.time()

print(f"TIME: {end_time - start_time:.4f} seconds")
if tables:
    print(f"Table Structure Detected: Found {len(tables)} tables")
else:
    print(f"Table Structure Detected: None")
print("-" * 20)

# --- MODEL 3: pymupdf4llm (The Local Hero) ---
print(f"RUNNING: pymupdf4llm (Markdown Converter)...")
start_time = time.time()
# This tool converts the layout to Markdown
md_text = pymupdf4llm.to_markdown(FILE_PATH, pages=[PAGE_INDEX])
end_time = time.time()

print(f"TIME: {end_time - start_time:.4f} seconds")
if "|" in md_text:
    print(f"   ✅ Table Structure Detected: Markdown pipes '|' found!")
else:
    print(f"   ❌ Table Structure Detected: None")

print("="*60)
print("🔎 PREVIEW OF MODEL 3 (pymupdf4llm):")
print(md_text[:500])
print("="*60)