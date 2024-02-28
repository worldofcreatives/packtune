from .db import db, environment, SCHEMA, add_prefix_for_prod


class Audio(db.Model):
    __tablename__ = "audio_content"

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey(add_prefix_for_prod("users.id")), nullable=False
    )
    genre = db.Column(db.String(500), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)
    audio_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=False)
    # rating to be talked about more? to compute average rating
    watchlists = db.relationship('Watchlist', back_populates='audio_content', cascade="all, delete", passive_deletes=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "genre": self.genre,
            "thumbnail_url": self.thumbnail_url,
            "video_url": self.video_url,
            "audio_url": self.audio_url,
            "user_id": self.user_id,
        }