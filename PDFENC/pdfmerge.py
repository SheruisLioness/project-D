from flask import Blueprint, render_template, request, send_file
import PyPDF2
import tempfile
import os
import shutil
import datetime

pdfmerge_bp = Blueprint("pdfmerge", __name__)

@pdfmerge_bp.route("/")
def index():
    return render_template("pdfmerge.html")

@pdfmerge_bp.route('/pdfmerge', methods=["GET", "POST"])
def merge_pdfs():
    if request.method == 'POST':
        try:
            # Create a temporary directory to store uploaded files
            temp_dir = tempfile.mkdtemp()

            # Merge the PDFs
            merged_pdf = PyPDF2.PdfMerger()

            for pdf_file in request.files.getlist("pdfs"):
                pdf_path = os.path.join(temp_dir, pdf_file.filename)
                pdf_file.save(pdf_path)
                merged_pdf.append(pdf_path)

            # Generate a unique output filename using current date and time
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            output_pdf_filename = f"merged_{current_datetime}.pdf"
            output_pdf_path = os.path.join(temp_dir, output_pdf_filename)

            # Save the merged PDF to the generated filename
            with open(output_pdf_path, "wb") as output_pdf:
                merged_pdf.write(output_pdf)

            # Send the merged PDF as a response for download
            return send_file(output_pdf_path, as_attachment=True, download_name=output_pdf_filename)

        finally:
            # Clean up: Use shutil.rmtree to ensure complete directory removal
            shutil.rmtree(temp_dir, ignore_errors=True)

    return render_template('pdfmerge.html')
