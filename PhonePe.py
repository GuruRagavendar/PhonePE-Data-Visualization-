import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import plotly.graph_objects as go

# Creating the StreamLit Page Configuration  
st.set_page_config(
    page_title="PhonePe Data Visualization",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded", )

# Creating the Sidebar
with st.sidebar:
    selected = option_menu("Main Menu", ["Home","Geo Visualisation","Charts"], 
                icons=['house','globe-central-south-asia','bar-chart-line'], menu_icon="bank", default_index=0,
                    styles={"nav-link-selected": {"background-color": "purple"} })
    
# Creating the Home menu         
if selected == "Home":
    st.title(":violet[Phonepe] Pulse Data Visualization and Exploration 📊 ")
    st.subheader('',divider='violet')
    st.write("""**The result of this project will be a comprehensive and user-friendly solution for extracting, transforming, and visualizing data from the Phonepe pulse Github repository.**""")
    st.subheader(":blue[Skills take away From This Project]")
    st.text("> Data extraction and processing")
    st.text("> Database management")
    st.text("> Visualization and dashboard creation")
    st.text("> Geo visualization")
    st.text("> Dynamic updation")
    st.text("> Project development and deployment")
    st.subheader('',divider='violet')

# Creating the Geo Visualisation Charts
elif selected == 'Geo Visualisation':
    st.title("Transactions and Users by State in India Map 🗺️")
    option = st.selectbox('Select the Details of the Map', ('Transactions', 'Users'))

    # Indian Map Chart for User details
    if option == 'Users':
        engine = create_engine('mysql+mysqlconnector://root:*****@localhost/phonepe')
        query = 'SELECT State, Sum(Count) as "Count of Users" FROM map_users WHERE Year = 2023 and Quater = 4 GROUP BY State ORDER BY "Count of Users" DESC'
        df = pd.read_sql(query,engine)

        #Ploting the Chart using Plotly library
        fig = px.choropleth(
        df,
        locations='State',
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        color='Count of Users',   
        color_continuous_scale='Reds',  
        title='Users By State in India' ) 

        fig.update_layout(
            geo=dict(
            showcoastlines=False,  
            projection_type='conic conformal',  
            lonaxis=dict(range=[68, 98]),   
            lataxis=dict(range=[6, 38]) ),       
            height=650,   
            width=700,   
            hovermode='closest',   
            coloraxis_colorbar=dict(title='Count') ) 
        st.plotly_chart(fig)

    #Indain Map Chart for Transaction Details
    elif option == 'Transactions':
        engine = create_engine('mysql+mysqlconnector://root:*****@localhost/phonepe')
        query = 'select State, sum(Transaction_count) as Transactions from map_transaction WHERE Year = 2023 and Quater = 4 group by state order by Transactions desc'
        df = pd.read_sql(query,engine)
        
        fig = px.choropleth(
        df,
        locations='State',
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM', 
        color='Transactions',   
        color_continuous_scale='Reds',   
        title='Transactions by State in India' )  

        fig.update_layout(
            geo=dict(
            showcoastlines=False,   
            projection_type='conic conformal',   
            lonaxis=dict(range=[68, 98]),   
            lataxis=dict(range=[6, 38]) ),  
            height=650,   
            width=700,   
            hovermode='closest',   
            coloraxis_colorbar=dict(title='Transactions') )

        st.plotly_chart(fig)
    else:
        st.empty()

#Creating the Charts
elif selected == 'Charts':
    t1,t2,t3,t4,t5,t6 = st.tabs(["📊 Bar Chart", "📈 Line Chart",'📊 Group Bar Chart','📉 Scatter Plot Chart','🍩 Donut Chart','📶 Histogram'])
    
    #Bar Chart
    with t1:

        #Function to Retreive the details from MY SQL with State and year as arguments        
        def state_year(s,y):
            engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
            query = f'SELECT state,Year, Quater,sum(Transacion_count) as Total_Transaction ,round(avg(Transacion_amount)) as Average_Amount FROM agg_transaction where state = "{s}" and Year = {y} group by Quater'
            sqdf = pd.read_sql(query,engine)
            quarter_mapping = {1: 'Q1', 2: 'Q2', 3: 'Q3', 4: 'Q4'}
            sqdf['Quater'] = sqdf['Quater'].map(quarter_mapping)
            return sqdf
        engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
        query = 'Select state, Year from agg_transaction'
        Tempdf = pd.read_sql(query,engine)
        st.header("**:blue[State-Wise Quarterly Analysis of Total Transactions]**")

        #Creating the Select Box for State and Year
        option1 = st.selectbox('Select the State', Tempdf['state'].unique(),index=None, placeholder="State",key='t1_state')
        option2 = st.selectbox('Select the Year', Tempdf['Year'].unique(),index=None, placeholder="Year",key='t1_year')
        if option1 and option2:            
            df = state_year(option1,option2)

            #Ploting the Bar Chart
            fig = px.bar(df, x="Quater", y="Total_Transaction", hover_data='Average_Amount', color="Total_Transaction",text = 'Total_Transaction',
             labels={'Quater':'Quarter','Average_Amount':'Average Transaction Amount','Total_Transaction':'Total Transactions'}
             )
            fig.update_layout( title=f"{option1}'s Transaction detatails in the Year - {option2}",width=900)
           
            st.plotly_chart(fig)
        else:
            st.empty()

    with t2:
        def brand(b):
            engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
            query = f'select state,Year, sum(User_count) as Total_Users from agg_users where brand = "{b}" group by state,Year'
            sqdf = pd.read_sql(query,engine)
            year_mapping = {2018: '2018', 2019: '2019', 2020: '2020', 2021: '2021',2022: '2022'}
            sqdf['Year'] = sqdf['Year'].map(year_mapping)
            return sqdf
        engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
        query = 'Select brand from agg_users'
        Tempdf = pd.read_sql(query,engine)
        st.header("**:blue[Yearly analysis of Total users for each Brand]**")
        option1 = st.selectbox('Select the brand', Tempdf['brand'].unique(),index=None, placeholder="Brand Name",key='t2_brand')

        if option1 :            
            df = brand(option1)
            fig = px.line(df, x='Year', y='Total_Users', color='state', markers=True)
            fig.update_layout(
                    title=f"{option1}'s User Count",
                    xaxis_title="Year",
                    yaxis_title="Total Users",
                    width=900 )
            st.plotly_chart(fig)
        else:
            st.empty()
    with t3:
        def state_year(s,y):
            engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
            query = f'SELECT district, SUM(Count) AS Transactions, SUM(amount) AS Amount FROM top_transaction_district WHERE state = "{s}" AND year = {y} GROUP BY district ORDER BY SUM(amount) desc limit  5'
            sqdf = pd.read_sql(query,engine)
            return sqdf
        engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
        query = 'Select state, Year from top_transaction_district'
        Tempdf = pd.read_sql(query,engine)
        st.header("**:blue[Top 5 Districts with Highest Amounts]**")
        option1 = st.selectbox('Select the State', Tempdf['state'].unique(),index=None, placeholder="State",key='t3_state')
        option2 = st.selectbox('Select the Year', Tempdf['Year'].unique(),index=None, placeholder="Year",key='t3_year')

        if option1 and option2:            
            df = state_year(option1,option2)
            fig = go.Figure()

            # Add left Y-axis
            fig.add_trace(go.Bar(
                x=df['district'],
                y=df['Transactions'],
                name='Transactions',
                marker_color='skyblue',
                offsetgroup=1 ))  # Use offsetgroup to place bars side by side
            
            # Add right Y-axis
            fig.add_trace(go.Bar(
                x=df['district'],
                y=df['Amount'],
                name='Amount',
                marker_color='mediumpurple',
                offsetgroup=2,  # Use offsetgroup to place bars side by side
                yaxis='y2' ))
            
            # Update layout to include two Y-axes
            fig.update_layout(
                title=f'Transactions and Amount for the Top 5 districts in {option1} in the Year - {option2}',
                yaxis=dict(title='Transactions', side='left', showgrid=False),
                yaxis2=dict(title='Amount', overlaying='y', side='right', showgrid=False),
                xaxis=dict(title='District'),
                barmode='group',
                bargap=0.1,  # Adjust the bargap as needed
                legend=dict(x=0.75, y=1.0, traceorder='normal', orientation='v'),
                width=900 )
            
            st.plotly_chart(fig)
        else:
            st.empty()
    
    with t4:
        def state_quarter(s,q):
            engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
            query = f'select District, Year, sum(Transaction_count)  as Count, sum(Amount) as Total_Amount from map_transaction  where state = "{s}" and quater = {q} group by District,Year'
            sqdf = pd.read_sql(query,engine)
            return sqdf
        engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
        query = 'Select state, quater from map_transaction'
        Tempdf = pd.read_sql(query,engine)
        st.header("**:blue[Transaction Analysis: Yearly Trends by District in Selected State & Quarter]**")
        option1 = st.selectbox('Select the State', Tempdf['state'].unique(),index=None, placeholder="State",key='t4_state')
        option2 = st.selectbox('Select the Quarter', Tempdf['quater'].unique(),index=None, placeholder="Quarter",key='t4_quarter')

        if option1 and option2:            
            df = state_quarter(option1,option2)
            fig = px.scatter(df, x="Count", y="Year", color="District", size='Total_Amount',
                 hover_name="District", labels={"Count": "Transaction Count", "Total_Amount": "Total Amount"},
                 title=f"Transaction Count and Total Amount by Year and District in {option1} (Quarter {option2})"
                 )

            fig.update_layout(xaxis_title="Transaction Count", yaxis_title="Year",
                  xaxis_rangeslider_visible=True, #Creating the Slider viewer
                  width = 900, height = 600
                )
           
            st.plotly_chart(fig)
        else:
            st.empty()

    with t5:
        def state_year(s,y):
            engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
            query = f'select Brand, sum(User_count) as total_users, round((sum(User_percentage) / 4),4) * 100 as Percentage from agg_users where state = "{s}" and year = {y} group by brand'
            sqdf = pd.read_sql(query,engine)
            return sqdf
        engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
        query = 'Select state, Year from agg_users'
        Tempdf = pd.read_sql(query,engine)
        st.header("**:blue[User Percentage Distribution Across Brands by State and Year]**")
        option1 = st.selectbox('Select the State', Tempdf['state'].unique(),index=None, placeholder="State",key='t5_state')
        option2 = st.selectbox('Select the Year', Tempdf['Year'].unique(),index=None, placeholder="Year",key='t5_year')

        if option1 and option2:            
            df = state_year(option1,option2)
            fig = px.pie(df, values='Percentage', names='Brand', title=f'Percentage of Users w.r.t Brand in {option1} for the Year : {option2}',
                        hover_data=['total_users'], labels={'total_users':'Total Users'}, hole=0.3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(width=700, height=700)

            st.plotly_chart(fig)
        else:
            st.empty()
    
    with t6:
        def brand(s):
            engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
            query = f'''with sq as (select Pincode,Year, quater,count, row_number() over(partition by Year order by Count desc) as row_num from top_user_pincode where state = "{s}")
                        select Pincode,Year, quater,count from sq where row_num < 20;'''
            sqdf = pd.read_sql(query,engine)
            sqdf['Pincode'] = sqdf['Pincode'].astype(str)
            return sqdf
        engine = create_engine('mysql+mysqlconnector://root:*******@localhost/phonepe')
        query = 'Select state from top_user_pincode'
        Tempdf = pd.read_sql(query,engine)
        st.header("**:blue[Average User Distribution by Pincode and Year for Selected State]**")
        option1 = st.selectbox('Select the State', Tempdf['state'].unique(),index=None, placeholder="State",key='t6_state')

        if option1 :            
            df = brand(option1)
            custom_color_sequence = ['#e6e6fa', '#dda0dd', '#ba55d3', '#9932cc', '#9467bd', '#8b008b']

            fig = px.histogram(df, x="Pincode", y="count", color='Year', histfunc='avg', labels={'count': 'User Count'}, color_discrete_sequence=custom_color_sequence)
            fig.update_xaxes(type='category')
            fig.update_layout(
                    title=f"Histogram of Average User Counts by Pincode and Year in {option1}",
                    xaxis_title="Pincode",
                    yaxis_title="Average User Count")
                    
                
            st.plotly_chart(fig)
        else:
            st.empty()
    




    
