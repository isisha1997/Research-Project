"""Pull text and references out of a finished document.

An audit is only as good as its extraction. A tool that quietly reads half a
PDF and reports no problems is worse than one that refuses, so every extractor
returns its own confidence and the audit prints that confidence next to the
result. `full` means the whole text was recovered; `best_effort` means some of
the document may not have been read, and a clean report is not proof of a clean
document.
"""

from __future__ import annotations

import html
import re
import zipfile
import zlib
from dataclasses import dataclass, field
from pathlib import Path

# A DOI runs until whitespace or a closing delimiter. Trailing sentence
# punctuation is stripped afterwards, since "...10.1000/abc." is one sentence,
# not a DOI ending in a period.
DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>,;\]}]+", re.IGNORECASE)
# Multi-part documents are joined with a "[part]" marker line so a reference can
# be reported as coming from the body, a footnote, or a reviewer's comment.
PART_MARKER = re.compile(r"^\[([a-z0-9_]+)\]$")
URL_PATTERN = re.compile(r"https?://[^\s\"'<>()\[\]{}]+", re.IGNORECASE)
TRAILING_PUNCT = ".,;:)]}>'\""

SUPPORTED = {".md", ".markdown", ".txt", ".html", ".htm", ".docx", ".pdf", ".yaml", ".yml", ".json"}


class ExtractionError(Exception):
    """Raised when a document cannot be read at all."""


@dataclass
class Extracted:
    """Text recovered from a document, plus how much to trust the recovery."""

    text: str
    fmt: str
    confidence: str = "full"          # full | best_effort
    note: str = ""
    linked_urls: list[str] = field(default_factory=list)  # hyperlink targets, not body text

    @property
    def is_complete(self) -> bool:
        return self.confidence == "full"


@dataclass
class Reference:
    """One citation-shaped thing found in a document."""

    raw: str
    kind: str          # doi | url
    line: int
    context: str       # the line it appeared on, for reporting the location
    from_hyperlink: bool = False
    block: str = ""    # surrounding lines, since reference entries wrap
    part: str = ""     # which part of the document it came from (body, footnotes, comments)

    @property
    def key(self) -> str:
        return self.raw.lower()


def extract(path: str | Path) -> Extracted:
    path = Path(path)
    if not path.exists():
        raise ExtractionError(f"{path}: no such file")
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ExtractionError(
            f"{path}: cannot read {suffix or 'files with no extension'}; "
            f"supported: {', '.join(sorted(SUPPORTED))}"
        )
    if suffix == ".docx":
        return _extract_docx(path)
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix in {".html", ".htm"}:
        return _extract_html(path)
    return Extracted(path.read_text(encoding="utf-8", errors="replace"), suffix.lstrip("."))


def find_references(extracted: Extracted) -> list[Reference]:
    """Every DOI and URL in the document, deduplicated, in order of appearance."""
    references: list[Reference] = []
    seen: set[tuple[str, str]] = set()
    lines = extracted.text.splitlines()

    def window(index: int) -> str:
        """The reference entry as a human sees it, not as the file wrapped it."""
        return " ".join(lines[max(0, index - 3):index + 2])

    part = ""
    for lineno, line in enumerate(lines, 1):
        marker = PART_MARKER.match(line.strip())
        if marker:
            part = marker.group(1)
            continue
        block = window(lineno - 1)
        for match in DOI_PATTERN.finditer(line):
            _add(references, seen, _clean(match.group()), "doi", lineno, line,
                 block=block, part=part)
        for match in URL_PATTERN.finditer(line):
            url = _clean(match.group())
            # A doi.org link is a DOI; recording it as both would double-count it.
            if "doi.org/" in url.lower():
                inner = DOI_PATTERN.search(url)
                if inner:
                    _add(references, seen, _clean(inner.group()), "doi", lineno, line,
                         block=block, part=part)
                else:
                    # A doi.org link whose path is not a DOI is a broken reference,
                    # not a web page; recording it as a URL would let it pass as live.
                    tail = url.split("doi.org/", 1)[1] or url
                    _add(references, seen, tail, "doi", lineno, line, block=block,
                         part=part)
                continue
            _add(references, seen, url, "url", lineno, line, block=block, part=part)

    for url in extracted.linked_urls:
        url = _clean(url)
        inner = DOI_PATTERN.search(url) if "doi.org/" in url.lower() else None
        if inner:
            _add(references, seen, _clean(inner.group()), "doi", 0, "(hyperlink)", True)
        else:
            _add(references, seen, url, "url", 0, "(hyperlink)", True)

    return references


def _add(refs, seen, raw, kind, line, context, from_hyperlink=False, block="",
         part="") -> None:
    if not raw:
        return
    key = (kind, raw.lower())
    if key in seen:
        return
    seen.add(key)
    refs.append(Reference(raw, kind, line, context.strip()[:300], from_hyperlink,
                          (block or context).strip()[:1200], part))


