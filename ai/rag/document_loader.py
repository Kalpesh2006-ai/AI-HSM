
from pathlib import Path

import fitz
import pytesseract

from langchain_core.documents import Document
from PIL import Image

from ai.rag.config import DOCUMENTS_PATH


# Government schemes with dedicated folders
KNOWN_GOVERNMENT_SCHEMES = {
    "mudra",
    "pmegp",
    "pm_vishwakarma",
    "pmfme",
    "day_nrlm",
    "cgtmse",
    "maharashtra_schemes",
}


# General knowledge categories in the documents directory
KNOWN_CATEGORIES = {
    "entrepreneurship",
    "digital_skills",
    "digital_marketing",
    "financial_literacy",
    "business_compliance",
    "cybersecurity",
    "other_government_schemes",
    "maharashtra",
}


# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def get_knowledge_metadata(file_path):
    """
    Determine category, topic, and scheme from the folder structure.

    Expected structure:
        documents/
            mudra/
            pmegp/
            day_nrlm/
            maharashtra_schemes/
            digital_skills/
                digital_payments/
                aadhaar_and_digital_identity/
            business_compliance/
                gst/
                income_tax/
                udyam/
            cybersecurity/
            financial_literacy/
            other_government_schemes/
    """

    documents_root = Path(DOCUMENTS_PATH).resolve()
    file_path = Path(file_path).resolve()

    try:
        relative_path = file_path.relative_to(documents_root)
    except ValueError:
        return {
            "category": "unknown",
            "topic": "unknown",
            "scheme": "none",
        }

    parts = relative_path.parts

    if not parts:
        return {
            "category": "unknown",
            "topic": "unknown",
            "scheme": "none",
        }

    first_folder = parts[0].lower()

    # Dedicated government scheme folders
    if first_folder in KNOWN_GOVERNMENT_SCHEMES:
        return {
            "category": "government_scheme",
            "topic": first_folder,
            "scheme": first_folder,
        }

    # General knowledge categories
    if first_folder in KNOWN_CATEGORIES:
        topic = (
            parts[1].lower()
            if len(parts) > 1
            else first_folder
        )

        return {
            "category": first_folder,
            "topic": topic,
            "scheme": "none",
        }

    # Handle unrecognized top-level folders
    return {
        "category": "other",
        "topic": first_folder,
        "scheme": "none",
    }


def extract_pdf_pages(file_path):
    """
    Extract text from each PDF page.
    Use OCR when a page has no extractable text.
    Return one Document per page.
    """

    documents = []
    knowledge_metadata = get_knowledge_metadata(file_path)

    try:
        with fitz.open(file_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text().strip()

                # OCR fallback for scanned pages
                if not text:
                    try:
                        pix = page.get_pixmap(
                            matrix=fitz.Matrix(2, 2),
                            alpha=False,
                        )

                        image = Image.frombytes(
                            "RGB",
                            (pix.width, pix.height),
                            pix.samples,
                        )

                        text = pytesseract.image_to_string(
                            image
                        ).strip()

                    except Exception as error:
                        print(
                            f"OCR failed for {file_path}, "
                            f"page {page_number}: {error}"
                        )
                        continue

                if not text:
                    print(
                        f"No text extracted from "
                        f"{file_path}, page {page_number}"
                    )
                    continue

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": str(Path(file_path)),
                            "page": page_number,
                            **knowledge_metadata,
                        },
                    )
                )

    except Exception as error:
        print(f"Error reading PDF {file_path}: {error}")

    return documents


def extract_txt_file(file_path):
    """
    Extract text from a TXT file.
    Return one Document for the file.
    """

    try:
        text = Path(file_path).read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            return []

        return [
            Document(
                page_content=text,
                metadata={
                    "source": str(Path(file_path)),
                    "page": 1,
                    **get_knowledge_metadata(file_path),
                },
            )
        ]

    except Exception as error:
        print(f"Error reading TXT {file_path}: {error}")
        return []


def load_documents():
    """
    Recursively discover PDF and TXT files in DOCUMENTS_PATH.
    Supports files in all nested category folders.
    """

    documents = []
    documents_path = Path(DOCUMENTS_PATH)

    if not documents_path.exists():
        print(
            f"Documents directory not found: "
            f"{documents_path.resolve()}"
        )
        return documents

    # Sort paths for predictable loading order
    files = sorted(
        path
        for path in documents_path.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".pdf", ".txt"}
    )

    print(f"Documents directory: {documents_path.resolve()}")
    print(f"PDF/TXT files discovered: {len(files)}")

    for file_path in files:
        if file_path.suffix.lower() == ".pdf":
            documents.extend(extract_pdf_pages(file_path))

        elif file_path.suffix.lower() == ".txt":
            documents.extend(extract_txt_file(file_path))

    print(f"Total documents/pages loaded: {len(documents)}")

    return documents
