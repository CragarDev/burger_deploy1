import pymysql.cursors


class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host="localhost",
            # ========================================================================================================
            user="root",  # change the user as needed
            password="rootroot",  # change the password as needed
            # ========================================================================================================
            db=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        self.connection = connection

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                executable = cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # ========================================================================================================
                    # if the query is an INSERT,
                    #   return the ID of the LAST row,
                    #   since that is the row we just ADDED
                    # ========================================================================================================
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # ========================================================================================================
                    # if the query is a SELECT,
                    #   return EVERYTHING that is
                    #   fetched from the database,
                    #
                    #   the result will be a LIST of DICTIONARIES
                    # ========================================================================================================
                    result = cursor.fetchall()
                    return result
                else:
                    # ========================================================================================================
                    # if the query is NOT an insert or a select,
                    #   such as an UPDATE or DELETE,
                    #   commit the changes,
                    #
                    #   return NOTHING
                    # ========================================================================================================
                    self.connection.commit()
            # except Exception as e:
            #     # in case the query fails
            #     print("Something went wrong", e)
            #     return False
            finally:
                # close the connection
                self.connection.close()


# this connectToMySQL function creates an instance of MySQLConnection,
# which will be used by server.py


# connectToMySQL receives the database we're using and
# uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
