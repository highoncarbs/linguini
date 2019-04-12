from flask import Flask, request, jsonify, json, session
from json import loads
import os
import subprocess
import helper

app = Flask(__name__)


UPLOAD_FOLDER = './sqldump'
log_line = '{STATUS} : {DESC}'


@app.route('/api/sqldump', methods=['POST', 'GET'])
def get_sqldump():
    if request.method == 'POST':
        if 'file' not in request.files:
            print(log_line.format(
                'INFO', 'File part not found in POST request . Please check if file is being uploaded'))
            return jsonify({'message': 'No file found', 'success': False})
        else:
            file = request.files['file']
            if file.filename == "":
                print(log_line.format(
                    'INFO', 'FIle not selected properly , or empty file being supplied'))
                return jsonify({'message': 'Empty file is being submitted', 'success': False})
            if file:
                session['file_name'] = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                return jsonify({'message': 'Filed saved under ./sqldump as {}'.format(file.filename), 'success': True})
            else:
                return jsonify({'message': 'Invalid Request', 'success': False})
    else:
        return jsonify({'message': 'Invalid Request', 'success': False})


@app.route('/api/nlp2sql', methods=['POST', "GET"])
def nlp2sql():
    input_text = request.get_json()
    dumpfile = session.get('file_name')

    # Logic for In2Sql
    xx = '"'+str(input_text['text'])+'"'
    file_directory = os.path.join('..', 'sqldump')

    query = f"python -m ln2sql.main -d {file_directory}/{dumpfile} -l lang_store/english.csv -j output.json -i {xx}"
    process = subprocess.Popen(
        query, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, error = process.communicate()

    if error is not None:
        return jsonify({
            'message': 'Unable to process to request',
            'success': False
        })

    output = output.decode('utf-8').replace('\r\n', ' ')

    saved_file = open('output.json', 'r')
    invalid_json_content = saved_file.read().strip()
    saved_file.close()

    last_comma_index = invalid_json_content.rfind(',')
    json_content = invalid_json_content[:last_comma_index] + \
        invalid_json_content[last_comma_index + 1:]

    return jsonify({
        'message': 'Executed SQL results',
        'success': False,
        'result': loads(json_content, object_pairs_hook=helper.log_error_on_duplicates),
        'query': output
    })

# python3 -m ln2sql.main -d database_store/city.sql -l lang_store/english.csv -j output.json -i "Count how many city there are with the name blob?"


@app.route('/home')
def home():
    # Setup of the application
    # Take SQL dump from the user and upload it to /api/sqldump -> Single user app!
    # Give user a few tips on how to navigate
    # Build chat interface for app
    if request.method == "POST":
        pass


# RASA NLU chat code
