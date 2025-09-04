import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import st_folium, folium_static
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import MarkerCluster
import io
import requests
import mimetypes

st.set_page_config(layout="wide")

st.logo("Forvis_Mazars_Logo_Color_RGB.jpg", size="large")
st.title(":blue[Accumulation Management Dashboard]")

tab_selection = st.sidebar.radio(
    "Select a tab:",
    [
        'RDS Conventional Inputs',
        'Emerging Scenarios Inputs',
        'Currency Convertion',
        'Resulting Visualisations',
        'Limit System',
        'Payback',
        'Geographic Information System (GIS) Analysis',
        'Output: Filled tables'
    ]
)

if tab_selection == 'RDS Conventional Inputs':

    if 'data' not in st.session_state:
        data = pd.DataFrame({'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [], 'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
                            'Estimated Net Loss': [], 'Observation Year': [], 'Country': [], 'Impacted Segments': []})
        st.session_state.data = data

    st.dataframe(st.session_state.data)

#####TEST########
    uploaded_file = st.file_uploader(
        "📤 Upload pre-filled Nat Cat and Man Made Risk Table (Excel)",
        type=["xlsx"],
        key="natcat_upload"
    )

    if uploaded_file is not None:
        uploaded_df = pd.read_excel(uploaded_file)
        st.session_state.data = uploaded_df
        st.success("✅ Uploaded data has been loaded into the dashboard.")
        st.dataframe(st.session_state.data)
