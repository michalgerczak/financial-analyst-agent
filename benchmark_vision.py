import os
import time
import base64
from dotenv import load_dotenv
from pdf2image import convert_from_path
from llama_parse import LlamaParse
from openai import OpenAI
import anthropic

load_dotenv()


FILE_PATH = "data/report.pdf"
PAGE_INDEX = 79  


try:
    openai_client = OpenAI()
    anthropic_client = anthropic.Anthropic()
except Exception as e:
    print(f"Client Init Error: {e}")

print(f"COMPARISON TEST: VISION EXTRACTION (Page {PAGE_INDEX})")
print("="*60)

def get_page_image(path, page_num):
    images = convert_from_path(path, first_page=page_num+1, last_page=page_num+1)
    temp_path = "temp_page.jpg"
    images[0].save(temp_path, "JPEG")
    with open(temp_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# --- MODEL 1: LlamaParse ---
print(f"1. RUNNING: LlamaParse...")
try:
    start = time.time()
    parser = LlamaParse(result_type="markdown", api_key=os.getenv("LLAMA_CLOUD_API_KEY"))
    documents = parser.load_data(FILE_PATH)

    full_text = documents[0].text
    if "ASSETS" in full_text:
         idx = full_text.find("ASSETS")
         preview = full_text[idx:idx+1000]
    else:
         preview = full_text[:1000]

    end = time.time()
    print(f"   TIME: {end - start:.2f}s")
    print(f"   PREVIEW: {preview[:300].replace(chr(10), ' ')}...")
except Exception as e:
    print(f"   FAILED: {e}")
print("-" * 20)

# --- MODEL 2: GPT-4o ---
print(f"2. RUNNING: GPT-4o (Vision)...")
try:
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Missing OPENAI_API_KEY in .env")

    base64_image = get_page_image(FILE_PATH, PAGE_INDEX)
    start = time.time()
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "Transcribe this financial table into Markdown. Output ONLY the table."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
            ]}
        ]
    )
    gpt_text = response.choices[0].message.content
    end = time.time()
    print(f"   TIME: {end - start:.2f}s")
    print(f"   PREVIEW: {gpt_text[:300].replace(chr(10), ' ')}...")
except Exception as e:
    print(f"   FAILED: {e}")
print("-" * 20)

# --- MODEL 3: Claude 4.5 Sonnet ---
print(f"3. RUNNING: Claude 4.5 Sonnet (Vision)...")
try:
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Missing ANTHROPIC_API_KEY in .env")

    start = time.time()
    message = anthropic_client.messages.create(
        model="claude-sonnet-4-5-20250929", 
        max_tokens=2000,
        messages=[
            {"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
                {"type": "text", "text": "Transcribe this financial table into Markdown exactly. Output ONLY the table."}
            ]}
        ]
    )
    claude_text = message.content[0].text
    end = time.time()
    print(f"   TIME: {end - start:.2f}s")
    print(f"   PREVIEW: {claude_text[:300].replace(chr(10), ' ')}...")
except Exception as e:
    print(f"   FAILED: {e}")
print("="*60)