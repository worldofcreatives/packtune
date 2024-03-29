from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from . import opp_media_table
from .submission import Submission
from sqlalchemy import JSON


VALID_GENRES = [
    "Afro", "Country", "Dancehall", "Disco", "Funk",
    "Hip Hop", "Latin", "Neo Soul", "Pop", "R&B",
    "Reggae", "Rock", "Other"
]

VALID_TYPES = [
    "Songwriter", "Musician", "Producer", "Artist"
]

class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_audience = db.Column(db.String(255), nullable=True)
    budget = db.Column(db.DECIMAL(10,2), nullable=True)
    guidelines = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('companies.id')), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    genres = db.Column(JSON, default=list, nullable=True)
    types = db.Column(JSON, default=list, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Company
    company = db.relationship('Company', backref=db.backref('opportunities', lazy=True))

    # Many-to-Many Relationship with Media
    opp_media = db.relationship('Media', secondary=opp_media_table, backref=db.backref('opportunities', lazy='dynamic'))

    def validate_genres(self):
        if not all(genre in VALID_GENRES for genre in self.genres):
            raise ValueError("One or more genres are invalid")

    def validate_types(self):
        if not all(type_ in VALID_TYPES for type_ in self.types):
            raise ValueError("One or more types are invalid")

    def count_pending_submissions(self):
        return Submission.query.filter(Submission.opportunity_id == self.id, Submission.status == 'Pending').count()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'types': self.types,
            'description': self.description,
            'target_audience': self.target_audience,
            'budget': str(self.budget),
            'guidelines': self.guidelines,
            'created_date': self.created_date.isoformat(),
            'user_id': self.user_id,
            'submissions_count': len(self.submissions),
            'pending_submissions': self.count_pending_submissions(),
            'updated_date': self.updated_date.isoformat(),
            'opp_media': [media.to_dict() for media in self.opp_media],
        }
