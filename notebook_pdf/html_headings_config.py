"""Export HTML headings as Markdown without modifying the source notebook.

Usage: python -m jupyter nbconvert --config notebook_pdf/html_headings_config.py ...
Handles standalone h1–h6 headings in Markdown cells; preserves fenced examples.
"""

import re

from nbconvert.preprocessors import Preprocessor


class HtmlHeadingsToMarkdown(Preprocessor):
    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type != "markdown":
            return cell, resources

        lines = []
        fence = None
        for line in cell.source.splitlines(keepends=True):
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if fence is not None:
                lines.append(line)
                if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not line[marker.end():].strip():
                    fence = None
                continue
            if marker:
                fence = marker[1]
                lines.append(line)
                continue

            heading = re.fullmatch(
                r" {0,3}<h([1-6])(?:\s+[^>]*)?>(.*?)</h\1>\s*",
                line,
                flags=re.IGNORECASE,
            )
            if heading:
                lines.append("\n" + "#" * int(heading[1]) + " " + heading[2].strip() + "\n\n")
            else:
                lines.append(line)

        cell.source = "".join(lines)
        return cell, resources


c = get_config()  # noqa: F821 — provided by Jupyter's config loader
c.Exporter.preprocessors.append(HtmlHeadingsToMarkdown)
