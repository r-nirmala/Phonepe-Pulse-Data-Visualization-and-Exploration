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
        img = Image.open(r"C:\Users\rnirm\OneDrive\Desktop\image\download (2).png")
        size = (230,85)
        img1 =img.resize(size)
        st.image(img1)
        st.markdown("#### India's top financial platform, PhonePe, has more than 300 million registered customers.")
        st.write("")
        st.write("#### :orange[***Simple, Fast and Secure***]")
        st.write("##### :green[_One app_ for all things money]")
        st.write("##### :green[_Pay whenever you like_, wherever you like]")
        st.write("##### :green[Find all your favourite apps on _PhonePe Switch_]")
    with col2:
        st.video(r"C:\Users\rnirm\OneDrive\Desktop\image\phone vid.mp4")
    col3,col4 = st.columns([3.5,3],gap="medium")
    with col3:
        img = Image.open(r"C:\Users\rnirm\OneDrive\Desktop\image\1413796-ph.webp")
        size = (470,500)
        img1 = img.resize(size)
        st.image(img1)
    with col4:
        st.write("#### :rainbow[***Features***]")
        st.write("##### -->_:blue[Credit & Debit card]_ linking")
        st.write("##### -->_:red[Bank Balance]_ check")
        st.write("##### -->_:blue[Money Storage]_")
        st.write("##### -->_:red[PIN Authorization]_")
        st.write("")
        st.write("")
        st.write("")
        st.write("##### * Payments on PhonePe are :orange[***safe, reliable and fast***].")
        st.write("##### * One in three Indians are now using the PhonePe app to :blue[***send money***], :red[***recharge***], :violet[***pay bills***] and do so much more, in just a few simple clicks.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

#-----------------------------Data Exploration ---------------------

def Agg_tran_count():
    mycursor.execute(f"select State, sum(Transaction_count) as Count from agg_tran where Year = {Year} and Quarter = {Quarter} group by State order by Count desc")
    df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transaction_Count'])
    fig_1 = px.bar(df, y='Transaction_Count',
            x ='State',
            orientation = 'v',
            color='Transaction_Count',
            title='States based on Transaction Count',
            color_discrete_sequence=px.colors.sequential.Magenta, height = 750, width =700)
                    
    return st.plotly_chart(fig_1, use_container_width = True)

def Agg_tran_amount():
    mycursor.execute(f"select State, sum(Transaction_amount) as Total from agg_tran where Year = {Year} and Quarter = {Quarter} group by State order by Total desc")
    df1 = pd.DataFrame(mycursor.fetchall(),columns = ['State', 'Transaction_Amount'])
    fig_2 = px.bar(df1, y='Transaction_Amount',
            x ='State',
            orientation = 'v',
            color='Transaction_Amount',
            title='States based on Transaction Amount',
            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 750, width =700)
    return st.plotly_chart(fig_2, use_container_width = True)

def Payment_type_count():
    mycursor.execute(f"select State, Transaction_type, sum(Transaction_count) as Tot_tran from agg_tran where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State,Transaction_type order by Tot_tran desc")
    df2 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Transaction_type','Transaction_count'])
    fig_pie = px.pie(df2, title=f"{selected_state} - Transaction Count",
                        names ='Transaction_type', values ='Transaction_count', 
                        hole = 0.4,height = 600, width =650,
                        color_discrete_sequence = px.colors.sequential.RdBu)
    fig_pie.update_traces(textinfo = 'percent+label', textposition='inside')
    return st.plotly_chart(fig_pie, use_container_width = True)

def Payment_type_amount():
    mycursor.execute(f"select State, Transaction_type, sum(Transaction_amount) as Tot_amount from agg_tran where Year =  {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State,Transaction_type order by Tot_amount desc")
    df2 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Transaction_type','Transaction_amount'])
    fig_pie = px.pie(df2, title=f"{selected_state} - Transaction Amount",
                        names ='Transaction_type', values ='Transaction_amount', 
                        hole = 0.5,height = 600, width =650,
                        color_discrete_sequence = px.colors.sequential.RdBu)
    fig_pie.update_traces(textinfo = 'percent+label', textposition='inside')
    return st.plotly_chart(fig_pie, use_container_width = True)

def Agg_user():
    mycursor.execute(f"select State, Brands, sum(Transaction_Count) as Tot_count, avg(Percentage)*100 as Percentage from agg_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, Brands order by Tot_count desc")
    df3 = pd.DataFrame(mycursor.fetchall(), columns = ['State','Brands','User_Count','Avg_percentage'])
    fig_line_1 = px.line(df3,title= f"Mobile Brands based on Phonepe User Count for '{selected_state}'",  
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
            color_discrete_sequence=px.colors.sequential.Burg, height = 750, width =700)                   
    return st.plotly_chart(fig_1, use_container_width = True)

def Map_tran_amount():
    mycursor.execute(f"select State, sum(Transaction_Amount) as Total from map_tran where Year = {Year} and Quarter = {Quarter} group by State order by Total desc")
    df = pd.DataFrame(mycursor.fetchall(),columns = ['State', 'Transaction_Amount'])
    fig = px.bar(df, y='Transaction_Amount',
            x ='State',
            orientation = 'v',
            color='Transaction_Amount',
            title='States based on Transaction Amount',
            color_discrete_sequence=px.colors.sequential.Magenta_r, height = 750, width =700)
    return st.plotly_chart(fig, use_container_width = True)

def Map_tran_state_explore_c():
    mycursor.execute(f"select State, District, Year, Quarter, Transaction_Count, Transaction_Amount from map_tran where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' order by District")
    df_ec = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Total_Transactions','Total_amount'])
    fig_e1 = px.bar(df_ec,
            title=f"{selected_state} - Transaction count", x="District", y="Total_Transactions",
            orientation='v',color='Total_Transactions',height = 700, width =750,
            color_continuous_scale = px.colors.sequential.Agsunset_r)
    return st.plotly_chart(fig_e1, use_container_width=True)

def Map_tran_state_explore_a():
    mycursor.execute(f"select State, District, Year, Quarter, Transaction_Count, Transaction_Amount from map_tran where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' order by District")
    df_ea = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Total_Transactions','Total_amount'])
    fig_e2 = px.bar(df_ea,
            title=f"{selected_state} - Transaction amount", x="District", y="Total_amount", orientation='v',
        height = 700, width =750,color='Total_amount',color_continuous_scale = px.colors.sequential.Agsunset_r)
    return st.plotly_chart(fig_e2, use_container_width=True)

def Map_user():
    mycursor.execute(f"select State, sum(RegisteredUser) as Total_users, sum(AppOpens) as app_opens from map_user where Year = {Year} and Quarter = {Quarter} group by State order by State desc" )
    df = pd.DataFrame(mycursor.fetchall(), columns = ['State','Total_users','AppOpens'])
    fig_line = px.line(df,  
                 x = 'State', y= ['Total_users','AppOpens'], height = 700, width =700,
                 markers = True, color_discrete_sequence = px.colors.sequential.Rainbow_r)
    return st.plotly_chart(fig_line, use_container_width = True)

def Map_user_state_explore_c():
    mycursor.execute(f"select State, District, Year, Quarter, RegisteredUser, AppOpens from map_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' order by District")
    df_ec = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Phonepe_Users','AppOpens'])
    fig = px.bar(df_ec,
    title = f"{selected_state} - Total users", x="District", y="Phonepe_Users", orientation='v',
    height = 700, width =750,color='Phonepe_Users', color_continuous_scale = px.colors.sequential.Agsunset)
    return st.plotly_chart(fig, use_container_width=True)

def Map_user_state_explore_a():
    mycursor.execute(f"select State, District, Year, Quarter, RegisteredUser, AppOpens from map_user where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' order by District")
    df_ea = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                        'Phonepe_Users','AppOpens'])
    fig = px.bar(df_ea,
     title=f"{selected_state} - Total AppOpens", x="District", y="AppOpens", orientation='v',
     height = 700, width =750, color='AppOpens', color_continuous_scale = px.colors.sequential.Agsunset)
    return st.plotly_chart(fig, use_container_width=True)

