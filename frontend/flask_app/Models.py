from frontend.flask_app.Extensions import DATABASE as db




class ResponseModel(db.Model):
    __tablename__ = 'response'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Fields from ScholarshipApplicationForm
    years_in_college = db.Column(db.String(10))
    field_of_study = db.Column(db.String(100))
    expected_graduation = db.Column(db.String(50))
    gpa = db.Column(db.Float)
    legal_name = db.Column(db.String(255))
    preferred_name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    gender_identity = db.Column(db.String(50))
    gender_self_describe = db.Column(db.String(255))
    florida_resident = db.Column(db.Boolean)
    first_gen_college_student = db.Column(db.Boolean)
    race_ethnicity = db.Column(db.String(50))
    race_self_describe = db.Column(db.String(255))
    mean_yearly_income = db.Column(db.Float)
    expected_yearly_scholarships = db.Column(db.Float)
    housing = db.Column(db.String(50))


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255))
    name = db.Column(db.String(255))

    responses = db.relationship(ResponseModel, backref='user', lazy=True)
