from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from sqlalchemy import Enum
# from . import sub_media_table

class Submission(db.Model):
    __tablename__ = 'submissions'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('creators.id')), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('opportunities.id')), nullable=False)
    name = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    notes = db.Column(db.Text, nullable=True)
    bpm = db.Column(db.Integer, nullable=True)
    file_url = db.Column(db.String(500), nullable=True)
    collaborators = db.Column(db.String(500), nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Creator
    creator = db.relationship('Creator', backref=db.backref('submissions', lazy=True))

    # Relationship to Opportunity
    opportunity = db.relationship('Opportunity', backref=db.backref('submissions', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'opportunity_id': self.opportunity_id,
            'name': self.name,
            'status': self.status,
            'notes': self.notes,
            'bpm': self.bpm,
            'file_url': self.file_url,
            'collaborators': self.collaborators,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
        }