def Top_tran_count():
    mycursor.execute(f"select State, sum(Transaction_count) as count from top_tran where Year = {Year} and Quarter = {Quarter} group by State order by count desc")
    df = pd.DataFrame(mycursor.fetchall(), columns = ['State','Transaction_count']) 
    fig = px.bar(df,
            title="States based on Transaction Count", x="State", y="Transaction_count", orientation='v',
            color='Transaction_count',height = 750, width =700,
           color_discrete_sequence = px.colors.sequential.BuGn)
    return st.plotly_chart(fig, use_container_width=True)

def Top_tran_amount():
    mycursor.execute(f"select State, sum(Transaction_amount) as amount from top_tran where Year = {Year} and Quarter = {Quarter} group by State order by amount desc")
    df = pd.DataFrame(mycursor.fetchall(), columns = ['State','Transaction_amount']) 
    fig = px.bar(df,
            title="States based on Transaction Amount", x="State", y="Transaction_amount", orientation='v',
            color='Transaction_amount',height = 750, width =700,
           color_discrete_sequence = px.colors.sequential.Blugrn_r)
    return st.plotly_chart(fig, use_container_width=True)

def  Top_user():
    mycursor.execute(f"select State, sum(RegisteredUsers) as users from top_user where Year = {Year} and Quarter = {Quarter} group by State order by users desc")
    df_u = pd.DataFrame(mycursor.fetchall(), columns = ['State','Registered_Users']) 
    fig = px.bar(df_u,
            title="States based on Registered Users", x="State", y="Registered_Users", orientation='v',
            color='Registered_Users',height = 750, width =700,
            color_discrete_sequence = px.colors.sequential.Magenta)
    return st.plotly_chart(fig, use_container_width=True)

          
