from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import topping
from flask import flash


class Burger:
    db = "burgers_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.bun = data["bun"]
        self.meat = data["meat"]
        self.calories = data["calories"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # a list to associate toppings with burgers
        self.toppings = []

    # ++++++++++++++++++++++++++++++++++++++++++++++++
    #       VALIDATION METHODS
    # ++++++++++++++++++++++++++++++++++++++++++++++++
    #

    @staticmethod
    def validate_burger(form_data):
        is_valid = True

        if len(form_data["name"]) < 3:
            flash("Burger Name must be at least 3 characters.")
            is_valid = False
        if len(form_data["bun"]) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False

        if form_data["calories"]:
            if int(form_data["calories"]) < 200:
                flash("Calories must be 200 or greater.")
                is_valid = False
        else:
            flash("Calories must be 200 or greater.")
            is_valid = False

        if len(form_data["meat"]) < 3:
            flash("Bun must be at least 3 characters.")
            is_valid = False

        return is_valid

    # ++++++++++++++++++++++++++++++++++++++++++++++++
    #       QUERY METHODS
    # ++++++++++++++++++++++++++++++++++++++++++++++++
    #

    @classmethod
    def save(cls, data):
        query = "INSERT INTO burgers (name,bun,meat,calories,created_at,updated_at, restaurant_id) VALUES (%(name)s,%(bun)s,%(meat)s,%(calories)s,NOW(),NOW(), %(restaurant_id)s)"
        result_id = connectToMySQL(cls.db).query_db(query, data)
        return result_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM burgers;"
        burgers_from_db = connectToMySQL(cls.db).query_db(query)
        burgers = []
        for burger in burgers_from_db:
            burgers.append(cls(burger))
        return burgers

    # This method will retrieve the burger with all the toppings that are associated with the burger.
    @classmethod
    def get_burger_with_toppings(cls, data):
        query = """SELECT * FROM burgers 
                    LEFT JOIN add_ons 
                    ON add_ons.burger_id = burgers.id 
                    LEFT JOIN toppings ON add_ons.topping_id = toppings.id 
                    WHERE burgers.id = %(id)s;"""

        result_id = connectToMySQL(cls.db).query_db(query, data)

        # results will be a list of burger objects with the topping attached to each row.

        burger = cls(result_id[0])

        for row in result_id:
            # Now we parse the topping data to make instances of
            # toppings and add them into our list.
            topping_data = {
                "id": row["toppings.id"],
                "topping_name": row["topping_name"],
                "created_at": row["toppings.created_at"],
                "updated_at": row["toppings.updated_at"],
            }
            burger.toppings.append(topping.Topping(topping_data))

        return burger

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM burgers WHERE burgers.id = %(id)s;"
        burger_from_db = connectToMySQL(cls.db).query_db(query, data)
        one_burger = cls(burger_from_db[0])
        return one_burger

    @classmethod
    def update(cls, data):
        query = "UPDATE burgers SET name=%(name)s, bun=%(bun)s, meat=%(meat)s, calories=%(calories)s,updated_at = NOW() WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM burgers WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        return result
