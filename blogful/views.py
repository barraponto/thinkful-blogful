from flask import redirect, render_template, request, url_for
from flask.ext.bower import Bower

from . import app
from .database import db
from .forms import EntryForm, EntryDeleteForm
from .models import Entry


Bower(app)

PAGINATE_BY = 10


@app.route('/')
@app.route('/page/<int:page>')
def entries(page=1):
    if page < 1:
        raise ValueError('Only positive values allowed for page number.')

    page_index = page - 1
    count = Entry.query.count()

    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    pages = count / PAGINATE_BY
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
def entry_edit(eid):
    entry = Entry.query.filter_by(id=eid).first_or_404()
    form = EntryForm(obj=entry)

    if form.validate_on_submit():
        entry = Entry(title=request.form['title'],
                    content=request.form['content'])
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries'))

    else:
        return render_template('add_entry.html', form=form)

@app.route('/entry/<int:eid>/delete', methods=['GET', 'POST'])
def entry_delete(eid):
    entry = Entry.query.filter_by(id=eid).first_or_404()
    form = EntryDeleteForm()

    if form.validate_on_submit():
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for('entries'))

    else:
        return render_template('delete_entry.html', form=form)


@app.route('/entry/add', methods=['GET', 'POST'])
def add_entry():
    form = EntryForm()

    if form.validate_on_submit():
        entry = Entry(title=request.form['title'],
                    content=request.form['content'])
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('entries'))

    else:
        return render_template('add_entry.html', form=form)