if selected == "Data Exploration":
    with st.sidebar:
        Year = st.slider("#### :orange[Year]", min_value=2018, max_value=2023)
        Quarter = st.slider("#### :orange[Quarter]", min_value=1, max_value=4)     
            
    tab1, tab2, tab3 = st.tabs(['##### :violet[Aggregated Analysis]','##### :green[Map Analysis]','##### :rainbow[Top Analysis]'])
    with tab1:
        option = st.selectbox("###### :orange[Select the Analysis]", ("Transaction", "Users"))  
      
        if option == "Transaction":
            
            select = st.radio("Select the options",["States based on Transaction Count",
                        "States based on Transaction Amount", 
                        "Top Payment Type based on Transaction Count and Amount"],
                        label_visibility="hidden",horizontal=True)  
                
            if select == "States based on Transaction Count":
                Agg_tran_count()           
            if  select == "States based on Transaction Amount":
                Agg_tran_amount()
            if select == "Top Payment Type based on Transaction Count and Amount":
                selected_state = st.selectbox("###### :green[Select any State]",
                           ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                            'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                            'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                            'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                            'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                            'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                            'Uttarakhand', 'West Bengal'))
                col1,col2 = st.columns([3.5,3.5],gap="medium")
                with col1:
                    Payment_type_count()
                with col2:
                    Payment_type_amount()
                
        if option == "Users":   
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
        
            select_t2 = st.radio("Select the options",["States based on Transaction Count",
                        "States based on Transaction Amount", 
                        "District wise Data Exploration"],
                        label_visibility="hidden",horizontal=True)  
        
            if select_t2 == "States based on Transaction Count":
                Map_tran_count()
            if select_t2 ==  "States based on Transaction Amount":
                Map_tran_amount()
            if select_t2 == "District wise Data Exploration":
                st.write("##### :green[Explore data for selected states based on transaction count and amount from various years and quarters]")
                st.write("")
                selected_state = st.selectbox("###### :blue[Select any State to explore more]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
                  
                Map_tran_state_explore_c()     
                Map_tran_state_explore_a()
    
        if Type == "Users":
            
            select_u = st.radio("Select the options",["States based on Phonepe Users and App Opens",
                    "District wise Data Exploration"],label_visibility="hidden",horizontal=True)     

            if select_u == "States based on Phonepe Users and App Opens":
                Map_user()
            if select_u == "District wise Data Exploration":
                st.write("##### :red[Explore data for selected states based on registered users and app opens from various years and quarters]")
                st.write("")
                selected_state = st.selectbox("###### :green[Select any State to explore more]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))               
               
                Map_user_state_explore_c()
                Map_user_state_explore_a()

    with tab3:
        opt = st.selectbox("###### :red[Select the Analysis]", ("Transaction", "Users"))  

        if opt == "Transaction":
            
            select_t3 = st.radio("Select the options",["States based on Transaction Count",
                        "States based on Transaction Amount"],
                        label_visibility="hidden",horizontal=True)  
                
            if select_t3 == "States based on Transaction Count":
                Top_tran_count()
            if select_t3 == "States based on Transaction Amount":    
                Top_tran_amount()

        if opt == "Users":
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
                    color_continuous_scale=px.colors.sequential.Agsunset)
    fig_g1.update_layout(title='Statewise Transaction Amount',
                        title_x=0.25,
                        title_y=0.93,
                        height=500, 
                        margin={"r":5,"t":5,"l":5,"b":5},
                        title_font=dict(size=18))

    fig_g1.update_geos(fitbounds="locations", visible=False)
    return st.plotly_chart(fig_g1, use_container_width=False)

def geo_agg_user_users():
    #mycursor.execute(f"select State,Year,Quarter,Brands, sum(Transaction_Count) as counts from agg_user where Year = {Year} and Quarter = {Quarter} group by State,Year,Quarter,Brands order by counts desc")
    mycursor.execute(f'''SELECT a.State, a.Year, a.Quarter, a.Brands, a.counts
                FROM (
                    SELECT State, Year, Quarter, Brands, SUM(Transaction_Count) AS counts
                    FROM agg_user
                    WHERE Year = {Year} AND Quarter = {Quarter}
                    GROUP BY State, Year, Quarter, Brands
                ) AS a
                JOIN (
                    SELECT State, MAX(counts) AS max_counts
                    FROM (
                        SELECT State, Brands, SUM(Transaction_Count) AS counts
                        FROM agg_user
                        WHERE Year = {Year} AND Quarter = {Quarter}
                        GROUP BY State, Brands
                    ) AS subquery
                    GROUP BY State
                ) AS b
                ON a.State = b.State AND a.counts = b.max_counts
                ORDER BY a.counts DESC''')
    df_u = pd.DataFrame(mycursor.fetchall(), columns = ['State','Year','Quarter','Brands','counts'])
    df = pd.read_csv(r"C:\Users\rnirm\OneDrive\Documents\Guvi Data Science - MDE86\Guvi Projects\Project_2\Statesname.csv")
    df_u.counts = df_u.counts.astype(np.int64)
    df_u.State = df

    fig_gu= px.choropleth(df_u,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='counts', hover_data ='Brands',
                    color_continuous_scale=px.colors.sequential.RdBu)
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
                    color_continuous_scale=px.colors.sequential.Plasma_r)
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
                    color_continuous_scale=px.colors.sequential.Rainbow)
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
                    color_continuous_scale = px.colors.sequential.Plasma_r)
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
                    color_continuous_scale=px.colors.sequential.Viridis)
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
    st.write("### :rainbow[Geo-Visualisation of all Indian States]")
    tab1, tab2, tab3 = st.tabs(['##### :violet[Aggregated Analysis]','##### :green[Map Analysis]','##### :rainbow[Top Analysis]'])
    with st.sidebar:
                Year = st.slider("##### :green[Year]", min_value=2018, max_value=2023)
                Quarter = st.slider("##### :green[Quarter]", min_value=1, max_value=4)
    with tab1:
        Type = st.selectbox("###### :orange[Select the Analysis]", ("Transaction", "Users"))
        
        if Type == "Transaction": 
            opt = st.radio("###### :violet[Choose the option to visualize]",["***All State Transaction Count***","***All State Transaction Amount***"],horizontal=True)
            if opt =="***All State Transaction Count***":
                geo_agg_tran_count()
            elif opt == "***All State Transaction Amount***":
                geo_agg_tran_amount()          
        if Type == "Users":         
            st.write("##### :orange[All State Phonepe User Counts with Mobile Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry.. No Data to Display for this Quarter")
            elif Year == 2023 and Quarter in [1,2,3,4]:
                st.markdown("#### Sorry.. No Data to Display for this Quarter")  
            else:
                geo_agg_user_users()

    with tab2:
        Type = st.selectbox("###### :violet[Select the Analysis]", ("Transaction", "Users"))
       
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
                if Year == 2018 and Quarter in [1,2,3,4]:
                    st.write("#### Sorry..No AppOpen count present")
                elif Year ==2019 and Quarter == 1:
                    st.write("#### Sorry..No AppOpen count present")
                else:
                    geo_map_user_appopens()

    with tab3:
        Type = st.selectbox("###### :red[Select the Analysis]", ("Transaction", "Users"))
        
        if Type == "Transaction": 
            opt = st.radio("###### :blue[Choose the option to visualize]",["***All State Transaction Count***","***All State Transaction Amount***"],horizontal=True)
            if opt =="***All State Transaction Count***":
                geo_top_tran_count()
            elif opt == "***All State Transaction Amount***":
                geo_top_tran_amount()
        if Type == "Users":
           geo_top_user_users()



