from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle as pk

# Load the data and model
read_file = pd.read_csv("CleanedData.csv")
model = pk.load(open("RandomForest_pred.pkl", 'rb'))

app = Flask(__name__)

@app.route("/", methods=["GET"])
def fun():
    compny = sorted(read_file['company'].unique())
    fuel_type = sorted(read_file['fuel_type'].unique())
    return render_template("home.html", compny=compny, fuel_type=fuel_type)
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get_models", methods=["GET"])
def get_models():
    company = request.args.get('company')
    models = sorted(read_file[read_file['company'] == company]['name'].unique())
    return jsonify(models=models)


@app.route("/predict", methods=["POST"])
@app.route("/predict", methods=["POST"])
def predict():
    car_name = request.form['carName']
    company = request.form['company']
    year = int(request.form['year'])
    km_driven = int(request.form['kmDriven'])
    fuel = request.form['fuel']

    # Prepare the input for the model
    input_data = pd.DataFrame([[car_name, company, year, km_driven, fuel]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Prepare data to display on the result panel
    result_data = {
        'Car Name': car_name,
        'Company': company,
        'Year': year,
        'KM Driven': km_driven,
        'Fuel': fuel,
        'Predicted Price': prediction
    }

    # Render the template with the result data
    compny = sorted(read_file['company'].unique())
    fuel_type = sorted(read_file['fuel_type'].unique())
    years = sorted(read_file['year'].unique())
    return render_template("home.html", compny=compny, fuel_type=fuel_type, years=years, result_data=result_data)