from datetime import datetime, timezone

from app.extensions import db


class DocumentChunk(db.Model):
    __tablename__ = "document_chunks"

    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"), nullable=False)
    chunk_index = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    embedding = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self, include_text: bool = True) -> dict:
        data = {
            "id": self.id,
            "document_id": self.document_id,
            "chunk_index": self.chunk_index,
        }
        if include_text:
            data["text"] = self.text
        return data