#--------------Basic Insights-------------
def que_1(table_name):
    connection = mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe")
    mycursor = connection.cursor()

    col1,col2 = st.columns([4,4],gap="large")  
    with col1:    
        mycursor.execute(f"select distinct State, sum(Transaction_count) as counts from {table_name} group by State order by counts desc limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title="Top 10 States Transaction Count",
                      orientation = 'v',x='State',y='Transaction_counts',
                      color_discrete_sequence=px.colors.sequential.Blugrn, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)
    with col2:
        mycursor.execute(f"select distinct State, sum(Transaction_count) as counts from {table_name} group by State order by counts limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title="Least 10 States Transaction Count",
                 orientation = 'v', x ='State', y ='Transaction_counts', 
                    color_discrete_sequence=px.colors.sequential.Blugrn, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)

    mycursor.execute(f"select distinct State, avg(Transaction_count) as average from {table_name} group by State order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title="Average Transaction Count", 
              orientation = 'h', x ='Transaction_counts', y ='State', 
            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
    
    col3,col4 = st.columns([4,4],gap="large")
    with col3:
        mycursor.execute(f"select distinct State, sum(Transaction_amount) as amount from {table_name}  group by State order by amount desc limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_amount'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title="Top 10 States Transaction Amount",
                orientation = 'v', x ='State', y ='Transaction_amount',  
             color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    with col4:
        mycursor.execute(f"select distinct State, sum(Transaction_amount) as amount from {table_name}  group by State order by amount limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_amount'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title="Least 10 States Transaction Amount",
                      orientation = 'v', x ='State', y ='Transaction_amount',   
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    
    mycursor.execute(f"select distinct State, avg(Transaction_amount) as average from {table_name}  group by State order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','Transaction_amount'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title="Average Transaction Amount", 
            orientation = 'h', x ='Transaction_amount', y ='State', 
        color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
        
def que_2(table_name):
    connection = mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe")
    mycursor = connection.cursor()
    
    selected_state = st.selectbox("###### :orange[Select any State]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
   
    col1,col2 = st.columns([4,4],gap="large")  
    with col1:    
        mycursor.execute(f"select distinct State,District, sum(Transaction_Count) as counts from {table_name} where State = '{selected_state}' group by State,District order by counts desc limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','District','Transaction_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title=f"Top 10 District Transaction Count of '{selected_state}'",
                      orientation = 'v',x='District',y='Transaction_counts',
                      color_discrete_sequence=px.colors.sequential.Magenta, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)
    with col2:
        mycursor.execute(f"select distinct State,District, sum(Transaction_Count) as counts from {table_name} where State = '{selected_state}' group by State,District order by counts limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','District','Transaction_counts'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title=f"Least 10 District Transaction Count of '{selected_state}'",
                 orientation = 'v', x ='District', y ='Transaction_counts', 
                    color_discrete_sequence=px.colors.sequential.Peach, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)

    mycursor.execute(f"select distinct State,District, avg(Transaction_Count) as average from {table_name} where State = '{selected_state}' group by State,District order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','District','Transaction_counts'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title=f"Average Transaction Counts of '{selected_state}'", 
              orientation = 'h', x ='Transaction_counts', y ='District', 
            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
    
    col3,col4 = st.columns([4,4],gap="large")
    with col3:
        mycursor.execute(f"select distinct State,District, sum(Transaction_Amount) as amount from {table_name} where State = '{selected_state}' group by State,District order by amount desc limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','District','Transaction_Amount'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title=f"Top 10 Districts Transaction Amount of '{selected_state}'",
                orientation = 'v', x ='District', y ='Transaction_Amount',  
             color_discrete_sequence=px.colors.sequential.Rainbow, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    with col4:
        mycursor.execute(f"select distinct State,District, sum(Transaction_Amount) as amount from {table_name} where State = '{selected_state}' group by State,District order by amount limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','District','Transaction_Amount'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title=f"Least 10 Districts Transaction Amount of '{selected_state}'",
                      orientation = 'v', x ='District', y ='Transaction_Amount',   
                    color_discrete_sequence=px.colors.sequential.Rainbow, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    
    mycursor.execute(f"select distinct State,District, avg(Transaction_Amount) as average from {table_name} where State = '{selected_state}' group by State,District order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','District','Transaction_Amount'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title=f"Average Transaction Amount of '{selected_state}'", 
            orientation = 'h', x ='Transaction_Amount', y ='District', 
        color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
        
def que_3(table_name):
    connection = mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe")
    mycursor = connection.cursor()

    col1,col2 = st.columns([4,4],gap="large")  
    with col1:    
        mycursor.execute(f"select distinct State, sum(Transaction_count) as counts from {table_name} group by State order by counts desc limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title="Top 10 States Transaction Count",
                      orientation = 'v',x='State',y='Transaction_counts',
                      color_discrete_sequence=px.colors.sequential.Agsunset, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)
    with col2:
        mycursor.execute(f"select distinct State, sum(Transaction_count) as counts from {table_name} group by State order by counts limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title="Least 10 States Transaction Count",
                 orientation = 'v', x ='State', y ='Transaction_counts', 
                    color_discrete_sequence=px.colors.sequential.Agsunset, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)

    mycursor.execute(f"select distinct State, avg(Transaction_count) as average from {table_name} group by State order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','Transaction_counts'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title="Average Transaction Count", 
              orientation = 'h', x ='Transaction_counts', y ='State', 
            color_discrete_sequence=px.colors.sequential.Agsunset_r, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
    
    col3,col4 = st.columns([4,4],gap="large")
    with col3:
        mycursor.execute(f"select distinct State, sum(Transaction_amount) as amount from {table_name}  group by State order by amount desc limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_amount'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title="Top 10 States Transaction Amount",
                orientation = 'v', x ='State', y ='Transaction_amount',  
             color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    with col4:
        mycursor.execute(f"select distinct State, sum(Transaction_amount) as amount from {table_name}  group by State order by amount limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','Transaction_amount'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title="Least 10 States Transaction Amount",
                      orientation = 'v', x ='State', y ='Transaction_amount',   
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    
    mycursor.execute(f"select distinct State, avg(Transaction_amount) as average from {table_name}  group by State order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','Transaction_amount'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title="Average Transaction Amount", 
            orientation = 'h', x ='Transaction_amount', y ='State', 
        color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
        
def que_4(table_name):
    selected_state = st.selectbox("###### :orange[Select any State]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))

    mycursor.execute(f"select State, Brands, sum(Transaction_Count) as counts from {table_name} where State = '{selected_state}' group by State,Brands order by counts desc limit 10")
    df = pd.DataFrame(mycursor.fetchall(), columns= ['State','Brands','User_counts'])
    
    fig = px.pie(df, title=f"Top Mobile Brands based on users of '{selected_state}'", 
                 names = "Brands", values = "User_counts", color = "Brands",
                 height = 500, width = 600, color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_traces(textinfo = "percent+label", textposition = "inside")
    st.plotly_chart(fig, use_container_width= False)

def que_5(table_name):
    connection = mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe")
    mycursor = connection.cursor()
    
    selected_state = st.selectbox("###### :orange[Select any State]",
                                ('Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh','Assam', 
                                'Bihar', 'Chandigarh', 'Chhattisgarh','Dadra and Nagar Haveli & Daman and Diu', 
                                'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                'Uttarakhand', 'West Bengal'))
   
    col1,col2 = st.columns([4,4],gap="large")  
    with col1:    
        mycursor.execute(f"select distinct State,District, sum(RegisteredUser) as users from {table_name} where State = '{selected_state}' group by State,District order by users desc limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','District','User_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title=f"Top 10 District Registered User Count of '{selected_state}'",
                      orientation = 'v',x='District',y='User_counts',
                      color_discrete_sequence=px.colors.sequential.Magenta_r, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)
    with col2:
        mycursor.execute(f"select distinct State,District, sum(RegisteredUser) as users from {table_name} where State = '{selected_state}' group by State,District order by users limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','District','User_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title=f"Least 10 District Registered User Count of '{selected_state}'",
                      orientation = 'v',x='District',y='User_counts',
                      color_discrete_sequence=px.colors.sequential.Magenta_r, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)

    mycursor.execute(f"select distinct State,District, avg(RegisteredUser) as average from {table_name} where State = '{selected_state}' group by State,District order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','District','User_counts'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title=f"Average Registered User Counts of '{selected_state}'", 
              orientation = 'h', x ='User_counts', y ='District', 
            color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
    
    col3,col4 = st.columns([4,4],gap="large")
    with col3:
        mycursor.execute(f"select distinct State,District, sum(AppOpens) as appopens from {table_name} where State = '{selected_state}' group by State,District order by appopens desc limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','District','App_opens'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title=f"Top 10 Districts App Open count of '{selected_state}'",
                orientation = 'v', x ='District', y ='App_opens',  
             color_discrete_sequence=px.colors.sequential.GnBu, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    with col4:
        mycursor.execute(f"select distinct State,District, sum(AppOpens) as appopens from {table_name} where State = '{selected_state}' group by State,District order by appopens  limit 10 ")
        data = mycursor.fetchall()
        df2 = pd.DataFrame(data, columns = ['State','District','App_opens'],index=range(1,len(data)+1))
        
        fig2 = px.bar(df2, title=f"Least 10 Districts App Open count of '{selected_state}'",
                orientation = 'v', x ='District', y ='App_opens',  
            color_discrete_sequence=px.colors.sequential.GnBu, height = 600, width =600)
        st.plotly_chart(fig2, use_container_width = True)
    
    mycursor.execute(f"select distinct State,District, avg(AppOpens) as average from {table_name} where State = '{selected_state}' group by State,District order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','District','App_opens'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title=f"Average App Open count of '{selected_state}'", 
            orientation = 'h', x ='App_opens', y ='District', 
        color_discrete_sequence=px.colors.sequential.Cividis_r, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
        

def que_6(table_name):
    connection = mysql.connector.connect(host="localhost",user="root",password="12345",database="Phonepe")
    mycursor = connection.cursor()
    
    col1,col2 = st.columns([4,4],gap="large")  
    with col1:    
        mycursor.execute(f"select distinct State, sum(RegisteredUsers) as users from {table_name} group by State order by users desc limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','User_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title=f"Top 10 States Registered User Count",
                      orientation = 'v',x='State',y='User_counts',
                      color_discrete_sequence=px.colors.sequential.Peach, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)
    with col2:
        mycursor.execute(f"select distinct State, sum(RegisteredUsers) as users from {table_name} group by State order by users limit 10 ")
        data = mycursor.fetchall()
        df1 = pd.DataFrame(data, columns = ['State','User_counts'],index=range(1,len(data)+1))   
        
        fig1 = px.bar(df1, title=f"Least 10 States Registered User Count",
                      orientation = 'v',x='State',y='User_counts',
                      color_discrete_sequence=px.colors.sequential.Rainbow, height = 600, width =600)
        st.plotly_chart(fig1, use_container_width = True)

    mycursor.execute(f"select distinct State, avg(RegisteredUsers) as average from {table_name} group by State order by average")
    data = mycursor.fetchall()
    df2 = pd.DataFrame(data, columns = ['State','User_counts'],index=range(1,len(data)+1))
    
    fig2 = px.bar(df2, title=f"Average Registered User Counts", 
              orientation = 'h', x ='User_counts', y ='State', 
            color_discrete_sequence=px.colors.sequential.Aggrnyl, height = 750, width =600)
    st.plotly_chart(fig2, use_container_width = True)
    
    
if selected ==  "Basic Insights":
    st.subheader(':violet[Basic Insights]')
    st.markdown("##### :green[These insights are derived by exploring Phonepe pulse data. It gives an overall understanding of the Phonepe data]")
    options = ["--select--",
            "1. Aggregated Transaction - Transaction Count and Amount",
            "2. Map Transaction - Transaction Count and Amount",
            "3. Top Transaction - Transaction Count and Amount",
            "4. Aggregated User - Mobile Brands",
            "5. Map User - Registered Users and AppOpens",
            "6. Top User - Registered Users"]
   
    slt = st.selectbox("###### :orange[Select any query]",options)
    
    if slt == "1. Aggregated Transaction - Transaction Count and Amount":
        que_1("agg_tran")
    if slt ==  "2. Map Transaction - Transaction Count and Amount":
        que_2("map_tran")     
    if slt == "3. Top Transaction - Transaction Count and Amount":
        que_3("top_tran")
    if slt == "4. Aggregated User - Mobile Brands":
        que_4("agg_user")
    if slt == "5. Map User - Registered Users and AppOpens":
        que_5("map_user")
    if slt == "6. Top User - Registered Users":
        que_6("top_user")
        
#-----------------------About-----------------------

if selected == "About":
    st.subheader(":red[About PhonePe]")
    st.markdown("###### :violet[***PhonePe***] is an Indian multinational digital payments and financial services company headquartered in :orange[***Bengaluru, Karnataka***], India. PhonePe was founded in December 2015, by :blue[Sameer Nigam], :red[Rahul Chari] and :green[Burzin Engineer]. It is owned by :green[Flipkart], a subsidiary of Walmart.")
    st.write("")
    st.write("")
    st.subheader(" :violet[About Phonepe Pulse]")
    st.write(" ###### India's first :blue[interactive website] with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than :orange[2000+ Crore transactions by consumers] on an interactive map of India.")
    st.write("")
    st.write("")
    st.subheader(":green[About Project:]")
    st.write("###### The website's insights and the report's findings were derived from two important sources: the whole transaction data of PhonePe, merchant and customer interviews. The report is freely downloadable from :orange[***GitHub***] and the :orange[***PhonePe Pulse website***].")
    st.write("###### The outcome of this project is a complete and user-friendly solution for :blue[extracting, processing, and visualising data] from the :red[***Phonepe pulse Github repository***].")
    st.subheader(" :rainbow[Thanks for Exploring! Visit Again!]")

    
