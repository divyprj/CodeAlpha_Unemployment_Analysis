import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import download_data
import analysis

# Configure Streamlit page options
st.set_page_config(
    page_title="India Unemployment Analysis Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling with dark theme and glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Global styles */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main container background */
    .stApp {
        background-color: #0d0e15;
        color: #e2e8f0;
    }
    
    /* Styling sidebar */
    section[data-testid="stSidebar"] {
        background-color: #12131e !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Header card */
    .header-box {
        background: linear-gradient(135deg, rgba(31, 38, 103, 0.3) 0%, rgba(109, 40, 217, 0.15) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .header-title {
        background: linear-gradient(to right, #38bdf8, #a78bfa, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    /* Glassmorphism KPI cards */
    .kpi-card {
        background: rgba(22, 28, 45, 0.6);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: rgba(167, 139, 250, 0.4);
    }
    .kpi-val {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0.5rem 0;
        background: linear-gradient(to right, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-val-rose {
        background: linear-gradient(to right, #f472b6, #fb7185) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    .kpi-label {
        color: #94a3b8;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1rem;
        font-weight: 600;
    }
    
    /* Insight/Tip Boxes */
    .insight-box {
        background: rgba(16, 185, 129, 0.05);
        border-left: 4px solid #10b981;
        border-radius: 4px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .policy-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .policy-title {
        font-weight: 600;
        color: #38bdf8;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Self-healing dataset download check
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)
if not os.path.exists(os.path.join(data_dir, "Unemployment in India.csv")) or \
   not os.path.exists(os.path.join(data_dir, "Unemployment_Rate_upto_11_2020.csv")):
    with st.spinner("Downloading dataset files..."):
        download_data.main()

# Load cleaned data
df_india, df_upto_2020 = analysis.load_data()

# Sidebar Setup
st.sidebar.markdown("<h2 style='text-align: center; color: #a78bfa; font-weight: 800;'>CONTROLS</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Navigation option
page = st.sidebar.radio(
    "Select Section:",
    ["Dashboard Overview", "National Trends", "State Breakdown", "COVID-19 Impact", "Rural vs Urban Analysis", "Policy Insights"]
)

# Sidebar metadata / indicators
st.sidebar.markdown("---")
st.sidebar.markdown("### Dataset Summary")
if df_india is not None:
    st.sidebar.caption(f"📅 Area Dataset Range: {df_india['Date'].min().strftime('%b %Y')} - {df_india['Date'].max().strftime('%b %Y')}")
if df_upto_2020 is not None:
    st.sidebar.caption(f"📅 Regional Dataset Range: {df_upto_2020['Date'].min().strftime('%b %Y')} - {df_upto_2020['Date'].max().strftime('%b %Y')}")

# Header markup
st.markdown("""
<div class="header-box">
    <div class="header-title">Unemployment in India</div>
    <div class="header-subtitle">Data cleaning, exploration, and visual analysis of the employment trends before and during the COVID-19 pandemic.</div>
</div>
""", unsafe_allow_html=True)

# ----------------- SECTION: Dashboard Overview -----------------
if page == "Dashboard Overview":
    st.subheader("Welcome to the Analytics Suite")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        This dashboard presents a structured analysis of unemployment in India between **2019 and 2020**. 
        By cleaning and aggregating economic indicators compiled by the **Centre for Monitoring Indian Economy (CMIE)**, we identify key seasonal behaviors, analyze spatial disparities, and measure the severe economic shock of the **COVID-19 nationwide lockdowns** starting in March 2020.
        
        ### Key Analytical Goals:
        * 🔍 **Clean and structure** the raw datasets (handle whitespace, parse dates, eliminate null values).
        * 📈 **Track national employment trends** across 2019 and 2020.
        * 🗺️ **State-wise mapping** of unemployment hotspots.
        * 🦠 **Isolate & quantify the lockdown shock** (Pre-COVID vs. Peak-COVID).
        * 🏢 **Examine Rural vs. Urban disparities**.
        """)
        
        # Show sample data preview
        st.markdown("### Data Sample Preview (`Unemployment_Rate_upto_11_2020.csv`)")
        if df_upto_2020 is not None:
            st.dataframe(df_upto_2020.head(5), use_container_width=True)
    
    with col2:
        st.markdown("### Key Statistics")
        if df_upto_2020 is not None:
            avg_unemp = df_upto_2020['Estimated Unemployment Rate (%)'].mean()
            max_unemp = df_upto_2020['Estimated Unemployment Rate (%)'].max()
            avg_labour = df_upto_2020['Estimated Labour Participation Rate (%)'].mean()
            
            st.markdown(f"""
            <div class="kpi-card" style="margin-bottom: 1rem;">
                <div class="kpi-label">Average Unemployment Rate</div>
                <div class="kpi-val">{avg_unemp:.2f}%</div>
                <div class="header-subtitle">Overall Average (2019-2020)</div>
            </div>
            <div class="kpi-card" style="margin-bottom: 1rem;">
                <div class="kpi-label">Peak Unemployment Spike</div>
                <div class="kpi-val-rose kpi-val">{max_unemp:.2f}%</div>
                <div class="header-subtitle">Recorded State-level Peak</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Labour Participation</div>
                <div class="kpi-val">{avg_labour:.2f}%</div>
                <div class="header-subtitle">Estimated Rate</div>
            </div>
            """, unsafe_allow_html=True)

# ----------------- SECTION: National Trends -----------------
elif page == "National Trends":
    st.subheader("📈 National Employment Trends (2019 - 2020)")
    
    if df_upto_2020 is not None:
        # Group by date to see national averages over time
        national_timeline = df_upto_2020.groupby('Date').agg({
            'Estimated Unemployment Rate (%)': 'mean',
            'Estimated Employed': 'sum',
            'Estimated Labour Participation Rate (%)': 'mean'
        }).reset_index()
        
        # Custom Plotly Theme configurations
        plotly_layout_opts = dict(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)'),
            legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.05)')
        )
        
        # Trend Chart 1: Unemployment Rate
        fig_unemp = go.Figure()
        fig_unemp.add_trace(go.Scatter(
            x=national_timeline['Date'], 
            y=national_timeline['Estimated Unemployment Rate (%)'],
            mode='lines+markers',
            name='Unemployment Rate (%)',
            line=dict(color='#a78bfa', width=3),
            marker=dict(size=6, color='#60a5fa'),
            hovertemplate="<b>Date</b>: %{x|%b %Y}<br><b>Avg Rate</b>: %{y:.2f}%<extra></extra>"
        ))
        
        # Add shape indicating COVID lockdown start
        fig_unemp.add_vrect(
            x0="2020-03-24", x1="2020-05-31",
            fillcolor="rgba(244, 114, 182, 0.15)", opacity=0.5,
            layer="below", line_width=0,
            annotation_text="Strict Lockdown Period",
            annotation_position="top left",
            annotation_font=dict(color="#f472b6", size=11)
        )
        
        fig_unemp.update_layout(
            title="National Average Unemployment Rate Over Time",
            xaxis_title="Timeline",
            yaxis_title="Unemployment Rate (%)",
            height=450,
            margin=dict(t=50, b=50, l=50, r=50),
            **plotly_layout_opts
        )
        
        st.plotly_chart(fig_unemp, use_container_width=True)
        
        # Trend Chart 2: Employed Population vs Labour Participation
        col1, col2 = st.columns(2)
        
        with col1:
            fig_employed = go.Figure()
            fig_employed.add_trace(go.Bar(
                x=national_timeline['Date'],
                y=national_timeline['Estimated Employed'] / 1e6, # Convert to millions
                name='Estimated Employed',
                marker_color='#38bdf8',
                hovertemplate="<b>Date</b>: %{x|%b %Y}<br><b>Employed</b>: %{y:.2f}M<extra></extra>"
            ))
            fig_employed.update_layout(
                title="Total Estimated Employed (Millions) Over Time",
                xaxis_title="Timeline",
                yaxis_title="Employed (Millions)",
                height=350,
                margin=dict(t=50, b=50, l=50, r=50),
                **plotly_layout_opts
            )
            st.plotly_chart(fig_employed, use_container_width=True)
            
        with col2:
            fig_lp = go.Figure()
            fig_lp.add_trace(go.Scatter(
                x=national_timeline['Date'],
                y=national_timeline['Estimated Labour Participation Rate (%)'],
                mode='lines+markers',
                line=dict(color='#34d399', width=2),
                marker=dict(size=5),
                hovertemplate="<b>Date</b>: %{x|%b %Y}<br><b>Participation Rate</b>: %{y:.2f}%<extra></extra>"
            ))
            fig_lp.update_layout(
                title="Avg Labour Participation Rate (%) Over Time",
                xaxis_title="Timeline",
                yaxis_title="Labour Participation Rate (%)",
                height=350,
                margin=dict(t=50, b=50, l=50, r=50),
                **plotly_layout_opts
            )
            st.plotly_chart(fig_lp, use_container_width=True)
            
        st.markdown("""
        <div class="insight-box">
            💡 <b>Insight:</b> The line charts clearly depict a stable national unemployment rate around 7% - 9% throughout 2019 and early 2020. 
            However, when the nationwide COVID-19 lockdowns were declared in <b>late March 2020</b>, the unemployment rate spiked dramatically, 
            reaching a peak average of over <b>20% in April 2020</b>. 
            Concurrently, the total employed population dropped by tens of millions, illustrating the immediate freeze in economic activities.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Regional dataset (Unemployment_Rate_upto_11_2020.csv) was not found or failed to load.")

# ----------------- SECTION: State Breakdown -----------------
elif page == "State Breakdown":
    st.subheader("🗺️ State-wise Unemployment Analysis")
    
    if df_upto_2020 is not None:
        # State filter
        states = sorted(df_upto_2020['Region'].unique())
        selected_states = st.multiselect("Filter by State(s):", states, default=states[:5])
        
        if not selected_states:
            st.warning("Please select at least one state.")
        else:
            # Filtered dataframe
            df_filtered = df_upto_2020[df_upto_2020['Region'].isin(selected_states)]
            
            # Line Chart: Selected States Comparison
            fig_states = px.line(
                df_filtered,
                x='Date',
                y='Estimated Unemployment Rate (%)',
                color='Region',
                title="Unemployment Rate Timeline comparison among Selected States",
                labels={'Estimated Unemployment Rate (%)': 'Unemployment Rate (%)', 'Date': 'Date', 'Region': 'State'},
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_states.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                height=450
            )
            st.plotly_chart(fig_states, use_container_width=True)
            
            # State ranking during COVID lockdown
            st.markdown("### 🏆 Highest State Unemployment Rates (Lockdown Period Apr-Oct 2020)")
            lockdown_start = pd.to_datetime('2020-04-01')
            df_lockdown = df_upto_2020[df_upto_2020['Date'] >= lockdown_start]
            state_ranking = df_lockdown.groupby('Region')['Estimated Unemployment Rate (%)'].mean().reset_index()
            state_ranking = state_ranking.sort_values(by='Estimated Unemployment Rate (%)', ascending=False)
            
            fig_ranking = px.bar(
                state_ranking,
                x='Region',
                y='Estimated Unemployment Rate (%)',
                title="Average Unemployment Rate by State during the COVID-19 Lockdown Period (Apr - Oct 2020)",
                color='Estimated Unemployment Rate (%)',
                color_continuous_scale='Picnic',
                labels={'Region': 'State', 'Estimated Unemployment Rate (%)': 'Avg Unemployment (%)'}
            )
            fig_ranking.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
                height=450
            )
            st.plotly_chart(fig_ranking, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
                💡 <b>Key Finding:</b> States like <b>Haryana, Tripura, and Jharkhand</b> experienced the most severe average unemployment rates 
                exceeding 25-30% during the pandemic lockdowns. Northern and eastern regions with large migrant worker populations 
                suffered disproportionately compared to other states.
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Regional dataset was not found.")

# ----------------- SECTION: COVID-19 Impact -----------------
elif page == "COVID-19 Impact":
    st.subheader("🦠 Quantifying the COVID-19 Shock")
    
    if df_upto_2020 is not None:
        # Pre and post lockdown calculations
        df_impact, impact_table = analysis.analyze_covid_impact(df_upto_2020)
        state_comparison = analysis.get_statewise_comparison(df_upto_2020)
        
        # Display KPI cards comparing Pre vs Post lockdown rates
        col1, col2, col3 = st.columns(3)
        
        pre_rate = impact_table.loc[impact_table['Period'].str.contains('Pre'), 'Avg Unemployment Rate (%)'].values[0]
        lock_rate = impact_table.loc[impact_table['Period'].str.contains('Lockdown'), 'Avg Unemployment Rate (%)'].values[0]
        abs_change = lock_rate - pre_rate
        
        with col1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Pre-Lockdown Average</div>
                <div class="kpi-val">{pre_rate:.2f}%</div>
                <div class="header-subtitle">Before April 2020</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Lockdown Average</div>
                <div class="kpi-val-rose kpi-val">{lock_rate:.2f}%</div>
                <div class="header-subtitle">April - October 2020</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Net Absolute Spike</div>
                <div class="kpi-val-rose kpi-val">+{abs_change:.2f}%</div>
                <div class="header-subtitle">Lockdown minus Pre-lockdown</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("### Period Summary Table")
        st.dataframe(impact_table.style.format({
            'Avg Unemployment Rate (%)': '{:.2f}%',
            'Min Unemployment Rate (%)': '{:.2f}%',
            'Max Unemployment Rate (%)': '{:.2f}%',
            'Std Dev Unemployment': '{:.2f}',
            'Avg Employed': '{:,.0f}',
            'Total Employed (Sum)': '{:,.0f}',
            'Avg Labour Participation Rate (%)': '{:.2f}%'
        }), use_container_width=True)
        
        # State-by-State Impact Visualizer
        st.markdown("### State-by-State Percentage Point Increase in Unemployment")
        
        fig_increase = px.bar(
            state_comparison,
            x='Region',
            y='Absolute Increase (%)',
            title="Absolute Increase in Unemployment Rate (Percentage Points) Pre-COVID vs During-COVID",
            color='Absolute Increase (%)',
            color_continuous_scale='Reds',
            labels={'Region': 'State', 'Absolute Increase (%)': 'Increase (Percentage Points)'}
        )
        fig_increase.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            height=500
        )
        st.plotly_chart(fig_increase, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            💡 <b>Shock Analysis:</b> Nationally, the average unemployment rate jumped from <b>8.02%</b> to <b>14.97%</b> (an absolute increase of <b>6.96 percentage points</b>). 
            At the state level, the spike was highly uneven: states like <b>Puducherry, Jharkhand, and Haryana</b> saw absolute rate increases of <b>15-20%+</b>, 
            representing severe regional distress. Conversely, states like <b>Sikkim and Assam</b> showed much lower absolute increases, suggesting either 
            local resilience or underreporting.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Dataset was not found.")

# ----------------- SECTION: Rural vs Urban Analysis -----------------
elif page == "Rural vs Urban Analysis":
    st.subheader("🏢 Rural vs Urban Unemployment Dynamics")
    st.markdown("This analysis utilizes the `Unemployment in India.csv` dataset, which contains separate classifications for Rural and Urban regions.")
    
    if df_india is not None:
        # Group by Area and Date
        area_trends = df_india.groupby(['Date', 'Area']).agg({
            'Estimated Unemployment Rate (%)': 'mean',
            'Estimated Employed': 'mean',
            'Estimated Labour Participation Rate (%)': 'mean'
        }).reset_index()
        
        # Plotly plot comparing Rural vs Urban over time
        fig_area = px.line(
            area_trends,
            x='Date',
            y='Estimated Unemployment Rate (%)',
            color='Area',
            markers=True,
            title="Comparison of Rural vs Urban Unemployment Rates over Time",
            labels={'Estimated Unemployment Rate (%)': 'Unemployment Rate (%)', 'Date': 'Date', 'Area': 'Area Type'},
            color_discrete_map={'Rural': '#34d399', 'Urban': '#f472b6'}
        )
        fig_area.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#94a3b8',
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            height=450
        )
        st.plotly_chart(fig_area, use_container_width=True)
        
        # Breakdown statistics
        st.markdown("### Average Rates by Area")
        area_summary = df_india.groupby('Area').agg({
            'Estimated Unemployment Rate (%)': ['mean', 'max'],
            'Estimated Labour Participation Rate (%)': 'mean'
        }).reset_index()
        area_summary.columns = ['Area', 'Avg Unemployment (%)', 'Max Unemployment (%)', 'Avg Labour Participation (%)']
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(area_summary.style.format({
                'Avg Unemployment (%)': '{:.2f}%',
                'Max Unemployment (%)': '{:.2f}%',
                'Avg Labour Participation (%)': '{:.2f}%'
            }), use_container_width=True)
            
        with col2:
            fig_pie = px.pie(
                area_summary,
                values='Avg Unemployment (%)',
                names='Area',
                title='Proportion of Average Unemployment Rate (Rural vs Urban)',
                color='Area',
                color_discrete_map={'Rural': '#34d399', 'Urban': '#f472b6'},
                hole=0.4
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#94a3b8',
                height=250,
                margin=dict(t=40, b=0, l=0, r=0)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.markdown("""
        <div class="insight-box">
            💡 <b>Rural vs Urban Highlights:</b> 
            Historically, <b>Urban areas</b> maintain a consistently higher base rate of unemployment compared to <b>Rural areas</b>. 
            During the lockdown peak (April-May 2020), both sectors saw severe spikes, but Urban unemployment reached higher extremes 
            (exceeding 25% average). Urban economies were harder hit due to their heavy dependence on construction, hospitality, 
            retail, and factory sectors, which came to a complete halt, whereas rural agriculture was partially insulated as an essential service.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Area-specific dataset (Unemployment in India.csv) was not found or failed to load.")

# ----------------- SECTION: Policy Insights -----------------
elif page == "Policy Insights":
    st.subheader("💡 Policy Insights & Economic Recommendations")
    
    st.markdown("""
    The analysis of the 2019-2020 unemployment data provides critical takeaways that can help shape policy responses to future economic crises.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="policy-card">
            <div class="policy-title">🛠️ 1. Strengthen Rural Safety Nets</div>
            <div>
                The relative stability of the rural labor market during the lockdown highlights the buffer capacity of agriculture. 
                Expanding scheme coverage under <b>MGNREGA</b> (Mahatma Gandhi National Rural Employment Guarantee Act) and ensuring 
                swift payments can alleviate rural financial stress and support migrant workers returning home during crises.
            </div>
        </div>
        
        <div class="policy-card">
            <div class="policy-title">🏙️ 2. Design Urban Job Guarantees</div>
            <div>
                Urban areas suffered a massive, sustained hit to employment during lockdowns. Policymakers should consider implementing 
                an <b>Urban Job Guarantee Scheme</b> focused on green municipal works, sanitation, public health infrastructure, and 
                social services to support urban informal workers.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="policy-card">
            <div class="policy-title">🚀 3. Targeted Regional Fiscal Assistance</div>
            <div>
                The state-wise variance in lockdown spikes shows that a uniform policy might not be optimal. Heavy-hit industrial 
                and labor-exporting states like <b>Haryana, Jharkhand, and Bihar</b> require targeted industrial incentives, credit guarantees 
                for MSMEs, and localized vocational rehabilitation programs to encourage job creation.
            </div>
        </div>
        
        <div class="policy-card">
            <div class="policy-title">📋 4. Skills Rescaling and Digital Infrastructure</div>
            <div>
                A drop in labor participation can be mitigated by investing in digital literacy and remote work infrastructure. 
                Providing subsidized digital training to youth in transition can buffer against massive disruptions in high-contact physical service sectors.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    ---
    ### Conclusions
    The COVID-19 pandemic highlighted the vulnerability of India's informal labor structure. Data-driven interventions focusing on 
    safety nets, urban employment support, and state-targeted fiscal measures are crucial to building a resilient, shock-resistant economy.
    """)
