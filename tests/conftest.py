import pytest
from app import create_app, db
from app.models import Product
from unittest.mock import patch, MagicMock

@pytest.fixture(scope='module')
def app():
    app = create_app('testing')    
    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context():
        try:
            db.session.remove()
        except RuntimeError as e:
            print(f"RuntimeError during session removal: {e}")
        except Exception as e:
            print(f"Exception during session removal: {e}")
        db.drop_all()
    
@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        product = Product(name='Test Product', description='A product for testing', price=999)
        db.session.add(product)
        db.session.commit()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def mock_create_price():
    mock_price = MagicMock()
    mock_price.id = "price_test_id"
    with patch("stripe.Price.create", return_value=mock_price):
        yield mock_price

@pytest.fixture
def mock_create_product():
    mock_product = MagicMock()
    mock_product.id = "prod_test_id"
    with patch("stripe.Product.create", return_value=mock_product):
        yield mock_product

