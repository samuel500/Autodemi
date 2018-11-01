from flask import (render_template, url_for, flash, redirect, request, abort, jsonify, Blueprint)
from flask_login import current_user, login_required
from autodemi import db
from autodemi.models import Content, UserLibrary
from autodemi.contents.forms import ContentForm
from sqlalchemy import and_
from autodemi.contents.helper import *



contents = Blueprint('contents', __name__)



@contents.route("/content/add", methods=['GET', 'POST'])
@login_required
def add_content():
    form = ContentForm()
    if form.validate_on_submit():
        image_file = screenshot_site(form.link.data)
        link = process_url(form.link.data)
        content = Content(title=form.title.data, link=link, image_file=image_file, description=form.description.data, creator=current_user)
        db.session.add(content)
        db.session.commit()
        flash('The content has been added to our database!', 'success')
        return redirect(url_for('main.home'))
    return render_template('add_content.html', title='Add Content',
                            form=form, legend='Add Content')

@contents.route("/content/user_interaction", methods=['POST'])
def content_user_interaction():
    if not current_user.is_authenticated:
        return jsonify(message="redirect", target=url_for('users.login'))

    button_id = request.form['button_id'].split('-')[0]
    button_id = "".join([x for x in button_id if not x.isdigit()])
    button_context = request.form['button_id'][len(button_id):]
    content_id = int(request.form['content_id'])

    record = UserLibrary.query.filter(and_(UserLibrary.content_id==content_id, UserLibrary.user_id==current_user.id)).first()

    if record:
        if button_id == 'add_to_library':
            db.session.delete(record)
            to_return = []
        else:
            setattr(record, button_id, not getattr(record, button_id))
            to_return = record
    else:
        new_library_content = UserLibrary(user_id=current_user.id, content_id=content_id, consumed=False, to_consume=False, consuming=False, star=False)
        if button_id != 'add_to_library':
            setattr(new_library_content, button_id, not getattr(new_library_content, button_id))
        db.session.add(new_library_content)
        to_return = new_library_content

    to_return = content_interactions_html_dict(to_return)
    db.session.commit()
    return jsonify(message="success", interactions=to_return, button_context=button_context)


@contents.route("/content/<int:content_id>")
def content(content_id):
    content = Content.query.get_or_404(content_id)
    interaction = UserLibrary.query.filter(and_(UserLibrary.content_id==content.content_id, UserLibrary.user_id==current_user.id)).first()
    content = [content, content_interactions_html_dict(interaction)]
    return render_template('content.html', content=content)


@contents.route("/content/delete", methods=['POST'])
@login_required
def delete_content():
    if not current_user.is_authenticated:
        return jsonify(message="redirect", target=url_for('users.login'))

    content_id = int(request.form['content_id'])
    content = Content.query.get_or_404(content_id)
    if content.creator != current_user:
        abort(403)
    interactions = UserLibrary.query.filter(UserLibrary.content_id==content.content_id).all()
    for interaction in interactions:
        db.session.delete(interaction)
    db.session.delete(content)


    db.session.commit()
    flash('Your content has been deleted!', 'success')
    return jsonify(message="redirect", target=url_for('main.home'))
