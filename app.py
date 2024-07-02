from flask import Flask, render_template

app = Flask(__name__)

car1 = {"number": "123-456", "problems": []}
car2 = {"number": "456-789", "problems": []}
cars = [car1, car2]


@app.route("/")
def cars_list():
   return render_template('car_list.html', car_list=cars)

    # final_str = ""
    # for car in cars:
    #     final_str += f"<p>{car['number']}</p>"

    # return final_str


@app.route("/single_car/<int:index>")
def single_car(index):
    return (
        f"<p>Number:{cars[index]['number']} <br> Problems:{cars[index]['problems']}</p>"
    )


@app.route("/add_car/")
def add_car():
    print("****** Adding car")
    return "Adding car"


if __name__ == "__main__":
    app.run(debug=True, port=9000)
