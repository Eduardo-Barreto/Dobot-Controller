from flask import Flask, redirect, request, render_template, Response
from flask_cors import CORS
import json
import logging
from tinydb import TinyDB, Query
from datetime import datetime

from dobot.dobotController import DobotController
from dobot.position import Position

app = Flask(__name__)
CORS(app)

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

db = TinyDB("logs.json")

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
    port = request.form.get("port")
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "connect",
        "parameters": {"port": port},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    dobot_controller.connect(port)

    resp = Response()
    resp.headers["HX-Redirect"] = "/dashboard"
    return resp


@app.route("/disconnect")
def disconnect():
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "disconnect",
        "parameters": {},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    dobot_controller.disconnect()
    resp = Response()
    resp.headers["HX-Redirect"] = "/dashboard"
    return resp


@app.route("/position")
def position():
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "position",
        "parameters": {},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    position = dobot_controller.pose()
    return json.dumps(position.__dict__)


@app.route("/home")
def home():
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "home",
        "parameters": {},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    dobot_controller.home()
    return "ok"


@app.route("/move", methods=["POST"])
def move():
    x = float(request.form.get("x"))
    y = float(request.form.get("y"))
    z = float(request.form.get("z"))
    r = float(request.form.get("r"))
    position = Position(x, y, z, r)

    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "move",
        "parameters": {"x": x, "y": y, "z": z, "r": r},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    dobot_controller.move_to(position)
    return "ok"


@app.route("/tool", methods=["POST"])
def suction():
    action = request.form["action"]

    ip_address = request.remote_addr

    if action == "enable":
        log_entry = {
            "timestamp": str(datetime.now()),
            "ip_address": ip_address,
            "action": "enable_tool",
            "parameters": {},
        }
        logger.info(log_entry)

        db.insert(log_entry)

        dobot_controller.enable_tool()
        return "enabled"
    else:
        log_entry = {
            "timestamp": str(datetime.now()),
            "ip_address": ip_address,
            "action": "disable_tool",
            "parameters": {},
        }
        logger.info(log_entry)

        db.insert(log_entry)

        dobot_controller.disable_tool()
        return "disabled"


@app.route("/toggle-tool")
def toggle_tool():
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "toggle_tool",
        "parameters": {},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    dobot_controller.toggle_tool()
    return "ok"


@app.route("/input-fields")
def get_fields():
    ip_address = request.remote_addr

    log_entry = {
        "timestamp": str(datetime.now()),
        "ip_address": ip_address,
        "action": "get_fields",
        "parameters": {},
    }
    logger.info(log_entry)

    db.insert(log_entry)

    pose = dobot_controller.pose()
    values = {"x": pose.x, "y": pose.y, "z": pose.z, "r": pose.r}
    return render_template("input_fields.html", values=values)


@app.route("/current-fields")
def current_fields():
    pose = dobot_controller.pose()
    values = {"x": pose.x, "y": pose.y, "z": pose.z, "r": pose.r}
    suction = "Enabled" if pose.suction else "Disabled"
    suction_tag = "success" if pose.suction else "danger"
    return render_template(
        "current_fields.html", values=values, suction=suction, suction_tag=suction_tag
    )


@app.route("/dashboard")
def dashboard():
    ip_address = request.remote_addr

    if dobot_controller.connected:
        log_entry = {
            "timestamp": str(datetime.now()),
            "ip_address": ip_address,
            "action": "view_dashboard",
            "parameters": {},
        }
        logger.info(log_entry)

        db.insert(log_entry)

        return render_template("dashboard.html")
    else:
        log_entry = {
            "timestamp": str(datetime.now()),
            "ip_address": ip_address,
            "action": "view_connect_page",
            "parameters": {},
        }
        logger.info(log_entry)

        db.insert(log_entry)

        return render_template("connect.html")


@app.route("/list-logs")
def list_logs():
    logs = db.all()
    logs_with_ids = [{"doc_id": log.doc_id, "data": log} for log in logs]
    print(logs_with_ids)
    return render_template("list_logs.html", logs=logs_with_ids)


@app.route("/logs")
def show_logs():
    return render_template("logs.html")


@app.route("/logs/<id>", methods=["DELETE"])
def delete_log(id: int):
    print(id)
    db.remove(doc_ids=[int(id)])

    resp = Response()
    resp.headers["HX-Redirect"] = "/logs"
    return resp


@app.route("/logs/all", methods=["DELETE"])
def clear_all_logs():
    db.truncate()

    resp = Response()
    resp.headers["HX-Redirect"] = "/logs"
    return resp
