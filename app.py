from contextlib import contextmanager, redirect_stdout
from io import StringIO
import streamlit as st
from streamlit.script_run_context import add_script_run_ctx
from streamlit.script_runner import StopException, RerunException
import base64
import textwrap
from CalibrationTools import Calibration
from ControlPlatesArray import PlatesArray
from loop import Mainloop
# Use the non-interactive Agg backend, which is recommended as a
# thread-safe backend.
# See https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads.
import matplotlib as mpl
mpl.use("agg")


def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


def render_svg_setup():

    with open('./appResources/setup.svg', 'r') as file:
        svg = file.read()

    render_svg(svg)
    st.write('Experimental setup')


@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret

        stdout.write = new_write
        yield


def init_plates():  # Initialize connection to plates array. Store init flag pa_init

    if 'pa' not in st.session_state:

        with st_capture(st.session_state['code_display'].code):
            st.session_state['pa'] = PlatesArray(1)

            st.session_state['pa_init'] = st.session_state['pa'].init()


def fina_plates():  # Close connection to plates array. Store init flag pa_init

    st.session_state['pa_init'] = False

    with st_capture(st.session_state['code_display'].code):
        st.session_state['pa'].fina()

    # raise RerunException()


def move_all_plates():  #

    with st_capture(st.session_state['code_display'].code):

        if st.session_state['pa_init']:

            st.session_state['pa'].setPlate(-1, 0, ang_Hm1)
            st.session_state['pa'].setPlate(-2, 0, ang_Hm2)
            st.session_state['pa'].setPlate(-3, 0, ang_Hm3)
            st.session_state['pa'].setPlate(-4, 0, ang_Hm4)

            st.session_state['pa'].setPlate(0, 0, ang_H0)

            st.session_state['pa'].setPlate(1, 0, ang_Q1)
            st.session_state['pa'].setPlate(2, 0, ang_Q2)
            st.session_state['pa'].setPlate(3, 0, ang_Q3)
            st.session_state['pa'].setPlate(4, 0, ang_Q4)
            st.session_state['pa'].setPlate(1, 1, ang_H1)

            st.session_state['pa'].setPlate(2, 1, ang_H2)
            st.session_state['pa'].setPlate(3, 1, ang_H3)
            st.session_state['pa'].setPlate(4, 1, ang_H4)


def move_plate():  #

    with st_capture(st.session_state['code_display'].code):

        if st.session_state['pa_init']:

            st.session_state['pa'].setPlate(path_id_tm, order_id_tm, ang4plate)


def init_loop():

    with st_capture(st.session_state['code_display_PhotonQ'].code):
        Mainloop(5)


