import streamlit as st
import requests
import io
from markdown_pdf import MarkdownPdf, Section
import fitz
import pdfplumber
import re

# def extract_text_from_pdf(pdf_file):
#     """
#     Extract text from PDF using RapidAPI and convert it to a single line
    
#     Args:
#         pdf_file: The uploaded PDF file
#     Returns:
#         str: Extracted text in a single line with proper spacing
#     """
#     # RapidAPI endpoint for PDF extraction
#     url = "https://ocr-text-extraction.p.rapidapi.com/v1/ocr/"
    
#     # RapidAPI headers - you need to get these from RapidAPI dashboard
#     headers = {
#         "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
#         "X-RapidAPI-Host": "ocr-text-extraction.p.rapidapi.com"
#     }
    
#     try:
#         # Convert PDF file to bytes for sending to API
#         pdf_bytes = pdf_file.getvalue()
        
#         # Make API request to RapidAPI
#         response = requests.post(
#             url,
#             headers=headers,
#             files={"pdf": pdf_bytes}
#         )
        
#         if response.status_code == 200:
#             # Get the extracted text from response
#             extracted_text = response.json().get('text', '')
            
#             # Convert text to single line:
#             # 1. Split text into lines
#             # 2. Join with spaces
#             # 3. Remove extra whitespace
#             single_line_text = " ".join(extracted_text.split())
            
#             return single_line_text
#         else:
#             # If RapidAPI fails, use fallback method
#             return fallback_extract_text(pdf_file)
            
#     except Exception as e:
#         st.warning("Using fallback PDF extraction method")
#         return fallback_extract_text(pdf_file)
    

# def extract_text_from_pdf(pdf_file):
#     """
#     Extract text from PDF using pdfplumber for improved layout accuracy.
    
#     Args:
#         pdf_file: The uploaded PDF file
#     Returns:
#         str: Extracted text with preserved line breaks and cleaned of extraneous links.
#     """
#     try:
#         pdf_file.seek(0)
#         text = ""
#         with pdfplumber.open(pdf_file) as pdf:
#             for page in pdf.pages:
#                 # Extract text while preserving layout
#                 page_text = page.extract_text()
#                 if page_text:
#                     text += page_text + "\n"
        
#         # Remove unwanted links (e.g., footer links) using regex
#         # This pattern removes URLs starting with http or https
#         text = re.sub(r'https?://\S+', '', text)
        
#         # Optionally, remove any extra form navigation or page numbering if needed:
#         text = re.sub(r'\d+/\d+\s*$', '', text, flags=re.MULTILINE)
        
#         # Normalize whitespace and line breaks
#         cleaned_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        
#         return cleaned_text
#     except Exception as e:
#         st.error(f"Error extracting text with pdfplumber: {str(e)}")
#         return fallback_extract_text(pdf_file)
    
import pdfplumber
import fitz  # PyMuPDF
import io

