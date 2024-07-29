import streamlit as st
import pandas as pd
import joblib

# Load the trained pipeline
rf_model = joblib.load("/Users/rohitsoni/Downloads/random_forest1_model.joblib")

# Title of the Streamlit app
st.title('Crash Severity Prediction App')

def blinking_light(severity):
    color = ""
    text = ""
    image = ""
    if severity == 'Low':
        color = "green"
        text = "Good to go"
        image = "https://media1.tenor.com/m/29ZyTEibyJoAAAAC/motorcycle-stunt.gif"  # URL for green image
    elif severity == 'Medium':
        color = "orange"
        text = "Be Careful!"
        image = "https://cdn.dribbble.com/users/103673/screenshots/3651289/dribble.gif"  # URL for orange image
    else:  # High severity
        color = "red"
        text = "Be very careful!"
        image = "https://i.makeagif.com/media/11-23-2018/_YOKRz.gif"  # URL for red image
        
    return f"""
    <div style="text-align: center;">
        <p style="margin-top: 5px; font-weight: bold; color: {color};">{text}</p>
        <img src="{image}" style="max-width: 700px;">
    </div>
    <style>
    @keyframes blink {{
        50% {{
            opacity: 0;
        }}
    }}
    </style>
    """

# Sidebar for user inputs
with st.sidebar:
    st.header('User Inputs')
    day_of_week = st.selectbox('Day of Week', options=[('Monday', 0), ('Tuesday', 1), ('Wednesday', 2), ('Thursday', 3), ('Friday', 4), ('Saturday', 5), ('Sunday', 6)], format_func=lambda x: x[0])[1]
    active_school_zone_flag = st.selectbox('Active School Zone Flag', options=[('Yes', 1), ('No', 0)], format_func=lambda x: x[0])[1]
    speed_category = st.selectbox('Speed Category', options=[('Stop', 0), ('Slow', 1), ('Medium', 2), ('High', 3)], format_func=lambda x: x[0])[1]
    crash_time_category = st.selectbox('Crash Time Category', options=[('Morning Rush Hour', 0), ('Midday', 1), ('Afternoon Rush Hour', 2), ('Evening', 3), ('Late Night to Early Morning', 4), ('Unknown', 5)], format_func=lambda x: x[0])[1]
    surface_condition = st.selectbox('Surface Condition', options=[('Dry', 0), ('Wet', 1), ('Snow', 2), ('Ice', 3), ('Sand', 4), ('Water (Standing/Moving)', 5), ('Oil', 6), ('Other', 7)], format_func=lambda x: x[0])[1]
    person_helmet = st.selectbox('Person Helmet', options=[('Helmet Used', 0), ('Helmet Not Used', 1), ('No Helmet', 2), ('Not Applicable', 3), ('Unknown', 4)], format_func=lambda x: x[0])[1]
    intersection_related = st.selectbox('Intersection Related', options=[('Intersection', 0), ('Non-Intersection', 1), ('Intersection Related', 2), ('Driveway Access', 3), ('Unknown', 4)], format_func=lambda x: x[0])[1]
    construction_zone_flag = st.selectbox('Construction Zone Flag', options=[('Yes', 1), ('No', 0)], format_func=lambda x: x[0])[1]
    roadway_part = st.selectbox('Roadway Part', options=[('Main Lane', 0), ('Service/Frontage Road', 1), ('Exit/Entrance Ramp', 2), ('Non-Trafficway Area', 3)], format_func=lambda x: x[0])[1]
    traffic_control_type = st.selectbox('Traffic Control Type', options=[('No Control', 0), ('Stop Sign', 1), ('Yield Sign', 2), ('Flagman', 3), ('No Passing Zone', 4), ('School Zone', 5), ('Officer/Guard', 6), ('Flashing Light', 7), ('Signal Light', 8), ('Warning Sign', 9), ('Railroad Crossbuck', 10), ('Railroad Flashing Light', 11), ('Railroad Gates', 12), ('Other', 13), ('Unknown', 14)], format_func=lambda x: x[0])[1]

# Prepare user inputs for prediction
if st.button('Predict Severity'):
    input_features = {
        'Day of Week': [day_of_week],
        'Active School Zone Flag': [active_school_zone_flag],
        'Surface Condition': [surface_condition],
        'Person Helmet': [person_helmet],
        'Intersection Related': [intersection_related],
        'Construction Zone Flag': [construction_zone_flag],
        'Roadway Part': [roadway_part],
        'Traffic Control Type': [traffic_control_type]
    }
    input_df = pd.DataFrame.from_dict(input_features)

    # Making a prediction using the loaded pipeline
    prediction = rf_model.predict(input_df)
    severity = {-1: 'Low', 0: 'Medium', 1: 'High'}[prediction[0]]
    
    # Displaying the prediction
    st.header('Predicted Severity Level: ' + severity)
    
    st.markdown(blinking_light(severity), unsafe_allow_html=True)

