@app.route('/sell', methods=['GET', 'POST'])

def sell():
    form = SellForm(request.form)
    if request.method=="POST" and form.validate():
        sel= Sell(name=form.name.data,email=form.email.data,Shop_Address=form.Shop_Address.data,category=form.category.data,budget=form.budget.data,question=form.question.data,phone=form.phone.data)
        db.session.add(sel)
        db.session.commit()
        server= smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login("Sparematenoreply@gmail.com","Sparemate@123")

        message1="Hi,Thanks for showing intrest to sell with us, we have recieved your data and will get back to you soon for further process"
        server.sendmail("Sparematenoreply@gmail.com",form.email.data,message1)


        flash('Seller form has been filled,an email will be sent to you for the same.','success')
        return redirect(request.args.get('next') or url_for('admin'))
    else:         
         return render_template('admin/sell.html',form=form,title='Seller Form')
    

            