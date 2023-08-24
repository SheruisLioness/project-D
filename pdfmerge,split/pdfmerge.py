from flask import Flask, render_template, request, send_file
import PyPDF2
import tempfile
import os
import shutil

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pdfmerge.html")

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    pdf_files = request.files.getlist("pdfs")

    try:
        # Create a temporary directory to store uploaded files
        temp_dir = tempfile.mkdtemp()

        pdf_paths = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(temp_dir, pdf_file.filename)
            pdf_file.save(pdf_path)
            pdf_paths.append(pdf_path)

        # Merge the PDFs
        merged_pdf = PyPDF2.PdfMerger()
        for pdf_path in pdf_paths:
            merged_pdf.append(pdf_path)

        # Save the merged PDF to a temporary file
        output_pdf_path = os.path.join(temp_dir, "merged.pdf")
        with open(output_pdf_path, "wb") as output_pdf:
            merged_pdf.write(output_pdf)

        # Send the merged PDF as a response for download
        return send_file(output_pdf_path, as_attachment=True, download_name="merged.pdf")

    finally:
        # Clean up: Use shutil.rmtree to ensure complete directory removal
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    app.run(debug=True)
