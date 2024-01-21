import pandas as pd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium
from PIL import Image
import warnings
import sqlalchemy
from sqlalchemy import create_engine, text, inspect, func

engine = create_engine("sqlite:///database/travel_db.sqlite")

#gives warning but easier to get the dataframe from querying
warnings.filterwarnings('ignore')
conn = engine.raw_connection()

im = Image.open("image/travel-image.png")
st.set_page_config(page_title="Travel Check-Ins App", page_icon=im, layout="wide")

#UNCOMMENT BEFORE SUBMITTING
#hide_default_format = """
#       <style>
       #MainMenu {visibility: hidden; }
#       footer {visibility: hidden;}
#       </style>
#       """
#st.markdown(hide_default_format, unsafe_allow_html=True)

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
          'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
          'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
          'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
          'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri',
          'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
          'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
          'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
          'Virginia',  'Washington', 'West Virginia', 'Wisconsin', 'Wyoming',
          'Washington D.C.']
st.title("PLEASE CHOOSE A STATE AND WHAT INFORMATION YOU WOULD LIKE TO SEE!")
selected_state = st.selectbox("State You're Visiting", states, index=None, placeholder="Select State...")


left, right = st.columns([1, 5])
with left:
    visual = st.radio('Information', options=['Temperature', 'Crime', 'Map', 'Ethics'], index=None)
with right:
    if visual == "Ethics":
        st.title('ETHICAL CONSIDERATIONS')
        st.write("Data ethics encompasses the moral obligation in collecting, protecting, sharing and using data. Researchers must consider the rights and privacy of individuals whose data is being collected. Ethical considerations that we took into account when collecting our data include:")
        st.write("- Respect ethical guidelines and privacy concerns when using datasets.")
        st.write("- Complies with data protection regulations and users do not misuse or misrepresent the data.")
        st.write("- Crediting original author of the data.")
        st.write("While most data posted on social media platforms like Instagram, is assumed to be in the public domain as users agree to allow third parties to use data when agreeing to the terms of use; there were ethical considerations taken into account such as users’ name privacy and safety.")
    for state in states:
        if state == selected_state:
            if visual == "Temperature": 
                temp_f = pd.read_sql_query(sql=f"SELECT State, \"Temp in F\", Year, Season FROM temperature_clean WHERE State = \"{state}\"", con=conn)
                temp_f = temp_f.groupby(['Season', 'Year'])[['Temp in F']].mean().round(0)
                temp_f = temp_f.reset_index()
        
                st.title(f"Average Temperature in {state} Per Season in Fahrenheit from 2016-2018")
                st.bar_chart(temp_f, x="Season", y="Temp in F", color="Year")

                temp_c = pd.read_sql_query(sql=f"SELECT State, \"Temp in C\", Year, Season FROM temperature_clean WHERE State = \"{state}\"", con=conn)
                temp_c = temp_c.groupby(['Season', 'Year'])[['Temp in C']].mean().round(0)
                temp_c = temp_c.reset_index()

                st.title(f"Average Temperature in {state} Per Season in Celsius from 2016-2018")
                st.bar_chart(temp_c, x="Season", y="Temp in C", color="Year")
            elif visual == "Crime":
                crime = pd.read_sql_query(sql=f"SELECT * FROM \"state-abbrevs\" INNER JOIN USCrime ON USCrime.State = \"state-abbrevs\".abbreviation WHERE \"state-abbrevs\".state = \"{state}\"",con=conn)
                crime = crime.drop(['State', 'abbreviation', 'population', 'Total'], axis=1)
                crime = crime.groupby(['state'])[['violent_crime', 'homicide', 'rape_revised', 'robbery', 'aggravated_assault',
                                                 'property_crime', 'burglary', 'larceny', 'motor_vehicle_theft']].mean().round(0)
                crime = crime.reset_index()
                column_names = list(crime.columns.values)
                column_names.pop(0)
                column_values = crime.loc[crime.state == state, ['violent_crime', 'homicide', 'rape_revised', 'robbery', 'aggravated_assault',
                                                                    'property_crime', 'burglary', 'larceny', 'motor_vehicle_theft']].values.flatten().tolist()
                labels = column_names
                sizes = column_values
                fig = px.pie(values=sizes, names=labels)
                st.title(f"Average US Crime in {state} from 2016-2018")
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            elif visual == "Map":
                location = pd.read_sql_query(sql=f"SELECT Location, State, Year, Address, Latitude, Longitude FROM location_clean WHERE State = \"{state}\"", con=conn)
                def coord(c):
                    return f"({c.Latitude}, {c.Longitude})"
                location['Coordinate'] = location.apply(coord, axis=1)
                location = location.drop_duplicates(subset=["Coordinate"])
                location = location.drop(["Coordinate"], axis=1)

                m = folium.Map(prefer_canvas=True)
                def plot(location):
                    folium.Marker([float(location.Latitude), float(location.Longitude)], 
                                        popup=location.Address, tooltip=f'Location: {location.Location} Address: {location.Address}').add_to(m)

                location.apply(plot, axis=1)
                st.title(f"Things to do in {state}")
                st_data = st_folium(m, use_container_width=True)