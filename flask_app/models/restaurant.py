from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.burger import Burger

# from flask_app.models import burger


class Restaurant:
    db = "burgers_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # We create a list so that later we can add in
        # all the burgers that are associated with a restaurant.
        self.burgers = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO restaurants (name,created_at,updated_at) VALUES (%(name)s,NOW(),NOW())"
        result_id = connectToMySQL(cls.db).query_db(query, data)

        return result_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM restaurants;"
        restaurants_from_db = connectToMySQL(cls.db).query_db(query)
        restaurants = []
        for restaurant in restaurants_from_db:
            restaurants.append(cls(restaurant))

        return restaurants
    
    

    # We need to import the burger class from our models
    @classmethod
    def get_restaurant_with_burgers(cls, data):
        query = """ 
                    SELECT * FROM restaurants 
                    LEFT JOIN burgers 
                    ON restaurants.id = burgers.restaurant_id 
                    WHERE restaurants.id = %(id)s;
                """
        results = connectToMySQL(cls.db).query_db(query, data)

        # results will be a list of topping objects
        # with the burger attached to each row.

        restaurant = cls(results[0])

        # Now we parse the burger data to make instances of burgers
        # and add them into our list.

        for row in results:
            burger_data = {
                "id": row["burgers.id"],
                "name": row["burgers.name"],
                "bun": row["bun"],
                "meat": row["meat"],
                "calories": row["calories"],
                "created_at": row["burgers.created_at"],
                "updated_at": row["burgers.updated_at"],
                "restaurant_id": row["restaurant_id"],
            }

            restaurant.burgers.append(Burger(burger_data))

        return restaurant

    # @classmethod
    # def get_one(cls, data):
    #     query = "SELECT * FROM burgers WHERE burgers.id = %(id)s;"
    #     burger_from_db = connectToMySQL(cls.db).query_db(query, data)
    #     one_burger = cls(burger_from_db[0])
    #     return one_burger

    # @classmethod
    # def update(cls, data):
    #     query = "UPDATE burgers SET name=%(name)s, bun=%(bun)s, meat=%(meat)s, calories=%(calories)s,updated_at = NOW() WHERE id = %(id)s;"
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     return result

    # @classmethod
    # def destroy(cls, data):
    #     query = "DELETE FROM burgers WHERE id = %(id)s;"
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     return result