def _clean(value: str) -> str:
    return value.rstrip(TRAILING_PUNCT)


# -- format-specific extractors --------------------------------------------

def _extract_html(path: Path) -> Extracted:
    raw = path.read_text(encoding="utf-8", errors="replace")
    hrefs = re.findall(r"href=[\"']([^\"']+)[\"']", raw, re.IGNORECASE)
    body = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    return Extracted(html.unescape(body), "html", linked_urls=hrefs)


def _extract_docx(path: Path) -> Extracted:
    """Word documents are a zip of XML, and the body is only one part of it.

    Citations live in footnotes and endnotes as often as in body text, and in a
    document under review they live in the comments. Reading only
    word/document.xml returns "no references found" on a document full of them,
    which is the worst possible failure for an audit: a confident clean result.
    """
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            if "word/document.xml" not in names:
                raise ExtractionError(f"{path}: not a Word document (no word/document.xml)")

            parts: list[tuple[str, str]] = [("body", "word/document.xml")]
            for label, part in (("footnotes", "word/footnotes.xml"),
                                ("endnotes", "word/endnotes.xml")):
                if part in names:
                    parts.append((label, part))
            for part in sorted(n for n in names
                               if re.fullmatch(r"word/(header|footer)\d*\.xml", n)):
                parts.append((part.split("/")[-1].removesuffix(".xml"), part))
            # Comments last: in a document under review they are annotations about
            # the text, not the text, and the report should be able to say so.
            if "word/comments.xml" in names:
                parts.append(("comments", "word/comments.xml"))

            chunks: list[str] = []
            urls: list[str] = []
            present: list[str] = []
            for label, part in parts:
                xml = archive.read(part).decode("utf-8", errors="replace")
                body = _docx_text(xml)
                if body.strip():
                    present.append(label)
                    chunks.append(f"[{label}]\n{body}")
                rels_name = f"word/_rels/{part.split('/')[-1]}.rels"
                if rels_name in names:
                    urls.extend(_docx_rel_urls(
                        archive.read(rels_name).decode("utf-8", errors="replace")))
    except zipfile.BadZipFile as exc:
        raise ExtractionError(f"{path}: not a readable .docx ({exc})") from exc

    return Extracted(
        "\n".join(chunks), "docx",
        note="read parts: " + ", ".join(present),
        linked_urls=urls,
    )


def _docx_text(xml: str) -> str:
    """Flatten Word XML to text, keeping paragraph breaks as newlines."""
    text = re.sub(r"(?i)</w:p>", "\n", xml)
    text = re.sub(r"(?i)<w:(br|cr)\b[^>]*/?>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", "", text)
    return html.unescape(text)


def _docx_rel_urls(rels: str) -> list[str]:
    """Hyperlink targets live in the relationships file, not the visible text.

    A link whose display text reads only "the study" is invisible without this.
    """
    found = re.findall(
        r'Target="([^"]+)"[^>]*TargetMode="External"|TargetMode="External"[^>]*Target="([^"]+)"',
        rels,
    )
    return [html.unescape(a or b) for a, b in found]


def _extract_pdf(path: Path) -> Extracted:
    """Best-effort PDF reading without a PDF library.

    Uses pypdf when it is installed. Otherwise it inflates the document's
    streams and scrapes link annotations, which recovers references from most
    text PDFs but will miss text in unusual encodings and anything in a scanned
    image. That result is always marked best_effort.
    """
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        urls: list[str] = []
        for page in reader.pages:
            for annot in page.get("/Annots") or []:
                try:
                    uri = annot.get_object().get("/A", {}).get("/URI")
                except Exception:  # a malformed annotation should not end the audit
                    continue
                if uri:
                    urls.append(str(uri))
        return Extracted(text, "pdf", linked_urls=urls)
    except ImportError:
        pass

    raw = path.read_bytes()
    if not raw.startswith(b"%PDF"):
        raise ExtractionError(f"{path}: not a PDF")

    chunks: list[str] = [raw.decode("latin-1", errors="replace")]
    for match in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.DOTALL):
        try:
            chunks.append(zlib.decompress(match.group(1)).decode("latin-1", errors="replace"))
        except zlib.error:
            continue  # not deflate-compressed, or not a content stream

    blob = "\n".join(chunks)
    urls = [u for u in re.findall(r"/URI\s*\(([^)]*)\)", blob)]
    # Text-showing operators hold the visible words; join them so DOIs split
    # across operators still form a searchable string.
    shown = " ".join(re.findall(r"\(([^()\\]{0,500})\)\s*Tj", blob))
    return Extracted(
        blob + "\n" + shown,
        "pdf",
        confidence="best_effort",
        note="read without a PDF library: text in unusual encodings or in scanned "
             "images was not recovered, so absence of a finding is not proof of absence",
        linked_urls=urls,
    )
