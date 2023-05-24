from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.controllers import burgers
from flask_app.controllers import restaurants


# # t- ===========================================
# # * ============================
# # t- ===========================================


# t- ===========================================
# @ READ Index
# t- ===========================================
@app.route("/")
def index():
    print()
    print("Hello Craig... Yes I'm working - index route")
    print()

    return render_template("index.html")


#! MUST BE AT THE BOTTOM ---------------
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
