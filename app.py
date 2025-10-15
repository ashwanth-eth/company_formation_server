from flask import Flask, request, jsonify, send_file
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import re
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
import os

app = Flask(__name__)

class CompanyFormation(BaseModel):
    company_name: str = Field(..., description="Company name")
    state_of_formation: str = Field(..., description="US state or territory")
    company_type: Literal["corporation", "LLC"] = Field(..., description="Type of company")
    incorporator_name: str = Field(..., description="Name of incorporator")
    
    # Additional fields for New York
    mailing_address: Optional[str] = Field(None, description="Mailing address")
    email_address: Optional[str] = Field(None, description="Email address")
    phone_number: Optional[str] = Field(None, description="Phone number")
    exact_name_of_entity: Optional[str] = Field(None, description="Exact name of entity")
    
    # Additional fields for filer information
    filer_name: Optional[str] = Field(None, description="Filer's name")
    filer_company: Optional[str] = Field(None, description="Filer's company")
    filer_address: Optional[str] = Field(None, description="Filer's address")
    filer_city_state_zip: Optional[str] = Field(None, description="Filer's city, state and zip")

    @validator('company_name')
    def validate_company_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9\s,\.\'&]+$', v):
            raise ValueError('Company name can only contain alphanumeric characters, spaces, commas, periods, apostrophes, and ampersands')
        return v

    @validator('state_of_formation')
    def validate_state(cls, v):
        states = {
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
            'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
            'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
            'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
            'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
            'DC', 'PR', 'GU', 'VI', 'AS', 'MP'
        }
        if v.upper() not in states:
            raise ValueError('Invalid US state or territory')
        return v.upper()

