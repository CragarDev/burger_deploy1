# restaurants.py

from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.restaurant import Restaurant
from flask_app.models.burger import Burger


# t- ===========================================
# @ READ /restaurants
# t- ===========================================
@app.route("/restaurants")
def restaurants():
    print("Hello Craig... Yes I'm working - restaurants route")
    # return "Hi Craig, and Hello World!"

    restaurants = Restaurant.get_all()

    return render_template("restaurants.html", restaurants=restaurants)


# t- ===========================================
# @ READ /create_restaurant
# t- ===========================================
@app.route("/create_restaurant")
def create_restaurant():
    print()
    print("Hello Craig... Yes I'm working - create_burger route")
    print()

    return render_template("create_restaurant.html")


# t- ===========================================
# @ READ /restaurant_details/<int:id>
# t- ===========================================
@app.route("/restaurant_details/<int:id>")
def restaurant_details(id):
    print()
    print("Hello Craig... Yes I'm working - restaurant_details route")
    print()

    data = {"id": id}

    restaurant = Restaurant.get_restaurant_with_burgers(data)

    restaurant_details = {
        "id": restaurant.id,
        "name": restaurant.name,
        "burgers": restaurant.burgers,
        "created_at": restaurant.created_at,
        "updated_at": restaurant.updated_at,
    }

    return render_template(
        "restaurant_details.html", restaurant_details=restaurant_details
    )


# # * ===========================================
# # ? RENDER FORM - /create_restaurant_process
# # * ===========================================
@app.route("/create_restaurant_process", methods=["POST"])
def create_restaurant_process():
    print()
    print("Hello Craig... Yes I'm working - create_restaurant_process route")
    print()

    data = {
        "name": request.form["name"],
    }

    for key, value in data.items():
        print(f"{key}: {value}")

    Restaurant.save(data)
    return redirect("/restaurants")


# t- ===========================================
# ? PROCESS FORM - /
# t- ===========================================

#! MUST BE AT THE BOTTOM ---------------
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
