import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import mysql.connector
import plotly.express as px
import PIL
from PIL import Image

#***************MySQL connection************
connection = mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe")
mycursor = connection.cursor()

#*********setting up page_config and dashboard*************
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   layout= "wide",
                   initial_sidebar_state= "auto",
                   menu_items={'About': """# This dashboard app is created for PhonePe Data Visualization!
                                        Data has been cloned from Phonepe Pulse Github Repository"""})

st.sidebar.header(":wave: :rainbow[**Welcome to the dashboard!**]")
with st.sidebar:
    selected = option_menu("Menu", ["Home","Data Exploration","Geo-visuals","Basic Insights","About"], 
                icons=["house","bar-chart-line","globe-central-south-asia","graph-up-arrow","exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "18px", "text-align": "left", "margin": "-3px", "--hover-color": "grey"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

#------------------------Home-----------------------------

if selected == "Home":
    st.header(":violet[PhonePe Pulse Data Visualization and Exploration]")
    st.write("")
    st.write("")
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        
        st.markdown("PhonePe is an Indian multinational digital payments and financial services company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. It is owned by Flipkart, a subsidiary of Walmart.")
        st.markdown(":green[This web app is built to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geo visualization output based on given requirements.]")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        st.write("#### ****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
    

#-----------------------------Data Exploration ---------------------

def Agg_tran_count():
    mycursor.execute(f"select State, sum(Transaction_count) as Count from agg_tran where Year = {Year} and Quarter = {Quarter} group by State order by Count desc")
    df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_Count'])
    fig_1 = px.bar(df, y='Transaction_Count',
            x ='State',
            orientation = 'v',
            color='Transaction_Count',
            title='States based on Transaction Count',
            color_discrete_sequence=px.colors.sequential.Magenta, height = 550, width =750)
                    
    return st.plotly_chart(fig_1, use_container_width = True)

def Agg_tran_amount():
    mycursor.execute(f"select State, sum(Transaction_amount) as Total from agg_tran where Year = {Year} and Quarter = {Quarter} group by State order by Total desc")
    df1 = pd.DataFrame(mycursor.fetchall(),columns = ['State', 'Transaction_Amount'])
    fig_2 = px.bar(df1, y='Transaction_Amount',
            x ='State',
            orientation = 'v',
            color='Transaction_Amount',
            title='States based on Transaction Amount',
            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 550, width =750)
    return st.plotly_chart(fig_2, use_container_width = True)

def Payment_type_count():
    mycursor.execute(f"select State, Transaction_type, sum(Transaction_count) as Tot_tran from agg_tran where Year = {Year} and Quarter = {Quarter} and State = '{selected_state_1}' group by State,Transaction_type order by Tot_tran desc")
    df2 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Transaction_type','Transaction_count'])
    fig_pie = px.pie(df2, title="Transaction Types based on Transaction Count",
                        names ='Transaction_type', values ='Transaction_count', 
                        hole = 0.4,height = 500, width =600,
                        color_discrete_sequence = px.colors.sequential.RdBu)
    fig_pie.update_traces(textinfo = 'percent+label', textposition='inside')
    return st.plotly_chart(fig_pie, use_container_width = True)

def Payment_type_amount():
    mycursor.execute(f"select State, Transaction_type, sum(Transaction_amount) as Tot_amount from agg_tran where Year =  {Year} and Quarter = {Quarter} and State = '{selected_state_2}' group by State,Transaction_type order by Tot_amount desc")
    df2 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Transaction_type','Transaction_amount'])
    fig_pie = px.pie(df2, title="Transaction Types based on Transaction Amount",
                        names ='Transaction_type', values ='Transaction_amount', 
                        hole = 0.5,height = 500, width =600,
                        color_discrete_sequence = px.colors.sequential.RdBu)
    fig_pie.update_traces(textinfo = 'percent+label', textposition='inside')
    return st.plotly_chart(fig_pie, use_container_width = True)

def Agg_user():
    mycursor.execute(f"select State, Brands, sum(Transaction_Count) as Tot_count, avg(Percentage)*100 as Percentage from agg_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, Brands order by Tot_count desc")
    df3 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Brands','User_Count','Avg_percentage'])
    fig_line_1 = px.line(df3,title= f"Mobile Brands based on Phonepe User Count for state '{selected_state}'",  
                 x = 'Brands', y= "User_Count", hover_data = "Avg_percentage",height = 600, width =750,
                 markers = True, color_discrete_sequence = px.colors.sequential.Inferno_r)
    return st.plotly_chart(fig_line_1, use_container_width = True)

def Map_tran_count():
    mycursor.execute(f"select State, sum(Transaction_Count) as Count from map_tran where Year = {Year} and Quarter = {Quarter} group by State order by Count desc")
    df5 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_Count'])
    fig_1 = px.bar(df5, y='Transaction_Count',
            x ='State',
            orientation = 'v',
            color='Transaction_Count',
            title='States based on Transaction Count',
            color_discrete_sequence=px.colors.sequential.Burg, height = 550, width =750)                   
    return st.plotly_chart(fig_1, use_container_width = True)

def Map_tran_amount():
    mycursor.execute(f"select State, sum(Transaction_Amount) as Total from map_tran where Year = {Year} and Quarter = {Quarter} group by State order by Total desc")
    df = pd.DataFrame(mycursor.fetchall(),columns = ['State', 'Transaction_Amount'])
    fig = px.bar(df, y='Transaction_Amount',
            x ='State',
            orientation = 'v',
            color='Transaction_Amount',
            title='States based on Transaction Amount',
            color_discrete_sequence=px.colors.sequential.Magenta_r, height = 550, width =750)
    return st.plotly_chart(fig, use_container_width = True)

def Map_tran_state_explore_c():
    mycursor.execute(f"select State, District, Year, Quarter, Transaction_Count, Transaction_Amount from map_tran where Year = {Year} and Quarter = {Quarter} and State = '{selected_state_ec}' order by District")
    df_ec = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Total_Transactions','Total_amount'])
    fig_e1 = px.bar(df_ec,
            title=selected_state, x="District", y="Total_Transactions",
            orientation='v',color='Total_Transactions',
            color_continuous_scale = px.colors.sequential.Agsunset_r)
    return st.plotly_chart(fig_e1, use_container_width=True)

def Map_tran_state_explore_a():
    mycursor.execute(f"select State, District, Year, Quarter, Transaction_Count, Transaction_Amount from map_tran where Year = {Year} and Quarter = {Quarter} and State = '{selected_state_ea}' order by District")
    df_ea = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Total_Transactions','Total_amount'])
    fig_e2 = px.bar(df_ea,
            title=selected_state, x="District", y="Total_amount", orientation='v',
            color='Total_amount',color_continuous_scale = px.colors.sequential.Agsunset_r)
    return st.plotly_chart(fig_e2, use_container_width=True)

def Map_user():
    mycursor.execute(f"select State, sum(RegisteredUser) as Total_users, sum(AppOpens) as app_opens from map_user where Year = {Year} and Quarter = {Quarter} group by State order by State desc" )
    df = pd.DataFrame(mycursor.fetchall(), columns = ['State','Total_users','AppOpens'])
    fig_line = px.line(df,  
                 x = 'State', y= ['Total_users','AppOpens'], height = 600, width =750,
                 markers = True, color_discrete_sequence = px.colors.sequential.Plasma)
    return st.plotly_chart(fig_line, use_container_width = True)

def Map_user_state_explore_c():
    mycursor.execute(f"select State, District, Year, Quarter, RegisteredUser, AppOpens from map_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' order by District")
    df_ec = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Phonepe_Users','AppOpens'])
    fig = px.bar(df_ec,
            title = selected_state, x="District", y="Phonepe_Users", orientation='v',
            color='Phonepe_Users', color_continuous_scale = px.colors.sequential.Agsunset)
    return st.plotly_chart(fig, use_container_width=True)

def Map_user_state_explore_a():
    mycursor.execute(f"select State, District, Year, Quarter, RegisteredUser, AppOpens from map_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' order by District")
    df_ea = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Phonepe_Users','AppOpens'])
    fig = px.bar(df_ea,
            title=selected_state, x="District", y="AppOpens", orientation='v',
            color='AppOpens', color_continuous_scale = px.colors.sequential.Agsunset)
    return st.plotly_chart(fig, use_container_width=True)

def Top_tran_count():
    mycursor.execute(f"select State,Pincode sum(Transaction_count) as count from top_tran where Year = {Year} and Quarter = {Quarter} group by State,Pincode order by count desc")
    df = pd.DataFrame(mycursor.fetchall(), columns = ['State','Pincode','Transaction_count']) 
    fig = px.bar(df,
            title="States based on Transaction Count", x="State", y="Transaction_count", orientation='v',
            color='Transaction_count',hover_data= 'Pincode',
            color_continuous_scale = px.colors.sequential.algae)
    return st.plotly_chart(fig, use_container_width=True)

def Top_tran_amount():
    mycursor.execute(f"select State,Pincode sum(Transaction_amount) as amount from top_tran where Year = {Year} and Quarter = {Quarter} group by State,Pincode order by amount desc")
    df = pd.DataFrame(mycursor.fetchall(), columns = ['State','Pincode','Transaction_amount']) 
    fig = px.bar(df,
            title="States based on Transaction Amount", x="State", y="Transaction_amount", orientation='v',
            color='Transaction_amount',hover_data= 'Pincode',
            color_continuous_scale = px.colors.sequential.algae)
    return st.plotly_chart(fig, use_container_width=True)

def  Top_user():
    mycursor.execute(f"select State,Pincode sum(RegisteredUsers) as users from top_tran where Year = {Year} and Quarter = {Quarter} group by State,Pincode order by users desc")
    df_u = pd.DataFrame(mycursor.fetchall(), columns = ['State','Pincode','Registered_Users']) 
    fig = px.bar(df_u,
            title="States based on Registered Users", x="State", y="Registered_Users", orientation='v',
            color='Registered_Users',hover_data= 'Pincode',
            color_continuous_scale = px.colors.sequential.Magenta)
    return st.plotly_chart(fig, use_container_width=True)

          
if selected == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(['##### :violet[Aggregated Analysis]','##### :green[Map Analysis]','##### :rainbow[Top Analysis]'])
    with tab1:
        Type = st.selectbox("###### :orange[Select the Analysis]", ("Transaction", "Users"))  
      
        if Type == "Transaction":
            with st.sidebar:
                select = st.radio("Select the options",["States based on Transaction Count",
                            "States based on Transaction Amount", 
                            "Top Payment Type based on Transaction Count and Amount"],
                            label_visibility="hidden")  
                Year = st.slider("#### :orange[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("#### :orange[Quarter]", min_value=1, max_value=4)     
            
            if select == "States based on Transaction Count":
                Agg_tran_count()           
            if  select == "States based on Transaction Amount":
                Agg_tran_amount()
            if select == "Top Payment Type based on Transaction Count and Amount":
                col1,col2 = st.columns([3.5,3.5],gap="medium")
                with col1:
                    selected_state_1 = st.selectbox("###### :green[Select any State]",
                           ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                            'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                            'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                            'Uttarakhand', 'West Bengal'))
                    Payment_type_count()
                with col2:
                    selected_state_2 = st.selectbox("###### :blue[Select any State]",
                           ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                            'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                            'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                            'Uttarakhand', 'West Bengal'))
                    Payment_type_amount()
                
        if Type == "Users":
            Year = st.slider("###### :violet[Year]", min_value=2018, max_value=2023)
            Quarter = st.slider("###### :violet[Quarter]", min_value=1, max_value=4)     
            st.subheader(" :green[Mobile Brands based on User Count]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry.. No Data to Display for this Quarter")
            elif Year == 2023 and Quarter in [1,2,3,4]:
                st.markdown("#### Sorry.. No Data to Display for this Quarter")  
            else:
                selected_state = st.selectbox("###### :orange[Select any State]",
                           ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                            'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                            'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                            'Uttarakhand', 'West Bengal'))
                Agg_user()
    
    with tab2:
        Type = st.selectbox("###### :blue[Select the Analysis]", ("Transaction", "Users"))  
      
        if Type == "Transaction":
            with st.sidebar:
                select_t2 = st.radio("Select the options",["States based on Transaction Count",
                            "States based on Transaction Amount", 
                            "District wise Data Exploration"],
                            label_visibility="hidden")  
                Year = st.slider("#### :orange[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("#### :orange[Quarter]", min_value=1, max_value=4)   

            if select_t2 == "States based on Transaction Count":
                Map_tran_count()
            if select_t2 ==  "States based on Transaction Amount":
                Map_tran_amount()
            if select_t2 == "District wise Data Exploration":
                st.write("##### :green[Explore data for selected states based on transaction count and amount from various years and quarters]")
                col1, col2 = st.columns([3.5,3.5], gap = "medium")
                with col1:
                    selected_state_ec = st.selectbox("###### :red[Select any State to explore more]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
                    Map_tran_state_explore_c()
                with col2:
                    selected_state_ea = st.selectbox("###### :blue[Select any State to explore more]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
                    Map_tran_state_explore_a()
        
        if Type == "Users":
            with st.sidebar:
                select_u = st.radio("Select the options",["States based on Phonepe Users and App Opens",
                        "District wise Data Exploration"],label_visibility="hidden")  
                Year = st.slider("#### :green[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("#### :green[Quarter]", min_value=1, max_value=4)   

            if select_u == "States based on Phonepe Users and App Opens":
                Map_user()
            if select_u == "District wise Data Exploration":
                st.write("##### :red[Explore data for selected states based on registered users and app opens from various years and quarters]")
                col1, col2 = st.columns([3.5,3.5], gap = "medium")
                with col1:
                    selected_state = st.selectbox("###### :blue[Select any State to explore more]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
                    Map_user_state_explore_c()
                with col2:
                    selected_state = st.selectbox("###### :green[Select any State to explore more]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
                    Map_user_state_explore_a()

    with tab3:
        Type = st.selectbox("###### :blue[Select the Analysis]", ("Transaction", "Users"))  

        if Type == "Transaction":
            with st.sidebar:
                select_t3 = st.radio("Select the options",["States based on Transaction Count",
                            "States based on Transaction Amount"],
                            label_visibility="hidden")  
                Year = st.slider("#### :violet[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("#### :violet[Quarter]", min_value=1, max_value=4)   

            if select_t3 == "States based on Transaction Count":
                Top_tran_count()
            if select_t3 == "States based on Transaction Amount":    
                Top_tran_amount()

        if Type == "Users":
            Year = st.slider("#### :green[Year]", min_value=2018, max_value=2023)
            Quarter = st.slider("#### :green[Quarter]", min_value=1, max_value=4)   
            Top_user()

#------------------------------Geo-visuals-----------------------------
def geo_agg_tran_count():
    mycursor.execute(f"select State,Year,Quarter,sum(Transaction_Count) as Count from agg_tran where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_g = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Total_Transactions'])
    df2 = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_g.Total_Transactions = df_g.Total_Transactions.astype(np.int64)
    df_g.State = df2
    
    fig_g= px.choropleth(df_g,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale=px.colors.sequential.Viridis_r)
    fig_g.update_layout(title='Statewise Transaction Count',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_g.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_g, use_container_width=False)

def geo_agg_tran_amount():
    mycursor.execute(f"select State,Year,Quarter, sum(Transaction_Amount) as Amount from agg_tran where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_g1 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Transaction_amount'])
    df3 = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_g1.Transaction_amount = df_g1.Transaction_amount.astype(np.int64)
    df_g1.State = df3
    
    fig_g1= px.choropleth(df_g1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Transaction_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset_r)
    fig_g1.update_layout(title='Statewise Transaction Amount',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_g1.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_g1, use_container_width=False)

def geo_agg_user_users():
    mycursor.execute(f"select State,Year,Quarter,Brands sum(Transaction_Count) as Tot_users from agg_user where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter,Brands order by State")
    df_u = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Brands','Tot_users'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_u.Tot_users = df_u.Tot_users.astype(np.int64)
    df_u.State = df

    fig_gu= px.choropleth(df_u,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Tot_users',hover_data ='Brands',
                    color_continuous_scale=px.colors.sequential.Aggrnyl)
    fig_gu.update_layout(title='State wise Total phonepe Users',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_gu.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_gu, use_container_width=False)

def geo_map_tran_count():
    mycursor.execute(f"select State,Year,Quarter,sum(Transaction_Count) as Count from map_tran where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_g = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Total_Transactions'])
    df2 = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_g.Total_Transactions = df_g.Total_Transactions.astype(np.int64)
    df_g.State = df2
    
    fig_g= px.choropleth(df_g,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale=px.colors.sequential.Viridis_r)
    fig_g.update_layout(title='Statewise Transaction Count',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_g.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_g, use_container_width=False)

def geo_map_tran_amount():
    mycursor.execute(f"select State,Year,Quarter, sum(Transaction_Amount) as Amount from map_tran where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_g1 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Transaction_amount'])
    df3 = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_g1.Transaction_amount = df_g1.Transaction_amount.astype(np.int64)
    df_g1.State = df3
    
    fig_g1= px.choropleth(df_g1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Transaction_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset_r)
    fig_g1.update_layout(title='Statewise Transaction Amount',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_g1.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_g1, use_container_width=False)

def geo_map_user_users():
    mycursor.execute(f"select State,Year,Quarter, sum(RegisteredUser) as Tot_users from map_user where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_u = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Tot_users'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_u.Tot_users = df_u.Tot_users.astype(np.int64)
    df_u.State = df

    fig_gu= px.choropleth(df_u,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Tot_users',
                    color_continuous_scale=px.colors.sequential.Aggrnyl)
    fig_gu.update_layout(title='State wise Total phonepe Users',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_gu.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_gu, use_container_width=False)

def geo_map_user_appopens():
    mycursor.execute(f"select State,Year,Quarter, sum(AppOpens) as AppOpens from map_user where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_u1 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','App_Opens'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_u1.App_Opens = df_u1.App_Opens.astype(np.int64)
    df_u1.State = df

    fig_gu1= px.choropleth(df_u1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='App_Opens',
                    color_continuous_scale = px.colors.sequential.Aggrnyl_r)
    fig_gu1.update_layout(title='State wise Total App Opens',
                    title_x=0.25,
                    title_y=0.93,
                    height=500, 
                    margin={"r":5,"t":5,"l":5,"b":5},
                    title_font=dict(size=18))

    fig_gu1.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_gu1, use_container_width=False)

def geo_top_tran_count():
    mycursor.execute(f"select State,Year,Quarter, sum(Transaction_count) as count from top_tran where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_tt= pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Total_transactions'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_tt.Total_transactions = df_tt.Total_transactions.astype(np.int64)
    df_tt.State = df

    fig_tt1= px.choropleth(df_tt,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_transactions',
                    color_continuous_scale=px.colors.sequential.Agsunset_r)
    fig_tt1.update_layout(title='State wise Transaction Count',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_tt1.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_tt1, use_container_width=False)

def geo_top_tran_amount():
    mycursor.execute(f"select State,Year,Quarter, sum(Transaction_amount) as amount from top_tran where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_tt= pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Transaction_amount'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_tt.Transaction_amount = df_tt.Transaction_amount.astype(np.int64)
    df_tt.State = df

    fig_tt2= px.choropleth(df_tt,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Transaction_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
    fig_tt2.update_layout(title='State wise Transaction Amount',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_tt2.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_tt2, use_container_width=False)

def geo_top_user_users():
    mycursor.execute(f"select State,Year,Quarter, sum(RegisteredUsers) as users from top_user where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter order by State")
    df_tt = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Registered_users'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_tt.Registered_users = df_tt.Registered_users.astype(np.int64)
    df_tt.State = df

    fig_tt3= px.choropleth(df_tt,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Registered_users',
                    color_continuous_scale = px.colors.sequential.RdBu)
    fig_tt3.update_layout(title='State wise Total Users',
                    title_x=0.25,
                    title_y=0.93,
                    height=500, 
                    margin={"r":5,"t":5,"l":5,"b":5},
                    title_font=dict(size=18))

    fig_tt3.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_tt3, use_container_width=False)

if selected == "Geo-visuals":
    st.write("## :rainbow[Geo-Visualisation of all Indian States]")
    tab1, tab2, tab3 = st.tabs(['##### :violet[Aggregated Analysis]','##### :green[Map Analysis]','##### :rainbow[Top Analysis]'])
    with tab1:
        Type = st.selectbox("###### :orange[Select the Analysis]", ("Transaction", "Users"))
        with st.sidebar:
                Year = st.slider("##### :green[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("##### :green[Quarter]", min_value=1, max_value=4)
        if Type == "Transaction": 
            opt = st.radio("###### :violet[Choose the option to visualize]",["***All State Transaction Count***","***All State Transaction Amount***"],horizontal=True)
            if opt =="***All State Transaction Count***":
                geo_agg_tran_count()
            elif opt == "***All State Transaction Amount***":
                geo_agg_tran_amount()          
        if Type == "Users":
            st.write("##### :orange[All State Phonepe User Counts with Mobile Brands]")
            geo_agg_user_users()

    with tab2:
        Type = st.selectbox("###### :violet[Select the Analysis]", ("Transaction", "Users"))
        with st.sidebar:
                Year = st.slider("##### :green[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("##### :green[Quarter]", min_value=1, max_value=4)
        if Type == "Transaction": 
            opt = st.radio("###### :orange[Choose the option to visualize]",["***All State Transaction Count***","***All State Transaction Amount***"],horizontal=True)
            if opt =="***All State Transaction Count***":
                geo_map_tran_count()
            elif opt == "***All State Transaction Amount***":
                geo_map_tran_amount()        
        if Type == "Users":
           opt = st.radio("###### :orange[Choose the option to visualize]",["***All State Phonepe User count***","***All State AppOpen count***"],horizontal=True)
           if opt == "***All State Phonepe User count***":
                geo_map_user_users()
           elif opt == "***All State AppOpen count***":
                geo_map_user_appopens()

    with tab3:
        Type = st.selectbox("###### :red[Select the Analysis]", ("Transaction", "Users"))
        with st.sidebar:
                Year = st.slider("##### :green[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("##### :green[Quarter]", min_value=1, max_value=4)
        if Type == "Transaction": 
            opt = st.radio("###### :blue[Choose the option to visualize]",["***All State Transaction Count***","***All State Transaction Amount***"],horizontal=True)
            if opt =="***All State Transaction Count***":
                geo_top_tran_count()
            elif opt == "***All State Transaction Amount***":
                geo_top_tran_amount()
        if Type == "Users":
           st.write("##### :orange[All State Phonepe User Counts]")
           geo_top_user_users()

#--------------Basic Insights-------------
if selected ==  "Basic Insights":
    st.subheader(':violet[Basic Insights]')
    st.markdown("##### :green[These insights gives an overall understanding of the Phonepe pulse data]")
    options = ["--select--",
            "1. States with Highest Transaction Count",
            "2. States with Lowest Transaction Count",
            "3. States with Highest Number of App Users",
            "4. States with Lowest Number of App Users",
            "5. Districts with Highest Number of App Opens",
            "6. Districts with Lowest Number of App Opens",
            "7. Mobile Brands with Highest Transaction Count",
            "8. Top Transaction Types based on Transaction Amount"]
   
    slt = st.selectbox("##### :orange[Select the option]",options)
    
    if slt ==  "1. States with Highest Transaction Count":
        col1,col2 = st.columns([4,4],gap="large")
        mycursor.execute("select distinct State, sum(Transaction_Count) as counts from map_tran group by State order by counts desc limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))
        
        fig1 = px.bar(df1, title='States with Highest Transaction Count',orientation = 'v',x='State',y='Transaction_counts',
                    color_discrete_sequence=px.colors.sequential.Agsunset,height = 500, width =600)
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df1)
        
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig1, use_container_width=True)

    if slt == "2. States with Lowest Transaction Count":
        col1,col2 = st.columns([4,4],gap="medium")
        mycursor.execute("select distinct State, sum(Transaction_Count) as counts from map_tran group by State order by counts limit 10")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_counts'], index = range(1,len(data)+1))
        
        fig2 = px.bar(df2, title='States with Lowest Transaction Count',orientation = 'v',x='State',y='Transaction_counts',
             color_discrete_sequence=px.colors.sequential.Agsunset_r,height = 500, width =600)
        
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df2)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig2, use_container_width=True)
    
    if slt == "3. States with Highest Number of App Users":
        col1,col2 = st.columns([4,4],gap="medium")
        mycursor.execute("select distinct State, sum(RegisteredUser) as Users from map_user group by State order by Users desc limit 10")
        data = mycursor.fetchall()
        df3 = pd.DataFrame(data, columns = ['State','Total_AppUsers'], index = range(1,len(data)+1))
        
        fig3 = px.bar(df3, title='States with Highest Number of App Users',orientation = 'v',x='State',y='Total_AppUsers',
             color_discrete_sequence=px.colors.sequential.Agsunset, height = 500, width =600)

        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df3)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig3, use_container_width=True)

    if slt == "4. States with Lowest Number of App Users":
        col1,col2 = st.columns([4,4],gap="medium")
        mycursor.execute("select distinct State, sum(RegisteredUser) as Users from map_user group by State order by Users limit 10 ")
        data = mycursor.fetchall()
        df4 = pd.DataFrame(data, columns = ['State','Total_AppUsers'], index = range(1,len(data)+1))
       
        fig4 = px.bar(df4, title='States with Lowest Number of App Users',orientation = 'v',x='State',y='Total_AppUsers',
             color_discrete_sequence=px.colors.sequential.Agsunset, height = 500, width =600)

        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df4)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig4, use_container_width=True)
    
    if slt == "5. Districts with Highest Number of App Opens":
        col1,col2 = st.columns([4,4],gap="medium")
        mycursor.execute("select District, sum(AppOpens) as AppOpen_Count from map_user group by District order by AppOpen_Count desc limit 10")
        data = mycursor.fetchall()
        df5 = pd.DataFrame(data, columns = ['District','AppOpen_Count'], index = range(1,len(data)+1))
        
        fig5 = px.bar(df5, x= 'District', y='AppOpen_Count',title='Districts with Highest Number of App Opens',
                    color_discrete_sequence=px.colors.sequential.Plasma, orientation='v',height = 500, width = 550)
       
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df5)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig5, use_container_width=True)

    if slt == "6. Districts with Lowest Number of App Opens":
        col1,col2 = st.columns([4,4],gap="medium")
        mycursor.execute("select District, sum(AppOpens) as AppOpen_Count from map_user group by District order by AppOpen_Count  limit 10")
        data = mycursor.fetchall()
        df6 = pd.DataFrame(data, columns = ['District','AppOpen_Count'], index = range(1,len(data)+1) )
        
        fig6 = px.bar(df6, x= 'District', y='AppOpen_Count',title='Districts with Lowest Number of App Opens',
                    color_discrete_sequence=px.colors.sequential.Plasma, orientation='v',height = 500, width = 550)
        
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df6)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig6, use_container_width=True)

    if slt == "7. Mobile Brands with Highest Transaction Count":
        col1,col2 = st.columns([3.3,4],gap="medium")
        mycursor.execute("select Brands, sum(Transaction_Count) as Count from agg_user group by Brands order by Count ")
        data = mycursor.fetchall()
        df7 = pd.DataFrame(data,columns = ['Brands','Transaction_Count'],index = range(1,len(data)+1))

        fig7 = px.bar(df7, x="Transaction_Count", y='Brands', 
            title='Mobile Brands with Highest Transaction Count',
            color_discrete_sequence=px.colors.sequential.Cividis, orientation='h',height = 500, width = 550)
        
        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df7)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig7, use_container_width=True)
    
    if slt == "8. Top Transaction Types based on Transaction Amount":
        col1,col2 = st.columns([3.3,4],gap="medium")
        mycursor.execute("SELECT Transaction_type, sum(Transaction_amount) AS Amount FROM agg_tran GROUP BY Transaction_type ORDER BY Amount desc")
        data = mycursor.fetchall()
        df8 = pd.DataFrame(data, columns = ['Transaction_type','Transaction_amount'], index = range(1, len(data)+1))

        fig8 = px.pie(df8, values='Transaction_amount',
                names='Transaction_type',
                title='Top Transaction Types based on Transaction Amount',
                color_discrete_sequence=px.colors.sequential.RdBu, width = 400)                     
        fig8.update_traces(textposition='inside', textinfo='percent+label')

        with col1:
            st.write("")
            st.write("")
            st.write("")
            st.write(df8)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.plotly_chart(fig8, use_container_width= False)
if selected == "About":
    st.subheader(":red[About PhonePe]")
    st.markdown("India's top financial platform, PhonePe, has more than 300 million registered customers. Users of PhonePe can send and receive money, recharge mobile phones and DTH, pay for goods and services at merchant locations, purchase gold, and make investments.")
    
    st.subheader(":green[About Project:]")
    st.write("The website's insights and the report's findings were derived from two important sources: the whole transaction data of PhonePe and merchant and customer interviews. The report is freely downloadable from GitHub and the PhonePe Pulse website.")
    st.write("The outcome of this project is a complete and user-friendly solution for extracting, processing, and visualising data from the Phonepe pulse Github repository.")

    