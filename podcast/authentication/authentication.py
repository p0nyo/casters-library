from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

from functools import wraps

import podcast.utilities.utilities as utilities
import podcast.authentication.services as services
import podcast.adapters.repository as repo

authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    
    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)

            # All is well, redirect the user to the login page.
            return redirect(url_for('authentication_bp.login'))
        except services.NameNotUniqueNameException:
            user_name_not_unique = 'Your user name is already taken - please supply another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/register.html',
        form=form,
        user_name_error_message=user_name_not_unique,
        password_error_message=None,
        handler_url=url_for('authentication_bp.register')
    )
    

@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user_name_not_recognised = None
    password_does_not_match_user_name = None

    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.user_name.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['user_name'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['user_name'] = user['user_name']
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            user_name_not_recognised = 'User name not recognised - please supply another'

        except services.AuthenticationException:
            # authentication failed, set a suitable error message.
            password_does_not_match_user_name = 'Password does not match supplied user name - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/login.html',
        user_name_error_message=user_name_not_recognised,
        password_error_message=password_does_not_match_user_name,
        form=form
    )
    
@authentication_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'user_name' in session:
        session.clear()
        return redirect(url_for('home_bp.home'))
    else:
        return redirect(request.referrer)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('authentication_bp.login'))
        return view(*args, **kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8)
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [DataRequired(message='Username required'),
                                         Length(min=8, message='Username must be at least 8 characters'),])
    password = PasswordField('Password', [DataRequired(message='Password Required'), PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    user_name = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Login')
