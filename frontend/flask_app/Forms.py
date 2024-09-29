# forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    RadioField,
    DecimalField,
    SubmitField,
)
from wtforms.fields import DateField
from wtforms.validators import (
    DataRequired,
    Optional,
    NumberRange,
    Email,
    ValidationError,
)
import re

class ScholarshipApplicationForm(FlaskForm):
    # List of majors
    majors = [('Architecture', 'Architecture'),
     ('Biological Sciences', 'Biological Sciences'),
     ('Business & Marketing', 'Business & Marketing'),
     ('Communication & Journalism', 'Communication & Journalism'),
     ('Computer & Information Sciences', 'Computer & Information Sciences'),
     ('Cultural Studies', 'Cultural Studies'),
     ('Education', 'Education'),
     ('Engineering', 'Engineering'),
     ('Engineering Technician', 'Engineering Technician'),
     ('English & Literature', 'English & Literature'),
     ('Health Professions', 'Health Professions'),
     ('History', 'History'),
     ('Interdisciplinary Studies', 'Interdisciplinary Studies'),
     ('Languages & Linguistics', 'Languages & Linguistics'),
     ('Liberal Arts & Sciences', 'Liberal Arts & Sciences'),
     ('Mathematics & Statistics', 'Mathematics & Statistics'),
     ('Natural Resources', 'Natural Resources'),
     ('Philosophy & Religious Studies', 'Philosophy & Religious Studies'),
     ('Physical Sciences', 'Physical Sciences'),
     ('Psychology', 'Psychology'),
     ('Public Administration', 'Public Administration'),
     ('Recreation & Fitness Studies', 'Recreation & Fitness Studies'),
     ('Security & Protective Services', 'Security & Protective Services'),
     ('Social Sciences', 'Social Sciences'),
     ('Visual & Performaing Arts', 'Visual & Performaing Arts')
    ]
    # 'other' input option ^ if major is not listed ***

    # Education Information
    years_in_college = SelectField(
        'Year in College',
        choices=[
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
            ('5', '5th Year'),
            ('6', '6th Year'),
        ],
        validators=[DataRequired()]
    )

    # Field of Study/Major/Program - Now a searchable dropdown
    field_of_study = SelectField(
        'Field of Study/Major/Program',
        choices=majors,
        validators=[DataRequired()]
    )

    # Expected Graduation Date (Season Year) - dropdown
    expected_graduation = SelectField(
        'Expected Graduation Date (Season Year)',
        choices=[],  # To be populated dynamically
        validators=[DataRequired()]
    )

    # GPA Input
    gpa = DecimalField(
        'GPA (if applicable) (X.X/4.0)',
        validators=[Optional(), NumberRange(min=0.0, max=4.0)],
        places=2
    )

    # Personal Information
    legal_name = StringField(
        'Name (as it appears on legal documents)',
        validators=[DataRequired()]
    )
    preferred_name = StringField(
        'Preferred name (if different)',
        validators=[Optional()]
    )

    # Date of Birth Input with Date Picker
    date_of_birth = DateField(
        'Date of Birth (MM/DD/YYYY)',
        format='%m/%d/%Y', validators=[DataRequired()]
        )



    # Gender Identity
    gender_identity = SelectField(
        'Gender Identity',
        choices=[
            ('woman', 'Woman'),
            ('man', 'Man'),
            ('non-binary', 'Non-binary'),
            ('transgender', 'Transgender'),
            ('gender-non-conforming', 'Gender non-conforming'),
            ('self-describe', 'Self-describe'),
            ('prefer-not-to-say', 'Prefer not to say')
        ],
        validators=[DataRequired()]
    )
    gender_self_describe = StringField(
        'Please self-describe your gender',
        validators=[Optional()]
    )

    # Additional Demographics
    florida_resident = RadioField(
        'Are you a Florida resident?',
        choices=[(True, 'Yes'), (False, 'No')],
        validators=[DataRequired()]
    )
    first_gen_college_student = RadioField(
        'Are you a first-generation college student?',
        choices=[(True, 'Yes'), (False, 'No')],
        validators=[DataRequired()]
    )

    # Race/Ethnicity
    race_ethnicity = SelectField(
        'Race/Ethnicity',
        choices=[
            ('asian', 'Asian'),
            ('black', 'Black or African American'),
            ('hispanic', 'Hispanic or Latino'),
            ('native-american', 'Native American or Alaska Native'),
            ('pacific-islander', 'Native Hawaiian or Other Pacific Islander'),
            ('white', 'White'),
            ('self-describe', 'Self-describe'),
            ('prefer-not-to-say', 'Prefer not to say')
        ],
        validators=[DataRequired()]
    )
    race_self_describe = StringField(
        'Please self-describe your race/ethnicity',
        validators=[Optional()]
    )

    # New Fields
    mean_yearly_income = DecimalField(
        'Mean Yearly Income',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )

    expected_yearly_scholarships = DecimalField(
        'Expected Yearly Scholarships',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )

    housing = SelectField(
        'Housing',
        choices=[
            ('on-campus', 'On-campus'),
            ('off-campus', 'Off-campus'),
            ('at-home', 'At home')
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField('Submit')

    def validate_gender_self_describe(form, field):
        if form.gender_identity.data == 'self-describe' and not field.data.strip():
            raise ValidationError("Please self-describe your gender.")

    def validate_race_self_describe(form, field):
        if form.race_ethnicity.data == 'self-describe' and not field.data.strip():
            raise ValidationError("Please self-describe your race/ethnicity.")
