import streamlit as st
from dobotController import DobotController
from position import Position


def connect(dobot):
    import streamlit as st

    available_ports = dobot.list_ports()
    selected_port = st.selectbox("Select the robot port:", available_ports)

    if st.button("Connect Robot"):
        dobot.connect(selected_port)

        st.success(f"Connected to port {selected_port}")


def speed(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    velocity = st.number_input("Velocity:", value=100.0)
    acceleration = st.number_input("Acceleration:", value=100.0)

    if st.button("Set Speed"):
        dobot.set_speed(velocity, acceleration)


def move(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    axis = st.selectbox("Select the axis to move:", ["x", "y", "z", "r"])
    distance = st.number_input("Distance to move:", value=1.0)
    wait = st.checkbox("Wait for movement to finish")

    if st.button("Move"):
        dobot.move_by_axis(axis, distance, wait)


def move_to(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    current_position = dobot.pose()

    x = st.number_input("X coordinate:", value=current_position.x)
    y = st.number_input("Y coordinate:", value=current_position.y)
    z = st.number_input("Z coordinate:", value=current_position.z)
    r = st.number_input("R coordinate:", value=current_position.r)

    col1, col2 = st.columns(2)

    wait = col1.checkbox("Wait for movement to finish")
    if col2.button("Move to"):
        dobot.move_to(Position(x, y, z, r), wait)


def home(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    home_button = st.button("Press to go home")

    if home_button:
        dobot.home()


def tool(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    st.button("Enable Tool", on_click=dobot.enable_tool)
    st.button("Disable Tool", on_click=dobot.disable_tool)


def control(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    current_position = dobot.pose()
    print(current_position)

    x = st.slider("X", -300.0, 300.0, current_position.x)
    y = st.slider("Y", -300.0, 300.0, current_position.y)
    z = st.slider("Z", -300.0, 300.0, current_position.z)
    r = st.slider("R", -180.0, 180.0, current_position.r)

    speed = st.number_input("Speed", value=100.0)
    acceleration = st.number_input("Acceleration", value=100.0)

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Move"):
        dobot.move_to(Position(x, y, z, r), wait=True)
        dobot.set_speed(speed, acceleration)

    if col2.button("Enable Tool"):
        dobot.enable_tool()

    if col3.button("Disable Tool"):
        dobot.disable_tool()

    col4.button("Home", on_click=dobot.home)


pages = {
    "Connect": connect,
    "Set speed": speed,
    "Move": move,
    "Move to": move_to,
    "Home": home,
    "Tool": tool,
    "Control": control,
    "Save": None,
    "Run": None,
}
