import stripe
from flask import current_app, Blueprint, request, redirect, url_for, render_template
from ..models import Product
from .. import db

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/products', methods=["POST"])
def add_product():
    name = request.form["name"]
    description = request.form["description"]
    price = int(request.form["price"])

    stripe_secret_key = current_app.config["STRIPE_SECRET_KEY"]
    stripe.api_key = stripe_secret_key

    # create product on Stripe
    stripe_product = stripe.Product.create(name=name, description=description)

    # create a price object on Stripe
    stripe_price = stripe.Price.create(
        product=stripe_product.id,
        unit_amount=price,
        currency='usd',
    )

    # store stripe product and price ids to db
    new_product = Product(
        name=name,
        description=description,
        price=price,
        stripe_product_id=stripe_product.id,
        stripe_price_id=stripe_price.id,
    )

    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for("frontend_bp.index"))
