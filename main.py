from flask import Flask, session, render_template, redirect, url_for, request
import sqlite3
from datetime import date
cartIn = 1
app = Flask('app')
app.secret_key = "secret"
loggedIn = 0
empty = 0


# @app.route('/')
# def hello_world():
#   return "Let's shop!???"

@app.route('/login', methods=['GET', 'POST'])
def login():
  global loggedIn
  user = 1
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  if request.method == 'POST':
    loggedIn = 1
    username = request.form["username"]
    password = request.form["password"]
    cursor.execute("Select username, password from user where username = ? and password = ?", (username,password,))
    uname = cursor.fetchone()
    if uname:
      user = 1
      session['username'] = uname['username']
      session['password'] = uname['password']      
      return redirect(url_for('home'))
    else:
      user = 0
  
  return render_template("login.html", title = "Login Page", user = user)

@app.route('/logout')
def logout():
  # Log the user out and redirect them to the login page
  global loggedIn
  loggedIn = 0
  session.clear()
  return redirect(url_for('home'))

@app.route('/', methods=['GET', 'POST'])
def home():
  global cartIn
  global loggedIn
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("Select * from product")
  products = cursor.fetchall()
  cursor.execute("Select distinct category from product order by category ASC")
  categories = cursor.fetchall()
  message = 1
  # uname = session['username']
  if 'cart' not in session :
    session['cart'] = list()

  # pid = cart.keys()
  # quantity = list(cart.values())  
  if 'username' in session:
    message = 1
    if request.method == 'POST':
      product_id = request.form['id']
      qty = request.form['qty']
      cart = session['cart']
      cursor.execute("Select * from product where id = ?", (product_id,))
      product = cursor.fetchone()
      total_cost = int(qty) * int(product["cost"])
      added_item = {"id":product_id, "name":product["name"], "qty":qty, "stock":product["stock"], "price":total_cost}
      for item in cart:
        if item["id"] == product_id:
          item["qty"] = int(qty) + int(item["qty"])
          item["price"] += int(qty) * int(product["cost"])
          session['cart'] = cart
          return redirect(url_for('cart'))
      copy_added_item = added_item.copy()
      cart.append(copy_added_item)
      session['cart'] = cart
      return redirect(url_for('cart'))
  else:
    if request.method == 'POST':
      message = 0
      return redirect(url_for('home'))
  return render_template("home.html", title = "Home Page", categories = categories, products = products, loggedIn = message, cartIn = cartIn, check = loggedIn)


