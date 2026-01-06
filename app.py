"""
🎯 Productivity Command Center
A comprehensive personal productivity dashboard built with Streamlit
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, date, timedelta
from textblob import TextBlob
from database import Database

# Page configuration
st.set_page_config(
    page_title="Productivity Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ MINIMAL LIGHT THEME CSS - FIXED TEXT VISIBILITY ============

st.markdown("""
<style>
    /* Import clean font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global text color fix */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* ===== SIDEBAR FIXES ===== */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    
    section[data-testid="stSidebar"] * {
        color: #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown span,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4,
    section[data-testid="stSidebar"] .stMarkdown h5,
    section[data-testid="stSidebar"] .stMarkdown h6 {
        color: #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        color: #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label span {
        color: #1a1a1a !important;
    }
    
    /* Sidebar metric text */
    section[data-testid="stSidebar"] [data-testid="metric-container"] label {
        color: #555555 !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMetricDelta"] {
        color: #555555 !important;
    }
    
    /* Sidebar info box */
    section[data-testid="stSidebar"] .stAlert p {
        color: #1a1a1a !important;
    }
    
    /* ===== MAIN CONTENT TEXT FIXES ===== */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li {
        color: #1a1a1a !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #1a1a1a !important;
    }
    
    /* Strong/Bold text */
    .stMarkdown strong, .stMarkdown b {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    /* Caption text */
    .stCaption, .stMarkdown small, .stCaptionContainer {
        color: #555555 !important;
    }
    
    /* ===== METRIC CONTAINERS ===== */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
    }
    
    [data-testid="metric-container"] label {
        color: #555555 !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
        font-weight: 600;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #666666 !important;
    }
    
    /* ===== INPUT FIELDS ===== */
    .stTextInput label, .stTextArea label, .stSelectbox label,
    .stSlider label, .stDateInput label, .stNumberInput label {
        color: #1a1a1a !important;
        font-weight: 500;
    }
    
    .stTextInput input, .stTextArea textarea {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
        border: 1px solid #d0d0d0 !important;
    }
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #888888 !important;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff;
    }
    
    .stSelectbox [data-baseweb="select"] * {
        color: #1a1a1a !important;
    }
    
    /* Number input */
    .stNumberInput input {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* Date input */
    .stDateInput input {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    /* ===== SLIDER ===== */
    .stSlider label {
        color: #1a1a1a !important;
    }
    
    .stSlider [data-baseweb="slider"] div {
        color: #1a1a1a !important;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        color: #1a1a1a !important;
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background-color: #f0f0f0;
        border-color: #b0b0b0;
        color: #1a1a1a !important;
    }
    
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #5c6bc0 !important;
        color: #ffffff !important;
        border: none;
    }
    
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #4a5ab0 !important;
        color: #ffffff !important;
    }
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {
        color: #1a1a1a !important;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        color: #1a1a1a !important;
    }
    
    .streamlit-expanderHeader p {
        color: #1a1a1a !important;
    }
    
    .streamlit-expanderContent {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-top: none;
    }
    
    /* Expander icon */
    .streamlit-expanderHeader svg {
        fill: #1a1a1a !important;
    }
    
    /* ===== ALERTS/INFO BOXES ===== */
    .stAlert, [data-testid="stAlert"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }
    
    .stAlert p, [data-testid="stAlert"] p {
        color: #1a1a1a !important;
    }
    
    /* Success alert */
    .stSuccess, [data-testid="stAlert"][data-baseweb="notification"]:has(svg[data-testid="stIconSuccess"]) {
        background-color: #e8f5e9 !important;
        border-left: 4px solid #4caf50;
    }
    
    .stSuccess p {
        color: #1a1a1a !important;
    }
    
    /* Info alert */
    .stInfo {
        background-color: #e3f2fd !important;
        border-left: 4px solid #2196f3;
    }
    
    .stInfo p {
        color: #1a1a1a !important;
    }
    
    /* Warning alert */
    .stWarning {
        background-color: #fff8e1 !important;
        border-left: 4px solid #ff9800;
    }
    
    .stWarning p {
        color: #1a1a1a !important;
    }
    
    /* Error alert */
    .stError {
        background-color: #ffebee !important;
        border-left: 4px solid #f44336;
    }
    
    .stError p {
        color: #1a1a1a !important;
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        background-color: #ffffff;
    }
    
    .stDataFrame * {
        color: #1a1a1a !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #ffffff;
    }
    
    /* ===== PROGRESS BAR ===== */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #5c6bc0, #7986cb);
    }
    
    .stProgress > div > div {
        background-color: #e0e0e0;
    }
    
    /* Progress text */
    .stProgress p {
        color: #1a1a1a !important;
    }
    
    /* ===== RADIO BUTTONS ===== */
    .stRadio > label {
        color: #1a1a1a !important;
    }
    
    .stRadio label span {
        color: #1a1a1a !important;
    }
    
    .stRadio [data-baseweb="radio"] span {
        color: #1a1a1a !important;
    }
    
    /* ===== CHECKBOX ===== */
    .stCheckbox label span {
        color: #1a1a1a !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #f0f0f0;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #555555 !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #1a1a1a !important;
        background-color: #ffffff;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border-color: #e0e0e0 !important;
    }
    
    /* ===== CUSTOM HEADER ===== */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a1a;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .main-header span {
        background: linear-gradient(135deg, #5c6bc0 0%, #7e57c2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ===== FOOTER ===== */
    .footer {
        text-align: center;
        color: #666666;
        font-size: 0.9rem;
        padding: 2rem 0;
        margin-top: 2rem;
    }
    
    /* ===== TOOLTIP ===== */
    [data-baseweb="tooltip"] {
        background-color: #333333 !important;
        color: #ffffff !important;
    }
    
    /* ===== PLOTLY CHART TEXT ===== */
    .js-plotly-plot .plotly text {
        fill: #1a1a1a !important;
    }
    
    .js-plotly-plot .plotly .gtitle {
        fill: #1a1a1a !important;
    }
    
    /* ===== STRIKETHROUGH TEXT ===== */
    s, strike, del {
        color: #888888 !important;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def get_database():
    return Database()

db = get_database()

# Mood emoji mapping
MOOD_EMOJIS = {
    1: "😢",
    2: "😔", 
    3: "😐",
    4: "🙂",
    5: "😊",
    6: "😄",
    7: "🤩"
}

PRIORITY_COLORS = {
    "low": "🟢",
    "medium": "🟡", 
    "high": "🔴"
}

# Chart color scheme
CHART_COLORS = {
    'primary': '#5c6bc0',
    'secondary': '#7e57c2',
    'success': '#66bb6a',
    'warning': '#ffa726',
    'danger': '#ef5350',
    'gray': '#9e9e9e',
    'light_gray': '#e0e0e0',
    'text': '#1a1a1a'
}

def analyze_sentiment(text: str) -> float:
    """Analyze sentiment of text using TextBlob"""
    if not text:
        return 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity

def create_minimal_chart(fig, height=300):
    """Apply minimal theme to Plotly charts with visible text"""
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(255,255,255,1)',
        plot_bgcolor='rgba(255,255,255,1)',
        font=dict(color='#1a1a1a', family='Inter, sans-serif', size=12),
        title_font=dict(color='#1a1a1a', size=14),
        xaxis=dict(
            gridcolor='#e0e0e0',
            linecolor='#cccccc',
            tickfont=dict(color='#1a1a1a', size=11),
            title_font=dict(color='#1a1a1a', size=12)
        ),
        yaxis=dict(
            gridcolor='#e0e0e0',
            linecolor='#cccccc',
            tickfont=dict(color='#1a1a1a', size=11),
            title_font=dict(color='#1a1a1a', size=12)
        ),
        legend=dict(
            font=dict(color='#1a1a1a', size=11),
            bgcolor='rgba(255,255,255,0.9)'
        )
    )
    return fig

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### 🎯 Productivity")
    st.caption("Your personal dashboard")
    
    st.markdown("---")
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "✅ Tasks", "🔄 Habits", "😊 Mood", "🎯 Goals", "📈 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Today's date
    st.markdown("##### 📅 Today")
    st.markdown(f"**{datetime.now().strftime('%B %d, %Y')}**")
    st.caption(datetime.now().strftime('%A'))
    
    st.markdown("---")
    
    # Quick stats
    stats = db.get_productivity_stats()
    
    st.markdown("##### 📊 Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tasks", f"{stats['completed_tasks']}/{stats['total_tasks']}")
    with col2:
        st.metric("Mood", f"{stats['average_mood']:.1f}")
    
    st.metric("Active Goals", stats['active_goals'])

# ============ DASHBOARD PAGE ============
if page == "📊 Dashboard":
    st.markdown('<h1 class="main-header"><span>Productivity Dashboard</span></h1>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Task Completion",
            value=f"{stats['completion_rate']:.0f}%",
            delta="Today"
        )
    
    with col2:
        st.metric(
            label="Habit Streak",
            value=stats['total_habit_completions'],
            delta="Total"
        )
    
    with col3:
        st.metric(
            label="Average Mood",
            value=f"{stats['average_mood']:.1f}/7",
            delta="30 days"
        )
    
    with col4:
        st.metric(
            label="Active Goals",
            value=stats['active_goals'],
            delta="In progress"
        )
    
    st.markdown("---")
    
    # Today's overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📋 Today's Tasks")
        pending_tasks = db.get_all_tasks(status="pending")[:5]
        if pending_tasks:
            for idx, task in enumerate(pending_tasks):
                priority_emoji = PRIORITY_COLORS.get(task['priority'], "⚪")
                
                with st.container():
                    task_col1, task_col2 = st.columns([0.85, 0.15])
                    with task_col1:
                        st.markdown(f"{priority_emoji} {task['title']}")
                    with task_col2:
                        if st.button("✓", key=f"complete_dash_task_{task['id']}_{idx}", help="Complete"):
                            db.update_task_status(task['id'], 'completed')
                            st.rerun()
        else:
            st.success("🎉 All tasks completed!")
    
    with col2:
        st.markdown("##### 🔄 Today's Habits")
        habits = db.get_all_habits()[:5]
        if habits:
            for idx, habit in enumerate(habits):
                status = "✅" if habit['completed_today'] else "○"
                streak_text = f" · 🔥{habit['streak']}" if habit['streak'] > 0 else ""
                
                with st.container():
                    habit_col1, habit_col2 = st.columns([0.85, 0.15])
                    with habit_col1:
                        st.markdown(f"{status} {habit['name']}{streak_text}")
                    with habit_col2:
                        if not habit['completed_today']:
                            if st.button("✓", key=f"complete_dash_habit_{habit['id']}_{idx}", help="Complete"):
                                db.log_habit(habit['id'])
                                st.rerun()
        else:
            st.info("No habits yet. Add some!")
    
    st.markdown("---")
    
    # Weekly activity chart
    st.markdown("##### 📈 Weekly Activity")
    
    weekly_data = db.get_weekly_activity()
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    day_names = [(datetime.now() - timedelta(days=i)).strftime('%a') for i in range(6, -1, -1)]
    
    tasks_data = [weekly_data['tasks_by_day'].get(d, 0) for d in dates]
    habits_data = [weekly_data['habits_by_day'].get(d, 0) for d in dates]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='Tasks', 
        x=day_names, 
        y=tasks_data, 
        marker_color=CHART_COLORS['primary'],
        marker_line_width=0
    ))
    fig.add_trace(go.Bar(
        name='Habits', 
        x=day_names, 
        y=habits_data, 
        marker_color=CHART_COLORS['secondary'],
        marker_line_width=0
    ))
    
    fig.update_layout(barmode='group')
    fig = create_minimal_chart(fig, height=280)
    st.plotly_chart(fig, use_container_width=True)

