import os
import zipfile
from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
from werkzeug.utils import secure_filename
from graph import open_zip, read_csv, compress_it

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('error'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('error'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print('saving file to ')
            print(os.path.join(UPLOAD_FOLDER, filename))
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            open_zip(os.path.join(UPLOAD_FOLDER, filename), UPLOAD_FOLDER)
            read_csv()
            compress_it(filename)

            #download_file(filename)

            #zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
            #zip_ref.extractall(UPLOAD_FOLDER)
            #zip_ref.close()

            #return redirect(url_for('upload_file', filename=filename))
            return render_template('index.html', name='confirm')
        
        else: return redirect('/error/File not Allowed')
    return render_template('index.html')

@app.route('/error/')
@app.route('/error/<name>')
def error(name=None):
    return render_template('error.html', name=name)

def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)