
from dotenv import load_dotenv

from utils.document_utils import (
    format_docx,
    format_pdf,
    format_html_preview,
    sanitize_text
)


# Load environment variables
load_dotenv()


# Backend URL
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "https://legalease-backend-d19f.onrender.com"
)


# Logo path
LOGO_PATH = os.path.join(
    PROJECT_ROOT,
    "assets",
    "logo.png"
)


# Streamlit page configuration
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# Custom styling
st.markdown(
    """
    <style>

    .legal-card {
        background-color: #111827;
        color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #374151;
        line-height: 1.7;
        max-height: 600px;
        overflow-y: auto;
    }

    .main-title {
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True
)

import os
import sys
from datetime import date

# Add project root to Python path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import requests
import streamlit as st
# -----------------------------
# HEADER
# -----------------------------

left, center, right = st.columns([1, 2, 1])

with center:

    if os.path.exists(LOGO_PATH):

        st.image(
            LOGO_PATH,
            width=100
        )

    st.title("LegalEase")

    st.caption(
        "AI-Powered Legal Document Generator"
    )


st.info(
    "LegalEase creates draft legal documents "
    "from your inputs. Review generated content "
    "carefully before real-world use."
)


# -----------------------------
# INPUT SECTION
# -----------------------------

st.header("Create Legal Document")


document_type = st.text_input(
    "Document Type",
    placeholder="Example: Freelance Work Contract"
)


parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example: Jane Doe (Service Provider), "
        "TechNova Inc. (Client)"
    ),
    height=100
)


terms = st.text_area(
    "Terms & Conditions",
    placeholder=(
        "Example: Payment within 30 days; "
        "Confidentiality must be maintained; "
        "Contract duration is one year"
    ),
    height=150
)


effective_date = st.text_input(
    "Effective Date",
    value=date.today().strftime("%B %d, %Y")
)


# -----------------------------
# GENERATE BUTTON
# -----------------------------

if st.button(
    "Generate Document",
    type="primary",
    use_container_width=True
):

    missing_fields = []

    if not document_type.strip():

        missing_fields.append(
            "Document Type"
        )

    if not parties.strip():

        missing_fields.append(
            "Parties Involved"
        )

    if not terms.strip():

        missing_fields.append(
            "Terms & Conditions"
        )

    if not effective_date.strip():

        missing_fields.append(
            "Effective Date"
        )


    # Check missing fields
    if missing_fields:

        st.error(
            "Please fill in: "
            + ", ".join(missing_fields)
        )


    else:

        try:

            with st.spinner(
                "Generating legal document..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": effective_date
                    },

                    timeout=120
                )


                response.raise_for_status()


                result = response.json()


                # Store generated document
                st.session_state[
                    "document_text"
                ] = result["text"]


                st.success(
                    "Document generated successfully!"
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend."
            )

            st.info(
                "Please make sure Terminal 1 "
                "is running the FastAPI server."
            )


        except requests.exceptions.Timeout:

            st.error(
                "The request took too long. "
                "Please try again."
            )


        except requests.exceptions.RequestException as error:

            st.error(
                f"Backend error: {error}"
            )


        except Exception as error:

            st.error(
                f"Unexpected error: {error}"
            )


# -----------------------------
# GENERATED DOCUMENT
# -----------------------------

if "document_text" in st.session_state:

    st.divider()

    st.header(
        "Generated Document"
    )


    document_text = st.session_state[
        "document_text"
    ]


    # Preview
    html_preview = format_html_preview(
        document_text
    )


    st.markdown(
        f"""
        <div class="legal-card">
            {html_preview}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -----------------------------
    # EDIT DOCUMENT
    # -----------------------------

    st.subheader(
        "Edit Document"
    )


    edited_text = st.text_area(

        "Modify your document here:",

        value=document_text,

        height=450
    )


    st.session_state[
        "document_text"
    ] = edited_text


    # -----------------------------
    # PREPARE DOWNLOAD FILES
    # -----------------------------

    clean_text = sanitize_text(
        edited_text
    )


    docx_data = format_docx(

        clean_text,

        document_type,

        LOGO_PATH
    )


    pdf_data = format_pdf(

        clean_text,

        document_type,

        LOGO_PATH
    )


    # -----------------------------
    # SAFE FILE NAME
    # -----------------------------

    safe_name = "".join(

        character

        if character.isalnum()
        or character in " _-"

        else "_"

        for character in document_type

    ).strip()


    if not safe_name:

        safe_name = "legal_document"


    # -----------------------------
    # DOWNLOAD SECTION
    # -----------------------------

    st.subheader(
        "Download Document"
    )


    col1, col2, col3 = st.columns(3)


    # TXT
    with col1:

        st.download_button(

            label="Download TXT",

            data=clean_text.encode(
                "utf-8"
            ),

            file_name=f"{safe_name}.txt",

            mime="text/plain",

            use_container_width=True
        )


    # DOCX
    with col2:

        st.download_button(

            label="Download DOCX",

            data=docx_data,

            file_name=f"{safe_name}.docx",

            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),

            use_container_width=True
        )


    # PDF
    with col3:

        st.download_button(

            label="Download PDF",

            data=pdf_data,

            file_name=f"{safe_name}.pdf",

            mime="application/pdf",

            use_container_width=True
        )


# -----------------------------
# FOOTER
# -----------------------------

st.divider()


st.caption(
    "LegalEase | "
    "Streamlit → FastAPI → Gemini → "
    "Document Generation → Export"
)