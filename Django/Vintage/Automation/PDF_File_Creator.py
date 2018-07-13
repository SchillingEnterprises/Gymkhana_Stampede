from io import BytesIO

from django.http import HttpResponse
from reportlab.pdfgen import canvas


def create_pdf():
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=self.file_name(suffix=".pdf")'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    pdf_object = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    pdf_object.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly.
    pdf_object.showPage()
    pdf_object.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
