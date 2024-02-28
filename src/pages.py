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


def move(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    axis = st.selectbox("Select the axis to move:", ["X", "Y", "Z", "R"])
    distance = st.number_input("Distance to move:", value=1.0)
    wait = st.checkbox("Wait for movement to finish")

    if st.button("Move"):
        dobot.move_by_axis(axis, distance, wait)


def move_to(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    x = st.number_input("X coordinate:", value=0.0)
    y = st.number_input("Y coordinate:", value=0.0)
    z = st.number_input("Z coordinate:", value=0.0)
    r = st.number_input("R coordinate:", value=0.0)
    wait = st.checkbox("Wait for movement to finish")

    if st.button("Move to"):
        dobot.move_to(Position(x, y, z, r), wait)


def home(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    # botao que manda pra home
    home_button = st.button("Press to go home")

    if home_button:
        dobot.home()


def tool(dobot):
    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    toggle = st.toggle("Tool state", dobot.tool_enabled)

    if toggle == dobot.tool_enabled:
        return

    if toggle:
        dobot.enable_tool()
    else:
        dobot.disable_tool()


def control(dobot):
    # slider x slider y slider z slider r
    #   Todos os sliders representam a posição atual do robô
    #   Ao mover o slider, o robô move
    #   Ao mover o robô, o slider se move
    # botao que manda pra home
    # toggle de ferramenta

    if not dobot.connected:
        st.warning("Please connect to the robot first")
        return

    current_position = dobot.pose()

    x = st.slider("X", -300, 300, current_position.x)
    y = st.slider("Y", -300, 300, current_position.y)
    z = st.slider("Z", -300, 300, current_position.z)
    r = st.slider("R", -180, 180, current_position.r)

    dobot.move_to(Position(x, y, z, r), wait=False)

    tool_toggle = st.checkbox("Tool State", dobot.tool_enabled)

    if tool_toggle != dobot.tool_enabled:
        if tool_toggle:
            dobot.enable_tool(time_to_wait=0)
        else:
            dobot.disable_tool(time_to_wait=0)

    st.button("Home", on_click=dobot.home)

    dobot.pose().to_dict()


pages = {
    "Connect": connect,
    "Move": move,
    "Move to": move_to,
    "Home": home,
    "Tool": tool,
    "Control": control,
    "Save": None,
    "Run": None,
}