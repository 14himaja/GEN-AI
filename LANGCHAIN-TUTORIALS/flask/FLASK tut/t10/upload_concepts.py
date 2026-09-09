"""
SECURE FILE UPLOADS FOR AI/ML (t10)
===================================

WHY SECURE UPLOADS ARE VITAL FOR AI ENGINEERS:
---------------------------------------------
AI models rarely work with just text. You will often build systems where users 
upload Images (Computer Vision), Audio (Speech-to-Text), or CSVs (Data Analysis).
If you don't secure these uploads, a hacker could:
1. Upload a virus instead of an image.
2. Overwrite important system files using '../' in the filename.
3. Crash your server by uploading a 100GB file.

CONCEPTS IN THIS TUTORIAL:
--------------------------
1. WERKZEUG SECURE_FILENAME:
   - This is the most important function. It cleans the filename.
   - Example: "my../../../etc/passwd" becomes "my_etc_passwd".
   - This prevents 'Path Traversal' attacks.

2. EXTENSION VALIDATION:
   - We define `ALLOWED_EXTENSIONS` (e.g., png, jpg, pdf).
   - We reject anything else (like .exe or .php).

3. FILE SIZE LIMITS:
   - `app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024`
   - This prevents "Denial of Service" (DoS) attacks by limiting uploads to 16MB.

4. FLASH MESSAGES:
   - A Flask feature to send one-time feedback to the user (e.g., "Upload Successful!").

HOW TO RUN:
-----------
1. cd t10
2. python app.py
3. Open http://127.0.0.1:5000
4. Try uploading a picture or a text file.
5. Notice how the file is saved into the `t10/uploads/` folder securely.
"""

def get_summary():
    return "Secure uploads protect your AI pipeline from malicious files."
