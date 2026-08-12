# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run main.py          # Start the MCP server
uv run pytest           # Run all tests
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx  # Run a single test
```

## Architecture

This is an MCP server built with `fastmcp`. The entry point is `main.py`, which instantiates a `FastMCP` server and registers tools by calling `mcp.tool()(fn)` for each function.

Tools live in the `tools/` package as plain Python functions — they are not coupled to MCP directly. `main.py` is the only place that wires functions into the server. `tools/document.py` contains document-processing helpers (using `markitdown`); `tools/math.py` contains the example `add` tool.

## Defining MCP Tools

Tools are plain Python functions registered in `main.py`:

```python
mcp.tool()(my_function)
```

Use `Field` from pydantic for parameter descriptions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - ...

    Examples:
    >>> my_tool("foo", 42)
    "result"
    """
```

Docstrings are surfaced to the AI as the tool description, so they should explain what the tool does, when to use it (and when not to), and include concrete examples.
