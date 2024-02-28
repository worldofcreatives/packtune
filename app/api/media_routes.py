from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Media
from app.forms import MediaForm
from sqlalchemy.exc import IntegrityError
from .aws_helpers import upload_file_to_s3, get_unique_filename

media_routes = Blueprint('media', __name__)

@media_routes.route("/test", methods=["POST"])
@login_required
def upload_image():
    form = MediaForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        name = form.data["name"]
        file = form.data["file"]
        file.filename = get_unique_filename(file.filename)
        upload = upload_file_to_s3(file)
        print(upload)

        if "url" not in upload:
            error_message = upload.get("errors", "Unknown error during file upload.")
            return jsonify({"errors": f"File upload failed: {error_message}"}), 500

        url = upload["url"]

        new_media = Media(
            name=name,
            file=url,
            user_id=current_user.id,
        )
        try:
            db.session.add(new_media)
            db.session.commit()
            return jsonify(new_media.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Could not upload media"}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500
    else:
        return jsonify({"error": "Form validation failed", "form_errors": form.errors}), 400

# POST /api/media/upload - Upload a media file

def is_allowed_file(filename, allowed_extensions):
    """Check if the file's extension is in the allowed list."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@media_routes.route('/upload', methods=['POST'])
@login_required
def upload_media():
    form = MediaForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        file = form.file.data
        name = form.name.data

        # Extract submission_id and opportunity_id from form data or query parameters
        submission_id = request.args.get('submission_id')
        opportunity_id = request.args.get('opportunity_id')

        allowed_extensions = {"mp3", "wav", "ogg", "flac"}
        if not is_allowed_file(file.filename, allowed_extensions):
            return jsonify({"error": "File type not allowed"}), 400

        unique_filename = get_unique_filename(file.filename)
        upload_response = upload_file_to_s3(file, unique_filename)

        if "errors" in upload_response:
            error_message = upload_response.get("errors", "Unknown error during file upload.")
            return jsonify({"errors": f"File upload failed: {error_message}"}), 500

        new_media = Media(
            name=name,
            file=upload_response["url"],
            user_id=current_user.id,
            # Conditionally adding submission_id and opportunity_id
            submission_id=submission_id if submission_id else None,
            opportunity_id=opportunity_id if opportunity_id else None
        )

        try:
            db.session.add(new_media)
            db.session.commit()
            return jsonify(new_media.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Could not upload media"}), 500
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500
    else:
        return jsonify({"error": "Form validation failed", "form_errors": form.errors}), 400



# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
# from flask_login import login_required, current_user
# from app.models import db, Media
# from app.forms.media_form import MediaForm
# import os

# media_routes = Blueprint('media', __name__)

# @media_routes.route('/upload', methods=['POST'])
# @login_required
# def upload_media():
#     form = MediaForm()
#     form["csrf_token"].data = request.cookies["csrf_token"]
#     if form.validate_on_submit():
#         file = form.file.data
#         filename = secure_filename(file.filename)
#         filepath = os.path.join('path/to/save/media', filename)
#         file.save(filepath)

#         new_media = Media(
#             name=form.name.data,
#             file=filename,
#             user_id=current_user.id
#         )

#         db.session.add(new_media)
#         db.session.commit()

#         return jsonify(new_media.to_dict()), 201
#     return jsonify({"errors": form.errors}), 400


