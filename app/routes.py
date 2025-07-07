from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Summary
from .tasks import summarize_text_task
from .utils import extract_text_from_pdf

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return {"message": "Note Summarizer API is running 🚀"}, 200

@main.route('/summarize', methods=['POST'])
@jwt_required()
def summarize():
    """
    Upload a PDF or text file to summarize
    ---
    tags:
      - Summarizer
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: Upload PDF or text file
    responses:
      202:
        description: Task accepted
    """
    user_id = get_jwt_identity()
    file = request.files['file']
    text = extract_text_from_pdf(file)
    task = summarize_text_task.delay(text, user_id)
    return jsonify({"task_id": task.id}), 202

@main.route('/summaries', methods=['GET'])
@jwt_required()
def get_summaries():
    """
    Get all user summaries
    ---
    tags:
      - Summarizer
    security:
      - Bearer: []
    responses:
      200:
        description: List of summaries
    """
    user_id = get_jwt_identity()
    summaries = Summary.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": s.id,
        "title": s.title,
        "summary": s.summarized_text,
        "orignal": s.original_text,
        "created": s.created_at.isoformat()
    } for s in summaries])