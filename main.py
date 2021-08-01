import streamlit as s
from PIL import Image
import requests
from fake_useragent import UserAgent
import pandas as pd

ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


def run():
    # img1 = Image.open('C:/Users/KIIT/Desktop/PYTHON AND ML/PROJECTS/VAccination Centre Checker/vaccine1.png')
    # img1 = img1.resize((300, 300))
    # s.image(img1, use_column_width=False)
    video_file = open('C:/Users/KIIT/Desktop/PYTHON AND ML/PROJECTS/VAccination Centre Checker/v_Trim.mp4', 'rb')
    video_bytes = video_file.read()
    s.video(video_bytes,start_time=0)
    s.title("Vaccination Centre Checker")
    s.markdown("<h4 style='text-align: left; color: red;'>* Data is fetched from Government API</h4><br>",
               unsafe_allow_html=True)

    area_pin = s.text_input("Enter your Area Pin-Code")

    vac_date = s.date_input("Choose the date")

    age_display = ['18-45', '45+']
    age = s.selectbox("Your Age", age_display)

    if s.button("Search"):
            vac_date = str(vac_date).split('-')
            new_date = vac_date[2] + '-' + vac_date[1] + '-' + vac_date[0]
            age_val = 0
            if age == '18-45':
                age_val = 18
            else:
                age_val = 45
            response = requests.get(
                f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={area_pin}&date={new_date}",
                headers=header)
            data = response.json()
            centers = pd.DataFrame(data.get('centers'))
            if centers.empty:
                s.warning("No centres found for " + new_date + " in " + str(area_pin) + ' Check Later! ')
            else:
                session_ids = []
                for j, row in centers.iterrows():
                    session = pd.DataFrame(row['sessions'][0])
                    session['center_id'] = centers.loc[j, 'center_id']
                    session_ids.append(session)

                sessions = pd.concat(session_ids, ignore_index=True)
                av_centers = centers.merge(sessions, on='center_id')
                print(av_centers.columns)

                av_centers.drop(
                    columns=['sessions', 'session_id', 'lat', 'block_name', 'long', 'date', 'from', 'to', 'state_name',
                             'district_name', 'pincode'], inplace=True, errors='ignore')
                av_centers = av_centers[av_centers['min_age_limit'] == age_val]
                new_df = av_centers.copy()
                print(new_df)
                s.dataframe(new_df.assign(hack='').set_index('hack'))

run()
