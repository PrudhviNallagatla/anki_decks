import glob
import pdfplumber
import sys

sys.stdout.reconfigure(encoding='utf-8')

pdfs = glob.glob('edb_postgres/*.pdf')
for pdf in pdfs:
    print(f'\n============================')
    print(f'--- Extracting {pdf} ---')
    print(f'============================')
    try:
        with pdfplumber.open(pdf) as p:
            print(f"Total Pages: {len(p.pages)}")
            # Read first 10 pages to capture TOC
            for i, page in enumerate(p.pages[:10]):
                text = page.extract_text()
                if text:
                    print(f'\n--- Page {i+1} ---')
                    print(text[:800])
                    if len(text) > 800:
                        print('... [truncated]')
                else:
                    print(f'\n--- Page {i+1} --- [NO TEXT EXTRACTED]')
    except Exception as e:
        print(f"Error reading {pdf}: {e}")
