class SellForm(Form):
    name = TextField('Name',[validators.Length(min=4, max=25)])
    email = TextField("Email",[validators.Length(min=6, max=35),validators.Email()])
    Shop_Address = TextField("Shop Address",[validators.Length(min=4, max=500)])
    category = TextAreaField("Category of parts",[validators.Length(max=20)])
    budget=IntegerField("what's your budget?",[validators.DataRequired()])
    question = TextAreaField("Do you provide mechanic services?",[validators.Length(max=3)])
    phone=IntegerField('Phone No.(Include STD code)',[validators.DataRequired()])
    submit = SubmitField("Send")