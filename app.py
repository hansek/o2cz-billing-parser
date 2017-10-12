from zipfile import ZipFile

from bs4 import BeautifulSoup
from flask import Flask, render_template, request

from util import allowed_file

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file sent to server', 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return 'File wasnt specified', 400

    if uploaded_file and not allowed_file(uploaded_file.filename):
        return 'Wrong file type, only ZIP type is accepted', 400

    with ZipFile(uploaded_file) as files_list:
        target_xml = None
        for file in files_list.namelist():
            if '-s-' in file:
                target_xml = file
                continue

        if not target_xml:
            return '-s- XML file not found in uploaded ZIP archive', 400

        with files_list.open(target_xml) as target_xml_file:
            file_content = target_xml_file.read()

        file_content = BeautifulSoup(file_content, 'xml')

        rows = []

        for i in file_content.find_all('subscriber'):
            price = float(i['summaryPrice'])

            payments = i.find('payments')

            payment = 0
            if payments:
                payment = float(payments['paymentTotalPrice'])

            total_price = price + payment

            rows.append([
                i['phoneNumber'],
                total_price
            ])

        response = []

        # response.append('<table>')

        for i in rows:
            response.append('<tr><td>{}</td><td>{:.2f} Kč</td></tr>'.format(*i))

        # response.append('</table>')

        # return jsonify(rows)
        return ''.join(response)

