from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from datetime import datetime, timedelta, timezone

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Sample car data
cars = [
    {
        "id": "1",
        "number": "5054064",
        "problems": ["engine", "brakes"],
        "urgent": True,
        "image": "https://www.gallery-aaldering.com/wp-content/uploads/gallery/34426179/34426179-83.jpg?v=7",
    },
    {
        "id": "2",
        "number": "1331569",
        "problems": ["engine", "brakes"],
        "urgent": True,
        "image": "https://cdn.ferrari.com/cms/network/media/img/resize/5db04650b6fd1830814bec82-ferrari-f12-berlinetta-architecture-1-image?",
    },
    {
        "id": "3",
        "number": "7060069",
        "urgent": False,
        "problems": ["gear", "brakes"],
        "image": "https://upload.wikimedia.org/wikipedia/commons/c/ca/2017_Lamborghini_Huracan_LP610.jpg",
    },
    {
        "id": "4",
        "number": "0011122",
        "urgent": False,
        "problems": ["gear", "engine"],
        "image": "https://imgd.aeplcdn.com/370x208/n/cw/ec/156405/xuv-3xo-exterior-right-front-three-quarter-33.jpeg?isig=0&q=80",
    },
]

SESSION_TIMEOUT = timedelta(minutes=15)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please Login to Continue", "danger")
            return redirect(url_for("login"))

        last_active = session.get("_last_active")
        if last_active and datetime.now(timezone.utc) > last_active + SESSION_TIMEOUT:
            session.clear()
            flash("idle for 15 minutes, Session Expired, Please Login", "danger")
            return redirect(url_for("login"))

        session["_last_active"] = datetime.now(timezone.utc)  # Set current UTC time
        return f(*args, **kwargs)

    return decorated_function



@app.route("/")
@login_required
def cars_list():
    problem_filter = request.args.get('problem', '').lower()
    urgent = request.args.get('urgent', '').lower()

    filtered_cars = [car for car in cars if (not problem_filter or problem_filter in car.get('problems', []))]
    new_cars = [car for car in filtered_cars if (urgent != "true" or car.get('urgent'))]

    return render_template("car_list.html", car_list=new_cars)



@app.route("/add_to_treatment/<id>")
@login_required
def add_to_treatment(id):
    if 'my_cars' not in session:
        session['my_cars'] = []
    car = next((car for car in cars if car["id"] == id), None)
    if car and car not in session['my_cars']:
        session['my_cars'].append(car)
        flash(f'Car {car["number"]} added to your treatment list!', 'success')
    return redirect(url_for('cars_list'))



@app.route("/single_car/<id>")
@login_required
def single_car(id):
    car = next((car for car in cars if car["id"] == id), None)
    return render_template("single_car.html", car=car)



@app.route('/add_car/', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'POST':
        new_car = {
            'id': str(len(cars) + 1),
            'number': request.form['number'],
            'image': request.form['image'],
            'problems': request.form.get('problems', '').split(','),
            'urgent': request.form.get('urgent', '').lower() == 'true'
        }
        cars.append(new_car)
        flash(f'Added Car {new_car["number"]}', 'success')
        return redirect(url_for('cars_list'))
    return render_template('add_car.html')



@app.route("/search_car", methods=["GET", "POST"])
@login_required
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
            session["logged_in"] = True
            session["_last_active"] = datetime.now(timezone.utc)  # Initialize _last_active
            flash('You have logged in!', 'success')
            return redirect(url_for('cars_list'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template("login.html")



@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("logged_in", None)
    session.pop("_last_active", None)
    flash('You have logged out!', 'success')
    return redirect(url_for("login"))



@app.route("/edit_car/<id>", methods=["GET", "POST"])
@login_required
def edit_car(id):
    car = next((car for car in cars if car['id'] == id), None)
    if request.method == "POST" and car:
        car['number'] = request.form.get("number")
        car['urgent'] = request.form.get("urgent").lower() == "true"
        car['image'] = request.form.get("image")
        car['problems'] = [prob.strip() for prob in request.form.get("problems", "").split(",") if prob.strip()]
        return redirect(url_for('cars_list'))
    return render_template("edit_car.html", car=car) if car else "Car not found", 404



@app.route('/delete_car/<int:id>', methods=['GET'])
@login_required
def delete_car(id):
    global cars
    car_to_delete = next((car for car in cars if car['id'] == str(id)), None)
    if car_to_delete:
        cars = [car for car in cars if car['id'] != str(id)]
        flash(f'{car_to_delete["number"]} has been deleted', 'success')
    else:
        flash('Car not found', 'danger')
    return redirect(url_for('cars_list'))



@app.route("/add_existing_car", methods=['GET', 'POST'])
@login_required
def add_existing_car():
    if request.method == 'POST':
        car_id = request.form.get('car_id')
        car = next((car for car in cars if car["id"] == car_id), None)
        if car:
            if 'my_cars' not in session:
                session['my_cars'] = []
            if car not in session['my_cars']:
                session['my_cars'].append(car)
                flash(f'Added Car {car["number"]} to the treatment list!', 'success')
            return redirect(url_for('my_cars'))
    return render_template("add_existing_car.html", car_list=cars)



@app.route("/my_cars")
@login_required
def my_cars():
    my_cars_list = session.get('my_cars', [])
    return render_template("my_cars.html", car_list=my_cars_list)



if __name__ == "__main__":
    app.run(debug=True, port=9000)
