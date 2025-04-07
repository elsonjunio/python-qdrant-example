from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Document:
    content: str
    metadata: Dict[str, Any]
    page_number: Optional[int] = None


@dataclass
class SearchResult:
    content: str
    score: float
    metadata: Dict[str, Any]
