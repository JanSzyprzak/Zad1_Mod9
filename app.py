import os
import requests
import csv
from flask import Flask, render_template, request



app = Flask(__name__)


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data = data[0]

with open('rates.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for i in range(len(data['rates'])):
        writer.writerow({'currency': data['rates'][i]['currency'] , 'code': data['rates'][i]['code'], 'bid': data['rates'][i]['bid'], 'ask': data['rates'][i]['ask']})
    

@app.route("/", methods=["GET", "POST"])
def currency_calc():
    bank_response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    nbp_data = bank_response.json()
    nbp_data = nbp_data[0]   
    if request.method == 'GET':
        return render_template('currency_calc.html', nbp_data = nbp_data['rates'])
    elif request.method == "POST":
        currency = request.form
        rate = currency['currencies']
        number = currency['number']
        result = f"{(float(rate) * float(number)):.02f}" + " PLN"
        return render_template('currency_calc.html', nbp_data = nbp_data['rates'], result = result)

if __name__ == '__main__':
    app.run(debug=True)