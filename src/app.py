from flask import Flask, redirect, request, render_template, Response
from flask_cors import CORS
import json

from werkzeug.datastructures import headers
from dobot.dobotController import DobotController
from dobot.position import Position

app = Flask(__name__)
CORS(app)

dobot_controller = DobotController()


@app.route("/")
def index():
    return redirect("/dashboard")


@app.route("/ping")
def ping():
    return "pong"


@app.route("/ports")
def ports():
    available_ports = dobot_controller.list_ports()
    return render_template("port.html", ports=available_ports)


@app.route("/connect", methods=["POST"])
def connect():
    global dobot
    print(request.data)
    port = request.form.get("port")

    if not port:
        port = request.json.get("port")

    dobot_controller.connect(port)

    resp = Response()
    resp.headers["HX-Redirect"] = "/dashboard"
    return resp


@app.route("/disconnect")
def disconnect():
    dobot_controller.disconnect()
    resp = Response()
    resp.headers["HX-Redirect"] = "/dashboard"
    return resp


@app.route("/position")
def position():
    position = dobot_controller.pose()
    return json.dumps(position.__dict__)


@app.route("/home")
def home():
    dobot_controller.home()
    return "OK"


@app.route("/move", methods=["POST"])
def move():
    position = Position(
        request.form.get("x"),
        request.form.get("y"),
        request.form.get("z"),
        request.form.get("r"),
    )
    dobot_controller.move_to(position)
    return "OK"


@app.route("/tool", methods=["POST"])
def suction():
    if request.form["action"] == "enable":
        dobot_controller.enable_tool()
        return "Enabled"

    dobot_controller.disable_tool()
    return "Disabled"


@app.route("/toggle-tool")
def toggle_tool():
    dobot_controller.toggle_tool()
    return "OK"


@app.route("/fields")
def get_fields():
    pose = dobot_controller.pose()
    values = {"x": pose.x, "y": pose.y, "z": pose.z, "r": pose.r}
    return render_template("fields.html", values=values)


@app.route("/dashboard")
def dashboard():
    if dobot_controller.connected:
        return render_template("dashboard.html")

    return render_template("connect.html")
