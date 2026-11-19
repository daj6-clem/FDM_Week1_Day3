from sqlalchemy.orm import Session
from src.models.models import Recommendation


class RecommendationRepository:
    def __init__(self, db:Session):
        self.db = db

    def create(self, recommendation: Recommendation):
        self.db.add(recommendation)
        self.db.commit()
        self.db.refresh(recommendation)
        return recommendation