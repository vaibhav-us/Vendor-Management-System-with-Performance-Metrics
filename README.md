# Vendor-Management-System-with-Performance-Metrics

This is a vendor management system API built with Django REST Framework. It allows users to manage vendors, purchase orders, and track performance metrics.

# Setup Instructions
Prerequisites
Python 3.x
Django
Django REST Framework
# Installation
Clone the repository:
  git clone https://github.com/your-username/vendor-management-system.git
Navigate to the project directory:
  cd vendor-management-system
Install dependencies:
  pip install -r requirements.txt
Run migrations:
  python manage.py migrate
Start the development server:
  python manage.py runserver
  The API will be accessible at http://127.0.0.1:8000/.

# API Endpoints
# Authentication
# Login
URL: /api/login/
Method: POST
Description: Logs in a user and returns a token for authentication.
Parameters:
username: User's username
password: User's password
Authentication required: No
# Logout
URL: /api/logout/
Method: POST
Description: Logs out a user by deleting their token.
Parameters:
token: User's authentication token
Authentication required: Yes
# Vendors
Create a Vendor
URL: /api/vendors/
Method: POST
Description: Creates a new vendor.
Parameters:
name: Name of the vendor
Add any additional parameters required for vendor creation.
Authentication required: Yes
# Retrieve, Update, Delete a Vendor
URL: /api/vendors/<vendor_id>/
Method: GET, PUT, DELETE
Description: Retrieves, updates, or deletes a specific vendor by ID.
Parameters: None
Authentication required: Yes
## Purchase Orders
# Create a Purchase Order
URL: /api/purchase_orders/
Method: POST
Description: Creates a new purchase order.
Parameters:
Add parameters required for purchase order creation.
Authentication required: Yes
# Retrieve, Update, Delete a Purchase Order
URL: /api/purchase_orders/<id>/
Method: GET, PUT, DELETE
Description: Retrieves, updates, or deletes a specific purchase order by ID.
Parameters: None
Authentication required: Yes
# Vendor Performance
# Retrieve Vendor Performance Metrics
URL: /api/vendors/<id>/performance/
Method: GET
Description: Retrieves performance metrics for a specific vendor.
Parameters: None
Authentication required: Yes
Acknowledge Purchase Order
# Acknowledge Receipt of Purchase Order
URL: /api/purchase_orders/<id>/acknowledge/
Method: POST
Description: Acknowledges receipt of a purchase order, updating its acknowledgement date and setting delivery date.
Parameters: None
Authentication required: Yes
