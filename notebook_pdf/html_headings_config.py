"""Export HTML headings and unordered lists as Markdown.

Usage: python -m jupyter nbconvert --config notebook_pdf/html_headings_config.py ...
Handles standalone h1–h6 headings and ul/li lists in Markdown cells without
modifying the source notebook; preserves fenced examples.
"""

import re

from nbconvert.preprocessors import Preprocessor


class HtmlHeadingsToMarkdown(Preprocessor):
    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type != "markdown":
            return cell, resources

        lines = []
        fence = None
        list_depth = 0
        # Split only list tags; retain inline formatting in item contents.
        list_tags = re.compile(r"(</?(?:ul|li)\b[^>]*>)", re.IGNORECASE)
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
            elif list_depth or list_tags.search(line):
                for part in list_tags.split(line):
                    tag = re.fullmatch(r"<(/?)(ul|li)\b[^>]*>", part, re.IGNORECASE)
                    if tag:
                        closing, name = tag[1], tag[2].lower()
                        if name == "ul":
                            if closing:
                                list_depth = max(0, list_depth - 1)
                                lines.append("\n\n" if list_depth == 0 else "\n")
                            else:
                                lines.append("\n\n" if list_depth == 0 else "\n")
                                list_depth += 1
                        elif not closing:
                            # Four spaces per level keeps nested Markdown lists
                            # inside the parent item in Pandoc/nbconvert.
                            if lines and not lines[-1].endswith("\n"):
                                lines.append("\n")
                            lines.append("    " * max(0, list_depth - 1) + "- ")
                        elif lines and not lines[-1].endswith("\n"):
                            lines.append("\n")
                    elif part.strip():
                        if list_depth:
                            # Indent wrapped text as a continuation of the item.
                            if lines and lines[-1].endswith("\n"):
                                lines.append("    " * list_depth)
                            lines.append(part.strip())
                        else:
                            lines.append(part)
                if not lines[-1].endswith("\n"):
                    lines.append("\n")
            else:
                lines.append(line)

        cell.source = "".join(lines)
        return cell, resources


c = get_config()  # noqa: F821 — provided by Jupyter's config loader
c.Exporter.preprocessors.append(HtmlHeadingsToMarkdown)