if __name__ == '__main__':

    # -- Set page config
    apptitle = 'PhotonQ'

    st.set_page_config(page_title=apptitle,
                       page_icon=":desktop_computer:", layout="wide")

    # Title the app
    st.title('PhotonQ control panel')

    mode_selectbox = st.sidebar.selectbox(
        'Select operation mode:',
        ('General', 'Calibration', 'Tomography', 'PhotonQ')
    )

    plates_h = range(-4, 5)
    plates_h = [*map(lambda x: 'Half-wave plate ' + str(x), plates_h)]

    plates_q = range(1, 5)
    plates_q = [*map(lambda x: 'Quarter-wave plate ' + str(x), plates_q)]

    plates = plates_q + plates_h

    if 'pa_init' not in st.session_state:

        st.session_state['pa_init'] = False

    if 'PhotonQ_init' not in st.session_state:

        st.session_state['PhotonQ_init'] = False

    # General mode
    if mode_selectbox == "General":

        # Initialization of plastes rotation mounts
        # init_plates =
        st.sidebar.button(
            'Connect to plates', disabled=st.session_state['pa_init'], on_click=init_plates)

        # Description
        if st.session_state['pa_init']:
            conection_message = 'Plates connected'
        else:
            conection_message = 'Plates disconnected'

        col1_gen_des, col2_gen_des = st.columns(2)

        with col1_gen_des:

            st.write('General operation mode - ' + conection_message)

        with col2_gen_des:

            # Close connection
            close = st.button(
                'Close connection', disabled=not st.session_state['pa_init'], on_click=fina_plates)

        # setup svg
        render_svg_setup()

        # plates angles input fields
        col1_gen, col2_gen, col3_gen, col4_gen = st.columns(4)

        with col1_gen:

            ang_Hm1 = st.number_input('Insert a H -1 angle', max_value=360)
            ang_Hm2 = st.number_input('Insert a H -2 angle', max_value=360)
            ang_Hm3 = st.number_input('Insert a H -3 angle', max_value=360)
            ang_Hm4 = st.number_input('Insert a H -4 angle', max_value=360)

        with col2_gen:

            ang_H0 = st.number_input('Insert a H 0 angle', max_value=360)

        with col3_gen:

            ang_Q1 = st.number_input('Insert a Q 1 angle', max_value=360)
            ang_Q2 = st.number_input('Insert a Q 2 angle', max_value=360)
            ang_Q3 = st.number_input('Insert a Q 3 angle', max_value=360)
            ang_Q4 = st.number_input('Insert a Q 4 angle', max_value=360)

        with col4_gen:

            ang_H1 = st.number_input('Insert a H 1 angle', max_value=360)
            ang_H2 = st.number_input('Insert a H 2 angle', max_value=360)
            ang_H3 = st.number_input('Insert a H 3 angle', max_value=360)
            ang_H4 = st.number_input('Insert a H 4 angle', max_value=360)

        plates_h = range(-4, 5)
        plates_h = [*map(lambda x: 'Half-wave plate ' + str(x), plates_h)]

        plates_q = range(1, 5)
        plates_q = [*map(lambda x: 'Quarter-wave plate ' + str(x), plates_q)]

        plates = plates_q + plates_h

        # Move individual plate
        #moveplate_form = st.form(key='moveplate_form')
        # moveplate_form.selectbox(
        #    'Select waveplate to move', plates)
        # ang4plate = moveplate_form.number_input(
        #    'Insert plate angle', max_value=360)
        #moveplate_form.form_submit_button('Move plate ', on_click=move_plate)

        # Move all plates control
        move_all = st.button(
            'Move all plates', disabled=not st.session_state['pa_init'], on_click=move_all_plates)

        # Move individual plate
        # plate_to_move = st.selectbox('Select waveplate to move', plates)

        # path_id_tm = plate_to_move[0]
        # order_id_tm = plate_to_move[1]

        # ang4plate = st.number_input(
        #     'Insert plate angle', max_value=360)
        # move = st.button('Move plate ', on_click=move_plate)

        if close:

            st.info('Plates disconnected - Reload page or change operation mode')

        if 'code_display' not in st.session_state:
            st.session_state['code_display'] = st.empty()

    # Calibration Mode
    elif mode_selectbox == "Calibration":

        detectors = []

        for detector in [*map(lambda x: 'Detector ' + str(x), range(1, 5))]:
            detectors.append(detector + ',0')
            detectors.append(detector + ',1')

        # Sidebar - Calibration
        # Select plate and detector for calibration - FORM
        cali_form = st.sidebar.form(key='cali_form')
        plate_to_calibrate = cali_form.selectbox(
            'Select waveplate to calibrate', plates)
        cali_form.selectbox(
            'Select detector to use', detectors)
        cali_form.form_submit_button('Calibrate')

        # Main - Calibration
        st.header('Calibration')

        col1, col2 = st.columns(2)

        with col1:

            render_svg_setup()

        with col2:

            st.write("Data")

    # Tomography mode
    elif mode_selectbox == "Tomography":

        st.write('Tomography')

    # PhotonQ mode
    elif mode_selectbox == "PhotonQ":

        # Initialization of plastes rotation mounts
        init_PhotonQ = st.sidebar.button(
            'Turn On', disabled=st.session_state['pa_init'], on_click=init_loop)

        # Description
        if st.session_state['PhotonQ_init']:
            conection_message = 'PhotonQ On'
        else:
            conection_message = 'PhotonQ Off'

        col1_gen_des, col2_gen_des = st.columns(2)

        with col1_gen_des:

            st.write('PhotonQ operation mode - ' + conection_message)

        with col2_gen_des:

            # Close connection
            close = st.button(
                'Close connection', disabled=not st.session_state['pa_init'])  # , on_click=fina_loop)

        # setup svg
        render_svg_setup()

        if 'code_display_PhotonQ' not in st.session_state:
            st.session_state['code_display_PhotonQ'] = st.empty()

    else:

        st.write('Select operaton mode')
