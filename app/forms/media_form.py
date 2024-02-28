from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf.file import FileAllowed, FileRequired
from app.api.aws_helpers import ALLOWED_EXTENSIONS


class MediaForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    file = FileField("Audio File", validators=[FileRequired(), FileAllowed(list(ALLOWED_EXTENSIONS))])
    submit = SubmitField("Submit")

    # def __init__(self, *args, is_update=False, **kwargs):
    #     super(MediaForm, self).__init__(*args, **kwargs)
    #     if is_update:
    #         self.file.validators.append(Optional())
