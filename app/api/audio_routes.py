from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Audio, Watchlist
from sqlalchemy.exc import IntegrityError
from .aws_helpers import upload_file_to_s3, remove_file_from_s3, get_unique_filename
from app.forms import AudioForm
from werkzeug.utils import secure_filename

audio_routes = Blueprint("audio", __name__)


# *====> FETCH <====

@audio_routes.route("", defaults={"contentId": None}, methods=["GET"])
@audio_routes.route("/<int:contentId>", methods=["GET"])
@login_required
def get_content(contentId):
    if contentId is None:
        files = Audio.query.all()
        return jsonify([file.to_dict() for file in files]), 200
    else:
        audio = Audio.query.get(contentId)
        if audio is None:
            return jsonify({"error": "Audio not found"}), 404
        return jsonify(audio.to_dict()), 200


# *====> CREATE <====


@audio_routes.route("/", methods=["POST"])
@login_required
def add_content():
    form = AudioForm()
    print("🚀 ~ form:", form)

    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        thumbnail = form.thumbnail.data
        video = form.video.data
        audio = form.audio.data

        allowed_extensions = set(["png", "jpg", "jpeg", "gif", "mov", "mp4", "wav", "mp3"])

        def is_allowed_file(filename, allowed_extensions):
            return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

        # Check if files are not None before checking if they are allowed
        if thumbnail is None or video is None or audio is None:
            return jsonify({"error": "Missing file(s)"}), 400

        if not is_allowed_file(
            thumbnail.filename, allowed_extensions
        ) or not is_allowed_file(video.filename, allowed_extensions):
            return jsonify({"error": "File type not allowed"}), 400

        thumbnail_file = get_unique_filename(thumbnail.filename)
        video_file = get_unique_filename(video.filename)
        audio_file = get_unique_filename(audio.filename)


        thumbnail_url_response = upload_file_to_s3(thumbnail, thumbnail_file)
        video_url_response = upload_file_to_s3(video, video_file)
        audio_url_response = upload_file_to_s3(audio, audio_file)

        # Check for errors in the responses
        if "errors" in thumbnail_url_response:
            error_message = thumbnail_url_response.get(
                "errors", "Unknown error during thumbnail upload."
            )
            return jsonify({"errors": f"Thumbnail upload failed: {error_message}"}), 500

        if "errors" in video_url_response:
            error_message = video_url_response.get(
                "errors", "Unknown error during video upload."
            )
            return jsonify({"errors": f"Video upload failed: {error_message}"}), 500

        if "errors" in audio_url_response:
            error_message = audio_url_response.get(
                "errors", "Unknown error during audio upload."
            )
            return jsonify({"errors": f"Audio upload failed: {error_message}"}), 500

        new_audio = Audio(
            title=form.title.data,
            description=form.description.data,
            genre=form.genre.data,
            thumbnail_url=thumbnail_url_response["url"],
            video_url=video_url_response["url"],
            audio_url=audio_url_response["url"],
            user_id=current_user.id,
        )

        try:
            db.session.add(new_audio)
            db.session.commit()
            return jsonify(new_audio.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Could not add new content"}), 500
        except:
            # Catch-all return in case of unexpected issues
            return jsonify({"error": "An unexpected error occurred"}), 500
    else:
        # Handle form validation failure
        return (
            jsonify({"error": "Form validation failed", "form_errors": form.errors}),
            400,
        )


# # *====> UPDATE <====
# @audio_routes.route("/<int:contentId>", methods=["PUT"])
# @login_required
# def update_content(contentId):
#     audio = Audio.query.get(contentId)
#     if not audio or audio.user_id != current_user.id:
#         return jsonify({"error": "Content not found or unauthorized"}), 404


#     title = request.form.get('title')
#     description = request.form.get('description')
#     genre = request.form.get('genre')
#     thumbnail_url = request.form.get('thumbnail_url')
#     video_url = request.form.get('video_url')

#     # Update text fields
#     if title:
#         audio.title = title
#     if description:
#         audio.description = description
#     if genre:
#         audio.genre = genre

#     # Handle thumbnail
#     thumbnail_file = request.files.get('thumbnail')
#     if thumbnail_file:
#         filename = secure_filename(thumbnail_file.filename)
#         upload_result = upload_file_to_s3(thumbnail_file, filename)
#         if upload_result.get('url'):
#             audio.thumbnail_url = upload_result['url']
#     elif thumbnail_url:
#         audio.thumbnail_url = thumbnail_url

#     # Handle video
#     video_file = request.files.get('video')
#     if video_file:
#         filename = secure_filename(video_file.filename)
#         upload_result = upload_file_to_s3(video_file, filename)
#         if upload_result.get('url'):
#             audio.video_url = upload_result['url']
#     elif video_url:
#         audio.video_url = video_url
#         try:
#             db.session.commit()
#             return jsonify(video.to_dict()), 200
#         except IntegrityError:
#             db.session.rollback()
#             return jsonify({"error": "Could not update content"}), 500
#     return jsonify({"error": "Invalid form data"}), 400


# # *====> DELETE <====
# @audio_routes.route("/<int:video_id>", methods=["DELETE"])
# @login_required
# def delete_content(video_id):
#     video = Audio.query.get(video_id)
#     if not video or video.user_id != current_user.id:
#         return jsonify({"error": "Content not found or unauthorized"}), 404

#     thumbnail_remove_result = remove_file_from_s3(video.thumbnail_url)
#     video_remove_result = remove_file_from_s3(video.video_url)

#     if thumbnail_remove_result != True:
#         return (
#             jsonify(
#                 {
#                     "error": f"Failed to delete thumbnail: {thumbnail_remove_result['errors']}"
#                 }
#             ),
#             500,
#         )
#     if video_remove_result != True:
#         return (
#             jsonify(
#                 {
#                     "error": f"Failed to delete video file: {video_remove_result['errors']}"
#                 }
#             ),
#             500,
#         )

#     try:
#         db.session.delete(video)
#         db.session.commit()
#         return jsonify({"message": "Content successfully deleted"}), 204
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error": str(e)}), 500
