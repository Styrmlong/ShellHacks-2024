# forms.py

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    RadioField,
    DecimalField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Optional,
    NumberRange,
    ValidationError,
    Length
)
import re

class ScholarshipApplicationForm(FlaskForm):

    # 1. Personal Info
    f_name = StringField('First Name', 
        validators = [DataRequired(), Length(min=2, max=50, message ='Please enter a valid First Name.' )])
    l_name = StringField('Last Name', validators = [DataRequired(),Length(min=2, max=50, message ='Please enter a valid Last Name.' )])
    
    date_of_birth = StringField('Date of Birth (MM/DD/YYYY)', validators=[DataRequired(message="Please enter date in MM/DD/YYYY format.")])


    # 2. Academic Info Updated
    majors = [
        ('', 'Select a Major'),
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
        ('other', 'Other (please specify)')
    ]

    major = SelectField('Field of Study: Major', choices=majors, validators=[DataRequired()])
    other_major = StringField('If Other, please specify your major')


    academic_standing = SelectField(
        'Academic Standing',
        choices=[
            ('', 'Select your academic standing'),
            ('freshman', 'Freshman'),
            ('sophomore', 'Sophomore'),
            ('junior', 'Junior'),
            ('senior', 'Senior'),
            ('graduate', 'Graduate')
        ],
        validators=[DataRequired()]
    )

graduation_month = SelectField(
'Expected Graduation Month',
choices=[
('Spring', 'Spring'),
     ('Fall', 'Fall'),
        ('Summer', 'Summer')
    ],
    validators=[DataRequired()]
)

graduation_year = SelectField(
    'Expected Graduation Year',
    choices=[(str(year), str(year)) for year in range(2024, 2030)],  # Example years
    validators=[DataRequired()]
)

gpa = DecimalField(
        'GPA (if applicable)',
        validators=[Optional(), NumberRange(min=0.0, max=4.0)],
        places=2
    )

gender_identity = SelectField(
        'Gender Identity',
        choices=[
            ('woman', 'Woman'),
            ('man', 'Man'),
            ('non-binary', 'Non-binary'),
            ('transgender', 'Transgender'),
            ('gender-non-conforming', 'Gender non-conforming'),
            ('prefer-not-to-say', 'Prefer not to say')
        ],
        validators=[DataRequired()]
    )

    # Additional Demographics
fl_resident = RadioField(
        'Are you a Florida resident?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )
first_gen_college_student = RadioField(
        'Are you a first-generation college student?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )

citizenship_status = SelectField(
        'Citizenship/Residency Status',
        choices=[
            ('us_citizen', 'U.S. Citizen'),
            ('permanent_resident', 'U.S. Permanent Resident'),
            ('international_f1', 'International Student (F-1 Visa)'),
            ('international_j1', 'International Student (J-1 Visa)')
        ],
        validators=[DataRequired()]
    )

race_ethnicity = SelectField(
        'Race/Ethnicity',
        choices=[
            ('asian', 'Asian'),
            ('black', 'Black or African American'),
            ('hispanic', 'Hispanic or Latino'),
            ('native-american', 'Native American or Alaska Native'),
            ('pacific-islander', 'Native Hawaiian or Other Pacific Islander'),
            ('white', 'White'),
            ('prefer-not-to-say', 'Prefer not to say')
        ],
        validators=[DataRequired()]
    )

    # 3. Financial Qs

employed_or_nah = RadioField(
        'Are you currently employed?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )

housing = SelectField(
        'Current Housing Circumstance',
        choices=[
            ('on-campus', 'On-campus'),
            ('off-campus', 'Off-campus'),
        ],
        validators=[DataRequired()]
    )

is_financially_independent = RadioField(
        'Are you financially independent?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )

    # Household Income
household_income = SelectField(
        'What is your annual household income?',
        choices=[
            ('', 'Select household income range'),
            ('less_than_25k', 'Less than $25,000'),
            ('25k_to_49k', '$25,000 - $49,999'),
            ('50k_to_74k', '$50,000 - $74,999'),
            ('75k_to_99k', '$75,000 - $99,999'),
            ('100k_or_more', '$100,000 or more')
        ],
        validators=[DataRequired()]
    )

 # Dependents
dependents = IntegerField(
        'Number of dependents in household (including yourself)',
        validators=[
            DataRequired(),
            NumberRange(min=1, max=20, message="Please enter a number between 1 and 20")
        ],
        render_kw={"placeholder": "Enter number between 1 and 20"}
    )

 # Educational Expenses - Based on FIU Tuition Calculator *can link in question*
est_expenses = DecimalField(
        'Estimated annual educational expenses at FIU',
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100000, message="Please enter an amount between $0 and $100,000")
        ],
        render_kw={"placeholder": "Enter amount in USD (max $100,000)"}
    )

 # FAFSA Eligibility *can link below in question*
fafsa = RadioField(
        'Are you eligible to file a FAFSA (Free Application for Federal Student Aid)?',
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
            ('unsure', 'I\'m not sure')
        ],
        validators=[DataRequired()]
    )

submit = SubmitField('Submit')

    # Custom Validators
def validate_gpa(self, field):
        if field.data is not None:
            if field.data < 0.0 or field.data > 4.0:
                raise ValidationError("GPA must be between 0.0 and 4.0")
            if len(str(field.data).split('.')[-1]) > 2:
                raise ValidationError("GPA should have at most 2 decimal places")
            
def validate_estimated_educational_expenses(self, field):
        if field.data > 100000:
            raise ValidationError("Please contact the financial aid office for expenses exceeding $100,000")
