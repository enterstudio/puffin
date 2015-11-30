import time
from flask import redirect, render_template, request, url_for, flash, abort, send_file
from flask_bootstrap import Bootstrap
from flask_security.core import current_user
from flask_security.decorators import login_required
from ..util import to_uuid
from ..core.db import db
from ..core.model import User
from . import gui


@gui.record_once
def record_once(state):
    app = state.app
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True

@gui.context_processor
def utility_processor():
    return dict(current_user=current_user)

@gui.route('/', methods=['GET'])
def index():
    return render_template('index.html')