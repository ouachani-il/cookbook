from flask import Flask, request, jsonify
import requests
import whois
from bs4 import BeautifulSoup
import ssl
import socket
import datetime

app = Flask(__name__)

def get_certificate_info(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        port = 443
        cert = ssl.get_server_certificate((hostname, port))
        return {'valid': True, 'expiration_date': cert}
    except Exception as e:
        return {'valid': False, 'error': str(e)}

def get_whois_info(domain):
    try:
        w = whois.whois(domain)
        return {
            'registrar': w.registrar,
            'creation_date': str(w.creation_date),
            'expiration_date': str(w.expiration_date),
        }
    except Exception as e:
        return {'error': str(e)}

def analyze_html(url):
    try:
        response = requests.get(url)
        html_size = len(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        return {
            'html_size': html_size,
            'title': soup.title.string if soup.title else 'No title found'
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Récupérer les informations WHOIS
    domain = url.split("//")[-1].split("/")[0]
    whois_info = get_whois_info(domain)

    # Analyser le certificat SSL
    cert_info = get_certificate_info(url)

    # Analyser le HTML
    html_info = analyze_html(url)

    return jsonify({
        'whois': whois_info,
        'certificate': cert_info,
        'html_analysis': html_info
    })

if __name__ == '__main__':
    app.run(debug=True)