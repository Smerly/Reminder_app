from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from reminderapp.main.forms import ReminderForm, FriendForm, CategoryForm
from reminderapp.models import User, Reminder, Category
main = Blueprint('main', __name__)

from reminderapp.extensions import db

# Create your routes here.

@main.route('/')
def homepage():
    all_reminders = Reminder.query.all()
    all_users = User.query.all()
    return render_template('home.html', all_reminders=all_reminders, all_users=all_users)

@main.route('/create_reminder', methods=['GET', 'POST'])
@login_required
def create_reminder():
    form = ReminderForm()
    if form.validate_on_submit():
        new_reminder = Reminder(
            name=form.name.data,
            soft_deadline=form.soft_deadline.data,
            hard_deadline=form.hard_deadline.data,
            final_deadline=form.final_deadline.data,
            categories=form.categories.data
        )
        db.session.add(new_reminder)
        db.session.commit()

        flash('Created new reminder.')
        return redirect(url_for('main.homepage', reminder_id=new_reminder.id))
    return render_template('create_reminder.html', form=form)

@main.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(
            name_of_category=form.name_of_category.data,
        )
        db.session.add(new_category)
        db.session.commit()

        flash('New category has been added')
        return redirect(url_for('main.homepage'))
    return render_template('create_category.html', form=form)
# name = db.Column(db.String(80), nullable=False)

# users = db.relationship('User', back_populates='current_reminders')

@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)
