from __future__ import annotations

import asyncio
import tempfile
import uuid
from pathlib import Path
from typing import Any

from amplifier_core.models import ToolResult


class CanvasRendererTool:
    """Converts Markdown content to DOCX or PDF using pandoc."""

    @property
    def name(self) -> str:
        return "render_document"

    @property
    def description(self) -> str:
        return (
            "Converts Markdown content to a formatted document file (docx or pdf) "
            "using pandoc. Provide the raw Markdown as 'content' and the target "
            "format as 'output_format'. Returns the absolute path to the output file. "
            "Use after the writer specialist to produce a deliverable document."
        )

    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "Markdown content to convert (e.g. writer specialist output).",
                },
                "output_format": {
                    "type": "string",
                    "enum": ["docx", "pdf"],
                    "description": "Target format. 'docx' works out of the box. "
                    "'pdf' requires a LaTeX engine installed.",
                    "default": "docx",
                },
                "output_filename": {
                    "type": "string",
                    "description": "Optional output filename without extension. "
                    "A unique name is generated if omitted.",
                },
            },
            "required": ["content"],
        }

    async def execute(self, input: dict[str, Any]) -> ToolResult:
        content = input.get("content")
        if not content:
            return ToolResult(
                success=False,
                error={"message": "'content' is required", "type": "ValueError"},
            )

        output_format = input.get("output_format", "docx")
        stem = input.get("output_filename") or f"document-{uuid.uuid4().hex[:8]}"

        try:
            output_path = await self._run_pandoc(content, output_format, stem)
            return ToolResult(
                success=True,
                output={
                    "output_path": str(output_path),
                    "format": output_format,
                    "filename": output_path.name,
                    "size_bytes": output_path.stat().st_size,
                },
            )
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error={
                    "message": "pandoc not found. Install with: brew install pandoc",
                    "type": "FileNotFoundError",
                },
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error={"message": str(e), "type": type(e).__name__},
            )

    async def _run_pandoc(self, content: str, output_format: str, stem: str) -> Path:
        output_dir = Path(tempfile.gettempdir())
        output_path = output_dir / f"{stem}.{output_format}"

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(content)
            input_path = fh.name

        proc = await asyncio.create_subprocess_exec(
            "pandoc",
            input_path,
            "--from",
            "markdown",
            "--to",
            output_format,
            "--output",
            str(output_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await proc.communicate()

        if proc.returncode != 0:
            raise RuntimeError(
                f"pandoc exited {proc.returncode}: {stderr.decode().strip()}"
            )

        return output_path


async def mount(coordinator, config: dict):
    tool = CanvasRendererTool()
    await coordinator.mount("tools", tool, name=tool.name)
    return tool
