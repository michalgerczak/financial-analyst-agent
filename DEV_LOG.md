### [Day 2] Ingestion Benchmark: The “Encoding Trap”

**Experiment:** Ran a local ingestion benchmark on the Accenture FY23 Report (page 63).

**Results:**
1. **pypdf:** **FAILED.** Returned garbage characters (#<DH<7<GL4A74C<G4?)...) 
2. **pymupdf4llm:** **FAILED.** Produced only empty boxes.
3. **pdfplumber:** **PARTIAL.** It picked up the table layout, but the text extraction itself was broken.

**Conclusion:** Local text-layer extractors can’t handle the heavily obfuscated font/encoding used in this financial report.

**Decision:** Switching to **vision-based models** (LlamaParse / GPT-4o), since they use OCR on pixel data instead of relying on the text layer.


### [Day 2.1] Vision Benchmark Results (The Solution)

**Experiment:** Compared LlamaParse, GPT-4o, and Claude 4.5 Sonnet on page 79 (Balance Sheet).

**Results:**
1. **LlamaParse:** **FASTEST (13s).** Great for high-volume structural parsing.
2. **GPT-4o:** **SUCCESS (30s).** Pulled the table data accurately.
3. **Claude 4.5 Sonnet:** **BEST QUALITY (26s).** Delivered the cleanest Markdown output with perfect headers.

**Decision:** Use **LlamaParse** for bulk ingestion and **Claude 4.5** for high-precision table extraction.
