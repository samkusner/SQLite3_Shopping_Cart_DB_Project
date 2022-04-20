## Description
This project was used to develop a web store application. This is an individual assignment using Python/SQL techniques as well as the basic Flask libraries, templating abilities, etc.

The website displays products being sold in several categories. A user visiting the web store can search for products (i.e., search for a specific item name and display that item) or display all items in a certain category. The website displays the available quantity and price for each product.

Only a logged in user can add products to a shopping cart and then checkout to complete a purchase and buy the products. To "buy" a product means to reduce the quantity from that product with the quantity that was "bought".

A logged in user's shopping cart can be viewed, edited, checked out or deleted. A logged in user can also see her order history which should include the list of items purchased and total cost of the order.

## Implementation
- Python Flask was used for all the server side scripting.
- The cart was implemented with Session variables. 
- Minimum information was kept about customers: username and password, first and last name.
- 
## Completed Levels

- [X] The user can see all the products the store sells; minimum of 10 products.
- [X] The user can see all the products in a specific category; minimum of 3 categories.
- [X] Database schema and scripts to create and populate the tables.
  - [X] This must be kept in the `store_schema.sql` file.
- [X] Minimal web interface: web page does not look professional, minimal styling, no form checks.
- [X] The user can search for a specific item by name.
- [X] The user can login, but not create a new account.
  - [X] Users who are not in the DB can't login.
  - [X] Must include a sample user named `testuser` with password `testpass`
- [X] The logged in user can view, add to, edit, check out or delete their cart.
  - [X] The cart should be stored as a session variable.
- [X] The database is updated when a user checks out.
- [X] The store doesn't let a user buy negative amounts or more than is in the inventory.
- [X] A new user can sign up.
- [X] A logged in user can see his/her previous order history.
- [X] The front end is user friendly: website is easy and intuitive to navigate, no server error messages are presented to to user (if an error occurs, give a user friendly message).
- [X] Website style: products have pictures.

## Additional Notes On Assumptions
- In order to view order history, go to order history page where you can view date and total price and click on the order id to view the exact products that were ordered.
- You can only add products to the cart when you are logged in, so the form returns you to the home page.
