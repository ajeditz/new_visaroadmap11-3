# import streamlit as st
# import requests
# import io
# from markdown_pdf import MarkdownPdf, Section

# def extract_text_from_pdf(pdf_file):
#     """
#     Extract text from PDF using RapidAPI and convert it to a single line
    
#     Args:
#         pdf_file: The uploaded PDF file
#     Returns:
#         str: Extracted text in a single line with proper spacing
#     """
#     url = "https://ocr-text-extraction.p.rapidapi.com/v1/ocr/"
    
#     headers = {
#         "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
#         "X-RapidAPI-Host": "ocr-text-extraction.p.rapidapi.com"
#     }
    
#     try:
#         pdf_bytes = pdf_file.getvalue()
        
#         response = requests.post(
#             url,
#             headers=headers,
#             files={"pdf": pdf_bytes}
#         )
        
#         if response.status_code == 200:
#             extracted_text = response.json().get('text', '')
#             single_line_text = " ".join(extracted_text.split())
#             return single_line_text
#         else:
#             return fallback_extract_text(pdf_file)
            
#     except Exception as e:
#         st.warning("Using fallback PDF extraction method")
#         return fallback_extract_text(pdf_file)

# def fallback_extract_text(pdf_file):
#     """
#     Fallback method to extract text using PyPDF2 if RapidAPI fails
    
#     Args:
#         pdf_file: The uploaded PDF file
#     Returns:
#         str: Extracted text in a single line
#     """
#     try:
#         import PyPDF2
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         text = ""
        
#         for page in pdf_reader.pages:
#             text += page.extract_text()
        
#         single_line_text = " ".join(text.split()).strip()
#         return single_line_text
#     except Exception as e:
#         st.error(f"Error in text extraction: {str(e)}")
#         return ""

# def call_visa_roadmap_api(text, roadmap_type, additional_information):
#     """
#     Call visa roadmap API with the single-line text
    
#     Args:
#         text (str): Single-line text from PDF
#         roadmap_type (str): Type of visa roadmap requested
#         additional_information (str): Any additional information provided
#     Returns:
#         dict: API response with roadmap data
#     """
#     # url = "https://latestvisaroadmap-247572588539.us-central1.run.app/generate_roadmap"
#     url = "http://127.0.0.1:8000/generate_roadmap"
#     try:
#         payload = {
#             "questionnaire": text,
#             "roadmap_type": roadmap_type,
#             "additional_information": additional_information
#         }

#         response = requests.post(url, params=payload)

#         if response.status_code == 200:
#             return response.json()
#         elif response.status_code == 404:
#             st.error(f"API Error: Data Not Found ({response.status_code})")
#         else:
#             st.error(f"API Error: {response.status_code}")
#             return None    
#     except Exception as e:
#         st.error(f"API Error: {str(e)}")
#         return None

# def convert_dict_to_markdown(data):
#     """
#     Convert the given dictionary into a Markdown-formatted string for UI display.
    
#     Args:
#         data: Dictionary containing the structured information
#     Returns:
#         str: A Markdown-formatted string
#     """
#     markdown_content = []

#     markdown_content.append("# Immigration Profile Report\n")
    
#     markdown_content.append("## 1. Questionnaire and Response:\n")
#     questionnaire = data.get('questionnaire', '')
#     for line in questionnaire.split('●'):
#         if line.strip():
#             markdown_content.append(f"- {line.strip()}\n")
    
#     markdown_content.append("## 2. Job Roles Based on Education and Work Experience:\n")
#     markdown_content.append(f"{data.get('job_roles', '')}\n")
    
#     markdown_content.append("## 3. NOC Codes:\n")
#     for noc in data.get('noc_codes', []):
#         markdown_content.append(f"- {noc.strip()}\n")
    
#     markdown_content.append("## 4. CRS Score Breakdown:\n")
#     markdown_content.append(f"{data.get('crs_score', '')}\n")
    
#     markdown_content.append("## 5. Roadmap for Canada Immigration:\n")
#     markdown_content.append(f"{data.get('roadmap', '')}\n")
    
#     return "\n".join(markdown_content)

# def create_pdf_content(data):
#     """
#     Create Markdown content for PDF that only includes the roadmap.
    
