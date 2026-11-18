from sqlalchemy.orm import Session
from src.models.models import ComplaintNote


class ComplaintNoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, note_id: str) -> ComplaintNote | None:
        return (self.db.query(ComplaintNote)
                .filter(ComplaintNote.note_id == note_id)
                .first()
                )
    
    def get_for_complaint(self, complaint_id: str) -> list[ComplaintNote]:
        return (self.db.query(ComplaintNote).filter(
            ComplaintNote.complaint_id == complaint_id
        )
        .order_by(
            ComplaintNote.created_at.desc()
        )
        .all()
        )

        
    def create(self, note: ComplaintNote):
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note