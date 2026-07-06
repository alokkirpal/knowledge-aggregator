#!/usr/bin/env python3
"""
Dump all text from a PDF, one page at a time, to stdout.
Run with the interpreter printed by setup_pdf_env.sh, e.g.:

    PY=$(bash setup_pdf_env.sh)
    $PY extract_pdf_text.py path/to/file.pdf > /tmp/file.txt
"""
import sys
from pypdf import PdfReader

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(1)

reader = PdfReader(sys.argv[1])
print(f"pages: {len(reader.pages)}", file=sys.stderr)
for page in reader.pages:
    print(page.extract_text())
    print("---PAGE---")
