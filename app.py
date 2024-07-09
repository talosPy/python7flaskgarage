from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Sample data for cars
car1 = {
    "id": "1",
    "number": "5054064",
    "problems": ["engine", "brakes"],
    "urgent": True,
    "image": "https://www.gallery-aaldering.com/wp-content/uploads/gallery/34426179/34426179-83.jpg?v=7",
}
car2 = {
    "id": "2",
    "number": "1331569",
    "problems": ["engine", "brakes"],
    "urgent": True,
    "image": "https://cdn.ferrari.com/cms/network/media/img/resize/5db04650b6fd1830814bec82-ferrari-f12-berlinetta-architecture-1-image?",
}
car3 = {
    "id": "3",
    "number": "7060069",
    "urgent": False,
    "problems": ["gear", "brakes"],
    "image": "https://upload.wikimedia.org/wikipedia/commons/c/ca/2017_Lamborghini_Huracan_LP610.jpg",
}
car4 = {
    "id": "4",
    "number": "0011122",
    "urgent": False,
    "problems": ["gear", "engine"],
    "image": "https://imgd.aeplcdn.com/370x208/n/cw/ec/156405/xuv-3xo-exterior-right-front-three-quarter-33.jpeg?isig=0&q=80",
}
cars = [car1, car2, car3, car4]


@app.route("/")
def cars_list():
    problem_filter = request.args.get('problem', '').lower()
    if problem_filter:
        filtered_cars = [car for car in cars if problem_filter in car.get('problems', [])]
    else:
        filtered_cars = cars

    urgent = request.args.get('urgent', '')
    if urgent.lower() == "true":
        new_cars = [car for car in filtered_cars if car.get('urgent')]
    else:
        new_cars = filtered_cars

    return render_template("car_list.html", car_list=new_cars)


@app.route("/single_car/<id>")
def single_car(id):
    car = next((car for car in cars if car["id"] == id), None)
    return render_template("single_car.html", car=car)


@app.route('/add_car/', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        new_car = {
            'id': len(cars) + 1,
            'number': request.form['number'],
            'image': request.form['image'],
            'problems': request.form.get('problems', '').split(','),
            'urgent': request.form.get('urgent', '').lower() == 'true'
        }
        cars.append(new_car)
        return redirect(url_for('car_list'))
    return render_template('add_car.html')



@app.route("/search_car", methods=["GET", "POST"])
def search_car():
    car = None
    if request.method == "POST":
        car_id = request.form.get("id")
        car = next((car for car in cars if car["id"] == car_id), None)
    return render_template("search_car.html", car=car)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "Talos" and password == "Solat":  # Simple check for example purposes
            session["user"] = username
            return redirect(url_for('cars_list'))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/edit_car/<id>", methods=["GET", "POST"])
def edit_car(id):
    global cars

    if request.method == "POST":
        for car in cars:
            if car['id'] == id:
                car['number'] = request.form.get("number")
                car['urgent'] = request.form.get("urgent").lower() == "true"
                car['image'] = request.form.get("image")
                car['problems'] = [prob.strip() for prob in request.form.get("problems", "").split(",") if prob.strip()]
        return redirect(url_for('cars_list'))

    car_to_edit = next((car for car in cars if car['id'] == id), None)
    if car_to_edit:
        return render_template("edit_car.html", car=car_to_edit)
    else:
        return "Car not found", 404

@app.route('/delete_car/<int:id>', methods=['GET', 'POST'])
def delete_car(id):
    global car_list
    car_list = [car for car in car_list if car['id'] != id]
    return redirect(url_for('car_list'))


if __name__ == "__main__":
    app.run(debug=True, port=9000)
