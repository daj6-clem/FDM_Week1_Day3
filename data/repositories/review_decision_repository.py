from sqlalchemy.orm import Session
from src.models.models import ReviewDecision

class ReviewDecisionRepository:
    def __init__(self, db:Session):
        self.db = db

    def get_by_id(self, decision_id: str) -> ReviewDecision | None:
        return (self.db.query(ReviewDecision).filter(
            ReviewDecision.decision_id == decision_id
        )
        .first()
        )

    def get_for_review_request(
        self,
        review_request_id: str
    ) -> list[ReviewDecision]:
        return (
            self.db.query(ReviewDecision)
            .filter(
                ReviewDecision.review_request_id
                == review_request_id
            )
            .order_by(
                ReviewDecision.decision_date.desc()
            )
            .all()
        )

    def create(
        self,
        review_decision: ReviewDecision
    ) -> ReviewDecision:
        self.db.add(review_decision)
        self.db.commit()
        self.db.refresh(review_decision)
        return review_decision