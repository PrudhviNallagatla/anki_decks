import pdfplumber
import glob
import os

os.makedirs('scratch/chunks', exist_ok=True)

pdfs = glob.glob('edb_postgres/*.pdf')
chunk_size = 50
chunk_idx = 1

for pdf in pdfs:
    print(f"Processing {pdf}...")
    try:
        with pdfplumber.open(pdf) as p:
            total_pages = len(p.pages)
            for i in range(0, total_pages, chunk_size):
                chunk_text = ""
                end_page = min(i + chunk_size, total_pages)
                for page_num in range(i, end_page):
                    page = p.pages[page_num]
                    text = page.extract_text()
                    if text:
                        chunk_text += text + "\n\n"
                
                if chunk_text.strip():
                    chunk_file = f'scratch/chunks/chunk_{chunk_idx:02d}.txt'
                    with open(chunk_file, 'w', encoding='utf-8') as f:
                        f.write(f"Source PDF: {os.path.basename(pdf)}\n")
                        f.write(f"Pages: {i+1} to {end_page}\n")
                        f.write("=" * 40 + "\n\n")
                        f.write(chunk_text)
                    print(f"Saved {chunk_file} (Pages {i+1}-{end_page})")
                    chunk_idx += 1
    except Exception as e:
        print(f"Error reading {pdf}: {e}")

print("Chunking complete.")
