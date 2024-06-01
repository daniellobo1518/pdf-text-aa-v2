from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import fitz  # PyMuPDF
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join('uploads', file.filename)
        file.save(pdf_path)
        txt_path = pdf_path.replace('.pdf', '.txt')
        convert_pdf_to_txt(pdf_path, txt_path)
        return redirect(url_for('download_file', filename=os.path.basename(txt_path)))
    return redirect(request.url)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory('uploads', filename)

def convert_pdf_to_txt(pdf_path, txt_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

