from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import burger


class Topping:
    db = "burgers_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.topping_name = data["topping_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # need a list to show which burgers are related to this topping
        self.on_burgers = []

    # a class method to save a topping to the database
    @classmethod
    def save(cls, data):
        query = """INSERT INTO toppings (topping_name, created_at, updated_at)  
                    VALUES (%(topping_name)s, NOW(), NOW());"""

        result_id = connectToMySQL(cls.db).query_db(query, data)

        return result_id

    # This method will retrieve the specific topping along with all the burgers associated with it.
    @classmethod
    def get_topping_with_burgers(cls, data):
        query = """SELECT * FROM toppings
                    LEFT JOIN add_ons 
                    ON add_ons.topping_id = toppings.id
                    LEFT JOIN burgers ON add_ons.burger_id = burgers.id
                    WHERE toppings.id = %(id)s;"""

        results = connectToMySQL(cls.db).query_db(query, data)

        # results will be a list of topping objects with the burger attached to each row.

        topping = cls(results[0])

        for row in results:
            # Now we parse the topping data to make instances of
            # toppings and add them into our list.
            burger_data = {
                "id": row["burgers.id"],
                "name": row["name"],
                "bun": row["bun"],
                "calories": row["calories"],
                "created_at": row["toppings.created_at"],
                "updated_at": row["toppings.updated_at"],
            }
            topping.on_burgers.append(burger.Burger(burger_data))

        return topping
