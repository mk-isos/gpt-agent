import pymupdf
import os

#①
pdf_file_path = "chap04/data/wheat_decision_support.pdf"
doc = pymupdf.open(pdf_file_path)

full_text = ''

#②
for page in doc: # 문서 페이지 반복
    text = page.get_text() # 페이지 텍스트 추출
    full_text += text

#③
pdf_file_name = os.path.basename(pdf_file_path)
pdf_file_name = os.path.splitext(pdf_file_name)[0] # 확장자 제거

#④
txt_file_path = f"chap04/data/{pdf_file_name}.txt"
with open(txt_file_path, 'w', encoding='utf-8') as f:
    f.write(full_text)