#     Args:
#         data: Dictionary containing the structured information
#     Returns:
#         str: A Markdown-formatted string with only the roadmap
#     """
#     if isinstance(data, dict):
#         markdown_content = []
#         markdown_content.append("# Immigration Roadmap\n")
#         markdown_content.append(f"{data.get('roadmap', '')}\n")
#         return "\n".join(markdown_content)
#     else:
#         # For non-Immigration visa types where data is a string
#         return f"# {roadmap_type} Roadmap\n\n{data}"

# # Set up Streamlit page
# st.set_page_config(page_title="Visa Roadmap Assistant", layout="wide")
# st.title("Visa Roadmap Assistant")

# # Check if RapidAPI key is configured
# if 'RAPIDAPI_KEY' not in st.secrets:
#     st.error("Please configure your RapidAPI key in .streamlit/secrets.toml")
#     st.stop()

# # Visa type selection
# roadmap_type = st.selectbox(
#     "Select Visa Type:",
#     ["Immigration Visa", "Study Visa", "Travel Visa", "Work Visa"],
#     index=None,
#     placeholder="Select Visa Type"
# )

# # Additional information input
# additional_info = st.text_area("Additional Information (Optional)")

# # File upload section
# uploaded_file = st.file_uploader("Upload your questionnaire PDF", type="pdf")

# # Handle Immigration Visa type
# if roadmap_type == "Immigration Visa" and uploaded_file is not None:
#     with st.spinner("Extracting text from PDF..."):
#         extracted_text = extract_text_from_pdf(uploaded_file)
        
#         if extracted_text:
#             st.success("PDF text extracted successfully!")
#             with st.expander("Preview extracted text"):
#                 st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
#         if st.button("Generate"):
#             with st.spinner("Processing..."):
#                 result = call_visa_roadmap_api(extracted_text, roadmap_type, additional_info)

#                 if result:
#                     # Display full report in UI
#                     st.subheader("Your Immigration Roadmap")
#                     with st.expander(label="Roadmap", expanded=True):
#                         st.markdown(result["roadmap"])
                    
#                     with st.expander("CRS Score Details"):
#                         st.markdown(result["crs_score"])
                    
#                     with st.expander("Eligible Job Roles"):
#                         st.markdown(result["job_roles"])
                    
#                     with st.expander("NOC Codes"):
#                         for noc in result["noc_codes"]:
#                             st.markdown(noc)
#                             st.markdown("---")

#                     # Generate PDF with roadmap only
#                     pdf_content = create_pdf_content(result)
#                     pdf = MarkdownPdf()
#                     pdf.add_section(Section(pdf_content, toc=False))
#                     pdf_output = io.BytesIO()
#                     pdf.save(pdf_output)
#                     pdf_output.seek(0)

#                     st.download_button(
#                         label="Download Roadmap as PDF",
#                         data=pdf_output,
#                         file_name="immigration_roadmap.pdf",
#                         mime="application/pdf"
#                     )

# # Handle other visa types
# if roadmap_type != "Immigration Visa" and roadmap_type is not None and uploaded_file is not None:
#     with st.spinner("Extracting text from PDF..."):
#         extracted_text = extract_text_from_pdf(uploaded_file)
        
#         if extracted_text:
#             st.success("PDF text extracted successfully!")
#             with st.expander("Preview extracted text"):
#                 st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
#         if st.button("Generate"):
#             with st.spinner("Processing..."):
#                 result = call_visa_roadmap_api(extracted_text, roadmap_type, additional_info)

#                 if result:
#                     st.subheader(f"Your {roadmap_type} Roadmap")
#                     with st.expander(label="Roadmap", expanded=True):
#                         st.markdown(result)

#                     # Generate PDF with roadmap only
#                     pdf_content = create_pdf_content(result)
#                     pdf = MarkdownPdf()
#                     pdf.add_section(Section(pdf_content, toc=False))
#                     pdf_output = io.BytesIO()
#                     pdf.save(pdf_output)
#                     pdf_output.seek(0)

#                     st.download_button(
#                         label="Download Roadmap as PDF",
#                         data=pdf_output,
#                         file_name=f"{roadmap_type.lower()}_roadmap.pdf",
#                         mime="application/pdf"
#                     )

