## E-commerce Shop with Django

This project is a full-stack e-commerce website built using Python's Django framework and front-end integration with django's templating system.

### Technologies Used

* **Backend:**
    * Django
* **Frontend:**
    * Django Templates
    * Bootstrap framework v4
    * HTML5
    * CSS3
    * JavaScript
* **Database:**
    * PostgreSQL 
* **Payment Gateway:**
    * PayPal

### Features

* User registration and login
* Product browsing by category and search
* Detailed product pages with descriptions, images, and variations
* Shopping cart & Wishlist management (add, remove, update quantities)
* Secure checkout process with PayPal integration
* Order history and tracking
* Customized Django Admin panel


### Running the Project

1. Clone this repository.
2. Create a virtual environment and activate it.
3. Install dependencies: `pip install -r requirements.txt`
4. Configure your database settings in `settings.py`.
5. Run database migrations: `python manage.py migrate`
6. Create a superuser for admin access: `python manage.py createsuperuser`
7. Configure PayPal API credentials.
8. Run the development server: `python manage.py runserver`

### Deployment

This project can be deployed to various platforms that support Python and Django.  Instructions for deployment will vary depending on the chosen platform. 

* Some popular options include:
    * Heroku
    * AWS Elastic Beanstalk
    * DigitalOcean

### Further Development

This project provides a solid foundation for a functional e-commerce website. Here are some ideas for further development:

* Integration with additional payment gateways
* User reviews and ratings
* Product recommendations using Elastic search or similar technology
* Discount codes and promotions
* Order fulfillment automation
