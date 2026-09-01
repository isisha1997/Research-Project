"""Verifiable education guides for next-generation materials.

A guide is a set of claims, each carrying its own sources. Prose is generated
from the claims, so an unsourced sentence cannot reach the page. Four gates
run before publication: coverage, citation resolution, source tiering, and
contradiction surfacing.
"""

from .loader import GuideLoadError, discover, load_guide, load_guides
from .models import Audience, Claim, Guide, Source, SourceTier, Stance
from .render import render_html, render_markdown
from .resolve import CitationResolver, Resolution
from .verify import (
    Contradiction,
    Finding,
    Gate,
    Severity,
    VerificationReport,
    verify,
)

__version__ = "1.0.0"

__all__ = [
    "Audience", "Claim", "CitationResolver", "Contradiction", "Finding", "Gate",
    "Guide", "GuideLoadError", "Resolution", "Severity", "Source", "SourceTier",
    "Stance", "VerificationReport", "discover", "load_guide", "load_guides",
    "render_html", "render_markdown", "verify", "__version__",
]
