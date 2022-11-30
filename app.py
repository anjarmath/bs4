import os
from flask import Flask, render_template, request, jsonify, url_for
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


@app.route('/', methods = ['GET'])
def covid_detection():
    return render_template("index.html")

@app.route('/predict', methods = ['POST'])
def predict():
    kota = dict(request.form).get('inputKota')

    city=kota.replace(" ","+")
    
    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8',headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')   
    print(soup)
    # location = soup.select('#wob_loc')[0].getText().strip()      
    # info = soup.select('#wob_dc')[0].getText().strip() 
    # print(location)
    # print(info)

    weather = soup.select('#wob_tm')[0].getText().strip()
    satuan = soup.select("span[aria-label*='°']")[0].getText().strip()
    if satuan=='°C':
      print(weather+"°C")
      return render_template("hasil.html", result=weather)
    else:
      celcius = (int(weather)-32)*5/9
      print("%.1f°C"%(celcius))
      return render_template("hasil.html", result=celcius)

if __name__ == '__main__':
    app.run(port=3000, debug=True)