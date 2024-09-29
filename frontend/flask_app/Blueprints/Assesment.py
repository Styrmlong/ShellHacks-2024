# app.py (or wherever your route is defined)

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    Blueprint,
    current_app, session
)
from datetime import datetime, date

from frontend.flask_app.Blueprints.User import logout
from frontend.flask_app.Forms import ScholarshipApplicationForm
from frontend.flask_app.Models import db, UserModel, ResponseModel  # Ensure correct import path
import os

assesment_bp = Blueprint("assessment", __name__, url_prefix="/assessment")  # Corrected spelling to "assessment"


@assesment_bp.route('/', methods=['GET', 'POST'])
def scholarship_application():


    user_info = session.get("user", {}).get("userinfo", {})
    auth0_id = user_info.get("sub")

    if not auth0_id:
        flash("User not authenticated.", "danger")
        return redirect(url_for("user.login"))

    user = UserModel.query.filter_by(auth0_id=auth0_id).first()

    form = ScholarshipApplicationForm()

    # Dynamically populate expected_graduation choices
    if not form.expected_graduation.choices:
        seasons = ['Fall', 'Spring', 'Summer']
        current_year = datetime.utcnow().year
        end_year = current_year + 10  # Adjust as needed
        graduation_choices = []
        for year in range(current_year, end_year + 1):
            for season in seasons:
                label = f"{season} {year}"
                value = f"{season} {year}"
                graduation_choices.append((value.lower().replace(' ', '-'), label))
        form.expected_graduation.choices = graduation_choices

    if form.validate_on_submit():
        # Retrieve the current user from the session
        auth0_id = session["user"]["userinfo"]["sub"]
        if not auth0_id:
            flash("User not authenticated.", "danger")
            return redirect(url_for("user.login"))

        user = UserModel.query.filter_by(auth0_id=auth0_id).first()
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("user.login"))

        # Ensure date_of_birth is a date object
        if not isinstance(form.date_of_birth.data, date):
            flash("Invalid date format.", "danger")
            return render_template('scholarship_application.html', form=form)

        # Create a new ResponseModel instance with form data
        response = ResponseModel(
            user_id=user.id,
            years_in_college=form.years_in_college.data.title(),
            field_of_study=dict(form.field_of_study.choices).get(form.field_of_study.data),
            expected_graduation=form.expected_graduation.data.replace('-', ' ').title(),
            gpa=form.gpa.data,
            legal_name=form.legal_name.data.title(),
            preferred_name=form.preferred_name.data.title() if form.preferred_name.data else 'N/A',
            date_of_birth=form.date_of_birth.data,  # Should be a date object
            gender_identity=form.gender_identity.data.title(),
            gender_self_describe=form.gender_self_describe.data.title() if form.gender_self_describe.data else 'N/A',
            florida_resident=form.florida_resident.data=="True",
            first_gen_college_student=form.first_gen_college_student.data=="True",
            race_ethnicity=form.race_ethnicity.data.title(),
            race_self_describe=form.race_self_describe.data.title() if form.race_self_describe.data else 'N/A',
            mean_yearly_income=form.mean_yearly_income.data,
            expected_yearly_scholarships=form.expected_yearly_scholarships.data,
            housing=form.housing.data.replace('-', ' ').title()
        )

        try:
            db.session.add(response)
            db.session.commit()
            flash('Submission Successful!', 'success')
            return redirect(url_for('user.profile'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error saving scholarship application: {e}")
            flash('An error occurred while submitting your application. Please try again.', 'danger')

    return render_template('scholarship_application.html', form=form)
