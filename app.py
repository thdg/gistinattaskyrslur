import os
from datetime import datetime
from flask import Flask, render_template, request
from main import read_reservations, calculate_stats, print_stats

app = Flask(__name__)
UPLOAD_FOLDER = "media/"

@app.route("/", methods=['POST', 'GET'])
def index():
    stats = None
    if request.method == "POST":
        fin = request.files["file"]
        fname = os.path.join(UPLOAD_FOLDER, fin.filename)
        fin.save(fname)
        with open(fname) as csvfile:
            lines = read_reservations(csvfile)
        stats = calculate_stats(lines, month=int(request.form["month"]))
    return render_template("index.html", stats=stats, default_month=datetime.now().month)

