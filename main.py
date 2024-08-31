import streamlit as st

st.set_page_config(page_title='Shark Tank Analysis',page_icon="🦈", layout='wide')

import pandas as pd
import numpy as np
import plotly.express as px
import functions
from streamlit_extras.metric_cards import style_metric_cards
from PIL import Image
import os

shark_full_names = {
    'ashneer_deal': 'Ashneer Grover',
    'anupam_deal': 'Anupam Mittal',
    'aman_deal': 'Aman Gupta',
    'namita_deal': 'Namita Thapar',
    'vineeta_deal': 'Vineeta Singh',
    'peyush_deal': 'Peyush Bansal',
    'ghazal_deal': 'Ghazal Alagh'
}
shark_original = {
'Ashneer Grover': 'ashneer_deal',
'Anupam Mittal': 'anupam_deal',
'Aman Gupta': 'aman_deal',
'Namita Thapar': 'namita_deal',
'Vineeta Singh': 'vineeta_deal',
'Peyush Bansal': 'peyush_deal',
'Ghazal Alagh': 'ghazal_deal'
}

# Importing data
df = functions.get_data()

# Importing CSS
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

# Static page
st.title('Shark Tank Analysis')
with st.expander("VIEW SHARK TANK DATASET"):
    showData=st.multiselect('Filter: ',df.columns,default=['episode_number', 'pitch_number', 'brand_name', 'idea', 'deal','pitcher_ask_amount', 'ask_equity', 'ask_valuation', 'deal_amount','deal_equity', 'deal_valuation', 'total_sharks_invested','amount_per_shark', 'equity_per_shark', 'deal_type'])
    st.dataframe(df[showData],use_container_width=True)

total_deal = df[df['total_sharks_invested']>0]['pitch_number'].count()
per_deal = (df[df['total_sharks_invested']>0]['pitch_number'].count()/len(df['pitch_number'].unique())*100).round(2)
total_episodes = len(df['episode_number'].unique())
total_shark = 7

col1, col2, col3 , col4 = st.columns([1,1,1,1], gap='small')
with col1:
    st.info('Total Episodes',icon="🎬")
    st.metric(label="Total",value=f"{total_episodes}")
with col2:
    st.info('Number of Sharks',icon="🦈")
    st.metric(label="Sum",value=f"{total_shark}")
with col3:
    st.info('Number of Pitch',icon="🗣")
    st.metric(label="Sum",value=117)
with col4:
    st.info('Deals Made',icon="💹")
    st.metric(label="Total",value= total_deal , delta=f'{per_deal}%')

style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")

st.header("Select Analysis")
start = st.selectbox(label= '' , options = ['Shark Analysis','Overall Analysis'] , index=1)
st.markdown("######")

# Side bars
image_path = os.path.join("images", "logo.png")
image = Image.open(image_path).resize((225,225))
st.sidebar.image(image)
if start == 'Shark Analysis':
    shark = functions.selectAll(
        "Sharks", ['Ashneer Grover','Aman Gupta','Anupam Mittal','Namita Thapar','Vineeta Singh','Peyush Bansal','Ghazal Alagh'] , 1)
if start == 'Overall Analysis':
    episode = functions.selectAll(
        "Episodes", df["episode_number"].unique().tolist() , 2)
    type = functions.selectAll(
        "Deal Categories", df[df['episode_number'].isin(episode)]["deal_type"].unique().tolist() , 3)

