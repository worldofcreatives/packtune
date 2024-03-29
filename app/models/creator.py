from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime
from sqlalchemy import JSON

VALID_GENRES = [
    "Afro", "Country", "Dancehall", "Disco", "Funk",
    "Hip Hop", "Latin", "Neo Soul", "Pop", "R&B",
    "Reggae", "Rock", "Other"
]

VALID_TYPES = [
    "Songwriter", "Musician", "Producer", "Artist"
]


class Creator(db.Model):
    __tablename__ = 'creators'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    stage_name = db.Column(db.String(255), nullable=True)
    profile_pic = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address_1 = db.Column(db.String(255), nullable=True)
    address_2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    previous_projects = db.Column(db.Text, nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    twitter = db.Column(db.String(255), nullable=True)
    facebook = db.Column(db.String(255), nullable=True)
    youtube = db.Column(db.String(255), nullable=True)
    other_social_media = db.Column(db.Text, nullable=True)
    reference_name = db.Column(db.String(255), nullable=True)
    reference_email = db.Column(db.String(255), nullable=True)
    reference_phone = db.Column(db.String(20), nullable=True)
    reference_relationship = db.Column(db.String(100), nullable=True)
    genres = db.Column(JSON, default=list, nullable=True)
    types = db.Column(JSON, default=list, nullable=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def validate_genres(self):
        if not all(genre in VALID_GENRES for genre in self.genres):
            raise ValueError("One or more genres are invalid")

    def validate_types(self):
        if not all(type_ in VALID_TYPES for type_ in self.types):
            raise ValueError("One or more types are invalid")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'stage_name': self.stage_name,
            'profile_pic': self.profile_pic,
            'bio': self.bio,
            'phone': self.phone,
            'address_1': self.address_1,
            'address_2': self.address_2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'portfolio_url': self.portfolio_url,
            'previous_projects': self.previous_projects,
            'instagram': self.instagram,
            'twitter': self.twitter,
            'facebook': self.facebook,
            'youtube': self.youtube,
            'other_social_media': self.other_social_media,
            'reference_name': self.reference_name,
            'reference_email': self.reference_email,
            'reference_phone': self.reference_phone,
            'reference_relationship': self.reference_relationship,
            'types': self.types,
            'genres': self.genres,
            'created_date': self.created_date.isoformat(),
            'updated_date': self.updated_date.isoformat(),
        }
