from flask import Flask, render_template, request, send_file
from docx import Document
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merge", methods=["POST"])
def merge_documents():
    # Get uploaded files
    file1 = request.files["file1"]
    file2 = request.files["file2"]

    # Load the documents
    doc1 = Document(file1)
    doc2 = Document(file2)

    # Merge the documents
    for element in doc2.element.body:
        doc1.element.body.append(element)

    # Generate a timestamp for the file name
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Create a unique merged file name using the timestamp
    merged_filename = f"merged_document_{timestamp}.docx"
    doc1.save(merged_filename)

    # Provide the merged document for download
    return send_file(
        merged_filename,
        as_attachment=True,
        download_name=merged_filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

if __name__ == "__main__":
    app.run(debug=True)