# ============ TASKS PAGE ============
elif page == "✅ Tasks":
    st.markdown("## ✅ Tasks")
    st.caption("Manage your to-do list")
    
    # Add new task form
    with st.expander("➕ Add New Task", expanded=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_task_title = st.text_input("Title", placeholder="What needs to be done?", key="new_task_title")
            new_task_desc = st.text_area("Description", height=80, placeholder="Add details...", key="new_task_desc")
        
        with col2:
            new_task_priority = st.selectbox("Priority", ["low", "medium", "high"], key="new_task_priority")
            new_task_due = st.date_input("Due Date", value=None, key="new_task_due")
        
        if st.button("Add Task", type="primary", key="add_task_btn"):
            if new_task_title:
                due_date = new_task_due.isoformat() if new_task_due else None
                db.add_task(new_task_title, new_task_desc, new_task_priority, due_date)
                st.success("Task added!")
                st.rerun()
            else:
                st.error("Please enter a title")
    
    st.markdown("---")
    
    # Task filters
    status_filter = st.selectbox(
        "Filter",
        ["all", "pending", "in_progress", "completed"],
        key="task_status_filter",
        label_visibility="collapsed"
    )
    
    # Display tasks
    all_tasks = db.get_all_tasks(status_filter if status_filter != "all" else None)
    
    if all_tasks:
        for idx, task in enumerate(all_tasks):
            col1, col2, col3, col4 = st.columns([0.08, 0.52, 0.3, 0.1])
            
            with col1:
                priority_emoji = PRIORITY_COLORS.get(task['priority'], "⚪")
                st.markdown(f"{priority_emoji}")
            
            with col2:
                if task['status'] == 'completed':
                    st.markdown(f"~~{task['title']}~~")
                else:
                    st.markdown(f"**{task['title']}**")
                if task['description']:
                    st.caption(task['description'][:50] + "..." if len(task['description']) > 50 else task['description'])
            
            with col3:
                new_status = st.selectbox(
                    "Status",
                    ["pending", "in_progress", "completed"],
                    index=["pending", "in_progress", "completed"].index(task['status']),
                    key=f"task_status_{task['id']}_{idx}",
                    label_visibility="collapsed"
                )
                if new_status != task['status']:
                    db.update_task_status(task['id'], new_status)
                    st.rerun()
            
            with col4:
                if st.button("×", key=f"del_task_{task['id']}_{idx}", help="Delete"):
                    db.delete_task(task['id'])
                    st.rerun()
            
            st.divider()
    else:
        st.info("No tasks found. Add one above!")

# ============ HABITS PAGE ============
elif page == "🔄 Habits":
    st.markdown("## 🔄 Habits")
    st.caption("Track your daily routines")
    
    # Add new habit
    with st.expander("➕ Add New Habit", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            new_habit_name = st.text_input("Habit Name", placeholder="e.g., Exercise, Read...", key="new_habit_name")
            new_habit_desc = st.text_input("Description", placeholder="Optional details", key="new_habit_desc")
        
        with col2:
            new_habit_freq = st.selectbox("Frequency", ["daily", "weekly"], key="new_habit_freq")
        
        if st.button("Add Habit", type="primary", key="add_habit_btn"):
            if new_habit_name:
                db.add_habit(new_habit_name, new_habit_desc, new_habit_freq)
                st.success("Habit added!")
                st.rerun()
    
    st.markdown("---")
    
    # Display habits
    all_habits = db.get_all_habits()
    
    if all_habits:
        for idx, habit in enumerate(all_habits):
            col1, col2, col3, col4 = st.columns([0.1, 2.4, 1, 0.5])
            
            with col1:
                status = "✅" if habit['completed_today'] else "○"
                st.markdown(f"### {status}")
            
            with col2:
                st.markdown(f"**{habit['name']}**")
                if habit['description']:
                    st.caption(habit['description'])
            
            with col3:
                if habit['streak'] > 0:
                    st.markdown(f"🔥 **{habit['streak']}** days")
                else:
                    st.caption("Start streak!")
                
                if not habit['completed_today']:
                    if st.button("Complete", key=f"complete_habit_{habit['id']}_{idx}", type="primary"):
                        db.log_habit(habit['id'])
                        st.rerun()
            
            with col4:
                if st.button("×", key=f"del_habit_{habit['id']}_{idx}"):
                    db.delete_habit(habit['id'])
                    st.rerun()
            
            st.divider()
        
        # Streak visualization
        st.markdown("---")
        st.markdown("##### 🏆 Streaks")
        
        streak_data = pd.DataFrame([
            {"Habit": h['name'], "Streak": h['streak']} 
            for h in all_habits
        ])
        streak_data = streak_data.sort_values('Streak', ascending=True)
        
        fig = px.bar(
            streak_data, 
            x='Streak', 
            y='Habit', 
            orientation='h',
            color='Streak',
            color_continuous_scale=[[0, CHART_COLORS['light_gray']], [1, CHART_COLORS['primary']]]
        )
        fig.update_traces(marker_line_width=0)
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        fig = create_minimal_chart(fig, height=250)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No habits yet. Add one above!")

# ============ MOOD PAGE ============
elif page == "😊 Mood":
    st.markdown("## 😊 Mood")
    st.caption("Track how you're feeling")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("##### How are you feeling?")
        mood_score = st.slider(
            "Mood Level",
            min_value=1,
            max_value=7,
            value=4,
            help="1 = Very Low, 7 = Excellent",
            key="mood_slider",
            label_visibility="collapsed"
        )
        st.markdown(f"<div style='text-align: center; font-size: 3rem;'>{MOOD_EMOJIS[mood_score]}</div>", unsafe_allow_html=True)
    
    with col2:
        mood_notes = st.text_area(
            "Notes",
            placeholder="What's on your mind today?",
            height=120,
            key="mood_notes",
            label_visibility="collapsed"
        )
    
    if st.button("Log Mood", type="primary", key="log_mood_btn"):
        sentiment = analyze_sentiment(mood_notes)
        db.add_mood_entry(mood_score, MOOD_EMOJIS[mood_score], mood_notes, sentiment)
        sentiment_label = 'Positive 😊' if sentiment > 0 else 'Neutral 😐' if sentiment == 0 else 'Reflective 💭'
        st.success(f"Mood logged! ({sentiment_label})")
        st.balloons()
        st.rerun()
    
    st.markdown("---")
    
    # Mood history
    st.markdown("##### 📈 Mood Trend")
    
    mood_entries = db.get_mood_entries(30)
    
    if mood_entries:
        mood_df = pd.DataFrame(mood_entries)
        mood_df['date'] = pd.to_datetime(mood_df['logged_at']).dt.date
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=mood_df['date'], 
            y=mood_df['mood_score'],
            mode='lines+markers',
            name='Mood',
            line=dict(color=CHART_COLORS['primary'], width=2),
            marker=dict(size=8, color=CHART_COLORS['primary']),
            fill='tozeroy',
            fillcolor='rgba(92, 107, 192, 0.15)'
        ))
        
        fig = create_minimal_chart(fig, height=280)
        fig.update_yaxes(range=[0, 8])
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent entries
        st.markdown("##### 📝 Recent Entries")
        for idx, entry in enumerate(mood_entries[:5]):
            col1, col2 = st.columns([0.12, 0.88])
            with col1:
                st.markdown(f"### {entry['mood_emoji']}")
            with col2:
                st.markdown(f"**{entry['logged_at'][:10]}** · {entry['mood_score']}/7")
                if entry['notes']:
                    st.caption(entry['notes'][:80] + "..." if len(entry['notes']) > 80 else entry['notes'])
            st.divider()
    else:
        st.info("No mood entries yet. Log your first mood above!")

