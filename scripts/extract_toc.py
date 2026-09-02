import glob

try:
    import fitz
except ImportError as e:
    print(f"Error importing fitz: {e}")
    exit(1)

pdfs = glob.glob('edb_postgres/*.pdf')
for pdf in pdfs:
    print(f'\n--- TOC for {pdf} ---')
    try:
        doc = fitz.open(pdf)
        toc = doc.get_toc()
        if toc:
            for item in toc[:20]: # Print first 20 items to get a sense
                print(f'Level: {item[0]}, Title: {item[1]}, Page: {item[2]}')
            if len(toc) > 20:
                print(f'... and {len(toc)-20} more items')
        else:
            print('No TOC found. Falling back to first 3 pages text preview.')
            for page_num in range(min(3, len(doc))):
                text = doc[page_num].get_text()
                print(f'--- Page {page_num+1} ---\n{text[:200]}...')
    except Exception as e:
        print(f"Error reading {pdf}: {e}")