# Main page Logics  
if start == 'Overall Analysis': 
    df_filtered_overall = df.query('episode_number==@episode & deal_type==@type')
    if df_filtered_overall.empty:
        st.warning("Provide Data for Filtering")
        st.stop()
    shark_deals_total = df_filtered_overall[['ashneer_deal', 'anupam_deal', 'aman_deal', 'namita_deal', 'vineeta_deal', 'peyush_deal', 'ghazal_deal']].sum().reset_index()
    shark_deals_total.columns = ['Shark', 'Total Deals']
    shark_deals_total['Shark'] = shark_deals_total['Shark'].replace(shark_full_names)
    multi_shark_deals = df_filtered_overall[df_filtered_overall['total_sharks_invested'] > 1][['ashneer_deal', 'anupam_deal', 'aman_deal', 'namita_deal', 'vineeta_deal', 'peyush_deal', 'ghazal_deal']].sum().reset_index()
    multi_shark_deals.columns = ["Shark's Name", 'Number of Multi-Shark Deals']
    multi_shark_deals['Shark\'s Name'] = multi_shark_deals['Shark\'s Name'].replace(shark_full_names)
    df_deals = df_filtered_overall[df_filtered_overall['total_sharks_invested'] > 0].groupby('episode_number')['total_sharks_invested'].count().reset_index().rename(columns={'total_sharks_invested': 'number_of_deals'})
    df_pitch = df_filtered_overall.groupby('episode_number')[['pitch_number']].count().reset_index().rename(columns={'pitch_number': 'number_of_pitches'})
    df_pitch_deals = pd.merge(df_deals, df_pitch, on='episode_number')
    df_pitch_deals['pitch_conversion_rate'] = (df_pitch_deals['number_of_deals']/df_pitch_deals['number_of_pitches']*100).round(2)
    df_long = df_pitch_deals.iloc[:,:3].melt(id_vars='episode_number', 
                    value_vars=['number_of_pitches', 'number_of_deals'],
                    var_name='Type', 
                    value_name='Count')
    df_filtered_overall['valuation_range'] = pd.cut(df_filtered_overall['ask_valuation'], bins=[0, 500, 1000, 2500, 5000, 10000], 
                               labels=['0-50Lakhs', '50Lakhs-1Cr', '1Cr-2.5Cr', '2.5Cr-5Cr', '5Cr-10Cr'])
    deals_by_valuation_range = df_filtered_overall.groupby('valuation_range')['deal'].sum().reset_index()
    shark_deals = df_filtered_overall[['ashneer_deal', 'anupam_deal', 'aman_deal', 'namita_deal', 'vineeta_deal', 'peyush_deal', 'ghazal_deal']]
    # Calculate the correlation matrix to show the frequency of partnerships
    partnership_matrix = shark_deals.corr().round(2).rename(index=shark_full_names,columns=shark_full_names)
    # Filter the dataframe to include only the selected numerical columns
    numerical_data = df_filtered_overall[['pitcher_ask_amount', 'ask_equity', 'ask_valuation', 
                     'deal_amount', 'deal_equity', 'deal_valuation', 
                     'total_sharks_invested', 'amount_per_shark', 'equity_per_shark']]
    # Calculate the correlation matrix
    renaming = {'pitcher_ask_amount':'Pitcher Ask Amount', 'ask_equity':'Ask Equity', 'ask_valuation':'Ask Valuation', 'deal_amount':'Deal Amount', 'deal_equity':'Deal Equity', 'deal_valuation':'Deal Valuation', 'total_sharks_invested':'Total Sharks Invested', 'amount_per_shark':'Amount Per Shark', 'equity_per_shark':'Equity Per Shark'}
    correlation_matrix = numerical_data.corr().rename(columns=renaming , index = renaming)
    # Round the correlation matrix values to 2 decimal places
    rounded_correlation_matrix = np.round(correlation_matrix, 2)

if start == 'Shark Analysis':
    shark_deals = df[['ashneer_deal', 'anupam_deal', 'aman_deal', 'namita_deal', 'vineeta_deal', 'peyush_deal', 'ghazal_deal']].sum().sort_values(ascending=False).reset_index()
    shark_deals.columns = ['Shark', 'Number of Deals']
    shark_deals['Shark'] = shark_deals['Shark'].replace(shark_full_names)
    df_filtered_shark = shark_deals.query("Shark==@shark")
    df_filtered_shark['Shark'] = df_filtered_shark['Shark'].replace(shark_original)
    if df_filtered_shark.empty:
        st.warning("Provide Data for Filtering")
        st.stop()
    

