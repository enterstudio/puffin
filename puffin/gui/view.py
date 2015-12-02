import time
from flask import redirect, render_template, request, url_for, flash, abort, send_file, send_from_directory
from flask_bootstrap import Bootstrap
from flask_security.core import current_user
from flask_security.decorators import login_required
from ..util import to_uuid
from ..core.db import db
from ..core.model import User
from ..core.apps import APP_HOME, get_app, get_app_list
from ..core.docker import get_client, create_app, delete_app, get_app_domain, is_app_running
from . import gui
from .form import AppForm


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
    return render_template('index.html', apps=get_app_list())

@gui.route('/app/<app_id>.html', methods=['GET', 'POST'])
def app(app_id):
    container = None
    container_domain = None
    form = None

    if current_user.is_authenticated():
        client = get_client()
        app = get_app(app_id)

        form = AppForm()
        
        if form.validate_on_submit():
            if form.install.data:
                create_app(client, current_user, app)
            
            if form.uninstall.data:
                delete_app(client, current_user, app)
        
        app_running = is_app_running(client, current_user, app)
        app_domain = get_app_domain(current_user, app)

    return render_template('app.html', app=get_app(app_id), 
        app_running=app_running, app_domain=app_domain, form=form)

@gui.route('/static/apps/<path:path>')
def app_static(path):
    return send_from_directory(APP_HOME, path)

