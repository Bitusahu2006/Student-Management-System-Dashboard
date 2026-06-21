import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os
import warnings

warnings.filterwarnings('ignore')

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Student Management Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    /* Main app styling */
    .main {
        padding: 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        padding: 30px;
        margin-bottom: 30px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
        animation: slideIn 0.5s ease-out;
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header p {
        margin: 10px 0 0 0;
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    
    .kpi-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
    }
    
    .kpi-value {
        font-size: 40px;
        font-weight: bold;
        margin: 15px 0;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .kpi-label {
        font-size: 14px;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8em;
        font-weight: bold;
        color: #667eea;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 30px;
        margin-top: 50px;
        border-top: 2px solid #e0e0e0;
        color: #666;
        font-size: 12px;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 10px;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 15px 0;
        border-left: 4px solid #667eea;
    }
    
    /* Image gallery */
    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .gallery-item {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        background: white;
    }
    
    .gallery-item:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    
    .gallery-item img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 15px;
    }
    
    /* Stat badge */
    .stat-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(245, 87, 108, 0.3);
    }
    
    .success-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(79, 172, 254, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================
# UTILITY FUNCTIONS
# =====================================================

@st.cache_data
def load_data(filepath, mtime=None):
    
    try:
        df = pd.read_csv(filepath)
        
        # Validate required columns
        required_columns = [
            'Student_ID', 'Name', 'Age', 'Gender', 'Department', 
            'City', 'Attendance_Percentage', 'CGPA', 'Total_Marks'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
            return None
        
        # Data cleaning
        df['Department'] = df['Department'].str.strip()
        df['City'] = df['City'].str.strip()
        df['Gender'] = df['Gender'].str.strip()
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        df['CGPA'] = pd.to_numeric(df['CGPA'], errors='coerce')
        df['Attendance_Percentage'] = pd.to_numeric(df['Attendance_Percentage'], errors='coerce')
        df['Total_Marks'] = pd.to_numeric(df['Total_Marks'], errors='coerce')
        
        return df
    
    except FileNotFoundError:
        st.error(f"❌ Dataset not found at: {filepath}")
        return None
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None


def create_age_range_bins(df):
    """Create age range bins for filtering."""
    if df['Age'].notna().any():
        return pd.cut(df['Age'], bins=[0, 18, 20, 22, 25, 100], 
                      labels=['<18', '18-20', '20-22', '22-25', '25+'])
    return None


def apply_filters(df, gender_filter, dept_filter, city_filter, age_range_filter):
    """Apply all filters to the dataframe."""
    filtered_df = df.copy()
    
    if gender_filter:
        filtered_df = filtered_df[filtered_df['Gender'].isin(gender_filter)]
    
    if dept_filter:
        filtered_df = filtered_df[filtered_df['Department'].isin(dept_filter)]
    
    if city_filter:
        filtered_df = filtered_df[filtered_df['City'].isin(city_filter)]
    
    if age_range_filter:
        age_bins = create_age_range_bins(df)
        if age_bins is not None:
            filtered_age_ranges = pd.cut(filtered_df['Age'], bins=[0, 18, 20, 22, 25, 100],
                                        labels=['<18', '18-20', '20-22', '22-25', '25+'])
            filtered_df = filtered_df[filtered_age_ranges.isin(age_range_filter)]
    
    return filtered_df


def get_kpi_metrics(df):
    """Calculate key performance indicators."""
    metrics = {
        'total_students': len(df),
        'avg_cgpa': df['CGPA'].mean(),
        'avg_attendance': df['Attendance_Percentage'].mean(),
        'total_departments': df['Department'].nunique(),
        'total_cities': df['City'].nunique()
    }
    return metrics


def download_csv(df):
    """Generate CSV download link."""
    csv = df.to_csv(index=False)
    return csv


# =====================================================
# DATA LOADING
# =====================================================

# Get the directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_dir, 'student_management_clean.csv')

# Compute dataset modification time and load data (forces cache invalidation when file changes)
dataset_mtime = None
if os.path.exists(dataset_path):
    try:
        dataset_mtime = os.path.getmtime(dataset_path)
    except Exception:
        dataset_mtime = None

# Load data (pass mtime so cached value updates when file changes)
df = load_data(dataset_path, dataset_mtime)

if df is not None:
    # =====================================================
    # SIDEBAR - FILTERS
    # =====================================================
    
    with st.sidebar:
        st.title("🔍 Filters")
        # Reload button to pick up external CSV updates
        if st.button("🔄 Reload dataset"):
            try:
                st.cache_data.clear()
            except Exception:
                pass
            st.experimental_rerun()

        st.markdown("---")
        
        # Gender Filter
        gender_options = sorted(df['Gender'].dropna().unique().tolist())
        gender_filter = st.multiselect(
            "Gender",
            options=gender_options,
            default=gender_options,
            help="Select one or more genders to filter"
        )
        
        # Department Filter
        dept_options = sorted(df['Department'].dropna().unique().tolist())
        dept_filter = st.multiselect(
            "Department",
            options=dept_options,
            default=dept_options,
            help="Select one or more departments to filter"
        )
        
        # City Filter
        city_options = sorted(df['City'].dropna().unique().tolist())
        city_filter = st.multiselect(
            "City",
            options=city_options,
            default=city_options,
            help="Select one or more cities to filter"
        )
        
        # Age Range Filter
        age_range_options = ['<18', '18-20', '20-22', '22-25', '25+']
        age_range_filter = st.multiselect(
            "Age Range",
            options=age_range_options,
            default=age_range_options,
            help="Select one or more age ranges to filter"
        )
        
        st.markdown("---")
        st.markdown(f"**Active Filters:** {len(gender_filter)} Genders | {len(dept_filter)} Depts | {len(city_filter)} Cities | {len(age_range_filter)} Age Ranges")
    
    # Apply filters
    filtered_df = apply_filters(df, gender_filter, dept_filter, city_filter, age_range_filter)
    
    # =====================================================
    # MAIN CONTENT - HEADER
    # =====================================================
    
    st.markdown("""
        <div class="header">
            <h1>📊 Student Management Dashboard</h1>
            <p style="margin: 10px 0; font-size: 16px;">
                Comprehensive analysis and insights into student performance, demographics, and academic metrics
            </p>
            <div style="margin-top: 15px; font-size: 0.9em; opacity: 0.9;">
                ✨ Real-time Analytics | 📈 Advanced Insights | 🎯 Performance Metrics
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # =====================================================
    # KPI CARDS
    # =====================================================
    
    metrics = get_kpi_metrics(filtered_df)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 2em; margin-bottom: 10px;">👥</div>
                <div class="kpi-label">Total Students</div>
                <div class="kpi-value">{metrics['total_students']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 2em; margin-bottom: 10px;">📚</div>
                <div class="kpi-label">Average CGPA</div>
                <div class="kpi-value">{metrics['avg_cgpa']:.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 2em; margin-bottom: 10px;">📍</div>
                <div class="kpi-label">Average Attendance</div>
                <div class="kpi-value">{metrics['avg_attendance']:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 2em; margin-bottom: 10px;">🏢</div>
                <div class="kpi-label">Total Departments</div>
                <div class="kpi-value">{metrics['total_departments']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class="kpi-card">
                <div style="font-size: 2em; margin-bottom: 10px;">🌍</div>
                <div class="kpi-label">Total Cities</div>
                <div class="kpi-value">{metrics['total_cities']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # =====================================================
    # VISUALIZATIONS - ROW 1
    # =====================================================
    
    st.markdown("<h3 style='color: #667eea; margin-top: 30px;'>📈 Demographics Overview</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Gender Distribution
        gender_dist = filtered_df['Gender'].value_counts()
        fig_gender = px.pie(
            values=gender_dist.values,
            names=gender_dist.index,
            title="Gender Distribution",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_gender.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        # Department Wise Student Count
        dept_dist = filtered_df['Department'].value_counts().sort_values(ascending=False)
        fig_dept = px.bar(
            x=dept_dist.index,
            y=dept_dist.values,
            title="Department Wise Student Count",
            labels={'x': 'Department', 'y': 'Count'},
            color=dept_dist.values,
            color_continuous_scale='Viridis'
        )
        fig_dept.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_dept, use_container_width=True)
    
    with col3:
        # City Wise Student Count
        city_dist = filtered_df['City'].value_counts().sort_values(ascending=False).head(10)
        fig_city = px.bar(
            x=city_dist.index,
            y=city_dist.values,
            title="Top 10 Cities by Student Count",
            labels={'x': 'City', 'y': 'Count'},
            color=city_dist.values,
            color_continuous_scale='Plasma'
        )
        fig_city.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_city, use_container_width=True)
    
    st.markdown("---")
    
    # =====================================================
    # VISUALIZATIONS - ROW 2
    # =====================================================
    
    st.markdown("<h3 style='color: #667eea; margin-top: 30px;'>📊 Academic Performance</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Age Distribution
        fig_age = px.histogram(
            filtered_df,
            x='Age',
            nbins=15,
            title="Age Distribution",
            labels={'Age': 'Age', 'count': 'Number of Students'},
            color_discrete_sequence=['#636EFA']
        )
        fig_age.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        # CGPA Distribution
        fig_cgpa = px.histogram(
            filtered_df,
            x='CGPA',
            nbins=20,
            title="CGPA Distribution",
            labels={'CGPA': 'CGPA', 'count': 'Number of Students'},
            color_discrete_sequence=['#00CC96']
        )
        fig_cgpa.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_cgpa, use_container_width=True)
    
    with col3:
        # Attendance Distribution
        fig_attend = px.histogram(
            filtered_df,
            x='Attendance_Percentage',
            nbins=20,
            title="Attendance Distribution",
            labels={'Attendance_Percentage': 'Attendance %', 'count': 'Number of Students'},
            color_discrete_sequence=['#EF553B']
        )
        fig_attend.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_attend, use_container_width=True)
    
    st.markdown("---")
    
    # =====================================================
    # VISUALIZATIONS - ROW 3
    # =====================================================
    
    st.markdown("<h3 style='color: #667eea; margin-top: 30px;'>🎯 Advanced Analytics</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Average CGPA by Department
        avg_cgpa_dept = filtered_df.groupby('Department')['CGPA'].mean().sort_values(ascending=False)
        fig_cgpa_dept = px.bar(
            x=avg_cgpa_dept.index,
            y=avg_cgpa_dept.values,
            title="Average CGPA by Department",
            labels={'x': 'Department', 'y': 'Average CGPA'},
            color=avg_cgpa_dept.values,
            color_continuous_scale='Blues'
        )
        fig_cgpa_dept.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig_cgpa_dept, use_container_width=True)
    
    with col2:
        # Attendance vs CGPA Scatter Plot
        fig_scatter1 = px.scatter(
            filtered_df,
            x='Attendance_Percentage',
            y='CGPA',
            title="Attendance vs CGPA Correlation",
            labels={'Attendance_Percentage': 'Attendance %', 'CGPA': 'CGPA'},
            color='CGPA',
            color_continuous_scale='Viridis',
            size='Total_Marks',
            hover_data=['Name', 'Department']
        )
        fig_scatter1.update_layout(height=400)
        st.plotly_chart(fig_scatter1, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Marks vs CGPA Scatter Plot
        if 'Total_Marks' in filtered_df.columns:
            fig_scatter2 = px.scatter(
                filtered_df,
                x='Total_Marks',
                y='CGPA',
                title="Total Marks vs CGPA Correlation",
                labels={'Total_Marks': 'Total Marks', 'CGPA': 'CGPA'},
                color='Attendance_Percentage',
                color_continuous_scale='Plasma',
                hover_data=['Name', 'Department', 'Gender']
            )
            fig_scatter2.update_layout(height=400)
            st.plotly_chart(fig_scatter2, use_container_width=True)
    
    with col2:
        # Box Plot: CGPA by Gender
        fig_box = px.box(
            filtered_df,
            x='Gender',
            y='CGPA',
            title="CGPA Distribution by Gender",
            labels={'Gender': 'Gender', 'CGPA': 'CGPA'},
            color='Gender',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    
    st.markdown("---")
    
    # =====================================================
    # IMAGE GALLERY - GENERATED VISUALIZATIONS
    # =====================================================
    
    st.markdown("<h2 style='text-align: center; color: #667eea;'>🖼️ Visualization Gallery</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; font-size: 0.95em;'>High-quality generated images for reports and presentations</p>", unsafe_allow_html=True)
    
    # Check if images directory exists
    images_dir = os.path.join(current_dir, 'images')
    
    if os.path.exists(images_dir):
        # Create tabs for different image categories
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard Views", "📈 Analytics", "🎯 Advanced Analysis"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if os.path.exists(os.path.join(images_dir, 'dashboard_home.png')):
                    st.image(os.path.join(images_dir, 'dashboard_home.png'), caption="Full Dashboard Overview", use_container_width=True)
            
            with col2:
                if os.path.exists(os.path.join(images_dir, 'kpi_cards.png')):
                    st.image(os.path.join(images_dir, 'kpi_cards.png'), caption="KPI Cards", use_container_width=True)
            
            with col3:
                if os.path.exists(os.path.join(images_dir, 'filtered_dashboard.png')):
                    st.image(os.path.join(images_dir, 'filtered_dashboard.png'), caption="Filtered Dashboard", use_container_width=True)
        
        with tab2:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if os.path.exists(os.path.join(images_dir, 'gender_distribution.png')):
                    st.image(os.path.join(images_dir, 'gender_distribution.png'), caption="Gender Distribution", use_container_width=True)
            
            with col2:
                if os.path.exists(os.path.join(images_dir, 'age_distribution.png')):
                    st.image(os.path.join(images_dir, 'age_distribution.png'), caption="Age Distribution", use_container_width=True)
            
            with col3:
                if os.path.exists(os.path.join(images_dir, 'cgpa_distribution.png')):
                    st.image(os.path.join(images_dir, 'cgpa_distribution.png'), caption="CGPA Distribution", use_container_width=True)
        
        with tab3:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if os.path.exists(os.path.join(images_dir, 'department_analysis.png')):
                    st.image(os.path.join(images_dir, 'department_analysis.png'), caption="Department Analysis", use_container_width=True)
            
            with col2:
                if os.path.exists(os.path.join(images_dir, 'city_distribution.png')):
                    st.image(os.path.join(images_dir, 'city_distribution.png'), caption="City Distribution", use_container_width=True)
            
            with col3:
                if os.path.exists(os.path.join(images_dir, 'attendance_vs_cgpa.png')):
                    st.image(os.path.join(images_dir, 'attendance_vs_cgpa.png'), caption="Attendance vs CGPA", use_container_width=True)
        
        # Download gallery as zip
        st.markdown("---")
        st.success("✅ All images ready for download and presentations!")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.info("📸 9 high-quality images available")
        with col2:
            st.info("🎨 Professional visualizations")
        with col3:
            st.info("📊 Ready for reports & presentations")
    
    else:
        st.warning("⚠️ Image gallery not available. Run 'python generate_images.py' to generate images.")
    
    st.markdown("---")
    
    # =====================================================
    # DATA TABLE
    # =====================================================
    
    st.markdown("<h3 style='color: #667eea; margin-top: 30px;'>📋 Student Records</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search functionality
        search_term = st.text_input(
            "🔎 Search by Student Name or ID",
            placeholder="Type name or student ID..."
        )
    
    with col2:
        sort_column = st.selectbox(
            "Sort by",
            options=['Name', 'CGPA', 'Attendance_Percentage', 'Age', 'Department'],
            index=0
        )
    
    # Apply search filter
    if search_term:
        search_df = filtered_df[
            (filtered_df['Name'].str.contains(search_term, case=False, na=False)) |
            (filtered_df['Student_ID'].str.contains(search_term, case=False, na=False))
        ]
    else:
        search_df = filtered_df
    
    # Sort data
    search_df = search_df.sort_values(by=sort_column, ascending=False)
    
    # Display table
    display_columns = [
        'Student_ID', 'Name', 'Age', 'Gender', 'Department', 
        'City', 'Attendance_Percentage', 'CGPA', 'Total_Marks'
    ]
    
    available_columns = [col for col in display_columns if col in search_df.columns]
    
    st.dataframe(
        search_df[available_columns].style.format({
            'Attendance_Percentage': '{:.2f}%',
            'CGPA': '{:.2f}',
            'Total_Marks': '{:.2f}',
            'Age': '{:.0f}'
        }),
        use_container_width=True,
        height=400
    )
    
    st.markdown("---")
    
    # =====================================================
    # DOWNLOAD SECTION
    # =====================================================
    
    st.markdown("<h3 style='color: #667eea; margin-top: 30px;'>📥 Export Data</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download filtered data as CSV
        csv_filtered = search_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_filtered,
            file_name=f"student_data_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download the currently filtered and searched student data"
        )
    
    with col2:
        # Download all data as CSV
        csv_all = df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Data (CSV)",
            data=csv_all,
            file_name=f"student_data_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download the complete unfiltered dataset"
        )
    
    with col3:
        # Display summary statistics (all based on search_df which is displayed in table)
        # Filter out invalid values: CGPA should be 0-10, Attendance should be 0-100
        valid_cgpa = search_df[(search_df['CGPA'] >= 0) & (search_df['CGPA'] <= 10)]['CGPA']
        valid_attendance = search_df[(search_df['Attendance_Percentage'] >= 0) & (search_df['Attendance_Percentage'] <= 100)]['Attendance_Percentage']
        
        cgpa_min = valid_cgpa.min() if len(valid_cgpa) > 0 else 0
        cgpa_max = valid_cgpa.max() if len(valid_cgpa) > 0 else 0
        att_min = valid_attendance.min() if len(valid_attendance) > 0 else 0
        att_max = valid_attendance.max() if len(valid_attendance) > 0 else 0
        
        st.info(f"""
        📊 **Summary Statistics**
        - **Displayed Records:** {len(search_df)} of {len(df)} total
        - **Departments:** {search_df['Department'].nunique()}
        - **Cities:** {search_df['City'].nunique()}
        - **CGPA Range (valid):** {cgpa_min:.2f} - {cgpa_max:.2f}
        - **Attendance Range (valid):** {att_min:.2f}% - {att_max:.2f}%
        """)
    
    st.markdown("---")
    
    # =====================================================
    # FOOTER
    # =====================================================
    
    st.markdown("""
        <div class="footer">
            <p>🎓 <strong>Student Management Dashboard</strong> | Version 1.0.0</p>
            <p>Built with ❤️ using Streamlit | Data updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p>© 2024 Student Management System. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Failed to load the dashboard. Please ensure 'student_management_clean.csv' is in the application directory.")
