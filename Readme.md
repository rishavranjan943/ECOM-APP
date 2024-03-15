# E-Commerce Website with Authentication, Wishlist, and Cart

This project is a Django-based e-commerce website that includes user authentication, wishlist functionality, and a shopping cart feature. It allows users to register, login, browse products, add them to the wishlist, and manage their shopping cart.

## Features

1. **User Authentication**:
   - Users can register, login, and logout securely.
   - Passwords are encrypted for security.
   - Forgot password feature available.

2. **Product Management**:
   - Admin users can add, update, and delete products.
   - Users can browse products and view detailed information.

3. **Wishlist Functionality**:
   - Users can add products to their wishlist for later purchase.
   - Wishlist items persist across sessions.

4. **Shopping Cart**:
   - Users can add products to their shopping cart.
   - They can view and modify the contents of their cart.
   - Cart items persist across sessions.

1. **Send Email**:
   - Emails are send to users on login,register,update etc.

## Additional Features for Staff Members


1. **Update Profile**:
   - Staff members can update user profiles, including email addresses and names

2. **Product Management**:
   - Staff members have additional privileges for product management:
     - Add Product: Staff members can add new products to the website.
     - Update Product: Staff members can modify existing product details.
     - Delete Product: Staff members can remove products from the website.

## Technologies Used

- Django: Python-based web framework for building the backend.
- HTML/CSS/JavaScript: Frontend technologies for building the user interface.
- SQLite: Lightweight database used for storing product, user, wishlist, and cart information.

## Setup Instructions

1. **Clone the Repository:**
    git clone https://github.com/your_username/e-commerce-project.git
    cd ecom


2. **Install Dependencies:**
    pip install -r requirements.txt


3. **.env file:**
    Create a .env file which consiste of SECRET_KEY of django,EMAIL for sending mail and its passkey

3. **Run Migrations:**
    python mange.py makemigrations
    python manage.py migrate


4. **Create Superuser (Admin):**
    python manage.py createsuperuser


5. **Start the Development Server:**
    python manage.py runserver


6. **Access the Website:**
=======
3. **Add django secret key in settings.py**

4. **Run Migrations:**
    python mange.py makemigrations
    python manage.py migrate

5. **Create Superuser (Admin):**
    python manage.py createsuperuser

6. **Start the Development Server:**
    python manage.py runserver

7. **Access the Website:**
>>>>>>> 9fc97f58b148631722827c287855216d099eb7ba

Open your web browser and go to http://127.0.0.1:8000 to access the website.
Admin dashboard: http://127.0.0.1:8000/admin


Feel free to customize this README according to your specific project structure, technologies used, and any additional features you might have implemented. Make sure to replace placeholder URLs, usernames, and project names with your actual information.
