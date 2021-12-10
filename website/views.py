from __future__ import unicode_literals
from warnings import catch_warnings
from flask import Blueprint, render_template, request, redirect, flash, jsonify
from flask.helpers import url_for
from flask_login import login_required, current_user

from website.auth import history
from .models import History, User
from . import db
import youtube_dl
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        video = request.form.get('video')
        audio = request.form.get('audio')
        userVideo = request.form.get('uvideo')
        userAudio = request.form.get('uaudio')
        if len(url) > 0:
            if video:
                ydl_opts = {'format':'best'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    download = info["url"]
                    return redirect(download)
            elif audio:
                ydl_opts = {'format':'bestaudio'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    download = info["url"]
                    return redirect(download)
            elif userVideo:
                ydl_opts = {'format':'best'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    download = info["url"]
                    title = info["title"]
                    type = "Video"
                    new_history = History(url=url, title=title, type=type, user_id=current_user.id)
                    db.session.add(new_history)
                    db.session.commit()
                    return redirect(download)
            elif userAudio:
                ydl_opts = {'format':'bestaudio'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    download = info["url"]
                    title = info["title"]
                    type = "Audio"
                    new_history = History(url=url, title=title, type=type, user_id=current_user.id)
                    db.session.add(new_history)
                    db.session.commit()
                    return redirect(download)
        else:
            flash('Enter a URL please', category='info')
            return render_template("home.html", user=current_user)
    return render_template("home.html", user=current_user)


@views.route('/delete-history', methods=['POST'])
def delete_history():
    history = json.loads(request.data)
    historyId = history['historyId']
    history = History.query.get(historyId)
    if history:
        if history.user_id == current_user.id:
            db.session.delete(history)
            db.session.commit()

    return jsonify({})