#####TEST########


    def add_df_form():
        estimated_net_loss = st.session_state.estimated_gross_loss - st.session_state.estimated_reinsurance_benefits
        row = pd.DataFrame({'Risk Type': [st.session_state.risk_type_option],
                            'Scenario Cluster': [st.session_state.scenario_cluster_option],
                            'Scenario Name': [st.session_state.scenario_name_option],
                            'Estimated Gross Loss': [st.session_state.estimated_gross_loss],
                            'Estimated Reinsurance Benefits': [st.session_state.estimated_reinsurance_benefits],
                            'Estimated Net Loss': [estimated_net_loss],
                            'Observation Year': [st.session_state.observation_year],
                            'Country': [st.session_state.country],
                            'Impacted Segments': [", ".join(st.session_state.impacted_segments)]
                            })
        st.session_state.data = pd.concat([st.session_state.data, row])

    risk_type_option = st.selectbox("Risk Type:", ("Man Made", "Nat Cat"), index = None, key='risk_type_option')

    ########

    if risk_type_option == "Man Made":
            scenario_cluster_option = st.selectbox(
                "Scenario cluster:",
                ("Motor", "Fire / Explosion", "Aviation / Space", "Marine / Transport", "Liability", "Political", "Cyber", "Infectious Disease",
                "SRCC", "Terrorism", "Other Man Made"),
                index = None, key = 'scenario_cluster_option'
            )
    elif risk_type_option == "Nat Cat":
            scenario_cluster_option = st.selectbox(
                "Scenario cluster:",
                ("Windstorm", "Cyclones / Hurricane", "Earthquake", "Flood", "Wildfires", "Volcanic Eruption", "Tornado", "Drought", "Other Nat Cat"),
                index = None, key = 'scenario_cluster_option'
            )
    else:
        scenario_cluster_option = st.selectbox("Scenario cluster:", ("Not Available"), index = None, key = 'scenario_cluster_option')

    ########

    if scenario_cluster_option == "Motor":
            scenario_name_option = st.selectbox(
                "Scenario Name",
                ("Car causes train accident and bridge or railway damage","Tunnel collision of two trucks", "Car collision with Football transport bus"),
                index = None, key = 'scenario_name_option'
            )
    elif scenario_cluster_option == "Fire / Explosion":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Aviation / Space":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Aviation collision", "Space weather - Solar energetic particle event", "Space weather - Design deficiency", "Generic defect of satellites", "Space debris"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Marine / Transport":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Ships collision", "Conflagoration at a marine complex", "Total loss of high value transport"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Liability":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Hazardous Substance or Contaminated product", "Faulty Advise or Negligence related to a Professional Service", "Pollution / Environmetal indicent",
            "Fraud or Financial Crime", "Professional Lines: Misselling of a Financial Product", "Professional Lines: Failure/Collapse of a Major Corporation",
            "Professional Lines: Failure of a Merger", "Professional Lines: Failure of a Construction Project", "Professional Lines: Recession-Related Losses",
            "Non-Professional Lines: Industrial/Transport Incident", "Non-Professional Lines: Multiple Public/Products Losses", "Back year deterioration"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Political":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Political Violence"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Cyber":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Power Blackout (Business Blackout)", "Cloud Outage (Cloud Cascade)", "Cyber Crime Event", "Cyber Motor", "Major Data Security Breach", "Ransomware Contagion"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Infectious Disease":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Regional outbreak of a disease", "Global outbreak of a disease"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "SRCC":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Strikes - Riots and Civil Commotion"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Terrorism":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Rockefeller Center: 2 tonne bomb blast", "One World Trade Center: 2 tonne bomb blast", "Terrorism accumulations other than Manhattan",
                "Conventional one-ton bomb", "9/11 plane attack type", "Gun fire/Truck goes to crowd"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Other Man Made":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Accumulation of casualties to members of sports team"),
            index = None, key = 'scenario_name_option'
        )

    ##################################

    elif scenario_cluster_option == "Windstorm":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("North East Windstorm", "South Carolina Windstorm", "Florida Windstorm - Miami-Dade", "Florida Windstorm - Pinellas", "Gulf of Mexico Windstorm",
                "European Windstorm", "Caribbean/USA Hurricane Windstorm Clash"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Cyclones / Hurricane":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Japanese Typhoon"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Earthquake":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("California Earthquake - Los Angeles", "California Earthquake - San Francisco", "New Madrid Earthquake", "Japanese Earthquake",
                "Other earthquakes (e.g. in China, Australia, New Zealand)"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Flood":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("UK Flood", "major flood outside of UK"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Wildfires":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Volcanic Eruption":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Tornado":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Drought":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Other Nat Cat":
        scenario_name_option = st.selectbox(
            "Scenario Name",
            ("Pandemic Risk"),
            index = None, key = 'scenario_name_option'
        )

    ###################

    else:
        scenario_name_option = st.selectbox(
            "Scenario name:",
            ("Not Available"),
            index = None, key = 'scenario_name_option'
        )

    ####################
      
    observation_year = st.selectbox(
        "Reporting Year:",
        list(range(2000, 2101)),
        index=None,
        key='observation_year'
    )

    
    ####################
    
    country = st.selectbox(
        "Geography:",
        ("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
         "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
         "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia",
         "Cameroon", "Canada", "Cape Verde", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
         "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
         "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea","Estonia",
         "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece",
         "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
         "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
         "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
         "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
         "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
         "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
         "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
         "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
         "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
         "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
         "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
         "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
         "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
         "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
         "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"),
         index = None, key = 'country'
    )

    
    impact_segments = st.multiselect(
        "Impacted Segments:",
        options=["Commercial Property","Residential Property","Motor Own Damage","Motor TPL PD","Motor TPL BI","General Liability","Business Interruption",
                 "Professional Indemnity (Errors & Omissions)","Product Liability","Employers Liability","Directors and Officers (D&O) Liability",
                 "Workers compensation ","Marine Cargo Insurance","Marine Hull Insurance","Aviation Insurance","Accident and Disability",
                 "Trip Cancellation","Lost Luggage or Documents","Machinery Breakdown / Electronic Equipment","Trade Credit Insurance Surety Bonds Fidelity Guarantee",
                 "Crop Insurance","Farm Equipment Insurance"],
        key="impacted_segments"
    )

    
    ####################

    df_form = st.form(clear_on_submit = True, key = 'df_form')
    with df_form:
        df_columns = st.columns(8)
        with df_columns[0]:
            st.write(risk_type_option)
        with df_columns[1]:
            st.write(scenario_cluster_option)
        with df_columns[2]:
            st.write(scenario_name_option)
        with df_columns[3]:
            gross_loss = st.number_input('Estimated Gross Loss in Single Unit Currency', min_value = 0.0, key = 'estimated_gross_loss')
        with df_columns[4]:
            reinsurance_benefits = st.number_input('Estimated Reinsurance Benefits in Single Unit Currency', min_value = 0.0, key = 'estimated_reinsurance_benefits')
        with df_columns[5]:
            # TODO: make calculation automatic
            estimated_net_loss = gross_loss - reinsurance_benefits
            st.write(estimated_net_loss)       
        with df_columns[6]:
            st.write(observation_year)
        with df_columns[7]:
            st.write(country)
        st.form_submit_button(on_click=add_df_form)


    if st.button('Restart Application', key = "restart_application"):
        # st.session_state.risk_type_option = None
        # st.session_state.scenario_cluster_option = None
        # st.session_state.scenario_name_option = None
        # st.session_state.estimated_gross_loss = None
        # st.session_state.estimated_reinsurance_benefits = None
        # st.session_state.estimated_net_loss = None
        # st.session_state.observation_year = None
        st.session_state.data = pd.DataFrame({'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [], 'Estimated Gross Loss': [],
                                            'Estimated Reinsurance Benefits': [], 'Estimated Net Loss': [], 'Observation Year': [], 'Country': [],'Impacted Segments': []})

############# INPUT: EMERGING AND EXTRAORDINARY RISKS

if tab_selection == 'Emerging Scenarios Inputs':
    st.image("ERI_Risk_Radar_2025_Emerging_Risk_Radar.jpg")

    if 'data_emerging_extraordinary' not in st.session_state:
        data_emerging_extraordinary = pd.DataFrame({'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [], 'Impact Assessment': [], 'Time Horizon': [],
                                                    'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [], 'Estimated Net Loss': [], 'Observation Year': [],
                                                    'Country': []})
        st.session_state.data_emerging_extraordinary = data_emerging_extraordinary

    st.dataframe(st.session_state.data_emerging_extraordinary)

    def add_df_form_emerging_extraordinary():
        estimated_net_loss_em_extr = st.session_state.estimated_gross_loss_em_extr - st.session_state.estimated_reinsurance_benefits_em_extr
        row = pd.DataFrame({'Risk Type': [st.session_state.risk_type_option_em_extr],
                            'Scenario Cluster': [st.session_state.scenario_cluster_option_em_extr],
                            'Scenario Name': [st.session_state.scenario_name_option_em_extr],
                            'Impact Assessment': [st.session_state.impact_assessment_option_em_extr],
                            'Time Horizon': [st.session_state.time_horizon_option_em_extr],
                            'Estimated Gross Loss': [st.session_state.estimated_gross_loss_em_extr],
                            'Estimated Reinsurance Benefits': [st.session_state.estimated_reinsurance_benefits_em_extr],
                            'Estimated Net Loss': [estimated_net_loss_em_extr],
                            'Observation Year': [st.session_state.observation_year_em_extr],
                            'Country': [st.session_state.country_em_extr]})
        st.session_state.data_emerging_extraordinary = pd.concat([st.session_state.data_emerging_extraordinary, row])

    risk_type_option_em_extr = st.selectbox(
        "Please select the risk type:",
        ("Emerging", "Extraordinary"),
        index = None, key = 'risk_type_option_em_extr'
        )
    
    st.write("If you enter your scenario cluster and / or scenario name manually, you need to press 'ENTER' afterwards for it to be considered by the programme.")

    if risk_type_option_em_extr == "Emerging":
        scenario_cluster_option_em_extr = st.selectbox(
            "Scenario cluster:",
            ("Environmental", "Technological", "Economic", "Regulatory"),
            index = None, placeholder = "Select an observed scenario cluster or enter a new one", accept_new_options = True, key = 'scenario_cluster_option_em_extr'
        )
    elif risk_type_option_em_extr == "Extraordinary":
        scenario_cluster_option_em_extr = st.selectbox(
            "Scenario cluster:",
            ("Climate Change Litigation (Greenwashing)", "E-Vehicle Explosion due to heatwaves", "Solar Storms", "Dam Breach"),
            index = None, placeholder = "Select an observed scenario cluster or enter a new one", accept_new_options = True, key = 'scenario_cluster_option_em_extr'
        )
    else:
        scenario_cluster_option_em_extr = st.selectbox("Scenario cluster:", ("Not Available"), index = None, key = 'scenario_cluster_option_em_extr')

    if scenario_cluster_option_em_extr == "Environmental":
        scenario_name_option_em_extr = st.selectbox(
        "Scenario Name:",
        ("Antimicrobial Resistance", "Climate Change Physical Risk", "Climate Engineering and Storage Techniques", "Emerging Infectious Diseases",
        "Environmental Pollution", "Nature and Biodiversity Loss", "Space Risk"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Technological":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Artificial Intelligence", "Autonomous Machines", "Critical Infrastructure Failures", "Cyber Risks",
            "Data Privacy and Data Ethics", "Hazardous Chemicals and Small Particles", "Information Reliability"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Economic":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Climate Change Transition Risk", "Deterioration of Public Healthcare Systems", "Economic Trade Conflicts and Sanctions", "Evolving Terrorism", "Geopolitical Tensions and Conflicts",
            "Global Debt Crisis", "Mental Health", "Metabolic Syndrome", "Resource Management", "Skills Shortage and Reskilling", "Social Fragmentation"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Regulatory":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Collective Redress", "Legal and Regulatory Complexity", "Medical Advances", "Substance Abuse", "Supply Chain Complexity"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
#########
    elif scenario_cluster_option_em_extr == "Climate Change Litigation (Greenwashing)":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Corporate Accountability Crisis", "Greenwashing Scandal Unveiled", "Eco-Fraud Legal Battle"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "E-Vehicle Explosion due to heatwaves":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Battery Meltdown Catastrophe", "Thermal Runaway Disaster", "Heatwave-Induced E-Vehicle Explosions"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Solar Storms":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Geomagnetic Storm Havoc", "Solar Flare Disruption", "Space Weather Crisis"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Dam Breach":
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Hydraulic Infrastructure Failure", "Catastrophic Flooding Event", "Dam Collapse Emergency"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
#########
    else:
        scenario_name_option_em_extr = st.selectbox(
            "Scenario Name",
            ("Not Available"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
#########
    impact_assessment_option_em_extr = st.selectbox(
        "Please enter the observed impact assessment:",
        ("Small", "Medium", "High"),
        index = None, key = "impact_assessment_option_em_extr"
    )
    time_horizon_option_em_extr = st.selectbox(
        "Please enter the observed time horizon:",
        ("Already seen", "1-5 years", "5-10 years"),
        index = None, key = "time_horizon_option_em_extr"
    )
#########


    observation_year_em_extr = st.selectbox(
    "Reporting Year:",
    list(range(2000, 2101)),
    index=None,
    key='observation_year_em_extr'
   )

    ####################
    
    country_em_extr = st.selectbox(
        "Geography:",
        ("Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
         "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
         "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia",
         "Cameroon", "Canada", "Cape Verde", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
         "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
         "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea","Estonia",
         "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece",
         "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
         "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
         "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
         "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
         "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
         "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
         "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
         "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
         "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
         "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
         "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
         "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
         "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
         "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City",
         "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"),
         index = None, key = 'country_em_extr'
    )
############
    df_form_em_extr = st.form(clear_on_submit = True, key = 'df_form_em_extr')
    with df_form_em_extr:
        df_columns_em_extr = st.columns(10)
        with df_columns_em_extr[0]:
            st.write(risk_type_option_em_extr)
        with df_columns_em_extr[1]:
            st.write(scenario_cluster_option_em_extr)
        with df_columns_em_extr[2]:
            st.write(scenario_name_option_em_extr)
        with df_columns_em_extr[3]:
            st.write(impact_assessment_option_em_extr)
        with df_columns_em_extr[4]:
            st.write(time_horizon_option_em_extr)
        with df_columns_em_extr[5]:
            gross_loss_em_extr = st.number_input('Estimated Gross Loss in Single Unit Currency', min_value = 0.0, key = 'estimated_gross_loss_em_extr')
        with df_columns_em_extr[6]:
            reinsurance_benefits_em_extr = st.number_input('Estimated Reinsurance Benefits in Single Unit Currency', min_value = 0.0, key = 'estimated_reinsurance_benefits_em_extr')
        with df_columns_em_extr[7]:
            # TODO: make calculation automatic
            estimated_net_loss_em_extr = gross_loss_em_extr - reinsurance_benefits_em_extr
            st.write(estimated_net_loss_em_extr)          
        with df_columns_em_extr[8]:
            st.write(observation_year_em_extr)
        with df_columns_em_extr[9]:
            st.write(country_em_extr)
        st.form_submit_button(on_click=add_df_form_emerging_extraordinary)

    if st.button('Restart Application', key = "restart_application_em_extr"):
        st.session_state.data_emerging_extraordinary = pd.DataFrame({'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [], 'Impact Assessment': [], 'Time Horizon': [],
                                                                     'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [], 'Estimated Net Loss': [],
                                                                     'Observation Year': [], 'Country': []})
############# CURRENCY CONVERSION

elif tab_selection == 'Currency Convertion':
    st.title("Convert your currency to EUR")
    st.write("Do you wish to use conversion rates from 31st December 2024 or custom currency conversion rates?")
    conversion_rate_choice = st.selectbox(
        "From 31st December 2024 or custom currency conversion rates:",
        ("From 31st December 2024", "Custom currency conversion rates"),
        index=None, key="conversion_rate_choice"
    )
    if conversion_rate_choice == "From 31st December 2024":
        usd_currency = st.number_input("Currency Amount in USD in Single Unit Currency (1 EUR = 1.0389 USD):", key='usd_currency')
        gbp_currency = st.number_input("Currency Amount in GBP in Single Unit Currency (1 EUR = 0.82918 GBP):", key='gbp_currency')
        jpy_currency = st.number_input("Currency Amount in JPY in Single Unit Currency (1 EUR = 163.06 JPY):", key='jpy_currency')
        usd_to_eur = usd_currency / 1.0389
        gbp_to_eur = gbp_currency / 0.82918
        jpy_to_eur = jpy_currency / 163.06
        st.write("The EUR amount converted from USD is equal to:", usd_to_eur)
        st.write("The EUR amount converted from GBP is equal to:", gbp_to_eur)
        st.write("The EUR amount converted from JPY is equal to:", jpy_to_eur)
    elif conversion_rate_choice == "Custom currency conversion rates":
        usd_conversion = st.number_input("How much USD are 1 EUR?", key='usd_conversion')
        gbp_conversion = st.number_input("How much GBP are 1 EUR?", key='gbp_conversion')
        jpy_conversion = st.number_input("How much JPY are 1 EUR?", key='jpy_conversion')
        usd_currency = st.number_input("Currency Amount in USD in Single Unit Currency:", key='usd_currency')
        gbp_currency = st.number_input("Currency Amount in GBP in Single Unit Currency:", key='gbp_currency')
        jpy_currency = st.number_input("Currency Amount in JPY in Single Unit Currency:", key='jpy_currency')
        usd_to_eur = usd_currency / usd_conversion if usd_conversion else 0
        gbp_to_eur = gbp_currency / gbp_conversion if gbp_conversion else 0
        jpy_to_eur = jpy_currency / jpy_conversion if jpy_conversion else 0
        st.write("The EUR amount converted from USD is equal to:", usd_to_eur)
        st.write("The EUR amount converted from GBP is equal to:", gbp_to_eur)
        st.write("The EUR amount converted from JPY is equal to:", jpy_to_eur)
    else:
        None

    
############# RESULTING VISUALisations

elif tab_selection == 'Resulting Visualisations':
    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)

    ###########

    fig = make_subplots(specs = [[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x = filled_table["Scenario Name"], y = filled_table["Estimated Gross Loss"],offsetgroup=1,
                         name = 'Estimated Gross Loss', marker_color = 'blue'), secondary_y=False)
    fig.add_trace(go.Bar(x = filled_table["Scenario Name"], y = filled_table["Estimated Net Loss"], offsetgroup=2,
                         name = 'Estimated Net Loss', marker_color = 'red'), secondary_y=True)
    
    fig.update_layout(
        title = "Bar Chart",
        xaxis = dict(title = "Scenario Name"),
        yaxis = dict(
            title=dict(text="Estimated Gross Loss", font=dict(color="blue")),
            tickfont = dict(color = "blue")
        ),
        yaxis2 = dict(
            title=dict(text="Estimated Gross Loss", font=dict(color="blue")),
            tickfont = dict(color = "red"),
            overlaying = 'y',
            side = 'right'
        ),
        barmode = 'group'
    )
    st.plotly_chart(fig, key = "fig")

    ##############

    fig_em_extr = make_subplots(specs = [[{"secondary_y": True}]])
    fig_em_extr.add_trace(go.Bar(x = filled_table_em_extr["Scenario Name"], y = filled_table_em_extr["Estimated Gross Loss"], offsetgroup=1,
                         name = 'Estimated Gross Loss', marker_color = 'blue'), secondary_y = False)
    fig_em_extr.add_trace(go.Bar(x = filled_table_em_extr["Scenario Name"], y = filled_table_em_extr["Estimated Net Loss"], offsetgroup=2,
                         name = 'Estimated Net Loss', marker_color = 'red'), secondary_y = True)
    
    fig_em_extr.update_layout(
        title = "Bar Chart",
        xaxis = dict(title = "Scenario Name"),
        yaxis = dict(
            title = dict(text="Estimated Gross Loss", font=dict(color="blue")),
            tickfont = dict(color = "blue")
        ),
        yaxis2 = dict(
            title = dict(text="Estimated Gross Loss", font=dict(color="blue")),
            tickfont = dict(color = "red"),
            overlaying = 'y',
            side = 'right'
        ),
        barmode = 'group'
    )
    st.plotly_chart(fig_em_extr, key = "fig_em_extr")


############# LIMIT SYSTEM

elif tab_selection == 'Limit System':
    st.header("Limit System")

    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)

    risk_limit = st.number_input('Type in your Risk Limit:')
    if not (filled_table.empty or filled_table_em_extr.empty) and risk_limit != 0.0:
        st.write("The Limit Utilisation is acceptable, if it lies inside [0.0, 0.90). It is close to not being acceptable, if it lies inside [0.90, 1.0)."
        " It is not acceptable, if it is higher or equal to 1.0.")
        max_net_loss_nat_cat_man_made = max(filled_table['Estimated Net Loss'])
        max_net_loss_em_extr = max(filled_table_em_extr['Estimated Net Loss'])
        max_net_loss = max(max_net_loss_nat_cat_man_made, max_net_loss_em_extr)
        st.write('Your Maximum Net Loss from both input tables is:', max_net_loss)
        limit_utilisation = max_net_loss / risk_limit
        st.write('Your Limit Utilisation is:', limit_utilisation)

        if limit_utilisation < 0.90:
            green_box_html = """
            <div style="background-color:green; padding:20px; border-radius:10px;">
            <h2 style="color:white; text-align:center;">Your Limit Utilisation level is acceptable.</h2>
            </div>
            """
            st.markdown(green_box_html, unsafe_allow_html=True)
        elif limit_utilisation < 1.0:
            orange_box_html = """
            <div style="background-color:orange; padding:20px; border-radius:10px;">
            <h2 style="color:white; text-align:center;">Your Limit Utilisation level is close to being not acceptable.</h2>
            </div>
            """
            st.markdown(orange_box_html, unsafe_allow_html=True)
        elif limit_utilisation >= 1.0:
            red_box_html = """
            <div style="background-color:red; padding:20px; border-radius:10px;">
            <h2 style="color:white; text-align:center;">Your Limit Utilisation level is not acceptable.</h2>
            </div>
            """
            st.markdown(red_box_html, unsafe_allow_html=True)
        else:
            None

######### PAYBACK

elif tab_selection == 'Payback':
    st.header("Payback")
    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)
    if not filled_table.empty or not filled_table_em_extr.empty:
        payback_intervals = st.slider(
            "Select your lower and upper payback acceptance bounds. From 0.0 until the first number the Payback Period Appetite is acceptable, from the first to the second number it may not be acceptable and from the second number to 30.0 it is not acceptable:",
            0.0, 30.0, (5.0, 10.0)
        )
        extreme_disaster_loss = st.number_input("Enter your Expected Profit:")
        array_affected_scenario_names_nat_cat_man_made = np.unique(filled_table["Scenario Name"].values)
        array_affected_scenario_names_em_extr = np.unique(filled_table_em_extr["Scenario Name"].values)
        payback_input_choice = st.selectbox(
            "Do you want to observe Nat Cat and Man Made or Emerging and Extraordinary Scenarios?",
            ("Nat Cat and Man Made", "Emerging and Extraordinary")
        )
        
        if payback_input_choice == "Nat Cat and Man Made":
            extreme_disaster_scenario = st.selectbox(
                "Select Scenario which is affected by the extreme disaster:",
                array_affected_scenario_names_nat_cat_man_made,
                key='extreme_disaster_scenario'
            )
            filtered_table = filled_table[filled_table["Scenario Name"] == extreme_disaster_scenario]
            corresponding_loss = filtered_table["Estimated Net Loss"].values[0]
        elif payback_input_choice == "Emerging and Extraordinary":
            extreme_disaster_scenario = st.selectbox(
                "Select Scenario which is affected by the extreme disaster:",
                array_affected_scenario_names_em_extr,
                key='extreme_disaster_scenario'
            )
            filtered_table = filled_table_em_extr[filled_table_em_extr["Scenario Name"] == extreme_disaster_scenario]
            corresponding_loss = filtered_table["Estimated Net Loss"].values[0]
        else:
            corresponding_loss = None
        
        st.write("The corresponding Estimated Net Loss in EUR equals to:", corresponding_loss)
        payback = corresponding_loss / extreme_disaster_loss if corresponding_loss else 0
        st.write("We compare the Payback against the Firm Risk Appetite of a single Realistic Disaster Scenario (RDS).")
        st.markdown(f"<h1 style='text-align: center; color: black;'>Corresponding Payback Period Appetite: {round(payback, 5)} years</h1>", unsafe_allow_html=True)

        if payback <= payback_intervals[0]:
            green_box_html = """
            <div style="background-color:green; padding:20px; border-radius:10px;">
            <h2 style="color:white; text-align:center;">Your level of Payback Period Appetite is acceptable.</h2>
            </div>
            """
            st.markdown(green_box_html, unsafe_allow_html=True)
        elif payback < payback_intervals[1]:
            orange_box_html = """
            <div style="background-color:orange; padding:20px; border-radius:10px;">
            <h2 style="color:white; text-align:center;">Your level of Payback Period Appetite may not be acceptable.</h2>
            </div>
            """
            st.markdown(orange_box_html, unsafe_allow_html=True)
        elif payback >= payback_intervals[1]:
            red_box_html = """
            <div style="background-color:red; padding:20px; border-radius:10px;">
            <h2 style="color:white; text-align:center;">Your level of Payback Period Appetite is not acceptable.</h2>
            </div>
            """
            st.markdown(red_box_html, unsafe_allow_html=True)
        else:
            None

########## GIS ANALYSIS

elif tab_selection == 'Geographic Information System (GIS) Analysis':
    st.header("Geographic Information System Analysis")

    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)

    countries_coordinates = {
        "Afghanistan": [33.93911, 67.709953],
        "Albania": [41.153332, 20.168331],
        "Algeria": [28.033886, 1.659626],
        "Andorra": [42.506285, 1.521801],
        "Angola": [-11.202692, 17.873887],
        "Argentina": [-38.416097, -63.616672],
        "Armenia": [40.069099, 45.038189],
        "Australia": [-25.274398, 133.775136],
        "Austria": [47.516231, 14.550072],
        "Azerbaijan": [40.143105, 47.576927],
        "Bahamas": [25.03428, -77.39628],
        "Bahrain": [26.0667, 50.5577],
        "Bangladesh": [23.684994, 90.356331],
        "Barbados": [13.193887, -59.543198],
        "Belarus": [53.709807, 27.953389],
        "Belgium": [50.503887, 4.469936],
        "Belize": [17.189877, -88.49765],
        "Benin": [9.30769, 2.315834],
        "Bhutan": [27.514162, 90.433601],
        "Bolivia": [-16.290154, -63.588653],
        "Bosnia and Herzegovina": [43.915886, 17.679076],
        "Botswana": [-22.328474, 24.684866],
        "Brazil": [-14.235004, -51.92528],
        "Brunei": [4.535277, 114.727669],
        "Bulgaria": [42.733883, 25.48583],
        "Burkina Faso": [12.238333, -1.561593],
        "Burundi": [-3.373056, 29.918886],
        "Cambodia": [12.565679, 104.990963],
        "Cameroon": [7.369722, 12.354722],
        "Canada": [56.130366, -106.346771],
        "Cape Verde": [16.002082, -24.013197],
        "Central African Republic": [6.611111, 20.939444],
        "Chad": [15.454166, 18.732207],
        "Chile": [-35.675147, -71.542969],
        "China": [35.86166, 104.195397],
        "Colombia": [4.570868, -74.297333],
        "Comoros": [-11.875001, 43.872219],
        "Congo (Congo-Brazzaville)": [-0.228021, 15.827659],
        "Costa Rica": [9.748917, -83.753428],
        "Croatia": [45.1, 15.2],
        "Cuba": [21.521757, -77.781167],
        "Cyprus": [35.126413, 33.429859],
        "Czech Republic": [49.817492, 15.472962],
        "Denmark": [56.26392, 9.501785],
        "Djibouti": [11.825138, 42.590275],
        "Dominica": [15.414999, -61.370976],
        "Dominican Republic": [18.735693, -70.162651],
        "Ecuador": [-1.831239, -78.183406],
        "Egypt": [26.820553, 30.802498],
        "El Salvador": [13.794185, -88.89653],
        "Equatorial Guinea": [1.650801, 10.267895],
        "Eritrea": [15.179384, 39.782334],
        "Estonia": [58.595272, 25.013607],
        "Eswatini": [-26.522503, 31.465866],
        "Ethiopia": [9.145, 40.489673],
        "Fiji": [-17.713371, 178.065032],
        "Finland": [61.92411, 25.748151],
        "France": [46.603354, 1.888334],
        "Gabon": [-0.803689, 11.609444],
        "Gambia": [13.443182, -15.310139],
        "Georgia": [42.315407, 43.356892],
        "Germany": [51.165691, 10.451526],
        "Ghana": [7.946527, -1.023194],
        "Greece": [39.074208, 21.824312],
        "Grenada": [12.1165, -61.679],
        "Guatemala": [15.783471, -90.230759],
        "Guinea": [9.945587, -9.696645],
        "Guinea-Bissau": [11.803749, -15.180413],
        "Guyana": [4.860416, -58.93018],
        "Haiti": [18.971187, -72.285215],
        "Honduras": [15.199999, -86.241905],
        "Hungary": [47.162494, 19.503304],
        "Iceland": [64.963051, -19.020835],
        "India": [20.593684, 78.96288],
        "Indonesia": [-0.789275, 113.921327],
        "Iran": [32.427908, 53.688046],
        "Iraq": [33.223191, 43.679291],
        "Ireland": [53.41291, -8.24389],
        "Israel": [31.046051, 34.851612],
        "Italy": [41.87194, 12.56738],
        "Jamaica": [18.109581, -77.297508],
        "Japan": [36.204824, 138.252924],
        "Jordan": [30.585164, 36.238414],
        "Kazakhstan": [48.019573, 66.923684],
        "Kenya": [-1.292066, 36.821946],
        "Kiribati": [-3.370417, -168.734039],
        "Kuwait": [29.31166, 47.481766],
        "Kyrgyzstan": [41.20438, 74.766098],
        "Laos": [19.85627, 102.495496],
        "Latvia": [56.879635, 24.603189],
        "Lebanon": [33.854721, 35.862285],
        "Lesotho": [-29.609988, 28.233608],
        "Liberia": [6.428055, -9.429499],
        "Libya": [26.3351, 17.228331],
        "Liechtenstein": [47.166, 9.555373],
        "Lithuania": [55.169438, 23.881275],
        "Luxembourg": [49.815273, 6.129583],
        "Madagascar": [-18.766947, 46.869107],
        "Malawi": [-13.254308, 34.301525],
        "Malaysia": [4.210484, 101.975766],
        "Maldives": [3.202778, 73.22068],
        "Mali": [17.570692, -3.996166],
        "Malta": [35.937496, 14.375416],
        "Marshall Islands": [7.131474, 171.184478],
        "Mauritania": [21.00789, -10.940835],
        "Mauritius": [-20.348404, 57.552152],
        "Mexico": [23.634501, -102.552784],
        "Micronesia": [7.425554, 150.550812],
        "Moldova": [47.411631, 28.369885],
        "Monaco": [43.733334, 7.416667],
        "Mongolia": [46.862496, 103.846656],
        "Montenegro": [42.708678, 19.37439],
        "Morocco": [31.791702, -7.09262],
        "Mozambique": [-18.665695, 35.529562],
        "Myanmar (Burma)": [21.913965, 95.956223],
        "Namibia": [-22.95764, 18.49041],
        "Nauru": [-0.522778, 166.931503],
        "Nepal": [28.394857, 84.124008],
        "Netherlands": [52.132633, 5.291266],
        "New Zealand": [-40.900557, 174.885971],
        "Nicaragua": [12.865416, -85.207229],
        "Niger": [17.607789, 8.081666],
        "Nigeria": [9.081999, 8.675277],
        "North Korea": [40.339852, 127.510093],
        "North Macedonia": [41.608635, 21.745275],
        "Norway": [60.472024, 8.468946],
        "Oman": [21.512583, 55.923255],
        "Pakistan": [30.375321, 69.345116],
        "Palau": [7.51498, 134.58252],
        "Panama": [8.537981, -80.782127],
        "Papua New Guinea": [-6.314993, 143.95555],
        "Paraguay": [-23.442503, -58.443832],
        "Peru": [-9.189967, -75.015152],
        "Philippines": [12.879721, 121.774017],
        "Poland": [51.919438, 19.145136],
        "Portugal": [39.399872, -8.224454],
        "Qatar": [25.354826, 51.183884],
        "Romania": [45.943161, 24.96676],
        "Russia": [61.52401, 105.318756],
        "Rwanda": [-1.940278, 29.873888],
        "Saint Kitts and Nevis": [17.357822, -62.782998],
        "Saint Lucia": [13.909444, -60.978893],
        "Saint Vincent and the Grenadines": [12.984305, -61.287228],
        "Samoa": [-13.759029, -172.104629],
        "San Marino": [43.94236, 12.457777],
        "Sao Tome and Principe": [0.18636, 6.613081],
        "Saudi Arabia": [23.885942, 45.079162],
        "Senegal": [14.497401, -14.452362],
        "Serbia": [44.016521, 21.005859],
        "Seychelles": [-4.679574, 55.491977],
        "Sierra Leone": [8.460555, -11.779889],
        "Singapore": [1.352083, 103.819836],
        "Slovakia": [48.669026, 19.699024],
        "Slovenia": [46.151241, 14.995463],
        "Solomon Islands": [-9.64571, 160.156194],
        "Somalia": [5.152149, 46.199616],
        "South Africa": [-30.559482, 22.937506],
        "South Korea": [35.907757, 127.766922],
        "South Sudan": [6.876991, 31.306978],
        "Spain": [40.463667, -3.74922],
        "Sri Lanka": [7.873054, 80.771797],
        "Sudan": [12.862807, 30.217636],
        "Suriname": [3.919305, -56.027783],
        "Sweden": [60.128161, 18.643501],
        "Switzerland": [46.818188, 8.227512],
        "Syria": [34.802075, 38.996815],
        "Taiwan": [23.69781, 120.960515],
        "Tajikistan": [38.861034, 71.276093],
        "Tanzania": [-6.369028, 34.888822],
        "Thailand": [15.870032, 100.992541],
        "Timor-Leste": [-8.874217, 125.727539],
        "Togo": [8.619543, 0.824782],
        "Tonga": [-21.178986, -175.198242],
        "Trinidad and Tobago": [10.691803, -61.222503],
        "Tunisia": [33.886917, 9.537499],
        "Turkey": [38.963745, 35.243322],
        "Turkmenistan": [38.969719, 59.556278],
        "Tuvalu": [-7.109535, 177.64933],
        "Uganda": [1.373333, 32.290275],
        "Ukraine": [48.379433, 31.16558],
        "United Arab Emirates": [23.424076, 53.847818],
        "United Kingdom": [55.378051, -3.435973],
        "United States": [37.09024, -95.712891],
        "Uruguay": [-32.522779, -55.765835],
        "Uzbekistan": [41.377491, 64.585262],
        "Vanuatu": [-15.376706, 166.959158],
        "Vatican City": [41.902916, 12.453389],
        "Venezuela": [6.42375, -66.58973],
        "Vietnam": [14.058324, 108.277199],
        "Yemen": [15.552727, 48.516388],
        "Zambia": [-13.133897, 27.849332],
        "Zimbabwe": [-19.015438, 29.154857]
    }

    chosen_countries_nat_cat_man_made = filled_table["Country"].values
    filtered_countries_coordinates_nat_cat_man_made = {country: coords for country, coords in countries_coordinates.items() if country in chosen_countries_nat_cat_man_made}
    country_estimated_net_loss_nat_cat_man_made = {row["Country"]: row["Estimated Net Loss"] for index, row in filled_table.iterrows()}
    country_scenario_name_option_nat_cat_man_made = {row["Country"]: row["Scenario Name"] for index, row in filled_table.iterrows()}

    world_map = folium.Map(location=[0, 0], tiles="OpenStreetMap", zoom_start=2)
    for country_dev, coords in filtered_countries_coordinates_nat_cat_man_made.items():
        estimated_net_loss = country_estimated_net_loss_nat_cat_man_made.get(country_dev, 0)
        scenario_name_option = country_scenario_name_option_nat_cat_man_made.get(country_dev, 0)
        radius = estimated_net_loss / 1000000
        folium.CircleMarker(
            location=coords,
            color="blue",
            radius=radius,
            popup=f"{country_dev}, Scenario Name: {scenario_name_option}, Estimated Net Loss: {estimated_net_loss}",
            fill=True,
            fill_color='blue'
        ).add_to(world_map)

    chosen_countries_em_extr = filled_table_em_extr["Country"].values
    filtered_countries_coordinates_em_extr = {country: coords for country, coords in countries_coordinates.items() if country in chosen_countries_em_extr}
    country_estimated_net_loss_em_extr = {row["Country"]: row["Estimated Net Loss"] for index, row in filled_table_em_extr.iterrows()}
    country_scenario_name_option_em_extr = {row["Country"]: row["Scenario Name"] for index, row in filled_table_em_extr.iterrows()}

    for country_dev, coords in filtered_countries_coordinates_em_extr.items():
        estimated_net_loss = country_estimated_net_loss_em_extr.get(country_dev, 0)
        scenario_name_option_em_extr = country_scenario_name_option_em_extr.get(country_dev, 0)
        radius = estimated_net_loss / 1000000
        folium.CircleMarker(
            location=coords,
            color="orange",
            radius=radius,
            popup=f"{country_dev}, Scenario Name: {scenario_name_option_em_extr}, Estimated Net Loss: {estimated_net_loss}",
            fill=True,
            fill_color='orange'
        ).add_to(world_map)

    st.title("World Map")
    folium_static(world_map, width=8000, height=1000)


elif tab_selection == 'Output: Filled tables':
    
    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)

    buffer = io.BytesIO()
    def to_excel(df):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine = 'openpyxl')
        df.to_excel(writer, index = False, sheet_name = 'Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data

    st.header("Nat Cat and Man Made Risk Table")
    st.write(filled_table)
    filled_table_xlsx = to_excel(filled_table)
    st.download_button("Download the Nat Cat and Man Made Risk Table", data = filled_table_xlsx, file_name = "Nat_Cat_Man_Made_Risk_Table.xlsx",
                       mime = "application/vnd.ms-excel")
    
    st.header("Emerging and Extraordinary Scenarios Table")
    st.write(filled_table_em_extr)
    filled_table_em_extr_xlsx = to_excel(filled_table_em_extr)
    st.download_button("Download the Emerging and Extraordinary Scenarios Table", data = filled_table_em_extr_xlsx, file_name = "Emerging_Extraordinary_Risk_Table.xlsx",
                       mime = "application/vnd.ms-excel")

############# OUTPUT: FILLED TABLES

    ####TEST#######

elif tab_selection == "Summary KPIs":
    st.title("📊 Summary KPIs")

    # Load data
    df = pd.DataFrame(st.session_state.data)

    # Year selector
    available_years = sorted(df["Observation Year"].dropna().unique())
    selected_year = st.selectbox("Select Year", available_years, index=available_years.index(2025) if 2025 in available_years else 0)

    # Filter data
    df_selected = df[df["Observation Year"] == selected_year]
    df_previous = df[df["Observation Year"] == selected_year - 1]

    # Max Net Loss
    max_manmade = df_selected[df_selected["Risk Type"] == "Man Made"]["Estimated Net Loss"].max()
    max_natcat = df_selected[df_selected["Risk Type"] == "Nat Cat"]["Estimated Net Loss"].max()

    # Previous year values
    prev_manmade = df_previous[df_previous["Risk Type"] == "Man Made"]["Estimated Net Loss"].max()
    prev_natcat = df_previous[df_previous["Risk Type"] == "Nat Cat"]["Estimated Net Loss"].max()

    # YoY change
    yoy_manmade = ((max_manmade - prev_manmade) / prev_manmade * 100) if prev_manmade else 0
    yoy_natcat = ((max_natcat - prev_natcat) / prev_natcat * 100) if prev_natcat else 0

    # Convert to EUR millions
    max_manmade_m = round(max_manmade / 1e6, 2)
    max_natcat_m = round(max_natcat / 1e6, 2)

    # Layout
    col1, col2 = st.columns(2)

    def kpi_box(title, value, yoy, color):
        arrow = "📈" if yoy >= 0 else "📉"
        yoy_text = f"{arrow} YoY Change: {yoy:.2f}%"
        html = f"""
        <div style="background-color:{color}; padding:20px; border-radius:15px; box-shadow:2px 2px 10px rgba(0,0,0,0.1); text-align:center;">
            <h3 style="color:white;">{title}</h3>
            <h1 style="color:white;">€{value}M</h1>
            <p style="color:white; font-size:18px;">{yoy_text}</p>
        </div>
        """
        return html

    with col1:
        st.markdown(kpi_box("Max Net Loss - Man Made", max_manmade_m, yoy_manmade, "#d9534f"), unsafe_allow_html=True)

    with col2:
        st.markdown(kpi_box("Max Net Loss - Nat Cat", max_natcat_m, yoy_natcat, "#0275d8"), unsafe_allow_html=True)
    
    
    ####TEST#######


if tab_selection == 'RDS Conventional Inputs':
    
    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)



    def to_excel(df):
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='openpyxl')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.close()
        processed_data = output.getvalue()
        return processed_data

    st.header("Nat Cat and Man Made Risk Table")
    st.write(filled_table)
    filled_table_xlsx = to_excel(filled_table)
    st.download_button(
        "Download the Nat Cat and Man Made Risk Table",
        data=filled_table_xlsx,
        file_name="Nat_Cat_Man_Made_Risk_Table.xlsx",
        mime="application/vnd.ms-excel"
    )

    st.header("Emerging and Extraordinary Scenarios Table")
    st.write(filled_table_em_extr)
    filled_table_em_extr_xlsx = to_excel(filled_table_em_extr)
    st.download_button(
        "Download the Emerging and Extraordinary Scenarios Table",
        data=filled_table_em_extr_xlsx,
        file_name="Emerging_Extraordinary_Risk_Table.xlsx",
        mime="application/vnd.ms-excel"
    )




