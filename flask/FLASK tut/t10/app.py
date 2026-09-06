import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecretkey" # Required for flashing messages

# -------------------------------------------------------------------------
# 1. CONFIGURATION
# -------------------------------------------------------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Limit the maximum upload size to 16 Megabytes to protect our server
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """
    Check if the file extension is allowed.
    This prevents users from uploading dangerous files like .exe or .py.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# -------------------------------------------------------------------------
# 2. ROUTES
# -------------------------------------------------------------------------

@app.route('/')
def index():
    # List all uploaded files so we can see them on the page
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Step 1: Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part in the request')
        return redirect(request.url)
    
    file = request.files['file']
    
    # Step 2: If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    # Step 3: Validate and Save
    if file and allowed_file(file.filename):
        # SECURE FILENAME is vital. It removes characters like '../' 
        # that could be used to overwrite system files (Path Traversal Attack).
        filename = secure_filename(file.filename)
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        flash(f'File "{filename}" successfully uploaded for ML processing!')
        return redirect(url_for('index'))
    else:
        flash('File type not allowed! Please upload an image, PDF, or CSV.')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve the uploaded files so we can view/download them."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