# ============ GOALS PAGE ============
elif page == "🎯 Goals":
    st.markdown("## 🎯 Goals")
    st.caption("Track your progress")
    
    # Add new goal
    with st.expander("➕ Add New Goal", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            goal_title = st.text_input("Goal", placeholder="e.g., Read 24 books", key="goal_title")
            goal_desc = st.text_area("Description", height=80, placeholder="Why is this important?", key="goal_desc")
        
        with col2:
            col2a, col2b = st.columns(2)
            with col2a:
                target_value = st.number_input("Target", min_value=1, value=100, key="goal_target")
            with col2b:
                unit = st.text_input("Unit", placeholder="books, km...", key="goal_unit")
            deadline = st.date_input("Deadline", value=None, key="goal_deadline")
        
        if st.button("Add Goal", type="primary", key="add_goal_btn"):
            if goal_title and target_value > 0:
                deadline_str = deadline.isoformat() if deadline else None
                db.add_goal(goal_title, target_value, unit, goal_desc, deadline_str)
                st.success("Goal added!")
                st.rerun()
    
    st.markdown("---")
    
    # Display goals
    all_goals = db.get_all_goals()
    
    if all_goals:
        for idx, goal in enumerate(all_goals):
            st.markdown(f"**{goal['title']}**")
            
            col1, col2, col3 = st.columns([3, 1.5, 0.5])
            
            with col1:
                progress = goal['progress']
                st.progress(progress / 100)
                st.caption(f"{goal['current_value']:.0f} / {goal['target_value']} {goal['unit']} ({progress:.0f}%)")
            
            with col2:
                new_value = st.number_input(
                    "Progress",
                    min_value=0.0,
                    max_value=float(goal['target_value']),
                    value=float(goal['current_value']),
                    key=f"goal_progress_{goal['id']}_{idx}",
                    label_visibility="collapsed"
                )
                if st.button("Update", key=f"update_goal_{goal['id']}_{idx}"):
                    db.update_goal_progress(goal['id'], new_value)
                    st.rerun()
            
            with col3:
                if st.button("×", key=f"del_goal_{goal['id']}_{idx}"):
                    db.delete_goal(goal['id'])
                    st.rerun()
            
            if goal['deadline']:
                days_left = (date.fromisoformat(goal['deadline']) - date.today()).days
                if days_left > 0:
                    st.caption(f"⏰ {days_left} days left")
                elif days_left == 0:
                    st.warning("Due today!")
                else:
                    st.error("Overdue")
            
            st.markdown("---")
    else:
        st.info("No goals yet. Set one above!")

# ============ ANALYTICS PAGE ============
elif page == "📈 Analytics":
    st.markdown("## 📈 Analytics")
    st.caption("Your productivity insights")
    
    stats = db.get_productivity_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tasks", stats['total_tasks'])
    with col2:
        st.metric("Completed", stats['completed_tasks'])
    with col3:
        st.metric("Completion %", f"{stats['completion_rate']:.0f}%")
    with col4:
        st.metric("Avg Mood", f"{stats['average_mood']:.1f}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Task Distribution")
        all_tasks = db.get_all_tasks()
        
        if all_tasks:
            status_counts = {}
            for task in all_tasks:
                status = task['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            colors = [CHART_COLORS['warning'], CHART_COLORS['primary'], CHART_COLORS['success']]
            
            fig = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                color_discrete_sequence=colors,
                hole=0.4
            )
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                textfont=dict(color='#ffffff', size=12)
            )
            fig = create_minimal_chart(fig, height=280)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    with col2:
        st.markdown("##### Mood Trend")
        mood_entries = db.get_mood_entries(30)
        
        if mood_entries:
            mood_df = pd.DataFrame(mood_entries)
            mood_df['date'] = pd.to_datetime(mood_df['logged_at']).dt.date
            daily_mood = mood_df.groupby('date')['mood_score'].mean().reset_index()
            
            fig = px.line(daily_mood, x='date', y='mood_score', markers=True)
            fig.update_traces(
                line_color=CHART_COLORS['primary'], 
                line_width=2,
                marker_size=6
            )
            fig = create_minimal_chart(fig, height=280)
            fig.update_yaxes(range=[0, 8])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    # Habit performance
    st.markdown("##### Habit Performance")
    all_habits = db.get_all_habits()
    
    if all_habits:
        habit_data = pd.DataFrame([
            {
                "Habit": h['name'],
                "Streak": h['streak'],
                "Status": "✅ Done" if h['completed_today'] else "○ Pending"
            }
            for h in all_habits
        ])
        st.dataframe(habit_data, use_container_width=True, hide_index=True)
    else:
        st.info("No habits tracked yet")
    
    # Goal progress
    st.markdown("##### Goal Progress")
    all_goals = db.get_all_goals()
    
    if all_goals:
        goal_data = pd.DataFrame([
            {
                "Goal": g['title'][:25] + "..." if len(g['title']) > 25 else g['title'],
                "Progress": g['progress']
            }
            for g in all_goals
        ])
        
        fig = px.bar(
            goal_data,
            x='Goal',
            y='Progress',
            color='Progress',
            color_continuous_scale=[[0, CHART_COLORS['light_gray']], [1, CHART_COLORS['success']]],
            text='Progress'
        )
        fig.update_traces(
            texttemplate='%{text:.0f}%', 
            textposition='outside', 
            marker_line_width=0,
            textfont=dict(color='#1a1a1a', size=11)
        )
        fig.update_layout(coloraxis_showscale=False)
        fig = create_minimal_chart(fig, height=300)
        fig.update_yaxes(range=[0, 110])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No goals set yet")

# Footer
st.markdown("""
<div class="footer">
    Productivity Dashboard · Built by Dakxh_69
</div>
""", unsafe_allow_html=True)