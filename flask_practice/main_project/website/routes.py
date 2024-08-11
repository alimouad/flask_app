import os
from flask import Blueprint ,render_template ,request,session ,url_for, redirect, send_from_directory , abort
from .models import Print_pdf
from website import create_app
from werkzeug.utils import secure_filename





routes = Blueprint('routes',__name__) 


def get_image_url(filename):
   
    return url_for('static', filename=os.path.join('img/', filename))




# # Home Page 
@routes.route("/")
def home_Page():
    return render_template('home.html')
    
    
    
   
   
@routes.route("/handle_image", methods=['GET', 'POST'])
def handle_image():

    if request.method == "POST":
        if 'image' not in request.files:
            return "No image part in the request", 400

        img = request.files['image']
        if img and img.filename:
            img_name = secure_filename(img.filename)
            upload_folder = os.path.join(os.getcwd(), 'main_project', 'website', 'static', 'img')
            img_path = os.path.join(upload_folder, img_name)
            try:
                img.save(img_path)
                image_url = get_image_url(img_name)
                session['image'] = img_path  # Save the file path in the session
                session['igt'] = request.form.get('igt')
                session['cds'] = request.form.get('cds')
                session['opt'] = request.form.get('opt')
                session['tf'] = request.form.get('tf')
                session['prn'] = request.form.get('prn')
            except Exception as e:
                print(f"Error saving file: {e}")
                return f"Error saving file: {e}", 500
        else:
            return "No file uploaded or file name is empty", 400

    return render_template('img.html', img=image_url if 'image' in session else None)



@routes.route("/download", methods=['GET', 'POST'])
def download():
   
    if request.method == "POST":
        option = request.form.get('option')
        if option:
            session['option'] = option
        else:
            return "No option provided", 400 
        # Return an error response if no option is provided
    
    # Render the download form (GET request)
    return render_template('download.html')




@routes.route("/download/generate")
def download_pdf():
    required_keys = ['cds', 'igt', 'opt', 'option', 'tf', 'prn', 'image']
    
    if all(key in session for key in required_keys):
        # Generate the PDF with session data
        pdf_filename = Print_pdf(
            cds=session.get('cds'),
            igt=session.get('igt'),
            opt=session.get('opt'),
            option=session.get('option'),
            tf=session.get('tf'),
            prn=session.get('prn'),
            img_path=session.get('image')
        )
        session['pdf_filename'] = pdf_filename
        # return render_template('success.html', filename=pdf_filename)
        # Redirect to the endpoint that serves the generated PDF
        return redirect(url_for('routes.print_pdf', filename=pdf_filename))
    else:
        # Return an error response if any required session data is missing
        return "Form data incomplete. Please submit both forms.", 400




@routes.route("/download/<filename>")
def print_pdf(filename):
   
    upload_folder = app.config['UPLOAD_FOLDER']
    app = create_app()
    

   
    if upload_folder:
        try:
            # Serve the PDF file from the upload folder
            return send_from_directory(upload_folder, filename)
        except FileNotFoundError:
            # Handle the case where the file does not exist
            abort(404, description="The requested file was not found.")
    else:
        # Return an error if the upload folder configuration is missing
        abort(500, description="Server configuration error: Upload folder not set.")
   
   
