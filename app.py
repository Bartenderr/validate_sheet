import os
import pandas as pd
import numpy as np
from flask import Flask, send_file, request, render_template

app = Flask(__name__, static_folder='static')

# Function to combine sheets into a single DataFrame
def combine_sheets_to_csv(xlsx_file):
    excel_file = pd.ExcelFile(xlsx_file)
    combined_data = pd.DataFrame()

    for sheet_name in excel_file.sheet_names:
        sheet_data = excel_file.parse(sheet_name)
        sheet_data['TARIFF_TYPE'] = sheet_name
        combined_data = pd.concat([combined_data, sheet_data], ignore_index=True)

    combined_data['S/N'] = range(1, len(combined_data) + 1)
    
    # Save the combined data to a CSV file immediately after combining
    combined_data.to_csv('combined.csv', index=False)
    
    return combined_data

# Function to evaluate and modify the standardized document
def evaluate_standardized_doc(standardized_file, combined_data):
    standardized_data = pd.read_excel(standardized_file)
    standardized_data['Target code'].fillna(value="1", inplace=True)
    standardized_data['Target code'] = standardized_data['Target code'].astype(int)

    # Rename 'raw_input' to 'Source display' in combined_data
    combined_data.rename(columns={'raw_input': 'Source display'}, inplace=True)

    # Fill NaN values in 'target_code' and convert to int
    combined_data['target_code'].fillna(value="1", inplace=True)
    combined_data['target_code'] = combined_data['target_code'].astype(int)

    # Merge standardized data with combined data on 'Source display'
    merged_data = pd.merge(standardized_data, combined_data[['Source display', 'target_code', 'tariff_type']], 
                           left_on='Source display', right_on='Source display', 
                           how='left')

    # Create an 'edited' column based on comparison of 'Target code' and 'target_code'
    merged_data['edited'] = np.where(
        merged_data['Target code'] == merged_data['target_code'],
        'NE',  # Not Edited if equal
        'E'    # Edited if not equal
    )
    
    # output me the merged and evalauted files
    output_file_path = 'evaluated_standardized_document.xlsx'
    merged_data.to_excel(output_file_path, index=False)
    
    return output_file_path

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            combined_data = combine_sheets_to_csv(file)
            poor_formats = combined_data[combined_data['raw_input'].str.contains('\n', na=False)]
            
            return render_template('result.html', 
                                   tables=[poor_formats.to_html(classes='data')], 
                                   titles=poor_formats.columns.values,
                                   download_link='combined.csv')  # Update link to point to combined.csv
    
    return render_template('upload.html')

@app.route('/evaluate', methods=['GET', 'POST'])
def upload_standardized_doc():
    if request.method == 'POST':
        standard_file = request.files['standardized_file']
        combined_data = pd.read_csv('combined.csv')  # Load previously saved combined data
        
        if standard_file:
            output_file_path = evaluate_standardized_doc(standard_file, combined_data)
            return render_template('evaluation_result.html', download_link=output_file_path)

    return render_template('upload_standardized.html')

@app.route('/download/<filename>')
def download_file(filename):
    if not os.path.exists(filename):
        return "File not found. Please upload and process a file first.", 404
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)