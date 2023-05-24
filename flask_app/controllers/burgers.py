# burgers.py

from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.burger import Burger
from flask_app.models.restaurant import Restaurant


# t- ===========================================
# @ READ /burgers
# t- ===========================================
@app.route("/burgers")
def burgers():
    print()
    print("Hello Craig... Yes I'm working - burgers route")
    print()

    burgers = Burger.get_all()

    return render_template("burgers.html", burgers=burgers)


# t- ===========================================
# @ READ /create_burger
# t- ===========================================
@app.route("/create_burger")
def create_burger():
    print()
    print("Hello Craig... Yes I'm working - create_burger route")
    print()

    restaurants = Restaurant.get_all()

    return render_template("create_burger.html", restaurants=restaurants)


# # * ===========================================
# # ? RENDER FORM - /create_burger_process
# # * ===========================================
@app.route("/create_burger_process", methods=["POST"])
def create_burger_process():
    print()
    print("Hello Craig... Yes I'm working - create_burger_process route")
    print()

    if not Burger.validate_burger(request.form):
        return redirect("/create_burger")

    data = {
        "restaurant_id": request.form["restaurant_id"],
        "name": request.form["name"],
        "bun": request.form["bun"],
        "meat": request.form["meat"],
        "calories": int(request.form["calories"]),
    }

    for key, value in data.items():
        print(f"{key}: {value}")

    Burger.save(data)
    return redirect("/burgers")


# t- ===========================================
# @ READ /burger_details/<int:id>
# t- ===========================================
@app.route("/burger_details/<int:id>")
def burger_details(id):
    print()
    print("Hello Craig... Yes I'm working - burger_details route")
    print()

    data = {"id": id}

    burger = Burger.get_burger_with_toppings(data)

    burger_details = {
        "id": burger.id,
        "name": burger.name,
        "created_at": burger.created_at,
        "updated_at": burger.updated_at,
    }

    return render_template("burger_details.html", burger_details=burger_details)


# t- ===========================================
# ? PROCESS FORM - /
# t- ===========================================

# #! MUST BE AT THE BOTTOM ---------------
# if __name__ == "__main__":
#     app.run(debug=True, host="localhost", port=8000)
