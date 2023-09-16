"""
.. include:: ../README.md
"""
from .similarity import similarity
from .structural_similarity import structural_similarity
from .style_similarity import style_similarity


__all__ = ["structural_similarity", "style_similarity", "similarity"]
