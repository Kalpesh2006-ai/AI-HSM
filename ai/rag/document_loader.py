from pathlib import Path
import fitz
import pytesseract

from langchain_core.documents import Document
from PIL import Image

from ai.rag.config import DOCUMENTS_PATH


# Government schemes currently supported
KNOWN_GOVERNMENT_SCHEMES = {
    "mudra",
    "pmegp",
    "pm_vishwakarma",
    "pmfme",
    "day_nrlm",
    "cgtmse",
    "maharashtra_schemes"
}


# Future knowledge-base categories
KNOWN_CATEGORIES = {
    "entrepreneurship",
    "digital_skills",
    "digital_marketing",
    "financial_literacy",
    "business_compliance",
    "maharashtra"
}


# Tesseract installation path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def get_knowledge_metadata(file_path):
    """
    Determine the category and topic of a document
    from its folder structure.

    Current structure:
        documents/
            mudra/
            pmegp/

    Future structure can be:
        documents/
            entrepreneurship/
                business_planning/
            digital_skills/
                digital_payments/
    """

    relative_path = file_path.relative_to(
        Path(DOCUMENTS_PATH)
    )

    parts = relative_path.parts

    if not parts:
        return {
            "category": "unknown",
            "topic": "unknown",
            "scheme": "unknown"
        }

    first_folder = parts[0]

    # Current government-scheme structure
    if first_folder in KNOWN_GOVERNMENT_SCHEMES:

        return {
            "category": "government_scheme",
            "topic": first_folder,
            "scheme": first_folder
        }

    # Future general knowledge structure
    if first_folder in KNOWN_CATEGORIES:

        topic = (
            parts[1]
            if len(parts) > 1
            else first_folder
        )

        return {
            "category": first_folder,
            "topic": topic,
            "scheme": "none"
        }

    return {
        "category": "other",
        "topic": first_folder,
        "scheme": "none"
    }


def load_documents():

    documents = []

    documents_path = Path(DOCUMENTS_PATH)

    if not documents_path.exists():

        print(
            f"Documents directory not found: "
            f"{documents_path}"
        )

        return documents

    for file_path in documents_path.rglob("*"):

        if not file_path.is_file():
            continue

        knowledge_metadata = get_knowledge_metadata(
            file_path
        )

        # -------------------------------------------------
        # PDF FILES
        # -------------------------------------------------

        if file_path.suffix.lower() == ".pdf":

            try:

                pdf = fitz.open(file_path)

                for page_number, page in enumerate(
                    pdf,
                    start=1
                ):

                    text = page.get_text().strip()

                    # If normal PDF extraction fails,
                    # use OCR.
                    if not text:

                        pix = page.get_pixmap(
                            matrix=fitz.Matrix(2, 2)
                        )

                        image = Image.frombytes(
                            "RGB",
                            [
                                pix.width,
                                pix.height
                            ],
                            pix.samples
                        )

                        text = pytesseract.image_to_string(
                            image
                        ).strip()

                    if not text:
                        continue

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": str(file_path),
                                "page": page_number,
                                "category":
                                    knowledge_metadata[
                                        "category"
                                    ],
                                "topic":
                                    knowledge_metadata[
                                        "topic"
                                    ],
                                "scheme":
                                    knowledge_metadata[
                                        "scheme"
                                    ]
                            }
                        )
                    )

                pdf.close()

            except Exception as error:

                print(
                    f"Error reading PDF "
                    f"{file_path}: {error}"
                )

        # -------------------------------------------------
        # TEXT FILES
        # -------------------------------------------------

        elif file_path.suffix.lower() == ".txt":

            try:

                text = file_path.read_text(
                    encoding="utf-8"
                ).strip()

                if text:

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": str(file_path),
                                "page": 1,
                                "category":
                                    knowledge_metadata[
                                        "category"
                                    ],
                                "topic":
                                    knowledge_metadata[
                                        "topic"
                                    ],
                                "scheme":
                                    knowledge_metadata[
                                        "scheme"
                                    ]
                            }
                        )
                    )

            except Exception as error:

                print(
                    f"Error reading TXT "
                    f"{file_path}: {error}"
                )

    print(
        f"Total documents/pages loaded: "
        f"{len(documents)}"
    )

    return documents