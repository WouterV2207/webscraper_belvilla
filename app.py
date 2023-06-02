import csv
from flask import Flask, render_template, request

from webscraper_belvilla import get_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
   if request.method == 'POST':
       country = request.form['country']
       if country == "belgie":
           url = "https://nl.belvilla.be/search/?filters%5Bcountry_id%5D=28&filters%5Bproperty_type%5D=bungalow%2Cchalet&guests=2&location=Belgi%C3%AB&searchType=country"
       elif country == "nederland":
           url = "https://nl.belvilla.be/search/?filters%5Bcountry_id%5D=143&filters%5Bproperty_type%5D=bungalow%2Cchalet&guests=2&location=Nederland&searchType=country"
       else:
           return render_template('index.html', message="Invalid country selected.")
       data = get_data(url)
       filename = f"{country}.csv"
       with open(filename, mode="w", newline="", encoding="utf-8") as file:
           writer = csv.DictWriter(file, fieldnames=data[0].keys())
           writer.writeheader()
           writer.writerows(data)
       return render_template('index.html', message=f"Data scraped and saved as {filename}")
   return render_template('index.html', message=None)
if __name__ == '__main__':
    app.run()