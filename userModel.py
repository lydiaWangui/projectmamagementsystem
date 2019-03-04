from main import db

class Authentication(db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer,primary_key=True)
    fullName = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)


    def createUser(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls,email,password):
        record = Authentication.query.filter_by(email=email,password =password)
        if record.first():
            return True
        else:
           return False


    # check if email already exists
    @classmethod
    def check_mail(cls, email):
        record = Authentication.query.filter_by(email=email)
        if record.first():
            return True
        else:
            return False

