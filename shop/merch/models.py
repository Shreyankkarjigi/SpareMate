from shop import db

class Sell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    Shop_Address = db.Column(db.String(500), unique=False, nullable=False)
    category = db.Column(db.String(100), unique=False, nullable=False)
    budget = db.Column(db.Integer, unique=False, nullable=False)
    question = db.Column(db.String(100), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=False, nullable=False)
    def __repr__(self):
        return '<Sell %r>' % self.name  

db.create_all()