# Main page displays
if 'Overall Analysis' in start:
    Total_ask_amount= int(df_filtered_overall["pitcher_ask_amount"].sum())
    pitcher_ask_amount_max= int(df_filtered_overall["pitcher_ask_amount"].max())
    pitcher_ask_amount_min= df_filtered_overall["pitcher_ask_amount"].min()
    Total_deal_amount= int(df_filtered_overall["deal_amount"].sum())
    deal_amount_min= int(df_filtered_overall[df_filtered_overall['deal'] == 1]["deal_amount"].min()*100000)
    deal_amount_max= int(df_filtered_overall[df_filtered_overall['deal'] == 1]["deal_amount"].max())
    Total_ask_equity= df_filtered_overall["ask_equity"].sum()
    pitcher_ask_equity_max= df_filtered_overall["ask_equity"].max()
    pitcher_ask_equity_min= df_filtered_overall["ask_equity"].min()
    Total_deal_equity= df_filtered_overall["deal_equity"].sum()
    deal_equity_min= df_filtered_overall[df_filtered_overall['deal'] == 1]["deal_equity"].min()
    deal_equity_max= df_filtered_overall[df_filtered_overall['deal'] == 1]["deal_equity"].max()
    col1, col2, col3 , col4 = st.columns([1,1,1,1], gap='small')
    with col1:
        st.info("Ask Amount(Lakhs)",icon="💲")
        st.metric(label="Sum",value=f"{Total_ask_amount}")
        st.metric(label="Max",value=f"{pitcher_ask_amount_max}")
        st.metric(label="Min",value=f"{pitcher_ask_amount_min}")
    with col2:
        st.info("Deal Amount(Lakhs)",icon="💲")
        st.metric(label="Sum",value=f"{Total_deal_amount}")
        st.metric(label="Max",value=f"{deal_amount_max}")
        st.metric(label="Min",value=f"{deal_amount_min} Rupees")
    with col3:
        st.info("Ask Equity(Percentage)",icon="🏷️")
        st.metric(label="Sum",value=f"{Total_ask_equity}")
        st.metric(label="Max",value=f"{pitcher_ask_equity_max}")
        st.metric(label="Min",value=f"{pitcher_ask_equity_min}")
    with col4:
        st.info("Deal Equity(Percentage)",icon="🏷️")
        st.metric(label="Sum",value=f"{Total_deal_equity}")
        st.metric(label="Max",value=f"{deal_equity_max}")
        st.metric(label="Min",value=f"{deal_equity_min}")
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
    st.divider()
    # Create the bar chart using Plotly Express
    st.title("Deal Analysis")
    st.subheader('Top N Largest Deals')
    r = len(df_filtered_overall[df_filtered_overall['deal_amount']>0]['brand_name'])
    if r <= 10:
        n = st.select_slider(label='Select N',options=range(1,r+1),value= r)
    else:
        n = st.select_slider(label='Select N',options=range(1,r+1),value= 10)
    top_10_deals = df_filtered_overall.nlargest(n, 'deal_amount')[['brand_name', 'deal_amount']]
    fig = px.bar(
        top_10_deals, 
        x='brand_name', 
        y='deal_amount', 
        labels={'brand_name': 'Brand Name', 'deal_amount': 'Deal Amount (in Lakhs)'},
        color='deal_amount',  # Optional: to apply a color scale similar to 'palette'
        color_continuous_scale='RdBu'  # Similar to 'coolwarm'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        width=1200,  # Adjust width if needed
        height=500  # Adjust height if needed
    )
    st.plotly_chart(fig)
    # Create the pie chart using Plotly Express
    st.subheader('Deal Amount Distribution')
    col1,col2 = st.columns([1.2,1],gap='small')
    with col1:
        fig = px.pie(
            shark_deals_total, 
            names='Shark', 
            values='Total Deals', 
            title='Share of Each Shark in Total Deals', # Similar to 'bright' palette
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        # Update the layout to start the pie chart at a specific angle
        fig.update_traces(rotation=140, textinfo='percent+label')
        fig.update_layout(
        width=800,  # Increase the width of the pie chart
        height=450,  # Increase the height of the pie chart
        )
        st.plotly_chart(fig)
    with col2:
        # Create the bar plot using Plotly Express
        fig = px.bar(shark_deals_total, x='Shark', y='Total Deals', title='Total Deals per Shark', color_discrete_sequence=px.colors.sequential.Viridis)
        fig.update_layout(
        width=800,  # Increase the width of the pie chart
        height=450,  # Increase the height of the pie chart
        )
        st.plotly_chart(fig)
    
    # Create the bar plot using Plotly Express
    st.subheader('Number of Deals by Valuation Range')
    fig = px.bar(deals_by_valuation_range, 
                x='valuation_range', 
                y='deal', 
                title='', 
                labels={'valuation_range': 'Valuation Range', 'deal': 'Number of Deals'},
                color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig)
    st.subheader("Deal-Related Numerical's Correlations")
    # Generate the heatmap using Plotly Express with rounded text annotations
    fig = px.imshow(rounded_correlation_matrix,
                    labels=dict(x="Columns", y="Columns", color="Correlation"),
                    x=rounded_correlation_matrix.columns,
                    y=rounded_correlation_matrix.index,
                    color_continuous_scale='Viridis',  # Using the 'viridis' color scale
                    aspect='auto',
                    text_auto=True)  # Automatically add rounded text annotations

    # Update the layout to include the title
    fig.update_layout(title='',
                    xaxis_title='Numerical Columns',
                    yaxis_title='Numerical Columns',
                    height=550,
                    width=1000)
    st.plotly_chart(fig)
    st.divider()
    st.title('Episode Analysis')
    st.subheader("Number of Pitches and Deals per Episode")
    fig = px.line(df_long, x='episode_number', y='Count', color='Type',
                labels={'episode_number': 'Episode Number', 'Count': 'Quantity'},
                title='Number of Pitches and Deals per Episode',
                markers='o'
                )
    fig.update_yaxes(range=[-2,10])
    fig.update_xaxes(range=[0.5,36])
    st.plotly_chart(fig)
    st.subheader("Total Investment by Episode")
    total_investment_episode = df_filtered_overall.groupby('episode_number')['deal_amount'].sum().reset_index()
    # Create the bar plot using Plotly Express
    fig = px.bar(total_investment_episode, 
                x='episode_number', 
                y='deal_amount', 
                title='', 
                labels={'episode_number': 'Episode Number', 'deal_amount': 'Total Investment'})
    st.plotly_chart(fig)

    st.divider()

    st.title('Shark Involvment Analysis')
    st.subheader("Sharks Involvement in Multi-Shark Deals")
    fig = px.bar(
    multi_shark_deals, 
    x="Shark's Name", 
    y='Number of Multi-Shark Deals', 
    title='',
    labels={"Shark's Name": "Shark's Name", 'Number of Multi-Shark Deals': 'Number of Multi-Shark Deals'},
    color="Shark's Name",  # Optional: to color bars by shark
    color_continuous_scale='RdBu'  # Use the 'Set1' palette
    )

    # Update the layout to match the Matplotlib figure size
    fig.update_layout(
        width=1000,  # Increase the width to match figsize
        height=600   # Increase the height to match figsize
    )
    st.plotly_chart(fig)
    # Generate the heatmap using Plotly Express
    st.subheader('Shark Partnerships in Deals')
    fig = px.imshow(partnership_matrix, 
                    labels=dict(x="Shark 1", y="Shark 2", color="Partnership Frequency"),
                    x=partnership_matrix.columns,
                    y=partnership_matrix.index,
                    color_continuous_scale='RdBu',
                    aspect='auto',
                    text_auto=True)

    fig.update_layout(title='', 
                    xaxis_title='Shark 1', 
                    yaxis_title='Shark 2')
    st.plotly_chart(fig)
    st.divider()

if 'Shark Analysis' in start:
    l = df_filtered_shark['Shark'].values
    # Display the image in Streamlit
    for i in l:
        functions.analyze_shark_investments(i)
        st.divider()






