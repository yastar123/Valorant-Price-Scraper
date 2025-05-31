from flask import Flask, render_template, send_file, jsonify
import os
from datetime import datetime
from valorant_scraper import scrape_valorant_prices

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Jalankan scraping
        filename = scrape_valorant_prices()
        return jsonify({
            'success': True,
            'message': 'Scraping berhasil!',
            'filename': filename
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(
            filename,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True) 