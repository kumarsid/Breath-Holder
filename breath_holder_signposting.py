import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Breath Holding Capacity Survey",
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
        margin-bottom: 10px;
        text-align: left;
    }
    .subheader-style {
        color: #424242;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
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
    .logo {
        display: inline-block;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Display logos on the top right
st.markdown("""
    <div style="display: flex; justify-content: flex-end; align-items: center; margin-top: 10px;">
        <img src="https://swlimo.southwestlondon.icb.nhs.uk/wp-content/uploads/2022/11/nhs-swlondon-logo.png" alt="Logo 1" width="200" class="logo">        
    </div>
""", unsafe_allow_html=True)

st.markdown('<p class="header-style">😮‍💨 Breath Holding Capacity Survey</p>', unsafe_allow_html=True)

def get_category_info(seconds):
    if seconds < 30:
        return {
            'color': '#FF9999',
            'category': 'Category 1: Beginner',
            'description': 'Your breath-holding capacity is at a beginner level. Consider practicing breathing exercises.',
            'recommendations': ['Practice deep breathing daily', 'Consider meditation for relaxation'],
            'nhs_links': [('NHS - When to see a GP', 'https://www.nhs.uk/conditions/shortness-of-breath/'),
                ('NHS - Breathing Difficulty', 'https://www.nhs.uk/conditions/breathing-difficulty/')]
        }
    elif 30 <= seconds < 60:
        return {
            'color': '#FFCC99',
            'category': 'Category 2: Intermediate',
            'description': 'Your breath-holding capacity is at an intermediate level. Keep practicing to improve further.',
            'recommendations': ['Try holding your breath while relaxed', 'Practice with controlled exhales'],
            'nhs_links': [    ('NHS - Physical Activity Guidelines', 'https://www.nhs.uk/live-well/exercise/'),
                ('NHS - Fitness Studio Exercise Videos', 'https://www.nhs.uk/conditions/nhs-fitness-studio/'),
                ('NHS - Better Health', 'https://www.nhs.uk/better-health/')]
        }
    elif 60 <= seconds < 150:
        return {
            'color': '#99FF99',
            'category': 'Category 3: Good Capacity',
            'description': 'Great job! Your breath-holding capacity is above average.',
            'recommendations': ['Continue regular practice', 'Incorporate exercises for endurance'],
            'nhs_links': [   ('NHS - Fitness Tips', 'https://www.nhs.uk/live-well/exercise/fitness-tips/'),
                ('NHS - Health Benefits of Swimming', 'https://www.nhs.uk/live-well/exercise/swimming-for-fitness/')]
        }
    else:
        return {
            'color': '#99CCFF',
            'category': 'Category 4: Advanced Capacity',
            'description': 'Excellent! You have advanced breath-holding capacity.',
            'recommendations': ['Explore breath-hold diving techniques', 'Stay relaxed during breath holds'],
            'nhs_links': [  ('NHS - Exercise Health Benefits', 'https://www.nhs.uk/live-well/exercise/exercise-health-benefits/'),
                ('NHS - Get Active Your Way', 'https://www.nhs.uk/live-well/exercise/get-active-your-way/'),
                ('NHS - Fitness Studio', 'https://www.nhs.uk/conditions/nhs-fitness-studio/')]
        }


def create_gauge_chart(value):
    """Create a smaller gauge chart showing breath-holding time."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Seconds", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [None, 180], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#1E88E5"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': "#FF9999"},
                {'range': [30, 60], 'color': "#FFCC99"},
                {'range': [60, 150], 'color': "#99FF99"},
                {'range': [150, 180], 'color': "#99CCFF"}
            ],
        }
    ))
    fig.update_layout(
        height=200,  # Reduced height for smaller chart size
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    return fig

def main():
    st.write("---")  # Adding a separator for visual clarity

    # Create two main columns for the layout
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown('<p class="subheader-style">Welcome to the Survey!</p>', unsafe_allow_html=True)
        st.write("""
        Measure your breath-holding capacity, understand your current level, and get personalized recommendations 
        along with relevant NHS resources.
        """)

        with st.expander("📋 Instructions", expanded=False):
            st.write("""
            1. Find a comfortable seated position.
            2. Take a few normal breaths to relax.
            3. Take a deep breath and hold it.
            4. Start the timer when you begin holding.
            5. Stop when you need to breathe.
            """)

       
        # Input for breath-holding time
        st.markdown("**Enter your breath-holding time (in seconds):**")  # Main input prompt
        seconds = st.number_input(
            "",  # Leave this empty for the input box
            min_value=0,
            max_value=300,
            value=0
        )
        st.markdown("Press Enter once done")  # Instruction below the input


    with right_col:
        if seconds > 0:
            # Get category information
            result = get_category_info(seconds)

            # Display smaller gauge chart
            st.plotly_chart(create_gauge_chart(seconds), use_container_width=True)

            # Display results in a card
            st.markdown(f"""
<div class="card" style="background-color: {result['color']}; padding: 10px; border-radius: 10px; margin: 10px 0;">
    <h3>{result['category']}</h3>
    <p>{result['description']}</p>
</div>
""", unsafe_allow_html=True)


            # Display recommendations
            st.markdown('<p class="subheader-style">Recommendations</p>', unsafe_allow_html=True)
            for rec in result['recommendations']:
                st.write(f"- {rec}")

            # Display NHS Links
            st.markdown('<p class="subheader-style">Relevant NHS Resources</p>', unsafe_allow_html=True)

            # Create a string to hold the HTML for the links
            links_html = ' | '.join([f'<a href="{link}" target="_blank" class="nhs-link">🔗 {title}</a>' for title, link in result['nhs_links']])
            st.markdown(links_html, unsafe_allow_html=True)

            # Show balloons for top categories
            if result['category'] in ['Category 3: Good Capacity', 'Category 4: Advanced Capacity']:
                st.balloons()

if __name__ == "__main__":
    main()
