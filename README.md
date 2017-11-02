# led-toggler
Toggle led lights via web

Play with your Rasperry Pi 3 and led lights. The leds on the breadboard can be toggled on and off via web. A standard web cam can be used to take the pictures.

What is needed: [flask](http://flask.pocoo.org/), [gpio utility](http://wiringpi.com/the-gpio-utility/) and [venv](https://pymotw.com/3/venv/) to isolate the development environment. A server is also needed, I used Apache 2.4.

<img src="/static/2017-10-18.png"/>

### to-do
A better readme with instructions.

### Requirements
<ul>
  <li>Raspberry Pi 3</li>
  <li>Breadboard</li>
  <li>Some leds</li>
  <li>Some resistors</li>
  <li>Jumper wires</li>
  <li>Webcam</li>
</ul>

Optional:
<ul>
  <li>Connector belt</li>
  <li>T-cobbler</li>
</ul>

<p>To make the connections between Pi, breadboard and leds, checkout this video: https://www.youtube.com/watch?v=Au3Gx7lm4xk</p>

### Webcam
To use the webcam, you need fswebcam package. To install:
```
sudo apt-get install fswebcam
```
For more information, check out: https://www.raspberrypi.org/documentation/usage/webcams/

### Create the development environment

Flask docs have good instructions on how to install venv/virtualen and Flask itself:
http://flask.pocoo.org/docs/dev/installation/#install-create-env

### Flask
<p>To get started with Flask, refer to: http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application</p>

This is a step by step commentary for the source code, see project files for the full code.
<br>
Create a new file called leds.py. First the necessary imports:
```
import datetime  // to name the images with date and time
from subprocess import call, check_output // to use command line
from flask import Flask, render_template, request
```

Create Flask instance and define the first route:
```
app = Flask(__name__)

@app.route("/")
def index():
    templateData = {}
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    pass
```

Let's first take a picture everytime a user enters the site(not very elegant, but good enough for this project). Add the following right  after ```def index()```:
```
  now = datetime.datetime.now()
  timeString = now.strftime("%Y-%m-%d-%H-%M-%S")
  call(["fswebcam", "-r", "640x480", "/route/to/your/static/folder"+ timeString + ".jpg"])
  imageName = "/static/" + timeString + ".jpg"
```

To tell the browser the status of the leds (is it on or off), we need to check it on the server side:
```
    led1 = check_output(["gpio", "-g", "read", "17"], universal_newlines=True).rstrip()
    led2 = check_output(["gpio", "-g", "read", "22"], universal_newlines=True).rstrip()
    led3 = check_output(["gpio", "-g", "read", "18"], universal_newlines=True).rstrip()
    led4 = check_output(["gpio", "-g", "read", "23"], universal_newlines=True).rstrip()
```
```check_output``` relays the output of a shell command "gpio -g read [pin number]", which is a call to the gpio pin and returns 0 if pin is not active and 1 if it is active. Replace the pin numbers according to your own setup.

Let's save the statuses to ```templateData```:
```
    templateData = {
        'led1status': led1,
        'led2status': led2,
        'led3status': led3,
        'led4status': led4,
        'image': imageName
    }
```

To get the toggle buttons to work, we need to define a new route:
```
@app.route('/ledToggle')
def ledToggle():
    input = request.args.get('input', 0)
    ledNumber = request.args.get('ledNumber', 0)

    if input == "ON":
        call(["gpio", "-g", "write", ledNumber, "1"])
    else:
        call(["gpio", "-g", "write", ledNumber, "0"])

    return render_template('index.html')
 ```
 
The new route checks the arguments passed from the browser, input is either "ON" or "OFF and ledNumber tells which led to turn on or off via shell command.
