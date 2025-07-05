from flask import Flask, render_template, request, make_response
from xhtml2pdf import pisa
import io

app = Flask(__name__)

# Path to wkhtmltopdf executable (set this only not in PATH)
#config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf') # For Linux/Mac
#config = pdfkit.configuration(wkhtmltopdf='c:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe') #For Windows


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume', methods=['POST'])
def resume():
    data = request.form
    return render_template('resume.html', data=data)

@app.route('/download', methods=['POST'])
def download():
    data = request.form
    rendered = render_template('resume.html', data=data)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(rendered.encode("UTF-8")), result)
    
    if not pdf.err:
        response = make_response(result.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
        return response
    return "PDF generation failed"

if __name__ == '__main__':
    app.run(debug=True)