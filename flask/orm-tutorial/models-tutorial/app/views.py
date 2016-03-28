from flask import render_template, redirect, request
from app import app, models, db
from .forms import CustomerForm, AddressForm, OrderForm


@app.route('/')
def index():
    return redirect('/customers')

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = models.Customer(
                            company = form.company.data,
                            email = form.email.data,
                            phone = form.phone.data)
        db.session.add(customer)
        #commit to get ID for associating address
        db.session.commit()
        
        address = models.Address(
            streetno = form.streetno.data,
            streetname = form.streetname.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            current = True,
            customer_id = customer.id)
        db.session.add(address)
        db.session.commit()
        return redirect('/customers')
    return render_template('customer.html', form=form)

@app.route('/customers', methods=['GET'])
def display_customer():
    customers = models.Customer.query.all()
    
    #get all current addresses, in order of customer id
    address_query = models.Address.query.filter(models.Address.current == True, models.Address.customer_id != None).order_by(models.Address.customer_id).all()
    addresses = ['dummy'] #dummy value so indices line up w/ customer ids
    for add in address_query:
        addresses.append(str(add.streetno) + ' ' + add.streetname + ', ' + add.city + ', ' + add.state + ' ' + str(add.zipcode))
  

    return render_template('home.html',
                            customers=customers, addresses=addresses)

@app.route('/addresses', methods=['GET', 'POST'])
def select_address_company():
    #get all customers and render in "select" menu
    customers = models.Customer.query.all()
    return render_template('chooseadd.html', customers=customers)

@app.route('/addresslist', methods=['GET', 'POST'])
def show_company_adds():

    cust_key=request.args['cust_select']

    customer = models.Customer.query.get(cust_key).company
    addresses = models.Address.query.filter_by(customer_id=cust_key).all()
    return render_template('addlist.html', customer = customer, addresses = addresses)

@app.route('/add_address', methods=['GET', 'POST'])
def add_address():
    #get list of companies for select field to control inputs
    companies = models.Customer.query.all()
    all_company_names = [cust.company for cust in companies]
    kv_company_names = list(enumerate(all_company_names))
    #adjust indices
    kv_company_names_adj = [(value+1, label) for value, label in kv_company_names]
    

    addForm = AddressForm()
    #populate "company" select field with company names
    addForm.company_name.choices = kv_company_names_adj
    if addForm.validate_on_submit():
        newaddress  = models.Address(
            streetno = addForm.streetno.data,
            streetname = addForm.streetname.data,
            city = addForm.city.data,
            state = addForm.state.data,
            zipcode = addForm.zipcode.data,
            current = True,
            customer_id = addForm.company_name.data)
        
        #set all other addresses to current==False
        currAddress = models.Address.query.filter(models.Address.current == True, models.Address.customer_id == newaddress.customer_id).all()
        for x in currAddress:
            x.current = False
        db.session.add(newaddress)
        
        db.session.commit()
        return redirect('/customers')


    return render_template('newaddress.html', addForm = addForm)

@app.route('/neworder', methods=['GET', 'POST'])
def add_order():
    #get list of companies for select field to control inputs
    #try and set this off into a function if there's time
    companies = models.Customer.query.all()
    all_company_names = [cust.company for cust in companies]
    kv_company_names = list(enumerate(all_company_names))
    #adjust indices
    kv_company_names_adj = [(value+1, label) for value, label in kv_company_names]

    newOrderForm = OrderForm()
    newOrderForm.company_name.choices = kv_company_names_adj

    #This is not working.  I have not been able to figure out how many-to-many relationships are handled and 
    #what data types/attributes are required.  
    if newOrderForm.validate_on_submit():
        print(newOrderForm.company_name.data, newOrderForm.total_spent.data, newOrderForm.num_parts_ordered.data)
        order_company = models.Customer.query.get(newOrderForm.company_name.data)
        print(order_company)
        order_company.orders.append(models.Order(
            customers = newOrderForm.company_name.data,
            total_spent = newOrderForm.total_spent.data,
            num_parts_ordered = newOrderForm.num_parts_ordered.data
        ))
        #print(newOrder)
    #else:
     #   print(newOrderForm.company_name.data, newOrderForm.total_spent.data, newOrderForm.num_parts_ordered.data)

      #  return redirect('/customers')

    return render_template('neworder.html', newOrderForm = newOrderForm)


