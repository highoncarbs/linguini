from flask import Flask , request , jsonify
import os
import subprocess 


app = Flask(__name__)


UPLOAD_FOLDER = './sqldump'
log_line = '{STATUS} : {DESC}'
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
            file.save(os.path.join(UPLOAD_FOLDER , file.filename))
            return jsonify({'message' : 'Filed saved under ./sqldump as {}'.format(file.filename) , 'status' : 'success' })


@app.route('/api/nlp2sql/<input>' , methods = ['POST'])
def nlp2sql(input):
    input_text = str(input)
    # Logic for In2Sql 
    if input_text:
        _dbsql = ""
        _query = input_text
        sql_result = suprocess.call(["python3 -m ln2sql.main -d {database} -l lang_store/english.csv -j output.json -i {query}".format( _dbsql , _query)])

    return jsonify({'message' : 'Executed SQL results' , 'query' : sql_result})

# python3 -m ln2sql.main -d database_store/city.sql -l lang_store/english.csv -j output.json -i "Count how many city there are with the name blob?"


@app.route('/home')
def home():
    # Setup of the application 
    # Take SQL dump from the user and upload it to /api/sqldump -> Single user app!
    # Give user a few tips on how to navigate 
    # Build chat interface for app


# RASA NLU chat code :



