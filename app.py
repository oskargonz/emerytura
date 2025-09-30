import streamlit as st
import pandas as pd
from retirement_calc import calculate_retirement_age

# Page configuration
st.set_page_config(
    page_title="Kalkulator Wczesnej Emerytury",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful dark and light theme styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    /* Dark theme (default) */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Light theme for users who prefer light mode */
    @media (prefers-color-scheme: light) {
        .stApp {
            background-color: #f8fafc;
            color: #1a202c;
        }
    }
    .main .block-container {
        background-color: #2d2d2d;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-top: 1rem;
        border: 1px solid #404040;
    }
    
    /* Light theme container */
    @media (prefers-color-scheme: light) {
        .main .block-container {
            background-color: #ffffff;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
        }
    }
    
    .metric-container {
        background-color: #3d3d3d;
        border: 2px solid #555555;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    /* Light theme metric container */
    @media (prefers-color-scheme: light) {
        .metric-container {
            background-color: #f7fafc;
            border: 2px solid #cbd5e0;
        }
    }
    
    .success-box {
        background-color: #1e3a2e;
        border: 2px solid #28a745;
        color: #4ade80;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Light theme success box */
    @media (prefers-color-scheme: light) {
        .success-box {
            background-color: #f0fff4;
            border: 2px solid #38a169;
            color: #2f855a;
        }
    }
    .info-box {
        background-color: #1e2a3a;
        border: 2px solid #3b82f6;
        color: #60a5fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Light theme info box */
    @media (prefers-color-scheme: light) {
        .info-box {
            background-color: #eff6ff;
            border: 2px solid #3b82f6;
            color: #1e40af;
        }
    }
    
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #555555;
        background-color: #3d3d3d;
        color: #ffffff;
    }
    
    /* Light theme inputs */
    @media (prefers-color-scheme: light) {
        .stNumberInput > div > div > input {
            border: 2px solid #cbd5e0;
            background-color: #ffffff;
            color: #2d3748;
        }
    }
    
    .stSelectbox > div > div > div {
        background-color: #3d3d3d;
        color: #ffffff;
    }
    
    /* Light theme selectbox */
    @media (prefers-color-scheme: light) {
        .stSelectbox > div > div > div {
            background-color: #ffffff;
            color: #2d3748;
        }
    }
    .stButton > button {
        background-color: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #2563eb;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59,130,246,0.4);
    }
    
    /* Light theme button hover */
    @media (prefers-color-scheme: light) {
        .stButton > button:hover {
            box-shadow: 0 4px 12px rgba(59,130,246,0.3);
        }
    }
    
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    /* Light theme headings */
    @media (prefers-color-scheme: light) {
        h1 {
            color: #1a202c;
        }
    }
    
    h2, h3 {
        color: #ffffff;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* Light theme h2, h3 */
    @media (prefers-color-scheme: light) {
        h2, h3 {
            color: #1a202c;
        }
    }
    .sidebar .stMarkdown {
        color: #cccccc;
    }
    
    /* Light theme sidebar text */
    @media (prefers-color-scheme: light) {
        .sidebar .stMarkdown {
            color: #4a5568;
        }
    }
    
    .stMarkdown {
        color: #ffffff;
    }
    
    /* Light theme markdown */
    @media (prefers-color-scheme: light) {
        .stMarkdown {
            color: #2d3748;
        }
    }
    
    .stMetric {
        background-color: #3d3d3d;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #555555;
    }
    
    /* Light theme metrics */
    @media (prefers-color-scheme: light) {
        .stMetric {
            background-color: #f7fafc;
            border: 1px solid #e2e8f0;
        }
    }
    
    .stDataFrame {
        background-color: #2d2d2d;
    }
    
    /* Light theme dataframe */
    @media (prefers-color-scheme: light) {
        .stDataFrame {
            background-color: #ffffff;
        }
    }
    
    div[data-testid="stSidebar"] {
        background-color: #2d2d2d;
    }
    
    /* Light theme sidebar */
    @media (prefers-color-scheme: light) {
        div[data-testid="stSidebar"] {
            background-color: #f7fafc;
        }
    }
    
    div[data-testid="stSidebar"] .stMarkdown {
        color: #cccccc;
    }
    
    /* Light theme sidebar markdown */
    @media (prefers-color-scheme: light) {
        div[data-testid="stSidebar"] .stMarkdown {
            color: #4a5568;
        }
    }
    
    /* Mobile Responsive Design */
    @media (max-width: 768px) {
        /* Title adjustments for mobile */
        h1 {
            font-size: 1.8rem !important;
            margin-bottom: 0.5rem !important;
            padding: 0 1rem;
        }
        
        /* Sidebar adjustments for mobile */
        div[data-testid="stSidebar"] {
            min-height: 100vh;
            position: sticky !important;
            top: 0;
        }
        
        div[data-testid="stSidebar"] > div {
            position: sticky !important;
            top: 0;
            max-height: 100vh;
            overflow-y: auto;
            padding-bottom: 2rem;
        }
        
        /* Main content adjustments */
        .main .block-container {
            padding-top: 1rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
        }
        
        /* Card adjustments for mobile */
        div[style*="background-color: #1e2a3a"], 
        div[style*="background-color: #3a2a1e"], 
        div[style*="background-color: #1e3a2e"] {
            margin: 0.5rem 0 !important;
            padding: 1rem !important;
        }
        
        /* Button improvements for mobile */
        .stButton > button {
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
            margin-top: 1rem;
        }
        
        /* Chart containers for mobile */
        div[style*="text-align: center; margin: 2rem 0"] {
            margin: 1rem 0 !important;
            padding: 1rem !important;
        }
        
        /* Success box adjustments */
        .success-box {
            font-size: 1rem !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
        }
        
        /* Metric cards for mobile */
        div[style*="text-align: center; margin: 1rem 0"] {
            margin: 0.5rem 0 !important;
            padding: 1rem !important;
        }
        
        div[style*="text-align: center; margin: 1rem 0"] h2 {
            font-size: 1.4rem !important;
        }
        
        div[style*="text-align: center; margin: 1rem 0"] h3 {
            font-size: 1rem !important;
            margin-bottom: 0.3rem !important;
        }
        
        /* Input field improvements */
        .stNumberInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
        
        /* Sidebar sections for mobile */
        .stMarkdown h3 {
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Help text improvements */
        .stNumberInput small {
            font-size: 0.8rem !important;
        }
        
        /* Column layout improvements for mobile */
        div[data-testid="column"] {
            padding: 0 0.5rem !important;
        }
        
        /* Chart improvements */
        .stPlotlyChart {
            margin: 0 !important;
        }
        
        /* Info box improvements */
        .stInfo {
            font-size: 0.9rem !important;
            padding: 1rem !important;
        }
        
        /* Table improvements for mobile */
        .stDataFrame {
            font-size: 0.8rem !important;
        }
        
        /* Ensure sidebar button always visible */
        div[data-testid="stSidebar"] .stButton {
            position: sticky;
            bottom: 1rem;
            z-index: 999;
            background-color: #2d2d2d;
            padding: 0.5rem 0;
        }
        
        /* Light theme mobile sidebar button */
        @media (prefers-color-scheme: light) {
            div[data-testid="stSidebar"] .stButton {
                background-color: #f7fafc;
            }
        }
    }
    
    /* Small mobile devices (phones in portrait) */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.5rem !important;
        }
        
        /* Further reduce card padding on small screens */
        div[style*="background-color: #1e2a3a"], 
        div[style*="background-color: #3a2a1e"], 
        div[style*="background-color: #1e3a2e"] {
            padding: 0.8rem !important;
        }
        
        /* Smaller text in cards */
        div[style*="text-align: center; margin: 1rem 0"] h2 {
            font-size: 1.2rem !important;
        }
        
        div[style*="text-align: center; margin: 1rem 0"] h3 {
            font-size: 0.9rem !important;
        }
        
        /* Column spacing for very small screens */
        div[data-testid="column"] {
            padding: 0 0.25rem !important;
        }
        
        /* Ensure adequate touch targets */
        .stButton > button {
            min-height: 44px !important;
        }
    }
    
    /* Light theme overrides for inline styled elements */
    @media (prefers-color-scheme: light) {
        /* Blue cards - Analysis theme - more specific selectors */
        div[style*="#1e2a3a"] {
            background-color: #f0f8ff !important;
        }
        
        div[style*="#3b82f6"] {
            border-color: #2563eb !important;
        }
        
        /* Orange cards - Charts theme */
        div[style*="#3a2a1e"] {
            background-color: #fffaf0 !important;
        }
        
        div[style*="#f59e0b"] {
            border-color: #d97706 !important;
        }
        
        /* Green cards - Planning theme */
        div[style*="#1e3a2e"] {
            background-color: #f0fdf4 !important;
        }
        
        div[style*="#10b981"] {
            border-color: #059669 !important;
        }
        
        /* Error/failure cards */
        div[style*="#3a1e1e"] {
            background-color: #fef2f2 !important;
        }
        
        div[style*="#dc2626"] {
            border-color: #dc2626 !important;
        }
        
        /* Container backgrounds - "Jak to działa" and chart sections */
        div[style*="#2d2d2d"] {
            background-color: #ffffff !important;
            border-color: #d1d5db !important;
        }
        
        /* Text color overrides - Blue theme colors */
        h3[style*="#60a5fa"] {
            color: #1d4ed8 !important;
        }
        
        h2[style*="#60a5fa"] {
            color: #1e40af !important;
        }
        
        /* Orange theme colors */
        h3[style*="#fbbf24"] {
            color: #b45309 !important;
        }
        
        h2[style*="#fbbf24"] {
            color: #d97706 !important;
        }
        
        /* Green theme colors */
        h3[style*="#4ade80"] {
            color: #047857 !important;
        }
        
        h2[style*="#4ade80"] {
            color: #059669 !important;
        }
        
        /* Error colors */
        h2[style*="#f87171"] {
            color: #dc2626 !important;
        }
        
        p[style*="#fca5a5"] {
            color: #991b1b !important;
        }
        
        /* General text colors */
        p[style*="#cccccc"] {
            color: #6b7280 !important;
        }
        
        h2[style*="#ffffff"] {
            color: #111827 !important;
        }
        
        /* Separator lines */
        hr[style*="#404040"] {
            border-color: #e5e7eb !important;
        }
        
        /* Main subtitle */
        div[style*="#cccccc"][style*="1.2rem"] {
            color: #6b7280 !important;
        }
        
        /* Chart section subtitles */
        p[style*="#cccccc"][style*="1.1rem"] {
            color: #6b7280 !important;
        }
    }
    
    /* CSS Classes for themed cards */
    .card-blue {
        background-color: #1e2a3a;
        border: 2px solid #3b82f6;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .card-orange {
        background-color: #3a2a1e;
        border: 2px solid #f59e0b;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .card-green {
        background-color: #1e3a2e;
        border: 2px solid #10b981;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .card-info {
        text-align: center;
        margin: 3rem 0;
        padding: 2rem;
        background-color: #2d2d2d;
        border: 3px solid #3b82f6;
        border-radius: 15px;
    }
    
    .card-metric-blue {
        background-color: #1e2a3a;
        border: 3px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .card-metric-orange {
        background-color: #3a2a1e;
        border: 3px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .card-metric-green {
        background-color: #1e3a2e;
        border: 3px solid #10b981;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .chart-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background-color: #2d2d2d;
        border-radius: 10px;
        border: 1px solid #404040;
    }
    
    .error-card {
        background-color: #3a1e1e;
        border: 3px solid #dc2626;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Light theme for CSS classes */
    @media (prefers-color-scheme: light) {
        .card-blue {
            background-color: #f0f8ff;
            border-color: #2563eb;
        }
        
        .card-orange {
            background-color: #fffaf0;
            border-color: #d97706;
        }
        
        .card-green {
            background-color: #f0fdf4;
            border-color: #059669;
        }
        
        .card-info {
            background-color: #ffffff;
            border-color: #2563eb;
        }
        
        .card-metric-blue {
            background-color: #f0f8ff;
            border-color: #2563eb;
        }
        
        .card-metric-orange {
            background-color: #fffaf0;
            border-color: #d97706;
        }
        
        .card-metric-green {
            background-color: #f0fdf4;
            border-color: #059669;
        }
        
        .chart-container {
            background-color: #ffffff;
            border-color: #d1d5db;
        }
        
        .error-card {
            background-color: #fef2f2;
            border-color: #dc2626;
        }
        
        /* Text colors for light theme */
        .card-blue h3, .card-metric-blue h3 {
            color: #1d4ed8 !important;
        }
        
        .card-orange h3, .card-metric-orange h3 {
            color: #b45309 !important;
        }
        
        .card-green h3, .card-metric-green h3 {
            color: #047857 !important;
        }
        
        .card-blue p, .card-orange p, .card-green p,
        .card-metric-blue p, .card-metric-orange p, .card-metric-green p {
            color: #6b7280 !important;
        }
        
        .card-blue h2, .card-orange h2, .card-green h2,
        .card-metric-blue h2, .card-metric-orange h2, .card-metric-green h2 {
            color: #111827 !important;
        }
        
        .card-info h2 {
            color: #1e40af !important;
        }
        
        .card-info p {
            color: #6b7280 !important;
        }
        
        .chart-container h2 {
            color: #1e40af !important;
        }
        
        .chart-container p {
            color: #6b7280 !important;
        }
        
        .error-card h2 {
            color: #dc2626 !important;
        }
        
        .error-card p {
            color: #991b1b !important;
        }
    }
    
    /* Buy Me A Coffee button styling */
    .coffee-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1.5rem;
        background-color: rgba(45, 45, 45, 0.3);
        border-radius: 12px;
        border: 1px solid #404040;
    }
    
    .coffee-container img {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 8px;
    }
    
    .coffee-container img:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 206, 84, 0.3);
    }
    
    /* Light theme for coffee button */
    @media (prefers-color-scheme: light) {
        .coffee-container {
            background-color: rgba(248, 250, 252, 0.5);
            border-color: #e2e8f0;
        }
        
        .coffee-container img:hover {
            box-shadow: 0 8px 25px rgba(255, 206, 84, 0.4);
        }
    }
</style>""", unsafe_allow_html=True)

st.title("💰 Kalkulator Wczesnej Emerytury")
st.markdown("<div style='text-align: center; font-size: 1.2rem; margin-bottom: 2rem;'>Zaplanuj swoją finansową przyszłość już dziś! 🚀</div>", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("### 🎯 Twoje dane finansowe")
    st.markdown("---")
    
    current_age = st.number_input(
        "🎂 Obecny wiek", min_value=0, max_value=100, value=30, step=1,
        help="Twój obecny wiek w latach"
    )
    
    capital = st.number_input(
        "💼 Kapitał początkowy (PLN)", min_value=0, value=300000, step=1000,
        help="Ile pieniędzy masz już zaoszczędzone"
    )
    
    monthly_contrib = st.number_input(
        "💸 Miesięczna inwestycja (PLN)", min_value=0, value=5000, step=100,
        help="Ile planujesz inwestować każdego miesiąca"
    )
    
    st.markdown("### 📊 Parametry inwestycyjne")
    st.markdown("---")
    
    annual_return = st.number_input(
        "📈 Średnia stopa zwrotu (%)", min_value=0.0, value=6.0, step=0.1,
        help="Oczekiwana roczna stopa zwrotu z inwestycji"
    )
    
    inflation = st.number_input(
        "🔥 Roczna inflacja (%)", min_value=0.0, value=3.0, step=0.1,
        help="Przewidywana roczna inflacja"
    )
    
    st.markdown("### 🏠 Styl życia")
    st.markdown("---")
    
    annual_expenses = st.number_input(
        "🛒 Miesięczne wydatki (PLN)", min_value=0, value=12000, step=100,
        help="Ile będziesz potrzebować miesięcznie na emeryturze"
    )
    
    projected_lifespan = st.number_input(
        "⏰ Przewidywany wiek śmierci", min_value=50, max_value=120, value=90, step=1,
        help="Do jakiego wieku planujesz żyć"
    )
    
    st.markdown("---")
    calculate_button = st.button("🚀 OBLICZ EMERYTURĘ", use_container_width=True)

# Main content area
if not calculate_button:
    # Welcome screen with beautiful cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='card-blue'>
            <h3 style='color: #60a5fa; margin-bottom: 1rem;'>📊 Analiza</h3>
            <p style='color: #cccccc; font-size: 1rem;'>Dokładne obliczenia uwzględniające inflację i stopy zwrotu</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='card-orange'>
            <h3 style='color: #fbbf24; margin-bottom: 1rem;'>📈 Wykresy</h3>
            <p style='color: #cccccc; font-size: 1rem;'>Wizualizacja wzrostu kapitału i kosztów w czasie</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='card-green'>
            <h3 style='color: #4ade80; margin-bottom: 1rem;'>🎯 Planowanie</h3>
            <p style='color: #cccccc; font-size: 1rem;'>Optymalizacja strategii finansowej na przyszłość</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-info'>
        <h2 style='color: #60a5fa; margin-bottom: 1.5rem;'>🌟 Jak to działa?</h2>
        <p style='font-size: 1.1rem; color: #cccccc; line-height: 1.6;'>
            <strong>1.</strong> Wprowadź swoje dane w panelu po lewej stronie<br>
            <strong>2.</strong> Kliknij przycisk "OBLICZ EMERYTURĘ"<br>
            <strong>3.</strong> Analizuj wyniki i dostosuj swoją strategię!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Buy Me A Coffee button
    st.markdown("""
    <div class='coffee-container'>
        <p style='margin-bottom: 1rem; font-size: 0.9rem;'>
            ☕ Jeśli ten kalkulator pomógł Ci w planowaniu emerytury, rozważ wsparcie projektu!
        </p>
        <a href="https://www.buymeacoffee.com/gons" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                 alt="Buy Me A Coffee" 
                 style="height: 60px !important;width: 217px !important;" >
        </a>
    </div>
    """, unsafe_allow_html=True)

if calculate_button:
    with st.spinner('🔄 Obliczam wiek emerytury i tworzę wykresy... ⏳'):
        age, kapital_po_emeryturze, chart, capital_timeline, cost_timeline = calculate_retirement_age(
            current_age=current_age,
            monthly_contribution=monthly_contrib,
            annual_investment_return=annual_return,
            death_age=projected_lifespan,
            inflation=inflation,
            retirement_value=annual_expenses,
            starting_capital=capital,
        )
    
    if age:
        # Beautiful success message
        st.markdown(f"""
        <div class='success-box'>
            🎉 GRATULACJE! 🎉<br>
            Możesz przejść na emeryturę w wieku <strong>{age} lat</strong>!<br>
            To już za <strong>{age - current_age} lat</strong>!
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics in beautiful cards
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='card-metric-blue'>
                <h3 style='color: #60a5fa; margin-bottom: 0.5rem;'>💰 Kapitał końcowy</h3>
                <h2 style='color: #ffffff; font-size: 1.8rem;'>{kapital_po_emeryturze:,.0f} PLN</h2>
                <p style='color: #cccccc;'>Pozostanie po śmierci</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            years_to_retirement = age - current_age
            total_invested = years_to_retirement * monthly_contrib * 12 + capital
            st.markdown(f"""
            <div class='card-metric-orange'>
                <h3 style='color: #fbbf24; margin-bottom: 0.5rem;'>📅 Lata do emerytury</h3>
                <h2 style='color: #ffffff; font-size: 1.8rem;'>{years_to_retirement} lat</h2>
                <p style='color: #cccccc;'>Czas na oszczędzanie</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class='card-metric-green'>
                <h3 style='color: #4ade80; margin-bottom: 0.5rem;'>💸 Całkowita inwestycja</h3>
                <h2 style='color: #ffffff; font-size: 1.8rem;'>{total_invested:,.0f} PLN</h2>
                <p style='color: #cccccc;'>Łączne wpłaty</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Beautiful separator
        st.markdown("<hr style='margin: 3rem 0; border: 2px solid #404040;'>", unsafe_allow_html=True)
        
        # Capital over time chart
        if capital_timeline:
            st.markdown("""
            <div class='chart-container'>
                <h2 style='color: #60a5fa; font-size: 2rem; margin-bottom: 0.5rem;'>📈 Kapitał w czasie</h2>
                <p style='color: #cccccc; font-size: 1.1rem;'>Zobacz jak rośnie Twoja wartość netto!</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.spinner('🎨 Tworzę wykres kapitału w czasie...'):
                # Create DataFrame for the chart
                df = pd.DataFrame(capital_timeline)
                
                # Separate data by phase
                accumulation_data = df[df['phase'] == 'Accumulation'].set_index('age')['capital']
                retirement_data = df[df['phase'] == 'Retirement'].set_index('age')['capital']
                
                # Create chart data with both phases
                chart_data = pd.DataFrame({
                    'Faza akumulacji': accumulation_data,
                    'Faza emerytury': retirement_data
                })
                
                # Display the line chart with colored series
                st.line_chart(chart_data)
            
            # Add phase information
            st.write("**Legenda:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write("🟢 **Faza akumulacji** - oszczędzanie do emerytury")
            with col2:
                st.write("🔴 **Faza emerytury** - wydawanie kapitału")
            
            # Show key milestones
            st.write("**Kluczowe punkty:**")
            retirement_capital = df[df['phase'] == 'Accumulation']['capital'].iloc[-1] if len(df[df['phase'] == 'Accumulation']) > 0 else 0
            st.write(f"• Kapitał w momencie przejścia na emeryturę: {retirement_capital:,.0f} PLN")
            max_capital = df['capital'].max()
            max_capital_age = df[df['capital'] == max_capital]['age'].iloc[0]
            st.write(f"• Maksymalny kapitał: {max_capital:,.0f} PLN w wieku {max_capital_age} lat")
        
        # Beautiful separator
        st.markdown("<hr style='margin: 3rem 0; border: 2px solid #404040;'>", unsafe_allow_html=True)
        
        # Monthly costs over time chart
        if cost_timeline:
            st.markdown("""
            <div class='chart-container'>
                <h2 style='color: #fbbf24; font-size: 2rem; margin-bottom: 0.5rem;'>💸 Miesięczne koszty w czasie</h2>
                <p style='color: #cccccc; font-size: 1.1rem;'>Wpływ inflacji na Twoje wydatki</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.spinner('📊 Tworzę wykres kosztów w czasie...'):
                # Create DataFrame for the costs chart
                cost_df = pd.DataFrame(cost_timeline)
                
                # Separate data by phase for costs
                accumulation_costs = cost_df[cost_df['phase'] == 'Accumulation'].set_index('age')['monthly_cost']
                retirement_costs = cost_df[cost_df['phase'] == 'Retirement'].set_index('age')['monthly_cost']
                
                # Create chart data with both phases
                cost_chart_data = pd.DataFrame({
                    'Koszty podczas akumulacji': accumulation_costs,
                    'Koszty podczas emerytury': retirement_costs
                })
                
                # Display the line chart
                st.line_chart(cost_chart_data)
            
            # Show cost information
            st.write("**Informacje o kosztach:**")
            current_monthly_cost = annual_expenses
            retirement_monthly_cost = cost_df[cost_df['phase'] == 'Retirement']['monthly_cost'].iloc[0] if len(cost_df[cost_df['phase'] == 'Retirement']) > 0 else current_monthly_cost
            final_monthly_cost = cost_df[cost_df['phase'] == 'Retirement']['monthly_cost'].iloc[-1] if len(cost_df[cost_df['phase'] == 'Retirement']) > 0 else current_monthly_cost
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Obecne koszty miesięczne", f"{current_monthly_cost:,.0f} PLN")
            with col2:
                st.metric("Koszty w momencie emerytury", f"{retirement_monthly_cost:,.0f} PLN", 
                         f"+{((retirement_monthly_cost/current_monthly_cost-1)*100):,.1f}%")
            with col3:
                st.metric("Koszty na koniec życia", f"{final_monthly_cost:,.0f} PLN",
                         f"+{((final_monthly_cost/current_monthly_cost-1)*100):,.1f}%")
            
            st.info(f"💡 **Wpływ inflacji:** Przy inflacji {inflation}% rocznie, Twoje koszty życia będą rosły każdego roku. "
                   f"To oznacza, że za {age - current_age} lat będziesz potrzebować {retirement_monthly_cost:,.0f} PLN miesięcznie "
                   f"zamiast obecnych {current_monthly_cost:,.0f} PLN, aby utrzymać ten sam standard życia.")
            
        # Beautiful separator
        st.markdown("<hr style='margin: 3rem 0; border: 2px solid #404040;'>", unsafe_allow_html=True)
        
        # Tworzenie wykresu danych z tabeli chart
        if chart:
            st.markdown("""
            <div class='chart-container'>
                <h2 style='color: #4ade80; font-size: 2rem; margin-bottom: 0.5rem;'>📊 Analiza scenariuszy emerytury</h2>
                <p style='color: #cccccc; font-size: 1.1rem;'>Porównanie różnych strategii emerytalnych</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.spinner('🔍 Tworzę wykres scenariuszy emerytury...'):
                # Przygotowanie danych do wykresu
                retirement_ages = [item[0] for item in chart]
                funds_depletion_ages = [item[1] for item in chart]
                
                # Tworzenie DataFrame dla wykresu
                chart_data = {
                    'Wiek przejścia na emeryturę': retirement_ages,
                    'Wiek wyczerpania funduszy': funds_depletion_ages
                }
                
                # Wykres liniowy
                st.line_chart(chart_data, x='Wiek przejścia na emeryturę', y='Wiek wyczerpania funduszy')
            
                    
            # Beautiful separator before coffee button
            st.markdown("<hr style='margin: 3rem 0; border: 2px solid #404040;'>", unsafe_allow_html=True)
            
            # Buy Me A Coffee button on results page
            st.markdown("""
            <div class='coffee-container'>
                <p style='margin-bottom: 1rem; font-size: 0.95rem;'>
                    🎯 <strong>Czy te analizy pomogły Ci w planowaniu emerytury?</strong><br>
                    Wspomóż rozwój kalkulatora i dodawanie nowych funkcji!
                </p>
                <a href="https://www.buymeacoffee.com/gons" target="_blank">
                    <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
                        alt="Buy Me A Coffee" 
                        style="height: 60px !important;width: 217px !important;" >
                </a>
            </div>
            """, unsafe_allow_html=True)
            # Dodatkowa tabela z danymi
            st.subheader("📋 Szczegółowe dane")
            
            with st.spinner('Przygotowuję szczegółowe dane...'):
                # Tworzenie danych tabeli
                table_data = {
                    'Wiek przejścia na emeryturę': retirement_ages,
                    'Wiek wyczerpania funduszy': funds_depletion_ages,
                    'Lata na emeryturze': [funds_age - ret_age for ret_age, funds_age in chart]
                }
                st.dataframe(table_data)

    else:
        st.markdown("""
        <div class='error-card'>
            <h2 style='color: #f87171; margin-bottom: 1rem;'>😞 Ups! Coś nie gra...</h2>
            <p style='font-size: 1.1rem; color: #fca5a5; margin-bottom: 1rem;'>Z podanymi parametrami przejście na emeryturę nie jest możliwe.</p>
            <p style='color: #fca5a5; font-weight: bold; margin-bottom: 0.5rem;'>💡 Spróbuj:</p>
            <p style='color: #fca5a5; line-height: 1.6;'>
            • Zwiększyć miesięczne inwestycje<br>
            • Zmniejszyć miesięczne wydatki<br>
            • Wydłużyć okres oszczędzania<br>
            • Zwiększyć oczekiwaną stopę zwrotu
            </p>
        </div>
        """, unsafe_allow_html=True)