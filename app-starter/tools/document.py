from io import BytesIO
from pathlib import Path
from typing import Literal

from markitdown import MarkItDown, StreamInfo
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to the PDF or DOCX file to convert"),
    file_type: Literal["pdf", "docx"] = Field(description="Format of the file: 'pdf' or 'docx'"),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path and returns its content as markdown.
    Delegates conversion to markitdown, which extracts text and structure
    from the document.

    When to use:
    - When you have a local file path and need its content as markdown
    - When processing PDF or DOCX documents for further analysis

    When not to use:
    - When you already have the file contents as bytes (use binary_document_to_markdown instead)
    - For file formats other than PDF or DOCX

    Examples:
    >>> document_path_to_markdown("/path/to/report.pdf", "pdf")
    "# Report Title\\n\\nContent..."
    >>> document_path_to_markdown("/path/to/doc.docx", "docx")
    "# Document Title\\n\\nContent..."
    """
    data = Path(file_path).read_bytes()
    return binary_document_to_markdown(data, file_type)