@app.route('/sign_up', methods=['GET', 'POST'])
def signUp():
  global loggedIn
  sign = 0
  repeat = 0
  complete = 0
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  if request.method == 'POST':
    loggedIn = 1
    username = request.form["username"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    password = request.form["password"]
    if not username or not fname or not lname or not password:
      complete = 1
    else:
      cursor.execute("select username from user where username = ?;", (username,))
      user = cursor.fetchone()
      if not user:
        # session["username"] = username
        # session["password"] = password
        # Insert a new student
        cursor.execute("INSERT INTO user (username, fname, lname, password) VALUES (?,?,?,?);",(username, fname, lname, password))
        # Ensure to call commit() to ensure the updates persist
        connection.commit()
        cursor.execute("select username from user where username = ?", (username,))
        uname = cursor.fetchone()
    
        if uname:
          session["username"] = username
          session["password"] = password
          sign = 1
          return redirect(url_for('home'))
  
      else:
          repeat = 1
	# Render the form template
  return render_template('sign_up.html', sign = sign, repeat = repeat, complete = complete)

@app.route('/category/<category>', methods=['GET', 'POST'])
def category(category):
  global loggedIn
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("Select * from product where category = ?", (category,))
  items = cursor.fetchall()
  # loggedIn = 1
  if 'cart' not in session :
    session['cart'] = list()

  # pid = cart.keys()
  # quantity = list(cart.values())  
  if 'username' in session:
    if request.method == 'POST':
      product_id = request.form['id']
      qty = request.form['qty']
      cart = session['cart']
      cursor.execute("Select * from product where id = ?", (product_id,))
      product = cursor.fetchone()
      total_cost = int(qty) * int(product["cost"])
      added_item = {"id":product_id, "name":product["name"], "qty":qty, "stock":product["stock"], "price":total_cost}
      for item in cart:
        if item["id"] == product_id:
          item["qty"] = int(qty) + int(item["qty"])
          item["price"] += int(qty) * int(product["cost"])
          session['cart'] = cart
          return redirect(url_for('cart'))
      copy_added_item = added_item.copy()
      cart.append(copy_added_item)
      session['cart'] = cart
  else:
    if request.method == 'POST':
      return redirect(url_for('home'))
  return render_template('category.html', title = category, items=items, loggedIn = loggedIn)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
  global cartIn
  global loggedIn
  
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cart = session['cart']
  total = 0
  for item in cart:
    total += int(item["price"])
  if request.method == 'POST':
    if request.form["submit"] == "Remove From Cart":
      id = request.form["id"]
      for item in cart:
        if item["id"] == id:
          cart.remove(item)
      session["cart"] = cart
      total = 0
      for item in cart:
        total += int(item["price"])
    elif request.form["submit"] == "Edit Quantity":
      product_id = request.form['id']
      qty = request.form['qty']
      for item in cart:
        if item["id"] == product_id:
          item["price"] = int(item["price"])/int(item["qty"])
          item["qty"] = qty
          item["price"] = int(item["price"]) * int(item["qty"])
      session['cart'] = cart
      total = 0
      for item in cart:
        total += int(item["price"])
    elif request.form["submit"] == "Delete Cart":
      session.pop("cart")
      return redirect(url_for("home"))
    elif request.form["submit"] == "Check Out":
      for item in cart:
        id = item["id"]
        cursor.execute("select stock from product where id = ?", (id,))
        stock = cursor.fetchone()
        qty = int(stock["stock"]) - int(item["qty"])
        cursor.execute("update product set stock = ? where id = ?", (qty,id))
        connection.commit()
      today = date.today()
      cursor.execute('select * from orders')
      orders = cursor.fetchall()
      total = 0
      for item in cart:
        total += int(item["price"])
      orderID = 0
      for order in orders:
        orderID = order["order_id"]
      # connection.commit()
      orderID += 1
      for item in cart:
        cursor.execute("insert or replace into orders (order_id, product_id, qty, username, date, price) values(?,?,?,?,?,?);", (orderID, item["id"],item["qty"],session["username"],today,total))
        connection.commit()
      session.pop("cart")
      return redirect(url_for("home"))
  return render_template('cart.html', items = cart, total = total)

@app.route('/search', methods=['GET', 'POST'])
def search():
  global loggedIn
  query = 1
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("Select * from product")
  products = cursor.fetchall()
  # loggedIn = 1
  if request.method == 'POST':
    if request.form['submit'] == "Search":
      name = request.form['name']
      cursor.execute("Select * from product where name like ?", ('%' + name + '%',))
      products = cursor.fetchall()
      if products:
        query = 1
      else:
        query = 0
    else:
      # loggedIn = 1
      if 'cart' not in session :
        session['cart'] = list()
      if 'username' in session:
        if request.method == 'POST':
          product_id = request.form['id']
          
          qty = request.form['qty']
          cart = session['cart']
          cursor.execute("Select * from product where id = ?", (product_id,))
          product = cursor.fetchone()
          total_cost = int(qty) * int(product["cost"])
          added_item = {"id":product_id, "name":product["name"], "qty":qty, "stock":product["stock"], "price":total_cost}
          for item in cart:
            if item["id"] == product_id:
              item["qty"] = int(qty) + int(item["qty"])
              item["price"] += int(qty) * int(product["cost"])
              session['cart'] = cart
          return redirect(url_for('cart'))
          copy_added_item = added_item.copy()
          cart.append(copy_added_item)
          
          session['cart'] = cart
      else:
        if request.method == 'POST':
          return redirect(url_for('home'))
  return render_template('search.html', items = products, loggedIn = loggedIn, query = query)

@app.route('/order_history')
def order_history():
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("Select distinct order_id, date, price from orders where username = ?", (session["username"],))
  history = cursor.fetchall()
  return render_template('order_history.html', categories = history)

@app.route('/order_history/<order_id>')
def order_history_spec(order_id):
  connection  = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("Select * from orders join product on orders.product_id = product.id where order_id = ?", (order_id,))
  history = cursor.fetchall()
  return render_template('spec_order.html', items = history)

app.run(host='0.0.0.0', port=8080)