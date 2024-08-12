from fpdf import FPDF
from PIL import Image
import os
from datetime import datetime
from website import create_app




def get_timestamp():

    now = datetime.now()
    return now.strftime("%Y%m%d_%H%M%S")





def Print_pdf(cds, igt, opt, option, tf, prn, img_path):
    app = create_app()
    # Initialize PDF
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page(format='A4')
    pdf.set_margins(2.8, 2.8, 2.8)
    pdf.set_font('Arial', size=10)
    
    
    # Generate Timestamp
    timestamp = get_timestamp()
    
    # Add Title Section
    pdf.set_y(10)
    pdf.cell(210, 5, "ROYAUME DU MAROC", ln=1, align="C")
    pdf.cell(210, 5, "*****", ln=1, align="C")
    pdf.cell(210, 5, "AGENCE NATIONALE", ln=1, align="C")
    pdf.cell(210, 5, "DE LA CONSERVATION FONCIERE", ln=1, align="C")
    pdf.cell(210, 5, "DU CADASTRE ET DE LA CARTOGRAPHIE", ln=1, align="C")
    pdf.cell(210, 5, "*****", ln=1, align="C")
    pdf.cell(210, 5, f"SERVICE DU CADASTRE DE {cds.upper()}", ln=1, align="C")

    # Construct absolute path
    base_path = os.path.join(os.getcwd(), 'main_project', 'website', 'static', 'img')
    abs_img_path = os.path.join(base_path, os.path.basename(img_path))

    # Add Image
    if os.path.exists(abs_img_path):
        try:
            cover = Image.open(abs_img_path)
            # width, height = cover.size
            # Convert dimensions to mm (assuming 96 DPI)
            # width_mm = width * 25.4 / 96
            # height_mm = height * 25.4 / 96
            # pdf.image(abs_img_path, 10, 50, width_mm, height_mm)
            pdf.image(cover,10,50,190,180)
        except Exception as e:
            print(f"Error opening image: {e}")
            pdf.cell(210, 10, "Error loading image", ln=1, align="C")
    else:
        print(f"Image file does not exist at: {abs_img_path}")
        pdf.cell(210, 10, "Image file not found", ln=1, align="C")

    # Add Additional Information
    pdf.set_y(250)
    pdf.cell(210, 5, f"Nature de Travail: {opt}", ln=1, align="C")
    pdf.cell(210, 5, f"Photo de : {option}", ln=1, align="C")
    pdf.cell(210, 5, f"Société / IGT: {igt}", ln=1, align="C")
    pdf.cell(210, 5, f"Titre Foncier: {tf}", ln=1, align="C")
    pdf.cell(210, 5, f"Propriete dite: {prn}", ln=1, align="C")
    

    # Save PDF
    pdf_filename = f"work_{timestamp}.pdf"
    # pdf.output(pdf_filename, 'F')
    pdf_output_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    pdf.output(pdf_output_path, 'F')
    print(f"PDF saved as: {pdf_filename}")
    return pdf_filename
    
  
