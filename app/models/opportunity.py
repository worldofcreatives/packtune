from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

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
    company_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('companies.id')), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Company
    company = db.relationship('Company', backref=db.backref('opportunities', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'target_audience': self.target_audience,
            'budget': str(self.budget),
            'guidelines': self.guidelines,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
        }
