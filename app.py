import streamlit as st
import base64
import textwrap
from CalibrationTools import Calibration
from ControlPlatesArray import PlatesArray
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


if __name__ == '__main__':

    # -- Set page config
    apptitle = 'PhotonQ'

    st.set_page_config(page_title=apptitle,
                       page_icon=":desktop_computer:", layout="wide")

    # Title the app
    st.title('PhotonQ control panel')

    mode_selectbox = st.sidebar.selectbox(
        'Select operation mode:',
        ('General', 'Calibration', 'Tomography', 'QC')
    )

    plates_h = range(-4, 5)
    plates_h = [*map(lambda x: 'Half-wave plate ' + str(x), plates_h)]

    plates_q = range(1, 5)
    plates_q = [*map(lambda x: 'Quarter-wave plate ' + str(x), plates_q)]

    plates = plates_q + plates_h

    if 'pa_init' not in st.session_state:

        st.session_state['pa_init'] = False

    # General mode
    if mode_selectbox == "General":

        st.write('General')

        init_plates = st.sidebar.button(
            'Initialize', disabled=st.session_state['pa_init'])

        if init_plates:

            if 'pa' not in st.session_state:

                st.session_state['pa'] = PlatesArray(1)
                # Initialize connection to plates array. Store init flag pa_init
                st.session_state['pa_init'] = st.session_state['pa'].init()

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

        # Move all plates control
        move_all = st.button(
            'Move all', disabled=not st.session_state['pa_init'])

        if st.session_state['pa_init'] and move_all:

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

        # Close connection
        close = st.button('Close connection',
                          disabled=not st.session_state['pa_init'])

        if close:

            st.session_state['pa'].fina()

            st.session_state['pa_init'] = False
            print(st.session_state['pa_init'])

    # Calibration Mode
    elif mode_selectbox == "Calibration":

        detectors = []

        for detector in [*map(lambda x: 'Detector ' + str(x), range(1, 5))]:
            detectors.append(detector + ',0')
            detectors.append(detector + ',1')

        # Sidebar - Calibration
        cali_form = st.sidebar.form(key='cali_form')
        cali_form.selectbox(
            'Select waveplate to calibrate', plates)
        cali_form.selectbox(
            'Select detector to use', detectors)
        cali_form.form_submit_button('Calibrate')

        # plate = st.sidebar.selectbox(
        #     'Select waveplate to calibrate', plates)

        # detector = st.sidebar.selectbox(
        #     'Select detector to use', detectors)

        # init_button = st.sidebar.form_submit_button('Initialize')

#            if init_button:
#                cali = Calibration()
#                cali.fina()

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

    # QC mode
    elif mode_selectbox == "QC":

        st.write('QC')

    else:

        st.write('Select operaton mode')
