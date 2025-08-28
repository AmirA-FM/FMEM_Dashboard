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
st.title(":blue[Exposure Management Dashboard]")

tab_selection = st.sidebar.radio(
    "Select a tab:",
    [
        'Input: Nat Cat and Man Made Risks',
        'Input: Emerging and Extraordinary Risks',
        'Currency Convertion',
        'Resulting Visualisations',
        'Limit System',
        'Payback',
        'Geographic Information System (GIS) Analysis',
        'Output: Filled tables'
    ]
)

if tab_selection == 'Input: Nat Cat and Man Made Risks':
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [],
            'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
            'Estimated Net Loss': [], 'Observation Year': [], 'Country': []
        })

    st.dataframe(st.session_state.data)

    def add_df_form():
        estimated_net_loss = st.session_state.estimated_gross_loss - st.session_state.estimated_reinsurance_benefits
        row = pd.DataFrame({'Risk Type': [st.session_state.risk_type_option],
                            'Scenario Cluster': [st.session_state.scenario_cluster_option],
                            'Scenario Name': [st.session_state.scenario_name_option],
                            'Estimated Gross Loss': [st.session_state.estimated_gross_loss],
                            'Estimated Reinsurance Benefits': [st.session_state.estimated_reinsurance_benefits],
                            'Estimated Net Loss': [estimated_net_loss],
                            'Observation Year': [st.session_state.observation_year],
                            'Country': [st.session_state.country]})
        st.session_state.data = pd.concat([st.session_state.data, row])

    risk_type_option = st.selectbox("Observed Risk Type:", ("Man Made", "Nat Cat"), index = None, key='risk_type_option')

    #################

    if risk_type_option == "Man Made":
            scenario_cluster_option = st.selectbox(
                "Please enter the observed scenario cluster:",
                ("Motor", "Fire / Explosion", "Aviation / Space", "Marine / Transport", "Liability", "Political", "Cyber", "Infectious Disease",
                "SRCC", "Terrorism", "Other Man Made"),
                index = None, key = 'scenario_cluster_option'
            )
    elif risk_type_option == "Nat Cat":
            scenario_cluster_option = st.selectbox(
                "Please enter the observed scenario cluster:",
                ("Windstorm", "Cyclones / Hurricane", "Earthquake", "Flood", "Wildfires", "Volcanic Eruption", "Tornado", "Drought", "Other Nat Cat"),
                index = None, key = 'scenario_cluster_option'
            )
    else:
        scenario_cluster_option = st.selectbox("Please enter the observed scenario cluster:", ("Not Available"), index = None, key = 'scenario_cluster_option')

    ########

    if scenario_cluster_option == "Motor":
            scenario_name_option = st.selectbox(
                "Please enter the observed scenario name:",
                ("Selby-type liability loss"),
                index = None, key = 'scenario_name_option'
            )
    elif scenario_cluster_option == "Fire / Explosion":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Aviation / Space":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Aviation collision", "Space weather - Solar energetic particle event", "Space weather - Design deficiency", "Generic defect of satellites", "Space debris"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Marine / Transport":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Ships collision", "Conflagoration at a marine complex", "Total loss of high value transport"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Liability":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Hazardous Substance or Contaminated product", "Faulty Advise or Negligence related to a Professional Service", "Pollution / Environmetal indicent",
            "Fraud or Financial Crime", "Professional Lines: Misselling of a Financial Product", "Professional Lines: Failure/Collapse of a Major Corporation",
            "Professional Lines: Failure of a Merger", "Professional Lines: Failure of a Construction Project", "Professional Lines: Recession-Related Losses",
            "Non-Professional Lines: Industrial/Transport Incident", "Non-Professional Lines: Multiple Public/Products Losses", "Back year deterioration"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Political":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Political Violence"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Cyber":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Power Blackout (Business Blackout)", "Cloud Outage (Cloud Cascade)", "Cyber Crime Event", "Cyber Motor", "Major Data Security Breach", "Ransomware Contagion"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Infectious Disease":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Regional outbreak of a disease", "Global outbreak of a disease"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "SRCC":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Strikes - Riots and Civil Commotion"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Terrorism":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Rockefeller Center: 2 tonne bomb blast", "One World Trade Center: 2 tonne bomb blast", "Terrorism accumulations other than Manhattan",
                "Conventional one-ton bomb", "9/11 plane attack type", "Gun fire/Truck goes to crowd"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Other Man Made":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Accumulation of casualties to members of sports team"),
            index = None, key = 'scenario_name_option'
        )

    ##################################

    elif scenario_cluster_option == "Windstorm":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("North East Windstorm", "South Carolina Windstorm", "Florida Windstorm - Miami-Dade", "Florida Windstorm - Pinellas", "Gulf of Mexico Windstorm",
                "European Windstorm", "Caribbean/USA Hurricane Windstorm Clash"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Cyclones / Hurricane":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Japanese Typhoon"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Earthquake":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("California Earthquake - Los Angeles", "California Earthquake - San Francisco", "New Madrid Earthquake", "Japanese Earthquake",
                "Other earthquakes (e.g. in China, Australia, New Zealand)"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Flood":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("UK Flood", "major flood outside of UK"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Wildfires":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Volcanic Eruption":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Tornado":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Drought":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Temp"),
            index = None, key = 'scenario_name_option'
        )
    elif scenario_cluster_option == "Other Nat Cat":
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Pandemic Risk"),
            index = None, key = 'scenario_name_option'
        )

    ###################

    else:
        scenario_name_option = st.selectbox(
            "Please enter the observed scenario name:",
            ("Not Available"),
            index = None, key = 'scenario_name_option'
        )

    ####################

    observation_year = st.number_input(
        "Select the observation year from 1900 until 2100:",
        min_value = 1900,
        max_value = 2100,
        step = 1, key='observation_year'
        )
    
    ####################
    
    country = st.selectbox(
        "Please select country where the scenario is observed:",
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
                                            'Estimated Reinsurance Benefits': [], 'Estimated Net Loss': [], 'Observation Year': [], 'Country': []})

