from flask import Flask, render_template, request

app = Flask(__name__)

car1 = {"number": "5064054", "problems": ['Fuel Pump'], "image": "https://www.gallery-aaldering.com/wp-content/uploads/gallery/34426179/34426179-83.jpg?v=7", "desc": 'Corvette C1', "urgent": True}
car2 = {"number": "1331356", "problems": ['Bonnet'], "image": "https://cdn.ferrari.com/cms/network/media/img/resize/5db04650b6fd1830814bec82-ferrari-f12-berlinetta-architecture-1-image?", "desc": 'Ferrari F12', "urgent": True}
car3 = {"number": "7065070", "problems": ['Paint Job'], "image": "https://upload.wikimedia.org/wikipedia/commons/c/ca/2017_Lamborghini_Huracan_LP610.jpg", "desc": 'Lamborghini Huracan', "urgent": False}
cars = [car1, car2, car3]


@app.route("/main")
def cars_list():
   return render_template('car_list.html', carz=cars)



@app.route("/single_car/<int:index>")
def single_car(index):
    for car in cars:
        if cars.index(car) == index:
            return render_template('single_car.html', car = car)



@app.route("/add_car/")
def add_car():
    return render_template('add_car.html') 


@app.route("/urgent_car/")
def urgent():
    urgent_cars = [car for car in cars if car['urgent']]
    return render_template('urgent_car.html', cars=urgent_cars)


@app.route("/add_to_list/", methods=["POST", "GET"])
def add_to_list():
    car_number = request.form["cNumber"]
    return "Added to List" + request.form['cNumber']




if __name__ == "__main__":
    app.run(debug=True, port=9000)
