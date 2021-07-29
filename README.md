# Ecommerce_app
This is a Ecommerce project based on the Python framework Django, I want to deliver a fully functional Ecommerce website from start to checkout functionality. This Ecommerce is focussed on the core functionality of the data structure ,how to add items to the chart, how to add payment integration, and the side cookies for unregistered customers, handling the whole backend in Python with a Postgres DB managed by AWS RDS, the statics and the media files are being served from AWS S3.
This Ecommerce project will:
Allow the registered  and unregistered users  to purchase  industrial second hand machinery and equipment.
Provide a secure payment integration with PayPal account  and checkout with PayPal debit/credit card.
View previous and pending orders for registered users.
Allows to registered users to manage (add, change, delete) his profile information  within the website.

## Usage

```python
# To run locally
# Create the virtual Environment and install the dependencies
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt

# Make the migrations
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
## Pictures
### Database Model Diagram
<img src="https://github.com/NorberMV/Ecommerce/blob/master/pics/Ecommerce_db_diagram.png" width="600">



## License
[MIT](https://choosealicense.com/licenses/mit/)

Author: Norberto Moreno | 2021