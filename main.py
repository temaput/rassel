
import json
import tempfile
from flask import send_file
from DocumentWriter import Document

def survey_pdf(request):
    request_json = request.get_json(silent=True)
    survey = request_json["survey"]
    originalFile = open("resources/original.pdf", "rb")
    outputFile = tempfile.TemporaryFile(suffix=".pdf")
    doc = Document(survey, originalFile, outputFile)
    doc.draw_blocks()
    doc.finalize()
    outputFile.seek(0)

    return send_file(outputFile, attachment_filename="survey.pdf")



if __name__ == "__main__":
    data = json.load(open("stuff/data.json", "r"))
    originalFile = open("resources/original.pdf", "rb")
    outputFile =  open("stuff/destination.pdf", "wb")
    doc = Document(data, originalFile, outputFile)
    doc.draw_blocks()
    doc.finalize()


