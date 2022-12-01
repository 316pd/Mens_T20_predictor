import streamlit as st
import pickle
import pandas as pd
from PIL import Image

image = Image.open("icc.jpg")
st.sidebar.image(image.resize((350, 80)))
Teams = ['Afghanistan', 'Australia', 'Bangladesh', 'England', 'India','Ireland', 'Netherlands', 'New Zealand', 'Pakistan', 'Scotland','South Africa', 'Sri Lanka', 'West Indies', 'Zimbabwe']
City = ['Abu Dhabi', 'Adelaide', 'Ahmedabad', 'Al Amarat', 'Amstelveen','Antigua', 'Auckland', 'Bangalore', 'Barbados', 'Basseterre','Belfast', 'Bengaluru', 'Birmingham', 'Bloemfontein', 'Bready',
       'Brisbane', 'Bristol', 'Bulawayo', 'Canberra', 'Cape Town','Cardiff', 'Carrara', 'Centurion', 'Chandigarh', 'Chattogram',
       'Chennai', 'Chester-le-Street', 'Chittagong', 'Christchurch','Colombo', 'Cuttack', 'Dehra Dun', 'Dehradun', 'Delhi', 'Derry',
       'Deventer', 'Dhaka', 'Dharamsala', 'Dharmasala', 'Dominica','Dubai', 'Dublin', 'Durban', 'East London', 'Edinburgh',
       'Greater Noida', 'Gros Islet', 'Guwahati', 'Guyana', 'Hambantota','Hamilton', 'Harare', 'Hobart', 'Hyderabad', 'Indore', 'Jamaica',
       'Johannesburg', 'Kandy', 'Kanpur', 'Karachi', 'Khulna','Kimberley', 'King City', 'Kolkata', 'Lahore', 'Lauderhill','London', 'Londonderry', 'Lucknow', 'Manchester', 'Melbourne',
       'Mirpur', 'Mount Maunganui', 'Mumbai', 'Nagpur', 'Nairobi','Napier', 'Nelson', 'Nottingham', 'Paarl', 'Pallekele', 'Perth',
       'Port Elizabeth', 'Potchefstroom', 'Providence', 'Pune', 'Rajkot','Ranchi', 'Rawalpindi', 'Rotterdam', 'Sharjah', 'Southampton',
       'St George\'s', 'St Kitts', 'St Lucia', 'St Vincent', 'Sydney','Sylhet', 'Taunton', 'The Hague', 'Thiruvananthapuram', 'Trinidad',
       'Victoria', 'Visakhapatnam', 'Wellington']

score_predictor = pickle.load(open('pipe_score_predict.pkl','rb'))
win_predictor = pickle.load(open('pipe_win_predict.pkl','rb'))

st.title('Men\'s T20 Predictor')

user_menu = st.sidebar.radio(
    'Select option',
    ('Score Predictor(1st Innings)','Win Predictor(2nd Innings)')
)
if user_menu == 'Score Predictor(1st Innings)':
    st.title('Batting team score predictor(1st Innings)')
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select the batting team', Teams)
    with col2:
        bowling_team = st.selectbox('Select the bowling team', Teams)
    selected_city = st.selectbox('Select the city(venue)', City)
    col3, col4 = st.columns(2)
    with col3:
        cur_score = st.number_input('Current score',min_value=0, value=0, step=1)
        cur_score = int(cur_score)
    with col4:
        cur_over = st.number_input('Overs completed(works for > 5 overs)')
    col5, col6 = st.columns(2)
    with col5:
        cur_out = st.number_input('Wickets out',min_value=0, max_value=10, value=0, step=1)
        cur_out = int(cur_out)
    with col6:
        run_prev5 = st.number_input('Runs scored in last 5 overs',min_value=0, value=0, step=1)
    if st.button('Predict'):
        cur_balls = int((int(cur_over)*6) + (cur_over%int(cur_over))*10)
        balls_left = 120-cur_balls
        crr = (cur_score*6)/cur_balls
        wickets_left = 10 - cur_out
        points = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],
        'current_score':[cur_score],'balls_left':[balls_left],'wickets_left':[wickets_left],
        'crr':[crr],'last_five':[run_prev5]})
        result = score_predictor.predict(points)
        st.header(batting_team + "'s predicted score : " + str(int(result)))
        # st.text(batting_team + "'s winning chances : " + str(round(result[0][1]*100, 2)) + "%")
        # st.text(bowling_team + "'s winning chances : " + str(round(result[0][0]*100, 2)) + "%")
if user_menu == 'Win Predictor(2nd Innings)':
    st.title('Winning percentage predictor')
    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select the batting team', Teams)
    with col2:
        bowling_team = st.selectbox('Select the bowling team', Teams)
    selected_city = st.selectbox('Select the city(venue)', City)
    col3, col4 = st.columns(2)
    with col3:
        target = st.number_input('Target',min_value=0, value=0, step=1)
        target = int(target)
    with col4:
        cur_score = st.number_input('Current score',min_value=0, value=0, step=1)
        cur_score = int(cur_score)
    col5, col6 = st.columns(2)
    with col5:
        cur_over = st.number_input('Overs completed')
    with col6:
        cur_out = st.number_input('Wickets out',min_value=0, max_value=10, value=0, step=1)
        cur_out = int(cur_out)
    if st.button('Predict'):
        runs_left = target - cur_score
        cur_balls = int((int(cur_over)*6) + (cur_over%int(cur_over))*10)
        balls_left = 120-cur_balls
        crr = (cur_score*6)/cur_balls
        rrr = (runs_left*6)/balls_left
        wickets_left = 10 - cur_out
        points = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],
        'runs_left':[runs_left],'balls_left':[balls_left],'wickets_left':[wickets_left],
        'target':[target],'crr':[crr],'rrr':[rrr]})
        result = win_predictor.predict_proba(points)
        st.text(batting_team + "'s winning chances : " + str(round(result[0][1]*100, 2)) + "%")
        st.text(bowling_team + "'s winning chances : " + str(round(result[0][0]*100, 2)) + "%")
