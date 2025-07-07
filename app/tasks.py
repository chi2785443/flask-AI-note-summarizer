import torch
from celery import Celery
from flask import current_app
from .models import db, Summary
from transformers import pipeline

celery = Celery(__name__)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def make_celery(app):
    celery.conf.update(app.config)
    celery.autodiscover_tasks(['app.tasks'])

@celery.task()
def summarize_text_task(text, user_id):
    short = summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    summary = Summary(user_id=user_id, original_text=text, summarized_text=short, title=short[:50])
    with current_app.app_context():
        db.session.add(summary)
        db.session.commit()
    return summary.id