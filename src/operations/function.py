import io
import math
from docx import Document
from PyPDF2 import PdfReader
from collections import Counter
import re


def calculate_tf_idf(texts) -> dict:
    # Сделал так, чтобы слова в итогом результате не отображались со знаками препинания, нарушая искомую стату
    without_signs = re.compile(r'[^\w\s]')
    words = []
    for text in texts:
        text_without_signs = without_signs.sub(' ', text)
        words.extend(text_without_signs.lower().split())
    word_count = Counter(words)
    num_documents = len(texts)
    idf_dict = {}
    for word in word_count:
        idf_dict[word] = sum(1 for text in texts if word in text) + 1
    tf_idf_val = {}
    for word, count in word_count.items():
        tf = count / len(words)
        idf = math.log10(num_documents / idf_dict[word])
        tf_idf_val[word] = {'number_of_times': word_count[word], 'tf': tf, 'idf': idf}
    return tf_idf_val


def read_docx(file) -> list:
    if not file:
        return []
    docx = Document(io.BytesIO(file))
    text = []
    for paragraph in docx.paragraphs:
        for run in paragraph.runs:
            text.append(run.text)
    return text


def read_pdf(file) -> list:
    pdf_reader = PdfReader(io.BytesIO(file))
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += '\n'.join(page.extract_text().splitlines())
    return text.split('\n')
