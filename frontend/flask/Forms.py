# forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    RadioField,
    DecimalField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Optional,
    NumberRange,
    Email,
    ValidationError,
    Length
)
import re

class ScholarshipApplicationForm(FlaskForm):
    # 1. Personal Info
    f_name = StringField('First Name', 
        validators = [DataRequired(), Length(min=2, max=50, message ='Please enter a valid First Name.' )])
    l_name = StringField('Last Name', validators = [DataRequired(),Length(min=2, max=50, message ='Please enter a valid First Name.' )])
    
    # 2. Academic Info
    majors = [
        ('accounting', 'Accounting'),
        ('anthropology', 'Anthropology'),
        ('art', 'Art'),
        ('biology', 'Biology'),
        ('business', 'Business Administration'),
        ('chemistry', 'Chemistry'),
        ('computer-engineering', 'Computer Engineering'),
        ('computer-science', 'Computer Science'),
        ('economics', 'Economics'),
        ('education', 'Education'),
        ('electrical-engineering', 'Electrical Engineering'),
        ('engineering', 'Engineering'),
        ('english', 'English'),
        ('environmental-science', 'Environmental Science'),
        ('finance', 'Finance'),
        ('history', 'History'),
        ('international-relations', 'International Relations'),
        ('journalism', 'Journalism'),
        ('marketing', 'Marketing'),
        ('mathematics', 'Mathematics'),
        ('mechanical-engineering', 'Mechanical Engineering'),
        ('music', 'Music'),
        ('nursing', 'Nursing'),
        ('philosophy', 'Philosophy'),
        ('physics', 'Physics'),
        ('political-science', 'Political Science'),
        ('psychology', 'Psychology'),
        ('sociology', 'Sociology'),
        ('software-engineering', 'Software Engineering'),
        ('statistics', 'Statistics'),
    ]
    # 'other' input option ^ if major is not listed ***

    # Education Information
    years_in_college = SelectField(
        'Years in College',
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

    # Date of Birth Input with Date Picker
    date_of_birth = StringField(
        'Date of Birth (MM/DD/YYYY)',
        validators=[DataRequired(message="Please enter date in MM/DD/YYYY format.")]
    )

    contact_email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    contact_phone = StringField(
        'Phone Number',
        validators=[DataRequired()]
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
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )
    first_gen_college_student = RadioField(
        'Are you a first-generation college student?',
        choices=[('yes', 'Yes'), ('no', 'No')],
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

    # Custom Validators
    def validate_expected_graduation(form, field):
        pattern = r"^(Fall|Spring|Summer) (202[4-9]|203[0-4])$"
        if not re.match(pattern, field.data):
            raise ValidationError("Invalid format. Please select a season and year (e.g., Fall 2024).")

    def validate_gender_self_describe(form, field):
        if form.gender_identity.data == 'self-describe' and not field.data.strip():
            raise ValidationError("Please self-describe your gender.")

    def validate_race_self_describe(form, field):
        if form.race_ethnicity.data == 'self-describe' and not field.data.strip():
            raise ValidationError("Please self-describe your race/ethnicity.")
