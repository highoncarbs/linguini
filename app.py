from flask import Flask , request , jsonify ,json
import os
import subprocess 
import requests

app = Flask(__name__)


UPLOAD_FOLDER = './sqldump'
log_line = '{STATUS} : {DESC}'
_dumpfile = 'sqldump.sql'

@app.route('/api/sqldump' , methods = ['POST' , 'GET'])
def get_sqldump():
    if request.method == 'POST':
        if 'file' not in request.files:
            print(log_line.format('INFO' , 'File part not found in POST request . Please check if file is being uploaded'))
            return jsonify({'message' : 'No file found'})
    else:
        file = request.files['file']
        if file.filename == "":
            print(log_line.format('INFO' , 'FIle not selected properly , or empty file being supplied'))
            return jsonify({'message' : 'Empty file is ebing submitted'})
        if file:
            file.save(os.path.join(UPLOAD_FOLDER , ))
            return jsonify({'message' : 'Filed saved under ./sqldump as {}'.format(_dumpfile) , 'status' : 'success' })


@app.route('/api/nlp2sql' , methods = ['POST' , "GET"])
def nlp2sql():
    
    input_text = request.get_json()
    # Logic for In2Sql 
    xx = '"'+str(input_text['text'])+'"'
               
    query = "python -m ln2sql.main -d database_store\\{0} -l lang_store/english.csv -j output.json -i {1}".format( _dumpfile , xx)
    print(query)
    
    sql_result = subprocess.call(query)
    # print(sql_result)

    return jsonify({'message' : 'Executed SQL results' , 'query' : "Check the output.json file"})

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