def generate_delaware_articles(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "CERTIFICATE OF INCORPORATION")
    c.setFont("Helvetica", 12)
    
    # Article First - Company Name
    c.drawString(50, 700, "FIRST: The name of this corporation is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article Second - Registered Office
    c.drawString(50, 630, "SECOND: Its registered office in the State of Delaware is located at:")
    c.drawString(70, 610, "251 Little Falls Drive, Wilmington, New Castle County, Delaware 19808")
    
    # Article Third - Purpose
    c.drawString(50, 560, "THIRD: The purpose of the corporation is to engage in any lawful act or activity for")
    c.drawString(50, 540, "which corporations may be organized under the General Corporation Law of Delaware.")
    
    # Article Fourth - Authorized Shares
    c.drawString(50, 490, "FOURTH: The total number of shares of stock which this corporation is authorized")
    c.drawString(50, 470, "to issue is 1,000 shares of Common Stock with $0.01 par value per share.")
    
    # Incorporator
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned, being the incorporator hereinbefore named,")
    c.drawString(50, 180, f"has executed this Certificate of Incorporation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 160, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Incorporator:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_delaware_llc_certificate(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "CERTIFICATE OF FORMATION")
    c.setFont("Helvetica", 12)
    
    # Article First - Company Name
    c.drawString(50, 700, "FIRST: The name of the limited liability company is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article Second - Registered Office
    c.drawString(50, 630, "SECOND: The address of its registered office in the State of Delaware is:")
    c.drawString(70, 610, "251 Little Falls Drive, Wilmington, New Castle County, Delaware 19808")
    
    # Article Third - Registered Agent
    c.drawString(50, 560, "THIRD: The name and address of its registered agent in the State of Delaware is:")
    c.drawString(70, 540, "Corporation Service Company")
    c.drawString(70, 520, "251 Little Falls Drive")
    c.drawString(70, 500, "Wilmington, DE 19808")
    
    # Article Fourth - Management
    c.drawString(50, 450, "FOURTH: The limited liability company shall be managed by its members.")
    
    # Execution
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned has executed this Certificate of Formation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 180, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Authorized Person:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_california_articles(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "ARTICLES OF INCORPORATION")
    c.setFont("Helvetica", 12)
    
    # Article I - Company Name
    c.drawString(50, 700, "ARTICLE I: The name of this corporation is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article II - Purpose
    c.drawString(50, 630, "ARTICLE II: The purpose of the corporation is to engage in any lawful act or activity")
    c.drawString(50, 610, "for which a corporation may be organized under the General Corporation Law of California.")
    
    # Article III - Agent for Service
    c.drawString(50, 560, "ARTICLE III: The name and address in California of the corporation's initial agent for service of process is:")
    c.drawString(70, 540, "California Registered Agent, Inc.")
    c.drawString(70, 520, "123 Main Street")
    c.drawString(70, 500, "Los Angeles, CA 90001")
    
    # Incorporator
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned, being the incorporator hereinbefore named,")
    c.drawString(50, 180, f"has executed these Articles of Incorporation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 160, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Incorporator:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_california_llc_certificate(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "ARTICLES OF ORGANIZATION")
    c.setFont("Helvetica", 12)
    
    # Article I - Company Name
    c.drawString(50, 700, "ARTICLE I: The name of the limited liability company is:")
    c.drawString(70, 680, company_data.company_name)
    
    # Article II - Purpose
    c.drawString(50, 630, "ARTICLE II: The purpose of the limited liability company is to engage in any lawful business.")
    
    # Article III - Agent for Service
    c.drawString(50, 560, "ARTICLE III: The name and address in California of the LLC's initial agent for service of process is:")
    c.drawString(70, 540, "California Registered Agent, Inc.")
    c.drawString(70, 520, "123 Main Street")
    c.drawString(70, 500, "Los Angeles, CA 90001")
    
    # Execution
    c.drawString(50, 200, f"IN WITNESS WHEREOF, the undersigned has executed these Articles of Organization this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 180, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 100, "Authorized Person:")
    c.drawString(70, 80, company_data.incorporator_name)
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_new_york_articles(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "CERTIFICATE OF INCORPORATION")
    c.setFont("Helvetica", 12)
    
    # Header
    c.drawString(50, 720, f"CERTIFICATE OF INCORPORATION OF")
    c.drawString(50, 700, f"{company_data.exact_name_of_entity or company_data.company_name}")
    c.drawString(50, 680, "Under Section 402 of the Business Corporation Law")
    
    # FIRST - Company Name
    c.drawString(50, 640, "FIRST: The name of the corporation is:")
    c.drawString(70, 620, company_data.exact_name_of_entity or company_data.company_name)
    
    # SECOND - Purpose
    c.drawString(50, 580, "SECOND: The purpose of the corporation is to engage in any lawful act or activity")
    c.drawString(50, 560, "for which a corporation may be organized under the Business Corporation Law.")
    c.drawString(50, 540, "The corporation is not formed to engage in any act or activity requiring the")
    c.drawString(50, 520, "consent or approval of any state official, department, board, agency or other")
    c.drawString(50, 500, "body without such consent or approval first being obtained.")
    
    # THIRD - County Location
    c.drawString(50, 460, "THIRD: The county, within this state, in which the office of the corporation")
    c.drawString(50, 440, "is to be located is: Albany County.")
    
    # FOURTH - Authorized Shares (Updated as requested)
    c.drawString(50, 400, "FOURTH: The corporation shall have authority to issue one class of shares")
    c.drawString(50, 380, "consisting of 1,000 common shares with $0.01 par value per share.")
    
    # FIFTH - Agent for Service (Updated address)
    c.drawString(50, 340, "FIFTH: The Secretary of State is designated as agent of the corporation")
    c.drawString(50, 320, "upon whom process against the corporation may be served.")
    c.drawString(50, 300, "The post office address to which the Secretary of State shall mail a copy")
    c.drawString(50, 280, "of any process against the corporation served upon the Secretary of State")
    c.drawString(50, 260, "by personal delivery is:")
    c.drawString(70, 240, "418 BROADWAY STE Y")
    c.drawString(70, 220, "ALBANY, ALBANY COUNTY, NY 12207")
    
    # Optional email address
    if company_data.email_address:
        c.drawString(50, 200, "The email address to which the Secretary of State shall email a notice")
        c.drawString(50, 180, "of the fact that process against the corporation has been served")
        c.drawString(50, 160, "electronically upon the Secretary of State is:")
        c.drawString(70, 140, company_data.email_address)
    
    # Signature section
    c.drawString(50, 100, f"IN WITNESS WHEREOF, the undersigned, being the incorporator hereinbefore named,")
    c.drawString(50, 80, f"has executed this Certificate of Incorporation this {datetime.now().strftime('%d')} day of")
    c.drawString(50, 60, f"{datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 30, "Incorporator:")
    c.drawString(70, 10, company_data.incorporator_name)
    
    # Add filer information if provided
    if company_data.filer_name or company_data.filer_company:
        c.showPage()  # Start new page
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "FILER'S NAME AND MAILING ADDRESS")
        c.setFont("Helvetica", 12)
        
        c.drawString(50, 700, "Name:")
        c.drawString(70, 680, company_data.filer_name or "")
        
        if company_data.filer_company:
            c.drawString(50, 650, "Company, if Applicable:")
            c.drawString(70, 630, company_data.filer_company)
        
        c.drawString(50, 600, "Mailing Address:")
        c.drawString(70, 580, company_data.filer_address or "")
        c.drawString(70, 560, company_data.filer_city_state_zip or "")
    
    c.save()
    buffer.seek(0)
    return buffer

def generate_new_york_llc_certificate(company_data: CompanyFormation) -> BytesIO:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Set up the document
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 750, "ARTICLES OF ORGANIZATION")
    c.setFont("Helvetica", 12)
    
    # Header
    c.drawString(50, 720, f"ARTICLES OF ORGANIZATION OF")
    c.drawString(50, 700, f"{company_data.exact_name_of_entity or company_data.company_name}")
    c.drawString(50, 680, "Under Section 203 of the Limited Liability Company Law")
    
    # FIRST - Company Name
    c.drawString(50, 640, "FIRST: The name of the limited liability company is:")
    c.drawString(70, 620, company_data.exact_name_of_entity or company_data.company_name)
    
    # SECOND - County Location (Updated to Albany County)
    c.drawString(50, 580, "SECOND: The county within this state in which the office of the limited")
    c.drawString(50, 560, "liability company is to be located is: Albany County.")
    
    # THIRD - Agent for Service (Updated address)
    c.drawString(50, 520, "THIRD: The Secretary of State is designated as agent of the limited")
    c.drawString(50, 500, "liability company upon whom process against the limited liability company")
    c.drawString(50, 480, "may be served.")
    c.drawString(50, 460, "The post office address to which the Secretary of State shall mail a copy")
    c.drawString(50, 440, "of any process against the limited liability company served upon the")
    c.drawString(50, 420, "Secretary of State by personal delivery is:")
    c.drawString(70, 400, "418 BROADWAY STE Y")
    c.drawString(70, 380, "ALBANY, ALBANY COUNTY, NY 12207")
    
    # Optional email address
    if company_data.email_address:
        c.drawString(50, 340, "The email address to which the Secretary of State shall email a notice")
        c.drawString(50, 320, "of the fact that process against the limited liability company has been")
        c.drawString(50, 300, "served electronically upon the Secretary of State is:")
        c.drawString(70, 280, company_data.email_address)
    
    # Signature section
    c.drawString(50, 240, f"IN WITNESS WHEREOF, the undersigned has executed these Articles of Organization")
    c.drawString(50, 220, f"this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B, %Y')}.")
    
    c.drawString(50, 180, "Organizer:")
    c.drawString(70, 160, company_data.incorporator_name)
    
    # Add filer information if provided
    if company_data.filer_name or company_data.filer_company:
        c.showPage()  # Start new page
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "FILER'S NAME AND MAILING ADDRESS")
        c.setFont("Helvetica", 12)
        
        c.drawString(50, 700, "Name:")
        c.drawString(70, 680, company_data.filer_name or "")
        
        if company_data.filer_company:
            c.drawString(50, 650, "Company, if Applicable:")
            c.drawString(70, 630, company_data.filer_company)
        
        c.drawString(50, 600, "Mailing Address:")
        c.drawString(70, 580, company_data.filer_address or "")
        c.drawString(70, 560, company_data.filer_city_state_zip or "")
    
    c.save()
    buffer.seek(0)
    return buffer

@app.route('/form-company', methods=['POST'])
def form_company():
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                "company_name": request.form.get("company_name"),
                "state_of_formation": request.form.get("state_of_formation"),
                "company_type": request.form.get("company_type"),
                "incorporator_name": request.form.get("incorporator_name"),
                "mailing_address": request.form.get("mailing_address"),
                "email_address": request.form.get("email_address"),
                "phone_number": request.form.get("phone_number"),
                "exact_name_of_entity": request.form.get("exact_name_of_entity"),
                "filer_name": request.form.get("filer_name"),
                "filer_company": request.form.get("filer_company"),
                "filer_address": request.form.get("filer_address"),
                "filer_city_state_zip": request.form.get("filer_city_state_zip")
            }
        
        company_data = CompanyFormation(**data)
        
        if company_data.state_of_formation == 'DE':
            if company_data.company_type == 'corporation':
                pdf_buffer = generate_delaware_articles(company_data)
            elif company_data.company_type == 'LLC':
                pdf_buffer = generate_delaware_llc_certificate(company_data)
            else:
                return jsonify({"error": "Unsupported company type"}), 400
        elif company_data.state_of_formation == 'CA':
            if company_data.company_type == 'corporation':
                pdf_buffer = generate_california_articles(company_data)
            elif company_data.company_type == 'LLC':
                pdf_buffer = generate_california_llc_certificate(company_data)
            else:
                return jsonify({"error": "Unsupported company type"}), 400
        elif company_data.state_of_formation == 'NY':
            if company_data.company_type == 'corporation':
                pdf_buffer = generate_new_york_articles(company_data)
            elif company_data.company_type == 'LLC':
                pdf_buffer = generate_new_york_llc_certificate(company_data)
            else:
                return jsonify({"error": "Unsupported company type"}), 400
        else:
            return jsonify({
                "error": "Only Delaware, California, and New York entities are supported at this time"
            }), 400
    
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{company_data.company_name}_certificate.pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/form-company-schema', methods=['GET'])
def form_company_schema():
    examples = [
        {
            "company_name": "Acme Corp, Inc.",
            "state_of_formation": "DE",
            "company_type": "corporation",
            "incorporator_name": "John Smith"
        },
        {
            "company_name": "Smith & Sons, LLC",
            "state_of_formation": "DE",
            "company_type": "LLC",
            "incorporator_name": "Jane Doe"
        },
        {
            "company_name": "Tech Innovators Co.",
            "state_of_formation": "CA",
            "company_type": "corporation",
            "incorporator_name": "Michael Johnson"
        },
        {
            "company_name": "California Dreaming, LLC",
            "state_of_formation": "CA",
            "company_type": "LLC",
            "incorporator_name": "Emily Chen"
        },
        {
            "company_name": "Empire State Corp",
            "state_of_formation": "NY",
            "company_type": "corporation",
            "incorporator_name": "Robert Johnson",
            "mailing_address": "123 Main Street, New York, NY 10001",
            "email_address": "robert@empirestate.com",
            "phone_number": "(555) 123-4567",
            "exact_name_of_entity": "Empire State Corp",
            "filer_name": "Robert Johnson",
            "filer_company": "Empire State Legal Services",
            "filer_address": "456 Broadway",
            "filer_city_state_zip": "New York, NY 10013"
        },
        {
            "company_name": "Big Apple Ventures, LLC",
            "state_of_formation": "NY",
            "company_type": "LLC",
            "incorporator_name": "Sarah Williams",
            "mailing_address": "789 Fifth Avenue, New York, NY 10022",
            "email_address": "sarah@bigappleventures.com",
            "phone_number": "(555) 987-6543",
            "exact_name_of_entity": "Big Apple Ventures, LLC",
            "filer_name": "Sarah Williams",
            "filer_company": "Big Apple Legal Group",
            "filer_address": "321 Park Avenue",
            "filer_city_state_zip": "New York, NY 10010"
        }
    ]
    return jsonify(examples)

@app.route('/', methods=['GET'])
def company_form():
    states = [
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'DC', 'PR', 'GU', 'VI', 'AS', 'MP'
    ]
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Company Formation</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            form {{ display: grid; gap: 15px; }}
            label {{ font-weight: bold; }}
            input, select, textarea {{ padding: 8px; font-size: 16px; width: 100%; box-sizing: border-box; }}
            button {{ background: #007bff; color: white; border: none; padding: 10px 20px; cursor: pointer; font-size: 16px; }}
            button:hover {{ background: #0056b3; }}
            .section {{ border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .section h3 {{ margin-top: 0; color: #333; }}
            .optional {{ color: #666; font-size: 14px; }}
        </style>
        <script>
            function toggleNYFields() {{
                const state = document.getElementById('state_of_formation').value;
                const nyFields = document.getElementById('ny-fields');
                if (state === 'NY') {{
                    nyFields.style.display = 'block';
                }} else {{
                    nyFields.style.display = 'none';
                }}
            }}
        </script>
    </head>
    <body>
        <h1>Company Formation</h1>
        <form action="/form-company" method="POST">
            <div class="section">
                <h3>Basic Information</h3>
                <label for="company_name">Company Name:</label>
                <input type="text" id="company_name" name="company_name" required>
                
                <label for="state_of_formation">State of Formation:</label>
                <select id="state_of_formation" name="state_of_formation" required onchange="toggleNYFields()">
                    <option value="">Select a state</option>
                    {"".join(f'<option value="{state}">{state}</option>' for state in states)}
                </select>
                
                <label for="company_type">Company Type:</label>
                <select id="company_type" name="company_type" required>
                    <option value="">Select a type</option>
                    <option value="corporation">Corporation</option>
                    <option value="LLC">LLC</option>
                </select>
                
                <label for="incorporator_name">Incorporator Name:</label>
                <input type="text" id="incorporator_name" name="incorporator_name" required>
            </div>
            
            <div id="ny-fields" class="section" style="display: none;">
                <h3>Additional Information for New York</h3>
                <p class="optional">These fields are optional but recommended for New York filings</p>
                
                <label for="exact_name_of_entity">Exact Name of Entity:</label>
                <input type="text" id="exact_name_of_entity" name="exact_name_of_entity" placeholder="Same as company name if not specified">
                
                <label for="mailing_address">Mailing Address:</label>
                <textarea id="mailing_address" name="mailing_address" rows="3" placeholder="Street address, city, state, zip"></textarea>
                
                <label for="email_address">Email Address:</label>
                <input type="email" id="email_address" name="email_address" placeholder="your@email.com">
                
                <label for="phone_number">Phone Number:</label>
                <input type="tel" id="phone_number" name="phone_number" placeholder="(555) 123-4567">
                
                <h4>Filer Information</h4>
                <label for="filer_name">Filer's Name:</label>
                <input type="text" id="filer_name" name="filer_name" placeholder="Name of person filing">
                
                <label for="filer_company">Filer's Company (if applicable):</label>
                <input type="text" id="filer_company" name="filer_company" placeholder="Company name">
                
                <label for="filer_address">Filer's Address:</label>
                <textarea id="filer_address" name="filer_address" rows="2" placeholder="Street address"></textarea>
                
                <label for="filer_city_state_zip">City, State, Zip:</label>
                <input type="text" id="filer_city_state_zip" name="filer_city_state_zip" placeholder="City, State, Zip Code">
            </div>
            
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    # Trigger fresh deployment - NY implementation ready for production
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port)
