from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import dropbox

# Configure Flask app
app = Flask(__name__)
app.secret_key = ''
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configure Dropbox API
DROPBOX_ACCESS_TOKEN = ''
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # Securely save the file with a secure filename
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Upload the file to Dropbox
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb') as f:
                dbx.files_upload(f.read(), f"/{filename}")
            
            flash('File uploaded successfully')
            return redirect(request.url)
        else:
            flash('Invalid file format. Allowed formats are: txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.run(debug=True)