############# INPUT: EMERGING AND EXTRAORDINARY RISKS

if tab_selection == 'Input: Emerging and Extraordinary Risks':
    st.image("ERI_Risk_Radar_2025_Emerging_Risk_Radar.jpg")

    if 'data_emerging_extraordinary' not in st.session_state:
        st.session_state.data_emerging_extraordinary = pd.DataFrame({
        'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [],
        'Impact Assessment': [], 'Time Horizon': [],
        'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
        'Estimated Net Loss': [], 'Observation Year': [], 'Country': []
    })

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
        "Please select the observed risk type:",
        ("Emerging", "Extraordinary"),
        index = None, key = 'risk_type_option_em_extr'
        )
    
    st.write("If you enter your scenario cluster and / or scenario name manually, you need to press 'ENTER' afterwards for it to be considered by the programme.")

    if risk_type_option_em_extr == "Emerging":
        scenario_cluster_option_em_extr = st.selectbox(
            "Please enter the observed scenario cluster:",
            ("Environmental", "Technological", "Economic", "Regulatory"),
            index = None, placeholder = "Select an observed scenario cluster or enter a new one", accept_new_options = True, key = 'scenario_cluster_option_em_extr'
        )
    elif risk_type_option_em_extr == "Extraordinary":
        scenario_cluster_option_em_extr = st.selectbox(
            "Please enter the observed scenario cluster:",
            ("Climate Change Litigation (Greenwashing)", "E-Vehicle Explosion due to heatwaves", "Solar Storms", "Dam Breach"),
            index = None, placeholder = "Select an observed scenario cluster or enter a new one", accept_new_options = True, key = 'scenario_cluster_option_em_extr'
        )
    else:
        scenario_cluster_option_em_extr = st.selectbox("Please enter the observed scenario cluster:", ("Not Available"), index = None, key = 'scenario_cluster_option_em_extr')

    if scenario_cluster_option_em_extr == "Environmental":
        scenario_name_option_em_extr = st.selectbox(
        "Please enter the observed scenario name:",
        ("Antimicrobial Resistance", "Climate Change Physical Risk", "Climate Engineering and Storage Techniques", "Emerging Infectious Diseases",
        "Environmental Pollution", "Nature and Biodiversity Loss", "Space Risk"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Technological":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Artificial Intelligence", "Autonomous Machines", "Critical Infrastructure Failures", "Cyber Risks",
            "Data Privacy and Data Ethics", "Hazardous Chemicals and Small Particles", "Information Reliability"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Economic":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Climate Change Transition Risk", "Deterioration of Public Healthcare Systems", "Economic Trade Conflicts and Sanctions", "Evolving Terrorism", "Geopolitical Tensions and Conflicts",
            "Global Debt Crisis", "Mental Health", "Metabolic Syndrome", "Resource Management", "Skills Shortage and Reskilling", "Social Fragmentation"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Regulatory":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Collective Redress", "Legal and Regulatory Complexity", "Medical Advances", "Substance Abuse", "Supply Chain Complexity"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
#########
    elif scenario_cluster_option_em_extr == "Climate Change Litigation (Greenwashing)":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Corporate Accountability Crisis", "Greenwashing Scandal Unveiled", "Eco-Fraud Legal Battle"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "E-Vehicle Explosion due to heatwaves":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Battery Meltdown Catastrophe", "Thermal Runaway Disaster", "Heatwave-Induced E-Vehicle Explosions"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Solar Storms":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Geomagnetic Storm Havoc", "Solar Flare Disruption", "Space Weather Crisis"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
    elif scenario_cluster_option_em_extr == "Dam Breach":
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
            ("Hydraulic Infrastructure Failure", "Catastrophic Flooding Event", "Dam Collapse Emergency"),
            index = None, placeholder = "Select an observed scenario name or enter a new one", accept_new_options = True, key = 'scenario_name_option_em_extr'
        )
#########
    else:
        scenario_name_option_em_extr = st.selectbox(
            "Please enter the observed scenario name:",
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

    observation_year_em_extr = st.number_input(
        "Select the observation year from 1900 until 2100:",
        min_value = 1900,
        max_value = 2100,
        step = 1, key='observation_year_em_extr'
        )
    
    ####################
    
    country_em_extr = st.selectbox(
        "Please select country where the scenario is observed:",
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
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [],
            'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
            'Estimated Net Loss': [], 'Observation Year': [], 'Country': []
        })
    if 'data_emerging_extraordinary' not in st.session_state:
        st.session_state.data_emerging_extraordinary = pd.DataFrame({
            'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [],
            'Impact Assessment': [], 'Time Horizon': [],
            'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
            'Estimated Net Loss': [], 'Observation Year': [], 'Country': []
        })
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
    if 'data' not in st.session_state:
        st.session_state.data = pd.DataFrame({
            'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [],
            'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
            'Estimated Net Loss': [], 'Observation Year': [], 'Country': []
        })
    if 'data_emerging_extraordinary' not in st.session_state:
        st.session_state.data_emerging_extraordinary = pd.DataFrame({
            'Risk Type': [], 'Scenario Cluster': [], 'Scenario Name': [],
            'Impact Assessment': [], 'Time Horizon': [],
            'Estimated Gross Loss': [], 'Estimated Reinsurance Benefits': [],
            'Estimated Net Loss': [], 'Observation Year': [], 'Country': []
        })
    filled_table = pd.DataFrame(st.session_state.data)
    filled_table_em_extr = pd.DataFrame(st.session_state.data_emerging_extraordinary)

    st.header("Limit System")

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
            "Do you want to observe Nat Cat and Man Made or Emerging and Extraordinary Risks?",
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
        payback = extreme_disaster_loss / corresponding_loss if corresponding_loss else 0
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

    if not filled_table.empty:
        m = folium.Map(location=[20,0], zoom_start=2.5)
        marker_cluster = MarkerCluster().add_to(m)
        for idx, row in filled_table.iterrows():
            folium.Marker(
              location=[row["Latitude"], row["Longitude"]],
              popup=f"Scenario Name: {row['Scenario Name']}<br>Estimated Net Loss: {row['Estimated Net Loss']}",
              icon=folium.Icon(color="blue", icon="info-sign"),































        st.success("Data exported to Excel successfully!")            st.session_state.data_emerging_extraordinary.to_excel(writer, sheet_name='Emerging and Extraordinary Risks', index=False)            st.session_state.data.to_excel(writer, sheet_name='Nat Cat and Man Made Risks', index=False)        with pd.ExcelWriter('Risk_Scenarios.xlsx') as writer:    if excel:    excel = st.button("Export to Excel")    st.dataframe(st.session_state.data_emerging_extraordinary)    st.subheader("Emerging and Extraordinary Risks")    st.dataframe(st.session_state.data)    st.subheader("Nat Cat and Man Made Risks")    st.header("Filled Tables")elif tab_selection == 'Output: Filled tables':############ OUTPUT: FILLED TABLES        st_folium(m_em_extr, width=700, height=500)            ).add_to(marker_cluster_em_extr)              icon=folium.Icon(color="red", icon="info-sign"),              popup=f"Scenario Name: {row['Scenario Name']}<br>Estimated Net Loss: {row['Estimated Net Loss']}",              location=[row["Latitude"], row["Longitude"]],            folium.Marker(        for idx, row in filled_table_em_extr.iterrows():        marker_cluster_em_extr = MarkerCluster().add_to(m_em_extr)        m_em_extr = folium.Map(location=[20,0], zoom_start=2.5)    if not filled_table_em_extr.empty:        st_folium(m, width=700, height=500)            ).add_to(marker_cluster)            ).add_to(marker_cluster)
        st.subheader("Geographic Distribution of Scenarios - Nat Cat and Man Made Risks")
        folium_static(m, width=725, height=500)

    if not filled_table_em_extr.empty:
        m2 = folium.Map(location=[20,0], zoom_start=2.5)
        marker_cluster_em_extr = MarkerCluster().add_to(m2)
        for idx, row in filled_table_em_extr.iterrows():
            folium.Marker(
              location=[row["Latitude"], row["Longitude"]],
              popup=f"Scenario Name: {row['Scenario Name']}<br>Estimated Net Loss: {row['Estimated Net Loss']}",
              icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(marker_cluster_em_extr)
        st.subheader("Geographic Distribution of Scenarios - Emerging and Extraordinary Risks")
        folium_static(m2, width=725, height=500)

############# OUTPUT: FILLED TABLES

elif tab_selection == 'Output: Filled tables':
    st.header("Filled Tables")

    st.subheader("Nat Cat and Man Made Risks")
    st.write(pd.DataFrame(st.session_state.data))

    st.subheader("Emerging and Extraordinary Risks")
    st.write(pd.DataFrame(st.session_state.data_emerging_extraordinary))

    csv = st.button("Download CSV")
    if csv:
        df = pd.concat([st.session_state.data, st.session_state.data_emerging_extraordinary])
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="filled_tables.csv">Download CSV file</a>'
        st.markdown(href, unsafe_allow_html=True)


