import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from PIL import Image
import os

def categorize_pitch(idea):
    idea_lower = idea.lower()
    if any(keyword in idea_lower for keyword in ['food', 'beverage', 'drink', 'restaurant', 'delicacies', 'pizza', 'vegetables', 'fruits', 'chips', 'momos', 'cocktails', 'pickle', 'lemonade', 'protein', 'flavors', 'eggs', 'ice', 'sweets', 'bacon']):
        return 'Food & Beverage'
    elif any(keyword in idea_lower for keyword in ['tech', 'software', 'app', 'platform', 'e-commerce', 'technology', 'digital', 'finder']):
        return 'Technology'
    elif any(keyword in idea_lower for keyword in ['medical', 'biotech', 'innovation', 'invention', 'science', 'disposable', 'lpg', 'rod', 'automatic', 'enhancer', 'building', 'pollution', 'machine', 'gadgets', 'vr', 'ar']):
        return 'Scientific Innovation'
    elif any(keyword in idea_lower for keyword in ['fashion', 'product', 'consumer', 'goods', 'shoes', 'items', 'oils', 'perfumes', 'toys', 'clothing', 'glass', 'sneaker', 'device', 'wear', 'underwear', 'bags', 'gifts', 'materials', 'handmade', 'handicrafts', 'shaper', 'sleeves', 'sportswear', 'shirt', 'jeans', 'pants' ]):
        return 'Consumer Goods'
    elif any(keyword in idea_lower for keyword in ['service', 'consulting', 'education', 'study', 'course', 'planning', 'book', 'teaching', 'solutions']):
        return 'Services'
    elif any(keyword in idea_lower for keyword in ['sustainability', 'eco', 'environmental', 'flowers']):
        return 'Environmental & Sustainability'
    elif any(keyword in idea_lower for keyword in ['health', 'wellness', 'fitness', 'mental', 'hygiene', 'treatment', 'ppe', 'hair']):
        return 'Health & Wellness'
    elif any(keyword in idea_lower for keyword in ['social', 'community', 'impact']):
        return 'Social Impact'
    elif any(keyword in idea_lower for keyword in ['transport', 'vehicle', 'car', 'bike', 'mobility', 'cab', 'motorcycle', 'helmets']):
        return 'Transport'
    else:
        return 'Others'

@st.cache_data
def get_data():
    df = pd.read_csv('Shark Tank India Dataset.csv')
    df['deal_type'] = df['idea'].apply(categorize_pitch)
    df.loc[19,'deal'] = 0
    df.loc[18,'deal'] = 1
    return df

df = get_data()

def selectAll(title , options_list , key):
    st.markdown(
    """
    <style>
    .stMultiSelect label {
        margin-bottom: -28px;  /* Adjust this value as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.sidebar.subheader(f'Select {title}')
    selected = st.sidebar.multiselect('', options_list)
    select_all = st.sidebar.checkbox(f"Select All {title}", value = True, key = key)
    if select_all:
        selected_options = options_list
    else:
        selected_options = selected
    return selected_options

def analyze_shark_investments(shark_name):
    shark_full_names = {
        'ashneer_deal': 'Ashneer Grover',
        'anupam_deal': 'Anupam Mittal',
        'aman_deal': 'Aman Gupta',
        'namita_deal': 'Namita Thapar',
        'vineeta_deal': 'Vineeta Singh',
        'peyush_deal': 'Peyush Bansal',
        'ghazal_deal': 'Ghazal Alagh'
    }
    dict_img ={
        'ashneer_deal': 'Ashneer.png',
        'anupam_deal': 'anupam.jpg',
        'aman_deal': 'Aman.jpg',
        'namita_deal': 'Namita.png',
        'vineeta_deal': 'Vinita.png',
        'peyush_deal': 'peyush.png',
        'ghazal_deal': 'Ghazal.png'
    }
    sharks_info = [
    {
        "Name": "Ashneer Grover",
        "Role": "Co-founder and Former MD of BharatPe",
        "Industry": "Fintech",
        "Style": "Focused on startups with strong unit economics and scalability."
    },
    {
        "Name": "Anupam Mittal",
        "Role": "Founder and CEO of Shaadi.com",
        "Industry": "Digital Platforms",
        "Style": "Invested in tech-enabled businesses and scalable platforms."
    },
    {
        "Name": "Aman Gupta",
        "Role": "Co-founder and CMO of boAt",
        "Industry": "Consumer Electronics",
        "Style": "Preferred consumer-facing brands, especially in lifestyle and electronics."
    },
    {
        "Name": "Namita Thapar",
        "Role": "Executive Director of Emcure Pharmaceuticals",
        "Industry": "Pharmaceuticals",
        "Style": "Interested in healthcare startups with social impact."
    },
    {
        "Name": "Vineeta Singh",
        "Role": "Co-founder and CEO of SUGAR Cosmetics",
        "Industry": "Beauty and Cosmetics",
        "Style": "Focused on strong brand identity and mass appeal in consumer products."
    },
    {
        "Name": "Peyush Bansal",
        "Role": "Co-founder and CEO of Lenskart",
        "Industry": "E-commerce, Eyewear",
        "Style": "Invested in tech-driven businesses disrupting retail."
    },
    {
        "Name": "Ghazal Alagh",
        "Role": "Co-founder of Mamaearth",
        "Industry": "Beauty and Personal Care",
        "Style": "Focused on sustainable, health-conscious brands."
    }
    ]
    # Filter rows where the given shark was involved in the deal
    shark_deals = df[df[shark_name] == 1]
    # 3. Brand names in which the shark invested and the total investment
    combined_data = shark_deals.groupby('brand_name').agg({
        'equity_per_shark': 'sum',
        'amount_per_shark': 'sum'
    }).reset_index()
    
    combined_data.rename(columns={
        'brand_name': 'Startup Name',
        'equity_per_shark': 'Investment Equity(%)',
        'amount_per_shark': 'Investment Amount(in Lakhs)'
    }, inplace=True)

    investment_by_domain = shark_deals.groupby('deal_type')['deal_amount'].sum().reset_index()
    col1,col2 = st.columns([1,2],gap='small')
    with col1:
        image_path = os.path.join("images", dict_img[shark_name])
        image = Image.open(image_path).resize((225,225))
        st.image(image, caption=shark_full_names[shark_name])
    with col2:
        st.write('\n'*5)
        for i in sharks_info:
            if i['Name'] == shark_full_names[shark_name]:
                st.write(f"**Name:** {i['Name']}")
                st.write(f"**Role:** {i['Role']}")
                st.write(f"**Industry:** {i['Industry']}")
                st.write(f"**Investment Style:** {i['Style']}")
        

    col3,col4 = st.columns(2,gap='small')
    with col3:
        fig = px.pie(investment_by_domain, names='deal_type', values='deal_amount', title=f"{shark_full_names[shark_name]}'s Investment Distribution by Business Domain")

        fig.update_layout(
        width=650,
        height=350, 
        title_x=0.03,  # Center title
        title_y=0.92,  # Position title# Adjust margins (top, bottom, left, right)
        showlegend=True
        )
        # Display the pie chart
        st.plotly_chart(fig)
    with col4:
        st.dataframe(combined_data , hide_index=True)
        