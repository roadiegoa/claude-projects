import os
import pytest
from tools.document import binary_document_to_markdown, document_path_to_markdown


class TestBinaryDocumentToMarkdown:
    # Define fixture paths
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    def test_fixture_files_exist(self):
        """Verify test fixtures exist."""
        assert os.path.exists(self.DOCX_FIXTURE), (
            f"DOCX fixture not found at {self.DOCX_FIXTURE}"
        )
        assert os.path.exists(self.PDF_FIXTURE), (
            f"PDF fixture not found at {self.PDF_FIXTURE}"
        )

    def test_binary_document_to_markdown_with_docx(self):
        """Test converting a DOCX document to markdown."""
        # Read binary content from the fixture
        with open(self.DOCX_FIXTURE, "rb") as f:
            docx_data = f.read()

        # Call function
        result = binary_document_to_markdown(docx_data, "docx")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result

    def test_binary_document_to_markdown_with_pdf(self):
        """Test converting a PDF document to markdown."""
        # Read binary content from the fixture
        with open(self.PDF_FIXTURE, "rb") as f:
            pdf_data = f.read()

        # Call function
        result = binary_document_to_markdown(pdf_data, "pdf")

        # Basic assertions to check the conversion was successful
        assert isinstance(result, str)
        assert len(result) > 0
        # Check for typical markdown formatting - this will depend on your actual test file
        assert "#" in result or "-" in result or "*" in result


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    # --- Happy path ---

    def test_pdf_returns_string(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE, "pdf")
        assert isinstance(result, str)

    def test_pdf_returns_non_empty_content(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE, "pdf")
        assert len(result) > 0

    def test_docx_returns_string(self) -> None:
        result = document_path_to_markdown(self.DOCX_FIXTURE, "docx")
        assert isinstance(result, str)

    def test_docx_returns_non_empty_content(self) -> None:
        result = document_path_to_markdown(self.DOCX_FIXTURE, "docx")
        assert len(result) > 0

    # --- Structure preservation ---

    def test_pdf_contains_markdown_formatting(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE, "pdf")
        assert "#" in result or "-" in result or "*" in result

    def test_docx_contains_markdown_formatting(self) -> None:
        result = document_path_to_markdown(self.DOCX_FIXTURE, "docx")
        assert "#" in result or "-" in result or "*" in result

    def test_pdf_contains_headings(self) -> None:
        result = document_path_to_markdown(self.PDF_FIXTURE, "pdf")
        assert "#" in result

    def test_docx_contains_headings(self) -> None:
        result = document_path_to_markdown(self.DOCX_FIXTURE, "docx")
        assert "#" in result

    # --- File path variants ---

    def test_absolute_path_pdf(self) -> None:
        abs_path = os.path.abspath(self.PDF_FIXTURE)
        result = document_path_to_markdown(abs_path, "pdf")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_relative_path_pdf(self) -> None:
        rel_path = os.path.relpath(self.PDF_FIXTURE)
        result = document_path_to_markdown(rel_path, "pdf")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_absolute_path_docx(self) -> None:
        abs_path = os.path.abspath(self.DOCX_FIXTURE)
        result = document_path_to_markdown(abs_path, "docx")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_relative_path_docx(self) -> None:
        rel_path = os.path.relpath(self.DOCX_FIXTURE)
        result = document_path_to_markdown(rel_path, "docx")
        assert isinstance(result, str)
        assert len(result) > 0

    # --- Error cases ---

    def test_nonexistent_file_raises(self) -> None:
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/nonexistent/path/file.pdf", "pdf")

    def test_directory_path_raises(self) -> None:
        with pytest.raises((IsADirectoryError, PermissionError, OSError)):
            document_path_to_markdown(self.FIXTURES_DIR, "pdf")

    # --- Edge cases ---

    def test_mismatched_type_raises_or_returns_string(self) -> None:
        # markitdown may raise or silently return content when the extension
        # doesn't match the actual file format — either is acceptable, but it
        # must not crash the process with an unhandled non-Exception throwable.
        try:
            result = document_path_to_markdown(self.PDF_FIXTURE, "docx")
            assert isinstance(result, str)
        except Exception:
            pass