# # Sidebar
# with st.sidebar:
#     st.header("How to Use")
#     st.write("""
#     1. Select your visa type
#     2. Optional: Add extra information
#     3. Upload questionnaire PDF
#     4. Click 'Generate Roadmap'
#     5. Review detailed roadmap sections
#     6. Download your roadmap as PDF
#     """)

import streamlit as st
import requests
import io
from markdown_pdf import MarkdownPdf, Section

def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF using RapidAPI and convert it to a single line
    
    Args:
        pdf_file: The uploaded PDF file
    Returns:
        str: Extracted text in a single line with proper spacing
    """
    url = "https://ocr-text-extraction.p.rapidapi.com/v1/ocr/"
    
    headers = {
        "X-RapidAPI-Key": st.secrets["RAPIDAPI_KEY"],
        "X-RapidAPI-Host": "ocr-text-extraction.p.rapidapi.com"
    }
    
    try:
        pdf_bytes = pdf_file.getvalue()
        
        response = requests.post(
            url,
            headers=headers,
            files={"pdf": pdf_bytes}
        )
        
        if response.status_code == 200:
            extracted_text = response.json().get('text', '')
            single_line_text = " ".join(extracted_text.split())
            return single_line_text
        else:
            return fallback_extract_text(pdf_file)
            
    except Exception as e:
        st.warning("Using fallback PDF extraction method")
        return fallback_extract_text(pdf_file)

def fallback_extract_text(pdf_file):
    """
    Fallback method to extract text using PyPDF2 if RapidAPI fails
    
    Args:
        pdf_file: The uploaded PDF file
    Returns:
        str: Extracted text in a single line
    """
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        single_line_text = " ".join(text.split()).strip()
        return single_line_text
    except Exception as e:
        st.error(f"Error in text extraction: {str(e)}")
        return ""

def call_visa_roadmap_api(text, roadmap_type, additional_information):
    """
    Call visa roadmap API with the single-line text
    
    Args:
        text (str): Single-line text from PDF
        roadmap_type (str): Type of visa roadmap requested
        additional_information (str): Any additional information provided
    Returns:
        dict: API response with roadmap data
    """
<<<<<<< HEAD
    url = "http://127.0.0.1:8000/generate_roadmap"
=======
    url = "https://latestvisaroadmap-247572588539.us-central1.run.app/generate_roadmap"
    # url = "http://127.0.0.1:8000/generate_roadmap"
>>>>>>> 028f3bb691e854a26d08474f07da18f783a29e59
    try:
        payload = {
            "questionnaire": text,
            "roadmap_type": roadmap_type,
            "additional_information": additional_information
        }

        response = requests.post(url, params=payload)

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

def format_roadmap_text(text):
    """
    Format roadmap text with numbered main points and bulleted sub-points
    
    Args:
        text (str): Raw roadmap text
    Returns:
        str: Formatted text with correct numbering and bullets
    """
    lines = text.split('\n')
    formatted_lines = []
    current_number = 0
    is_subpoint = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line is a main point (starts with "Main" or certain keywords)
        if (line.lower().startswith('main') or 
            line.lower().startswith('step') or 
            line.lower().startswith('process') or
            (line[0].isdigit() and '.' in line[:3])):
            
            current_number += 1
            is_subpoint = False
            formatted_lines.append(f"\n{current_number}. {line.split('.', 1)[-1].strip()}")
        
        # Check if line is a sub-point
        elif (line.startswith('•') or line.startswith('-') or 
              line.startswith('*') or line.startswith('>')):
            is_subpoint = True
            # Indent sub-points with 3 spaces for better formatting
            formatted_lines.append(f"   - {line.lstrip('•-*> ')}")
        
        # Handle continuation of sub-points or additional information
        else:
            if is_subpoint:
                formatted_lines.append(f"   - {line}")
            else:
                # If it's not clearly a sub-point, make it a new main point
                current_number += 1
                formatted_lines.append(f"\n{current_number}. {line}")
    
    return '\n'.join(formatted_lines)

def create_pdf_content(data):
    """
    Create Markdown content for PDF with proper formatting.
    
    Args:
        data: Dictionary containing the structured information
    Returns:
        str: A properly formatted Markdown string
    """
    if isinstance(data, dict):
        markdown_content = []
        markdown_content.append("# Immigration Roadmap\n")
        
        # Add a brief introduction if available
        if 'introduction' in data:
            markdown_content.append(f"{data['introduction']}\n")
        
        # Format the roadmap content
        roadmap_text = data.get('roadmap', '')
        formatted_roadmap = format_roadmap_text(roadmap_text)
        markdown_content.append(formatted_roadmap)
        
        # Add any additional notes or summary if available
        if 'notes' in data:
            markdown_content.append(f"\n## Additional Notes\n{data['notes']}")
        
        return '\n'.join(markdown_content)
    else:
        # For non-Immigration visa types where data is a string
        return f"# {roadmap_type} Roadmap\n\n{format_roadmap_text(data)}"

def convert_dict_to_markdown(data):
    """
    Convert the given dictionary into a Markdown-formatted string for UI display.
    
    Args:
        data: Dictionary containing the structured information
    Returns:
        str: A Markdown-formatted string
    """
    markdown_content = []

    markdown_content.append("# Immigration Profile Report\n")
    
    markdown_content.append("## 1. Questionnaire and Response:\n")
    questionnaire = data.get('questionnaire', '')
    for line in questionnaire.split('●'):
        if line.strip():
            markdown_content.append(f"- {line.strip()}\n")
    
    markdown_content.append("## 2. Job Roles Based on Education and Work Experience:\n")
    markdown_content.append(f"{data.get('job_roles', '')}\n")
    
    markdown_content.append("## 3. NOC Codes:\n")
    for noc in data.get('noc_codes', []):
        markdown_content.append(f"- {noc.strip()}\n")
    
    markdown_content.append("## 4. CRS Score Breakdown:\n")
    markdown_content.append(f"{data.get('crs_score', '')}\n")
    
    markdown_content.append("## 5. Roadmap for Canada Immigration:\n")
    markdown_content.append(f"{data.get('roadmap', '')}\n")
    
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

# Handle Immigration Visa type
if roadmap_type == "Immigration Visa" and uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)
        
        if extracted_text:
            st.success("PDF text extracted successfully!")
            with st.expander("Preview extracted text"):
                st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
        if st.button("Generate"):
            with st.spinner("Processing..."):
                result = call_visa_roadmap_api(extracted_text, roadmap_type, additional_info)

                if result:
                    # Display full report in UI
                    st.subheader("Your Immigration Roadmap")
                    with st.expander(label="Roadmap", expanded=True):
                        st.markdown(result["roadmap"])
                    
                    with st.expander("CRS Score Details"):
                        st.markdown(result["crs_score"])
                    
                    with st.expander("Eligible Job Roles"):
                        st.markdown(result["job_roles"])
                    
                    with st.expander("NOC Codes"):
                        for noc in result["noc_codes"]:
                            st.markdown(noc)
                            st.markdown("---")

                    # Generate PDF with roadmap only
                    pdf_content = create_pdf_content(result)
                    pdf = MarkdownPdf()
                    pdf.add_section(Section(pdf_content, toc=False))
                    pdf_output = io.BytesIO()
                    pdf.save(pdf_output)
                    pdf_output.seek(0)

                    st.download_button(
                        label="Download Roadmap as PDF",
                        data=pdf_output,
                        file_name="immigration_roadmap.pdf",
                        mime="application/pdf"
                    )

# Handle other visa types
if roadmap_type != "Immigration Visa" and roadmap_type is not None and uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        extracted_text = extract_text_from_pdf(uploaded_file)
        
        if extracted_text:
            st.success("PDF text extracted successfully!")
            with st.expander("Preview extracted text"):
                st.text(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
        if st.button("Generate"):
            with st.spinner("Processing..."):
                result = call_visa_roadmap_api(extracted_text, roadmap_type, additional_info)

                if result:
                    st.subheader(f"Your {roadmap_type} Roadmap")
                    with st.expander(label="Roadmap", expanded=True):
                        st.markdown(result)

                    # Generate PDF with roadmap only
                    pdf_content = create_pdf_content(result)
                    pdf = MarkdownPdf()
                    pdf.add_section(Section(pdf_content, toc=False))
                    pdf_output = io.BytesIO()
                    pdf.save(pdf_output)
                    pdf_output.seek(0)

                    st.download_button(
                        label="Download Roadmap as PDF",
                        data=pdf_output,
                        file_name=f"{roadmap_type.lower()}_roadmap.pdf",
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
    6. Download your roadmap as PDF
    """)