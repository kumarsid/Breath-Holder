import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Breath Holding Capacity Signposting",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        margin-top: 20px;
        background-color: #1E88E5;
        color: white;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-style {
        color: #1E88E5;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .subheader-style {
        color: #424242;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .nhs-link {
        color: #005EB8;
        text-decoration: none;
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f0f0;
        display: inline-block;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def get_category_info(seconds):
    """Return category information based on breath-holding time."""
    if seconds < 30:
        return {
            'category': 'Category 1: Initial Assessment Required',
            'color': '#FF9999',
            'description': 'Your breath-holding capacity suggests that further assessment might be beneficial.',
            'recommendations': [
                'Schedule a GP appointment for respiratory assessment',
                'Start with very gentle breathing exercises',
                'Monitor your daily breathing patterns'
            ],
            'nhs_links': [
                ('NHS - Breathing Exercises for Stress', 'https://www.nhs.uk/mental-health/self-help/guides-tools-and-activities/breathing-exercises-for-stress/'),
                ('NHS - When to see a GP', 'https://www.nhs.uk/conditions/shortness-of-breath/'),
                ('NHS - Breathing Difficulty', 'https://www.nhs.uk/conditions/breathing-difficulty/')
            ]
        }
    elif 30 <= seconds <= 60:
        return {
            'category': 'Category 2: Developing Capacity',
            'color': '#99FF99',
            'description': 'You have a developing breath-holding capacity. Regular practice can help improve this.',
            'recommendations': [
                'Practice regular breathing exercises',
                'Consider lifestyle factors that might affect breathing',
                'Monitor progress weekly'
            ],
            'nhs_links': [
                ('NHS - Physical Activity Guidelines', 'https://www.nhs.uk/live-well/exercise/'),
                ('NHS - Fitness Studio Exercise Videos', 'https://www.nhs.uk/conditions/nhs-fitness-studio/'),
                ('NHS - Better Health', 'https://www.nhs.uk/better-health/')
            ]
        }
    elif 61 <= seconds <= 150:
        return {
            'category': 'Category 3: Good Capacity',
            'color': '#99CCFF',
            'description': 'Your breath-holding capacity is good, showing effective breathing control.',
            'recommendations': [
                'Maintain current breathing practices',
                'Consider incorporating advanced techniques',
                'Focus on consistency in practice'
            ],
            'nhs_links': [
                ('NHS - Fitness Tips', 'https://www.nhs.uk/live-well/exercise/fitness-tips/'),
                ('NHS - Running Tips', 'https://www.nhs.uk/live-well/exercise/running-tips-for-beginners/'),
                ('NHS - Health Benefits of Swimming', 'https://www.nhs.uk/live-well/exercise/swimming-for-fitness/')
            ]
        }
    else:
        return {
            'category': 'Category 4: Advanced Capacity',
            'color': '#FFCC99',
            'description': 'You demonstrate advanced breath-holding capacity. Your level indicates excellent respiratory control.',
            'recommendations': [
                'Maintain this excellent level',
                'Consider advanced breathing techniques',
                'Share your expertise with others'
            ],
            'nhs_links': [
                ('NHS - Exercise Health Benefits', 'https://www.nhs.uk/live-well/exercise/exercise-health-benefits/'),
                ('NHS - Get Active Your Way', 'https://www.nhs.uk/live-well/exercise/get-active-your-way/'),
                ('NHS - Fitness Studio', 'https://www.nhs.uk/conditions/nhs-fitness-studio/')
            ]
        }

def create_gauge_chart(value):
    """Create a gauge chart showing breath-holding time."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Seconds", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 180], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1E88E5"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': "#FF9999"},
                {'range': [30, 60], 'color': "#99FF99"},
                {'range': [60, 150], 'color': "#99CCFF"},
                {'range': [150, 180], 'color': "#FFCC99"}
            ],
        }
    ))
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    return fig

def main():
    # Create two main columns for the layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.markdown('<p class="header-style">😮‍💨 Breath Holding Capacity Signposting</p>', unsafe_allow_html=True)
        
        with st.expander("📋 Instructions"):
            st.markdown("""
            1. Find a comfortable seated position
            2. Take a few normal breaths to relax
            3. Take a deep breath and hold it
            4. Start the timer when you begin holding
            5. Stop when you need to breathe
            """)
        
        seconds = st.number_input(
            "Enter your breath-holding time (in seconds)",
            min_value=0,
            max_value=300,
            value=0,
            help="Input the number of seconds you were able to hold your breath"
        )

    with right_col:
        if seconds > 0:
            # Get category information
            result = get_category_info(seconds)
            
            # Display gauge chart
            st.plotly_chart(create_gauge_chart(seconds), use_container_width=True)
            
            # Balloon celebration if in top 2 categories
            if result['category'] in ['Category 3: Good Capacity', 'Category 4: Advanced Capacity']:
                st.balloons()
            
            # Display results in a card
            st.markdown(f"""
            <div class="card" style="background-color: {result['color']}20;">
                <h3>{result['category']}</h3>
                <p>{result['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display recommendations
            st.markdown('<p class="subheader-style">Recommendations</p>', unsafe_allow_html=True)
            for rec in result['recommendations']:
                st.markdown(f"• {rec}")
            
            # Display NHS Links
            st.markdown('<p class="subheader-style">Relevant NHS Resources</p>', unsafe_allow_html=True)
            for title, link in result['nhs_links']:
                st.markdown(f'<a href="{link}" target="_blank" class="nhs-link">🔗 {title}</a>', unsafe_allow_html=True)
            


if __name__ == "__main__":
    main()