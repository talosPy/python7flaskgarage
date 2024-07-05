from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

car1 = {
    "id": "1",
    "number": "123-456",
    "problems": ["engine", "breaks"],
    "urgent": True,
    "image": "https://www.gallery-aaldering.com/wp-content/uploads/gallery/34426179/34426179-83.jpg?v=7",
}
car2 = {
    "id": "2",
    "number": "456-789",
    "problems": ["engine", "breaks"],
    "urgent": True,
    "image": "https://cdn.ferrari.com/cms/network/media/img/resize/5db04650b6fd1830814bec82-ferrari-f12-berlinetta-architecture-1-image?",
}
car3 = {
    "id": "3",
    "number": "333-333",
    "urgent": False,
    "problems": ["gear", "breaks"],
    "image": "https://upload.wikimedia.org/wikipedia/commons/c/ca/2017_Lamborghini_Huracan_LP610.jpg",
}
car4 = {
    "id": "4",
    "number": "444-444",
    "urgent": False,
    "problems": ["gear", "engine"],
    "image": "https://imgd.aeplcdn.com/370x208/n/cw/ec/156405/xuv-3xo-exterior-right-front-three-quarter-33.jpeg?isig=0&q=80",
}
cars = [car1, car2, car3, car4]


@app.route("/")
def cars_list():
    # handling problem filter
    problem_filter = request.args.get('problem','').lower()
    if problem_filter:
        filtered_cars = []
        for car in cars:
            if problem_filter in car.get('problems',[]):
                filtered_cars.append(car)
    else:
        filtered_cars = cars  # Return all cars if no problem filter is requested

    # handling urgent after problem filter
    urgent = request.args.get('urgent','')
    if urgent == "true":
        new_cars = [car for car in filtered_cars if car.get('urgent')]
    else:
        new_cars = filtered_cars

    return render_template("car_list.html", car_list=new_cars, problem=problem_filter, urgent=urgent)

    

    # speific problem filter
    # if problem_filter == "engine":
    #     filtered_cars = [car for car in cars if "engine" in car.get('problems')]

        # list comprehension is equivalent to the following code
        # new_cars = []
        # for car in cars:
        #     if car.get('urgent'):
        #         new_cars.append(car)
        


@app.route("/single_car/<id>")
def single_car(id):
    for car in cars:
        if car["id"] == id:
            return render_template("single_car.html", car=car)
    return render_template("single_car.html", car=None)



@app.route("/add_car/", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        new_car = {
            "id": request.form.get("id"),
            "number": request.form.get("number"),
            "urgent": request.form.get("urgent").lower() == "true",  # Convert to boolean
            "image": request.form.get("image"),
            "problems": [prob.strip() for prob in request.form.get("problems", "").split(",") if prob.strip()]
        }
        cars.append(new_car)
        # return redirect('/')  # simple version of redirect
        return redirect(url_for('cars_list'))  # Redirect to cars_list route or any other page
    return render_template("add_car.html")



@app.route("/add_to_list/", methods=["POST", "GET"])
def add_to_list():
    print("****** Adding to list", request.form["cNumber"])
    return "Added to list:" + request.form["cNumber"]


if __name__ == "__main__":
    app.run(debug=True, port=9000)