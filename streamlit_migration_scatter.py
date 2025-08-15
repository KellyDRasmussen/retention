import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="Migration Retention Analysis",
    page_icon="🌍",
    layout="wide"
)

@st.cache_data
def load_data():
    # Load the data
    immigration = pd.read_csv('immigration2024.csv', header=None, encoding='ISO-8859-1')
    immigration.columns = ['Citizenship', 'Immigration']
    emigration = pd.read_csv('emigration2024.csv', header=None, encoding='ISO-8859-1')
    emigration.columns = ['Citizenship', 'Emigration']
    
    # Merge the dataframes
    df = pd.merge(immigration, emigration, on='Citizenship')
    df['Net_migration'] = df['Immigration'] - df['Emigration']
    df['Retention_percentage'] = (df['Net_migration'] / df['Immigration']) * 100
    
    # Filter out countries with very low immigration
    df_filtered = df[df['Immigration'] >= 500].copy()
    
    # Define country groups
    eu_nordic_countries = [
        'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
        'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden', 'United Kingdom', 'Norway', 'Iceland'
    ]
    
    special_countries = ['USA', 'United Kingdom', 'Singapore', 'China', 'Japan', 
                        'Australia', 'Canada', 'India', 'Brazil', 'Malaysia', 
                        'Montenegro', 'Serbia', 'Republic of North Macedonia', 
                        'Albania', 'Ukraine', 'Moldova']
    
    # Debug: Print countries that aren't being categorized correctly
    all_countries = set(df_filtered['Citizenship'].unique())
    eu_set = set(eu_nordic_countries)
    special_set = set(special_countries)
    
    uncategorized = all_countries - eu_set - special_set
    print("Countries not in EU+Nordic or 16 Key:")
    for country in sorted(uncategorized):
        if 'norway' in country.lower() or 'iceland' in country.lower():
            print(f"  -> {country} (contains nordic keyword)")
        elif len(country) < 50:  # Don't print super long country names
            print(f"  -> {country}")
    
    print(f"\nNorway in EU list: {'Norway' in eu_nordic_countries}")
    print(f"Norway in data: {'Norway' in all_countries}")
    print(f"Countries with 'norw' in name: {[c for c in all_countries if 'norw' in c.lower()]}")
    
    # Function to categorize countries
    def categorize_country(country):
        if country in eu_nordic_countries:
            return 'EU + Nordic + UK'
        elif country in special_countries:
            return '16 Key Countries'
        else:
            return 'Rest of World'
    
    df_filtered['Category'] = df_filtered['Citizenship'].apply(categorize_country)
    df_filtered['Log_Immigration'] = np.log10(df_filtered['Immigration'])
    

    
    return df_filtered

def create_scatter_plot(df, selected_categories):
    # Filter data based on selected categories
    filtered_df = df[df['Category'].isin(selected_categories)]
    
    # Define colors for each category
    color_map = {
        'EU + Nordic + UK': '#69C4C0',
        '16 Key Countries': '#43AEFF', 
        'Rest of World': '#E08800'
    }
    
    # Define symbols for each category
    symbol_map = {
        'EU + Nordic + UK': 'circle',
        '16 Key Countries': 'square',
        'Rest of World': 'triangle-up'
    }
    
    # Create the scatter plot
    fig = go.Figure()
    
    for category in selected_categories:
        cat_data = filtered_df[filtered_df['Category'] == category]
        
        # Create hover text
        hover_text = [
            f"<b>{row['Citizenship']}</b><br>" +
            f"Immigration: {row['Immigration']:,}<br>" +
            f"Emigration: {row['Emigration']:,}<br>" +
            f"Net Migration: {row['Net_migration']:,}<br>" +
            f"Retention: {row['Retention_percentage']:.1f}%<br>" +
            f"Category: {row['Category']}"
            for _, row in cat_data.iterrows()
        ]
        
        fig.add_trace(go.Scatter(
            x=cat_data['Log_Immigration'],
            y=cat_data['Retention_percentage'],
            mode='markers',
            name=category,
            marker=dict(
                color=color_map[category],
                size=8,
                symbol=symbol_map[category],
                line=dict(width=1, color='black'),
                opacity=0.8
            ),
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=hover_text,
            text=cat_data['Citizenship']  # For potential text annotations
        ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Migration Retention vs Immigration Volume: All Countries (2024)",
            'x': 0.5,
            'font': {'size': 18, 'family': 'Georgia'}
        },
        xaxis_title="Total Immigration (Log Scale)",
        yaxis_title="Retention Percentage (%)",
        width=900,
        height=600,
        plot_bgcolor='#F8FAFB',
        paper_bgcolor='#F8FAFB',
        font=dict(family="Georgia", size=12),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        ),
        hovermode='closest'
    )
    
    # Customize axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#EEEEEE',
        tickmode='array',
        tickvals=[2, 3, 4, 5],
        ticktext=['100', '1K', '10K', '100K']
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='#EEEEEE',
        zeroline=True,
        zerolinewidth=2,
        zerolinecolor='#888888'
    )
    
    # Add reference line at 100%
    fig.add_hline(y=100, line_dash="dash", line_color="#CCCCCC", opacity=0.6)
    
    return fig

def main():
    st.title("🌍 Migration Retention Analysis Dashboard")
    st.markdown("### Interactive visualization of migration patterns to Denmark (2024)")
    
    # Load data
    df = load_data()
    
    # Sidebar for controls
    st.sidebar.header("Filter Options")
    
    # Category selection
    categories = ['EU + Nordic + UK', '16 Key Countries', 'Rest of World']
    selected_categories = st.sidebar.multiselect(
        "Select Country Groups:",
        categories,
        default=categories,
        help="Click to toggle country groups on/off"
    )
    
    if not selected_categories:
        st.warning("Please select at least one country group to display.")
        return
    
    # Create and display the plot
    fig = create_scatter_plot(df, selected_categories)
    st.plotly_chart(fig, use_container_width=True)
    
    
    # Data table
    st.header("📋 Detailed Data")
    
    # Filter data for display
    display_df = df[df['Category'].isin(selected_categories)].copy()
    display_df = display_df.sort_values('Retention_percentage', ascending=False)
    
    # Format the dataframe for display
    display_df['Immigration'] = display_df['Immigration'].apply(lambda x: f"{x:,}")
    display_df['Emigration'] = display_df['Emigration'].apply(lambda x: f"{x:,}")
    display_df['Net_migration'] = display_df['Net_migration'].apply(lambda x: f"{x:,}")
    display_df['Retention_percentage'] = display_df['Retention_percentage'].apply(lambda x: f"{x:.1f}%")
    
    # Select columns for display
    columns_to_show = ['Citizenship', 'Category', 'Immigration', 'Emigration', 'Net_migration', 'Retention_percentage']
    
    st.dataframe(
        display_df[columns_to_show],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Citizenship": "Country",
            "Category": "Group",
            "Immigration": "Immigration",
            "Emigration": "Emigration", 
            "Net_migration": "Net Migration",
            "Retention_percentage": "Retention %"
        }
    )
    
    # Footer
    st.markdown("---")
    st.markdown("**Data Source:** Danish migration statistics (2015-2024) https://www.statbank.dk/VAN1AAR and https://www.statbank.dk/VAN2AAR| **Note:** Only countries with 500+ immigrants shown")

if __name__ == "__main__":
    main()