# %load menu.py
# !/usr/bin/python
import sqlite3
from sys import argv
import matplotlib.pyplot as plt

import numpy as np
from sklearn.linear_model import LinearRegression

# for Python 2.x users
try:
    input = raw_input
except NameError:
    pass


class Program:
    def __init__(self):  # PG-connection setup
        self.conn = sqlite3.connect('mondial.db')  # establish database connection
        self.cur = self.conn.cursor()  # create a database query cursor

        # specify the command line menu here
        self.actions = [self.population_query, self.raw_data_population, self.total_city_population_by_year,
                        self.city_population_and_prediction, self.linear_prediction_for_all_cities,
                        self.prediction_per_year, self.population_prediction, self.hypothesis, self.exit]
        # menu text for each of the actions above
        self.menu = ["Population Query", "Raw yearly data population", "Total city population by year",
                     "City population and prediction", "linear prediction for all cities",
                     "Prediction population per year", "Prediction vizualisation", "Hypothesis", "Exit"]
        self.cur = self.conn.cursor()

    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i, x in enumerate(self.menu):
            print("%i. %s" % (i + 1, x))
        return self.get_int()

    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number, genious.... :(")

    def population_query(self):
        minpop = input("min_population: ")
        maxpop = input("max_population: ")
        print("minpop: %s, maxpop: %s" % (minpop, maxpop))
        try:
            query = "SELECT * FROM city WHERE population >=%s AND population <= %s" % (minpop, maxpop)
            print("Will execute: ", query)
            result = self.cur.fetchall()
            self.cur.execute(query)
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            connection1.rollback()
            exit()

        self.print_answer(result)

    def exit(self):
        self.cur.close()
        self.conn.close()
        exit()

    # ------------------------------------------------------Solution------------------------------------------------------------
    # ------------------------------------------------------Question a----------------------------------------------------------
    def raw_data_population(self):
        xy = "select Year, Population from Citypops";
        print("Q1: (start) " + xy)
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

        xs = []
        ys = []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            if (r[0] != None and r[1] != None):
                xs.append(int(r[0]))
                ys.append(int(r[1]))
            else:
                print("Dropped tuple ", r)
        plt.scatter(xs, ys)
        plt.title("City population raw data")
        plt.savefig("figure.png")  # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    # --------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Question b----------------------------------------------------------
    def total_city_population_by_year(self):
        xy = "Select Year, sum(population) from Citypops group by Year";
        print("Q2: (start) " + xy)
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

        xs = []
        ys = []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            if (r[0] != None and r[1] != None):
                xs.append(int(r[0]))
                ys.append(int(r[1]))
            else:
                print("Dropped tuple ", r)
        plt.scatter(xs, ys)
        plt.title("Total City population by year in database")
        plt.savefig("figure.png")  # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    # --------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------Question c----------------------------------------------------------

    def city_population_and_prediction(self):
        # ask for city country code and city name
        country_code, city_name = self.get_country_code_and_city_name()

        xy = f"Select Year, population from Citypops where Country='{country_code}' and city='{city_name}';"
        print("Q3: (start) " + xy)
        try:
            self.cur.execute(xy)
            data = self.cur.fetchall()
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

        xs = []
        ys = []
        for r in data:
            # you access ith component of row r with r[i], indexing starts with 0
            # check for null values represented as "None" in python before conversion and drop
            # row whenever NULL occurs
            if (r[0] != None and r[1] != None):
                xs.append(int(r[0]))
                ys.append(int(r[1]))
            else:
                print("Dropped tuple ", r)

        # predict the graph
        regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        a = regr.coef_[0][0]
        b = regr.intercept_[0]

        x = np.linspace(xs[0], 2030, 250000)
        y = a * x + b

        plt.scatter(xs, ys)
        plt.plot(x, y, '-r')
        plt.title(f"City population and prediction for: {city_name} a= {a}, b={b}, score={score}")
        plt.savefig("figure.png")  # save figure as image in local directory
        plt.show()  # display figure if you run this code locally, otherwise comment out

    def get_country_code_and_city_name(self):
        """Retrieves inputs from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                country_code = input("country code: ")

                while True:
                    try:
                        city_name = input("city name: ")
                        return country_code, city_name
                    except (NameError, ValueError, TypeError, SyntaxError):
                        print("That was not a number, genious.... :(")

            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number, genious.... :(")

            # --------------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------Question d----------------------------------------------------------

    def linear_prediction_for_all_cities(self):
        try:
            # create second cursor
            second_conn = sqlite3.connect('mondial.db')
            second_cur = second_conn.cursor()

            # drop table and create table with the correct columns
            drop_table = "Drop table if exists linearprediction;"

            create_table = "CREATE TABLE IF NOT EXISTS linearprediction (name VARCHAR2(50) NOT NULL, country VARCHAR2(4) NOT NULL, a REAL NOT NULL, b REAL NOT NULL, score REAL NOT NULL);"

            print("Q4: (start) " + drop_table)
            print(create_table)

            self.cur.execute(drop_table)
            self.cur.execute(create_table)

            # loop over the city query
            city_iterator = "Select distinct city, country from citypops;"

            self.cur.execute(city_iterator)
            city = self.cur.fetchone()

            self.conn.commit()

            while (city != None):

                if (city[0] != None and city[1] != None):

                    select_data = "Select year, population from citypops where city = :city and country = :country"
                    second_cur.execute(select_data, {"city": str(city[0]), "country": str(city[1])})
                    data = second_cur.fetchall()

                    # extract the data
                    xs = []
                    ys = []
                    for r in data:
                        # you access ith component of row r with r[i], indexing starts with 0
                        # check for null values represented as "None" in python before conversion and drop
                        # row whenever NULL occurs
                        if (r[0] != None and r[1] != None):
                            xs.append(int(r[0]))
                            ys.append(int(r[1]))
                        else:
                            print("Dropped tuple ", r)

                    # predict the graph
                    if (len(xs) > 1 and len(ys) > 1):
                        regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
                        score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
                        a = regr.coef_[0][0]
                        b = regr.intercept_[0]

                        if (score <= 1 and score >= 0):
                            second_cur.execute("insert into linearPrediction values (:name, :country, :a, :b, :score)",
                                               {"name": str(city[0]), "country": str(city[1]), "a": str(a), "b": str(b),
                                                "score": str(score)})

                    city = self.cur.fetchone()
                    self.conn.commit()
                else:
                    print("Dropped tuple ", r)
                    city = self.cur.fetchone()
                    self.conn.commit()

            second_conn.commit()
            # show the new relation
            self.cur.execute("Select * from linearPrediction")
            result = self.cur.fetchall()
            self.conn.commit()

        #            self.print_answer(result)

        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            second_conn.rollback()
            exit()

    # --------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------question e----------------------------------------------------

    def prediction_per_year(self):
        try:
            # drop table and create table with the correct columns
            drop_table = "Drop table if exists prediction;"

            create_table = "CREATE TABLE IF NOT EXISTS prediction (name VARCHAR2(50) NOT NULL, country VARCHAR2(4) NOT NULL, population INT NOT NULL, year INT NOT NULL);"

            print("Q4: (start) " + drop_table)
            print(create_table)

            self.cur.execute(drop_table)
            self.cur.execute(create_table)
            self.conn.commit()

            # create the table linear prediction
            self.linear_prediction_for_all_cities()

            # iterate over the years
            for year in range(1950, 2051):
                self.cur.execute(
                    "INSERT INTO prediction (name, country, population, year) SELECT name, country, a * :year + b AS population, :year AS year FROM linearprediction",
                    {"year": str(year)})

            self.conn.commit()

            self.cur.execute("SELECT * FROM prediction")
            result = self.cur.fetchall()
            self.conn.commit()


        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

    # --------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------question f----------------------------------------------------

    def population_prediction(self):
        try:
            # query for prediction
            self.prediction_per_year()

            country = input("Country: ")
            city = input("City: ")

            self.cur.execute("Select year, population FROM prediction where name like :city and country like :country",
                             {"country": country, "city": city})
            data = self.cur.fetchall()
            self.conn.commit()

            # query for evg and max population
            self.cur.execute(
                "SELECT AVG(population), MAX(population) FROM prediction WHERE name like :city and country like :country",
                {"country": country, "city": city})
            avg_max = self.cur.fetchall()
            self.conn.commit()

            avg_population = avg_max[0][0]
            max_population = avg_max[0][1]

            #  uses our new prediction table to visualize the population trends for all cities and years as a scatter plot
            title = f"Population trends for {city} in {country} with predicted mean of {avg_population} and predicted maximum population {max_population} "

            xs = []
            ys = []
            for r in data:
                if (r[0] != None and r[1] != None):
                    xs.append(int(r[0]))
                    ys.append(int(r[1]))

            plt.scatter(xs, ys)
            plt.title(title)
            plt.show()


        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            exit()

    # --------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------question g---------------------------------------------------

    # You could ask if there are correlations between (longitude, latitude) position of a city and population growth.
    def hypothesis(self):
        try:

            query = "CREATE VIEW IF NOT EXISTS Popdata AS SELECT Year year, city name, citypops.population population, citypops.country country, longitude longitude, latitude latitude, elevation elevation, agriculture agriculture, service service, industry industry, inflation inflation FROM Citypops JOIN city ON citypops.city = city.name AND citypops.country = city.country AND citypops.province = city.province JOIN Economy ON citypops.country = economy.country;"

            self.cur.execute(query)
            self.conn.commit()

            min_latitude = input("Minimum latitude : ")
            max_latitude = input("Maximum latitude : ")

            min_longitude = input("Minimum longitude : ")
            max_longitude = input("Maximum longitude : ")

            query = ("Select longitude, latitude, AVG(population) FROM Popdata WHERE Latitude > :min_latitude " +
                     "and latitude < :max_latitude " +
                     "and longitude > :min_longitude " +
                     "and longitude < :max_longitude group by name")

            data = self.cur.execute(query, {"min_latitude": min_latitude, "max_latitude": max_latitude,
                                            "min_longitude": min_longitude, "max_longitude": max_longitude})
            self.conn.commit()

            xs = []
            ys = []
            zs = []
            for r in data:
                if (r[0] != None and r[1] != None and r[2] != None):
                    xs.append(float(r[0]))
                    ys.append(float(r[1]))
                    zs.append(float(np.log(r[2])))

            print(xs)
            print(ys)
            print(zs)

            plt.scatter(xs, ys, c=zs, s=2)
            plt.xlim([min_longitude, max_longitude])
            plt.ylim([min_latitude, max_latitude])
            plt.axis('scaled')
            plt.show()

        except sqlite3.Error as e:
            print("Error message:", e.args[0])
            self.conn.rollback()
            exit()

    # --------------------------------------------------------------------------------------------------------------------------

    def print_answer(self, result):
        print("-----------------------------------")
        for r in result:
            print(r)
        print("-----------------------------------")

    def run(self):
        while True:
            try:
                self.actions[self.print_menu() - 1]()
            except IndexError:
                print("Bad choice")
                continue


if __name__ == "__main__":
    db = Program()
    db.run()
