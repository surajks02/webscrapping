import requests
import re
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def validate():
    key = request.args.get('key')
    url = 'https://internshala.com/internships/matching-jobs?keywords=' + key
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('div', {'class': 'individual_internship'})
    
    result = []
    for job in jobs:
        title = job.find('h4').text.strip()
        role = job.find('h3').text.strip()
        link = job.find('a').get('href')
        result.append({
            'title': title,
            'link': "https://internshala.com/" + link,
            'role': role
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run()