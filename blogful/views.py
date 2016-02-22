from flask import flash, redirect, render_template, request, url_for
from flask.ext.bower import Bower
from flask.ext.login import login_user, login_required, logout_user, current_user
from werkzeug import check_password_hash
from werkzeug.exceptions import Forbidden

from . import app
from .database import db
from .forms import EntryForm, EntryDeleteForm, LoginForm
from .models import Entry, User


Bower(app)

PAGINATE_BY = 10


@app.route('/')
@app.route('/page/<int:page>')
def entries(page=1):
    if page < 1:
        raise ValueError('Only positive values allowed for page number.')

    try:
        paginate_by = int(request.args.get('limit', PAGINATE_BY))
    except ValueError:
        paginate_by = PAGINATE_BY

    page_index = page - 1
    count = Entry.query.count()

    start = page_index * paginate_by
    end = start + paginate_by

    pages = count / paginate_by
    has_prev = page < pages
    has_next = page_index > 0

    entries = Entry.query.order_by(Entry.datetime.desc())[start:end]
    return render_template('entries.html', entries=entries,
                           has_next=has_next, has_prev=has_prev,
                           current_page=page, total_pages=pages)

@app.route('/entry/<int:eid>')
def entry(eid):
    entry = Entry.query.filter_by(id=eid).first_or_404()
    return render_template('entry.html', entry=entry)

@app.route('/entry/<int:eid>/edit', methods=['GET', 'POST'])
@login_required
def entry_edit(eid):
    entry = Entry.query.filter_by(id=eid).first_or_404()

    if not all([entry.author, current_user]) or entry.author.id != current_user.id:
        raise Forbidden('Only entry author can edit it.')

    form = EntryForm(obj=entry)

    if form.validate_on_submit():
        form.populate_obj(entry)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries'))

    else:
        return render_template('add_entry.html', form=form)

@app.route('/entry/<int:eid>/delete', methods=['GET', 'POST'])
@login_required
def entry_delete(eid):
    entry = Entry.query.filter_by(id=eid).first_or_404()

    if not all([entry.author, current_user]) or entry.author.id != current_user.id:
        raise Forbidden('Only entry author can edit it.')

    form = EntryDeleteForm()

    if form.validate_on_submit():
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for('entries'))

    else:
        return render_template('delete_entry.html', form=form)


@app.route('/entry/add', methods=['GET', 'POST'])
@login_required
def add_entry():
    form = EntryForm()

    if form.validate_on_submit():
        entry = Entry(title=form.title.data,
                      content=form.content.data,
                      author=current_user)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries'))

    else:
        return render_template('add_entry.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(request.args.get('next', url_for('entries')))
        else:
            flash('Incorrect username or password', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('entries'))
