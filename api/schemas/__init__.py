"""
API schemas package for request/response models.
"""
from api.schemas.requests import (
    ResearchRequest,
    ResearchFeedbackRequest,
    BatchResearchRequest,
    DocumentSearchRequest
)
from api.schemas.responses import (
    ResearchResponse,
    ResearchStatusResponse,
    ResearchReportResponse,
    ResearchListResponse,
    DocumentResponse,
    DocumentListResponse,
    ErrorResponse
)

__all__ = [
    # Requests
    "ResearchRequest",
    "ResearchFeedbackRequest",
    "BatchResearchRequest",
    "DocumentSearchRequest",
    # Responses
    "ResearchResponse",
    "ResearchStatusResponse",
    "ResearchReportResponse",
    "ResearchListResponse",
    "DocumentResponse",
    "DocumentListResponse",
    "ErrorResponse"
]