import os
import sys
import pandas as pd

from flask import Flask, send_file, request, render_template, app as application

app = Flask(__name__)

def combine_sheets_to_csv(xlsx_file):
    excel_file = pd.ExcelFile(xlsx_file)
    combined_data = pd.DataFrame()

    for sheet_name in excel_file.sheet_names:
        sheet_data = excel_file.parse(sheet_name)
        sheet_data['TARIFF_TYPE'] = sheet_name
        combined_data = pd.concat([combined_data, sheet_data], ignore_index=True)

    combined_data['S/N'] = range(1, len(combined_data) + 1)
    return combined_data

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            combined_data = combine_sheets_to_csv(file)
            poor_formats = combined_data[combined_data['TARIFF NAME'].str.contains('\n', na=False)]
            return render_template('result.html', tables=[poor_formats.to_html(classes='data')], titles=poor_formats.columns.values)
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True)