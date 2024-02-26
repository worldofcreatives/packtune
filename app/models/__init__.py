from .db import db
from .db import environment, SCHEMA, add_prefix_for_prod

# Associations
creator_genre_table = db.Table('creator_genres',
    db.Column('creatorId', db.Integer, db.ForeignKey(add_prefix_for_prod('creators.creatorId')), primary_key=True),
    db.Column('genreId', db.Integer, db.ForeignKey(add_prefix_for_prod('genres.genreId')), primary_key=True)
)

creator_type_table = db.Table('creator_types',
    db.Column('creatorId', db.Integer, db.ForeignKey(add_prefix_for_prod('creators.creatorId')), primary_key=True),
    db.Column('typeId', db.Integer, db.ForeignKey(add_prefix_for_prod('types.typeId')), primary_key=True)
)

opp_genre_table = db.Table('opp_genres',
    db.Column('oppId', db.Integer, db.ForeignKey('opportunities.oppId'), primary_key=True),
    db.Column('genreId', db.Integer, db.ForeignKey('genres.genreId'), primary_key=True)
)

opp_type_table = db.Table('opp_types',
    db.Column('oppId', db.Integer, db.ForeignKey('opportunities.oppId'), primary_key=True),
    db.Column('typeId', db.Integer, db.ForeignKey('types.typeId'), primary_key=True)
)

opp_media_table = db.Table('opp_media',
    db.Column('oppId', db.Integer, db.ForeignKey(add_prefix_for_prod('opportunities.oppId')), primary_key=True),
    db.Column('mediaId', db.Integer, db.ForeignKey(add_prefix_for_prod('media.mediaId')), primary_key=True)
)

sub_media_table = db.Table('sub_media',
    db.Column('subId', db.Integer, db.ForeignKey(add_prefix_for_prod('submissions.subId')), primary_key=True),
    db.Column('mediaId', db.Integer, db.ForeignKey(add_prefix_for_prod('media.mediaId')), primary_key=True)
)

feedback_media_table = db.Table('feedback_media',
    db.Column('feedbackId', db.Integer, db.ForeignKey(add_prefix_for_prod('feedback.feedbackId')), primary_key=True),
    db.Column('mediaId', db.Integer, db.ForeignKey(add_prefix_for_prod('media.mediaId')), primary_key=True)
)



# Models
from .user import User
from .creator import Creator
from .genre import Genre
from .type import Type
from .company import Company
from .opportunity import Opportunity
from .media import Media
from .submission import Submission
from .feedback import Feedback
