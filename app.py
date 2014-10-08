#!/usr/bin/env python
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from utils import get_local_time
import short_url
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import CtfEvent, CtfAdmin, CtfEventChallenge

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/<string:short_code>', methods=['GET'])
def event_page(short_code=None):
    event = None
    try:
        event_id = short_url.decode_url(short_code)
        event = CtfEvent.query.get(event_id)

        event.local_start_date = get_local_time(event.start_date, request.remote_addr)
        event.local_end_date = get_local_time(event.end_date, request.remote_addr)
        event.details = json.loads(event.details)
    except Exception as e:
        print e
    return render_template('event.html', event=event, short_code=short_code)

@app.route('/update-item-status', methods=['POST'])
def update_item_status():
    event_code = request.form.get('event_code')
    category = request.form.get('category')
    point_value = request.form.get('point_value')
    assigned = request.form.get('assigned')

    record = CtfEventChallenge.query.filter_by(event_code=event_code)\
        .filter_by(category=category)\
        .filter_by(point_value=point_value).first()

    if record:
        try:
            record.assigned = assigned
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            return jsonify(data = {'status': 'error'})
    else:
        new_entry = CtfEventChallenge(event_code=event_code, category=category, point_value=point_value, assigned=assigned)
        try:
            db.session.add(new_entry)
            db.session.commit()
        except Exception as e:
            print e
            db.session.rollback()
            return jsonify(data = {'status': 'error'})
    return jsonify({'status': 'success'})