def extract_text_with_forms(uploaded_file):
    """
    Extracts both text and form selections (radio buttons, checkboxes, dropdowns) from a Google Forms PDF.

    Args:
        uploaded_file: The uploaded PDF file (from Streamlit).

    Returns:
        str: Extracted text with form selections included.
    """
    extracted_text = ""

    # Store original file position to reset later
    original_position = uploaded_file.tell()
    
    # Reset file position
    uploaded_file.seek(0)
    
    # Convert uploaded file to BytesIO for compatibility with PyMuPDF
    pdf_bytes = uploaded_file.read()
    pdf_stream = io.BytesIO(pdf_bytes)

    # Extract text using pdfplumber (for normal text fields)
    with pdfplumber.open(pdf_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            extracted_text += page_text + "\n"

    # Reset BytesIO stream position for PyMuPDF
    pdf_stream.seek(0)
    
    # Extract form fields using PyMuPDF (fitz)
    form_data = []
    try:
        doc = fitz.open(stream=pdf_stream, filetype="pdf")
        
        for page_num, page in enumerate(doc):
            # Get form fields on this page
            widgets = page.widgets()
            
            for widget in widgets:
                field_type = widget.field_type
                field_name = widget.field_name or "Unnamed Field"
                field_label = field_name
                field_value = None
                
                # Get field value based on field type
                if field_type == fitz.WIDGET_TYPE_CHECKBOX:
                    field_value = "Selected" if widget.is_checked() else "Not Selected"
                elif field_type == fitz.WIDGET_TYPE_RADIO:
                    field_value = "Selected" if widget.is_checked() else "Not Selected"
                elif field_type == fitz.WIDGET_TYPE_LISTBOX:
                    field_value = widget.choice_values[widget.choice] if widget.choice >= 0 else None
                elif field_type == fitz.WIDGET_TYPE_COMBOBOX:
                    field_value = widget.choice_values[widget.choice] if widget.choice >= 0 else widget.text
                else:
                    field_value = widget.text
                
                # Only add if we have a value
                if field_value:
                    form_data.append(f"{field_label}: {field_value}")
        
        # Append form data to the extracted text if we found any
        if form_data:
            extracted_text += "\n\n--- FORM SELECTIONS ---\n"
            for item in form_data:
                extracted_text += f"{item}\n"
                
    except Exception as e:
        print(f"Error extracting form fields with PyMuPDF: {str(e)}")
    
    # Reset uploaded file to its original position
    uploaded_file.seek(original_position)
    
    return extracted_text.strip()



def call_visa_roadmap_api(text,roadmap_type,additional_information):
    """
    Call your visa roadmap API with the single-line text
    
    Args:
        text (str): Single-line text from PDF
    Returns:
        dict: API response with roadmap data
    """
    # url = "https://langraph-visaroadmap-247572588539.us-central1.run.app/generate_roadmap"
    url = "https://latestvisaroadmap-247572588539.us-central1.run.app/generate_roadmap"
    # url="http://localhost:8000/generate_roadmap"
    # url ="https://lang-visaroadmap-v4.onrender.com/generate_roadmap"
    try:
        # Prepare the payload - make sure text is in single line
        payload = {
            "questionnaire": text,
            "roadmap_type":roadmap_type,
            "additional_information":additional_information
        }

        # Make API request
        response = requests.post(url, params=payload)
        print(response)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error(f"API Error: Data Not Found ({response.status_code})")
        else:
            st.error(f"API Error: {response.status_code}")
            return None    
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


def convert_dict_to_markdown(data):
    """
    Convert the given dictionary into a Markdown-formatted string.
    
    :param data: Dictionary containing the structured information.
    :return: A Markdown-formatted string.
    """
    markdown_content = []

    # Add Title
    markdown_content.append("# Immigration Profile Report\n")
    
    # Add Questionnaire and Response
    markdown_content.append("## 1. Questionnaire and Response:\n")
    questionnaire = data.get('questionnaire', '')
    for line in questionnaire.split('●'):
        if line.strip():  # Avoid empty lines
            markdown_content.append(f"- {line.strip()}\n")
    
    # Add Job Roles
    markdown_content.append("## 2. Job Roles Based on Education and Work Experience:\n")
    markdown_content.append(f"{data.get('job_roles', '')}\n")
    
    # Add NOC Codes
    markdown_content.append("## 3. NOC Codes:\n")
    for noc_entry in data.get('noc_codes', []):
        if isinstance(noc_entry, dict):  # Ensure noc_entry is a dictionary
            noc_info = noc_entry.get("noc_info", "").strip()
            category = noc_entry.get("category", "Unknown Category").strip()
            markdown_content.append(f"- {noc_info} (Category: {category})\n")
        else:  # If it's a string, process normally
            markdown_content.append(f"- {noc_entry.strip()}\n")

    
    # Add CRS Score Breakdown
    markdown_content.append("## 4. CRS Score Breakdown:\n")
    markdown_content.append(f"{data.get('crs_score', '')}\n")
    
    # Add Roadmap
    markdown_content.append("## 5. Roadmap for Canada Immigration:\n")
    markdown_content.append(f"{data.get('roadmap', '')}\n")
    
    # Combine all the sections into a single string
    return "\n".join(markdown_content)


# Set up Streamlit page
st.set_page_config(page_title="Visa Roadmap Assistant", layout="wide")
st.title("Visa Roadmap Assistant")

# Check if RapidAPI key is configured
if 'RAPIDAPI_KEY' not in st.secrets:
    st.error("Please configure your RapidAPI key in .streamlit/secrets.toml")
    st.stop()

# Visa type selection
roadmap_type = st.selectbox(
    "Select Visa Type:",
    ["Immigration Visa", "Study Visa", "Travel Visa", "Work Visa"],
    index=None,
    placeholder="Select Visa Type"
)

# Additional information input
additional_info = st.text_area("Additional Information (Optional)")

# File upload section
uploaded_file = st.file_uploader("Upload your questionnaire PDF", type="pdf")


if roadmap_type == "Immigration Visa" and uploaded_file is not None:
    # Extract and process text
    with st.spinner("Extracting text from PDF..."):
        # Get text and convert to single line
        extracted_text = extract_text_with_forms(uploaded_file)
        
        # Show success message with preview
        if extracted_text:
            st.success("PDF text extracted successfully!")
            with st.expander("Preview extracted text"):
                print(extracted_text)
                st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
        # Process button
        if st.button("Generate"):
            with st.spinner("Processing..."):
                # Call your API with single-line text
                result = call_visa_roadmap_api(extracted_text,roadmap_type,additional_info)
      #          print(result)

                if result:
                    # Display roadmap in main section
                    st.subheader("Your Immigration Roadmap")
                    with st.expander(label="Roadmap", expanded=True):
                        st.markdown(result["roadmap"])
                    
                    # Create expandable sections
                    with st.expander("CRS Score Details"):
                        st.markdown(result["crs_score"])
                    
                    with st.expander("Eligible Job Roles"):
                        st.markdown(result["job_roles"])
                    
                    with st.expander("NOC Codes"):
                        for noc in result["noc_codes"]:
                            st.markdown(noc)
                            st.markdown("---")

                    response = convert_dict_to_markdown(result)
                    pdf = MarkdownPdf()
                    pdf.add_section(Section(response, toc=False))
                    # Save PDF to memory (in BytesIO buffer)
                    pdf_output = io.BytesIO()
                    pdf.save(pdf_output)
                    # Seek to the beginning of the BytesIO buffer
                    pdf_output.seek(0)

                    st.download_button(
                        label="Download Report as PDF",
                        data=pdf_output,
                        file_name="immigration_assessment.pdf",
                        mime="application/pdf"
                    )

if roadmap_type != "Immigration Visa" and uploaded_file is not None:
    # Extract and process text
    with st.spinner("Extracting text from PDF..."):
        # Get text and convert to single line
        extracted_text = extract_text_with_forms(uploaded_file)
        
        # Show success message with preview
        if extracted_text:
            st.success("PDF text extracted successfully!")
            with st.expander("Preview extracted text"):
                st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
        # Process button
        if st.button("Generate"):
            with st.spinner("Processing..."):
                # Call your API with single-line text
                result = call_visa_roadmap_api(extracted_text,roadmap_type,additional_info)
                print(result)

                if result:
                    # Display roadmap in main section
                    st.subheader(f"Your {roadmap_type} Roadmap")
                    with st.expander(label="Roadmap", expanded=True):
                        st.markdown(result)
                    
                    # # Create expandable sections
                    # with st.expander("CRS Score Details"):
                    #     st.markdown(result["crs_score"])
                    
                    # with st.expander("Eligible Job Roles"):
                    #     st.markdown(result["job_roles"])
                    
                    # with st.expander("NOC Codes"):
                    #     for noc in result["noc_codes"]:
                    #         st.markdown(noc)
                    #         st.markdown("---")

                    pdf = MarkdownPdf()
                    pdf.add_section(Section(result, toc=False))
                    # Save PDF to memory (in BytesIO buffer)
                    pdf_output = io.BytesIO()
                    pdf.save(pdf_output)
                    # Seek to the beginning of the BytesIO buffer
                    pdf_output.seek(0)

                    st.download_button(
                        label="Download Report as PDF",
                        data=pdf_output,
                        file_name="immigration_assessment.pdf",
                        mime="application/pdf"
                    )

# Sidebar
with st.sidebar:
    st.header("How to Use")
    st.write("""
    1. Select your visa type
    2. Optional: Add extra information
    3. Upload questionnaire PDF
    4. Click 'Generate Roadmap'
    5. Review detailed roadmap sections
    6. Download your report as PDF
    """)