from sqlalchemy.orm import Session
from src.models.models import ReviewRequest

class ReviewRequestRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_id(self, review_request_id: str) -> ReviewRequest | None:
        return (
            self.db.query(ReviewRequest)
            .filter(ReviewRequest.review_request_id == review_request_id)
            .first()
        )

    def get_for_complaint(self, complaint_id: str) -> list[ReviewRequest]:
        return (self.db.query(ReviewRequest)
                .filter(ReviewRequest.complaint_id == complaint_id)
                .all()
                )

    def create(self, review_request: ReviewRequest) -> ReviewRequest:
        self.db.add(review_request)
        self.db.commit()
        self.db.refresh(review_request)
        return review_request

    def update(self, review_request: ReviewRequest) -> ReviewRequest:
        self.db.commit()
        self.db.refresh(review_request)
        return review_request