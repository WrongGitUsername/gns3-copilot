"""
GNS3 Copilot Process Analyzer Module

This module provides comprehensive process analysis functionality for GNS3 Copilot,
capturing complete execution processes including Thought/Action/Action Input/
Observation/Final Answer.
"""

from .process_callback import LearningDocumentationCallback
from .langchain_callback import LearningLangChainCallback
from .documentation_generator import DocumentationGenerator

__version__ = "1.0.0"
__author__ = "GNS3 Copilot Team"

__all__ = [
    "LearningDocumentationCallback",
    "LearningLangChainCallback",
    "DocumentationGenerator"
]
