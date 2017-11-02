import datetime
from subprocess import call, check_output
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d-%H-%M-%S")
    call(["fswebcam", "-r", "640x480", "/home/ville/ledit/static/"+ timeString + ".jpg"])
    imageName = "/static/" + timeString + ".jpg"

    led1 = check_output(["gpio", "-g", "read", "17"], universal_newlines=True).rstrip()
    led2 = check_output(["gpio", "-g", "read", "22"], universal_newlines=True).rstrip()
    led3 = check_output(["gpio", "-g", "read", "18"], universal_newlines=True).rstrip()
    led4 = check_output(["gpio", "-g", "read", "23"], universal_newlines=True).rstrip()

    templateData = {
        'led1status': led1,
        'led2status': led2,
        'led3status': led3,
        'led4status': led4,
        'image': imageName
    }
    return render_template('index.html', **templateData)

@app.route('/ledToggle')
def ledToggle():
    input = request.args.get('input', 0)
    ledNumber = request.args.get('ledNumber', 0)

    if input == "ON":
        call(["gpio", "-g", "write", ledNumber, "1"])
    else:
        call(["gpio", "-g", "write", ledNumber, "0"])

    return render_template('index.html')

if __name__ == "__main__":
    pass
