import os
<<<<<<< HEAD
=======
from fuzzywuzzy import fuzz
>>>>>>> origin/baby
import uuid
import pandas as pd
import numpy as np
from flask import Flask, send_file, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')


<<<<<<< HEAD
=======
tags_list = ['(medicinal product form)', '(medicinal product)', '(clinical drug)',
            '(physical object)', '(product)', '(substance)', '(procedure)', '(finding)']

active_ingredient_url = '/home/user/validatesheet/data/Active_ingredient.xlsx'
act_df = pd.read_excel(active_ingredient_url)
act_list = act_df['Active_substance(s)'].to_list()

act_list = [item.lower() for item in act_list]


>>>>>>> origin/baby
# Function to combine sheets into a single DataFrame
def combine_sheets_to_csv(xlsx_file):
    excel_file = pd.ExcelFile(xlsx_file)
    dataframes = []

    for sheet_name in excel_file.sheet_names:
        sheet_data = excel_file.parse(sheet_name)
        sheet_data['TARIFF_TYPE'] = sheet_name
        dataframes.append(sheet_data)

    combined_data = pd.concat(dataframes, ignore_index=True)
    combined_data['S/N'] = range(1, len(combined_data) + 1)
    combined_data.to_csv('combined.csv', index=False)

    return combined_data

<<<<<<< HEAD
=======
def extract_and_remove_tag(text):
    extracted_tag = None
    for tag in tags_list:
        if tag in text:
            extracted_tag = tag
        #text = text.replace(tag, '')
        break  # Stop after finding and removing the first matching tag
    #return text, extracted_tag
    return extracted_tag

# Function to extract active ingredients from text
def get_active_ingredients(text):
    extracted_ing = set()
    for ing in act_list:
        if ing in text:
            extracted_ing.add(ing.strip())
        else:
            pass
    return extracted_ing

>>>>>>> origin/baby

# Function to evaluate and modify the standardized document
def evaluate_standardized_doc(standardized_file, combined_data):
    standardized_data = pd.read_excel(standardized_file)
    standardized_data['Target code'] = standardized_data['Target code'].fillna(value="1")
    standardized_data['Target code'] = standardized_data['Target code'].astype(int)
    standardized_data['new_tag'] = standardized_data['Target display'].apply(extract_and_remove_tag).apply(pd.Series)
    standardized_data['act_new'] = standardized_data['Target display'].apply(get_active_ingredients)

    combined_data.rename(columns={'raw_input': 'Source display'}, inplace=True)
<<<<<<< HEAD
    combined_data['target_code'].fillna(value="1", inplace=True)
=======
    combined_data['target_code'] = combined_data['target_code'].fillna(value="1")
>>>>>>> origin/baby
    combined_data['target_code'] = combined_data['target_code'].astype(int)
    combined_data['old_tag'] = combined_data['Source display'].apply(extract_and_remove_tag).apply(pd.Series)
    combined_data['act_old'] = combined_data['display_name'].apply(get_active_ingredients)

    merged_data = pd.merge(
<<<<<<< HEAD
        standardized_data,
        combined_data[['Source display', 'target_code', 'tariff_type', 'display_name', 'match_percent']],
=======
        standardized_data, combined_data[['Source display', 'target_code', 'tariff_type', 'display_name', 'match_percent', 'location_ref', 'act_old']],
>>>>>>> origin/baby
        left_on='Source display',
        right_on='Source display',
        how='left'
    )

    merged_data['edited'] = np.where(
        merged_data['Target code'] == merged_data['target_code'],
        'NE',  # Not Edited if equal
        'E'  # Edited if not equal
    )

<<<<<<< HEAD
    output_file_path = f'evaluated_standardized_document_{uuid.uuid4().hex}.xlsx'
    merged_data.to_excel(output_file_path, index=False)

    return output_file_path


=======
    merged_data['similarity'] = merged_data.apply(lambda row: fuzz.ratio(row['act_new'], row['act_old']), axis=1)

    output_file_path = f'evaluated_standardized_document_{uuid.uuid4().hex}.xlsx'
    merged_data.to_excel(output_file_path, index=False)



    return output_file_path




>>>>>>> origin/baby
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                combined_data = combine_sheets_to_csv(file)
                poor_formats = combined_data[combined_data['raw_input'].str.contains('\n', na=False)]

                context = {
                    'tables': [poor_formats.to_html(classes='data')],
                    'titles': poor_formats.columns.values,
                    'download_link': 'combined.csv'
                }
                return render_template('result.html', **context)
        except Exception as e:
            return render_template('upload.html', error=str(e))

    return render_template('upload.html')


@app.route('/evaluate', methods=['GET', 'POST'])
def upload_standardized_doc():
    if request.method == 'POST':
        try:
<<<<<<< HEAD
            standard_file = request.files['standardized_file']
            combined_data = pd.read_csv('combined.csv')  # Load previously saved combined data
=======
            print("Trying to get file...")  # Debug line
            standard_file = request.files['standardized_file']
            print("Got file, trying to read CSV...")  # Debug line
            combined_data = pd.read_csv('combined.csv')  # Load previously saved combined data
            print("CSV read successfully!")
>>>>>>> origin/baby

            if standard_file:
                output_file_path = evaluate_standardized_doc(standard_file, combined_data)
                return render_template('evaluation_result.html', download_link=output_file_path)
        except Exception as e:
<<<<<<< HEAD
=======
            print(f"ERROR: {str(e)}")
>>>>>>> origin/baby
            return render_template('upload_standardized.html', error=str(e))

    return render_template('upload_standardized.html')


@app.route('/split-excel', methods=['GET', 'POST'])
def split_excel():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file:
                input_file = secure_filename(file.filename)
                file.save(input_file)

                df = pd.read_excel(input_file, engine='openpyxl')
                category_column = 'tariff_type'
                unique_categories = df[category_column].unique()

                timestamp = pd.Timestamp.now().strftime('%Y%m%d')
                output_file = f'classified_{timestamp}_split.xlsx'

                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Complete_Dataset', index=True)
                    for category in unique_categories:
                        subset_df = df[df[category_column] == category]
                        subset_df.to_excel(writer, sheet_name=str(category), index=True)

                os.remove(input_file)

                context = {
                    'filename': output_file,
                    'category_count': len(unique_categories)
                }
                return render_template('split_result.html', **context)

        except Exception as e:
            return render_template('split_excel.html', error=str(e))

    return render_template('split_excel.html')


@app.route('/download/<filename>')
def download_file(filename):
    if not os.path.exists(filename):
        return "File not found. Please upload and process a file first.", 404
    return send_file(filename, as_attachment=True)


@app.route('/download-split/<filename>')
def download_split(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return str(e), 404


@app.route('/split-excel-modal')
def split_excel_modal():
    return render_template('split_excel_modal.html')


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")