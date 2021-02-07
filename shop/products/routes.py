from flask import redirect ,render_template,url_for,flash,request,session,current_app
from shop import db ,app,photos
from .models import Brand,Category,Addproduct
from .forms import Addproducts
import secrets,os
from sqlalchemy.sql import exists
from sqlalchemy.exc import IntegrityError
@app.route("/car")
def car():
    products=Addproduct.query.filter(Addproduct.stock>0)
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/car.html',products=products,brands=brands,categories=categories)
    
 


@app.route("/cat")
def cat():
    return render_template('products/cat.html')

@app.route("/home")

def home():
   
    return render_template('main/index.html')


@app.route('/brand/<int:id>')

def get_brand(id):
    brand=Addproduct.query.filter_by(brand_id=id)
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/car.html',brand=brand,brands=brands,categories=categories)


@app.route('/categories/<int:id>')

def get_category(id):
    get_cat_prod=Addproduct.query.filter_by(category_id=id)
    brands= Brand.query.join(Addproduct,(Brand.id==Addproduct.brand_id)).all()
    categories=Category.query.join(Addproduct,(Category.id==Addproduct.category_id)).all()
    return render_template('products/car.html',get_cat_prod=get_cat_prod, categories=categories,brands=brands)






@app.route('/addbrand', methods=['GET','POST'])

def addbrand():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))

    if request.method=="POST":
        try:
            getbrand=request.form.get('brand')
            brand=Brand(name=getbrand)
            db.session.add(brand)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f'Brand {getbrand} already exists','danger')
            return redirect('addbrand')
        flash(f'Brand {getbrand} was added to database','success')   
        return redirect(url_for('addcat'))

        getbrand=request.form.get('brand')
        brand=Brand(name=getbrand)
        db.session.add(brand)
        flash(f'The brand {getbrand} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addcat'))

    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>',methods=['GET','POST'])

def updatebrand(id):
    if 'email' not in session:
        flash(f'Please login first','danger')

    updatebrand=Brand.query.get_or_404(id)
    brand=request.form.get('brand')
    if request.method=="POST":
        updatebrand.name=brand
        flash(f'Your brand has been updated','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    
    return render_template('products/updatebrand.html',title='Update brand page',updatebrand=updatebrand)



@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
   
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('brands'))
    
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))
@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    if request.method=="POST":
        try:
            getcat=request.form.get('category')
            cat=Category(name=getcat)
            db.session.add(cat)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash(f'Category {getcat} already exists','danger')
            return redirect('addcat')
        flash(f'category {getcat} was added to database','success')   
        return redirect(url_for('addproduct'))
        getcat=request.form.get('category')
        cat=Category(name=getcat)
        db.session.add(cat)
        flash(f'The category {getcat} was added to your database','success')
        db.session.commit()
        return redirect(url_for('addproduct'))
    return render_template('products/addbrand.html')
    return render_template('products/addbrand.html', brands='brands')
@app.route('/updatecategory/<int:id>',methods=['GET','POST'])

def updatecategory(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
    updatecategory=Category.query.get_or_404(id)
    category=request.form.get('category')
    if request.method=="POST":
        updatecategory.name=category
        flash(f'Your category has been updated','success')
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatebrand.html',title='Update category page',updatecategory=updatecategory)
@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The category {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('category'))
    flash(f"The category {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))
@app.route('/Addproduct',methods=['GET','POST'])
def addproduct():
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    form=Addproducts(request.form)
    if request.method=="POST":
        name=form.name.data
        price=form.price.data
        discount=form.discount.data
        stock=form.stock.data
        origin=form.origin.data
        description=form.description.data
        colors=form.colors.data
        brand=request.form.get('brand')
        category=request.form.get('category')
        image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
        image_2=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
        image_3=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
        certificate=photos.save(request.files.get('certificate'),name=secrets.token_hex(10)+".")
        addpro=Addproduct(name=name,price=price,discount=discount,stock=stock,origin=origin,description=description,colors=colors,brand_id=brand,category_id=category,image_1=image_1,image_2=image_2,image_3=image_3,certificate=certificate)
        db.session.add(addpro)
        flash(f'The product {name} has been added to your database','success')
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('products/addproduct.html',title="Add Product",form=form,brands=brands,categories=categories)
@app.route('/updateproduct/<int:id>',methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash(f'Please login first','danger')
        return redirect(url_for('login'))
    brands=Brand.query.all()
    categories=Category.query.all()
    product=Addproduct.query.get_or_404(id)
    brand=request.form.get('brand')
    category=request.form.get('category')
    form=Addproducts(request.form)
    if request.method=="POST":
        product.name=form.name.data
        product.price=form.price.data
        product.discount=form.discount.data
        product.stock=form.stock.data
        product.origin=form.origin.data
        product.description=form.description.data
        product.colors=form.colors.data
        product.brand_id=brand
        product.category_id=category
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_1))
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_1'),name=secrets.token_hex(10)+".")

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_2))
                product.image_1=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_2'),name=secrets.token_hex(10)+".")

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.image_3))
                product.image_1=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('image_3'),name=secrets.token_hex(10)+".")

        if request.files.get('certificate'):
            try:
                os.unlink(os.path.join(current_app.root_path,"static/images/"+product.certificate))
                product.image_1=photos.save(request.files.get('certificate'),name=secrets.token_hex(10)+".")
            except:
                product.image_1=photos.save(request.files.get('certificate'),name=secrets.token_hex(10)+".")

        db.session.commit()
        flash(f'Your product has been updated','success')
        return redirect(url_for('admin'))
    form.name.data=product.name
    form.price.data=product.price
    form.discount.data=product.discount
    form.stock.data=product.stock
    form.origin.data=product.origin
    form.description.data=product.description
    form.colors.data=product.colors
    brand=request.form.get('brand')
    category=request.form.get('category')
    return render_template('products/updateproduct.html',form=form,brands=brands,categories=categories,product=product)
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))