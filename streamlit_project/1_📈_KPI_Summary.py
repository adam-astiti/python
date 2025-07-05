import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# --- PAGE CONFIG ---
# Set the page title, icon, and layout. The dark theme is a good base.
st.set_page_config(
    page_title="Pro Pizza Dashboard",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils import css_load
from utils import load_and_clean_data
from utils import create_barplot
from utils import create_countplot
from utils import create_lineplot

css_load()
df = load_and_clean_data()

all_category = np.append(df['pizza_category'].unique(), 'All')






# --- MAIN PAGE LAYOUT ---
st.image(r"streamlit_project/Pizza Title.jpg", use_column_width=True)
st.title("KPI and Metrics")
st.markdown("---") # A subtle separator line

# --- SIDEBAR FILTERS ---
# Note: The text color on the sidebar is automatically handled by Streamlit,
# but we can override it with more specific CSS if needed.
st.sidebar.header("Dashboard Filters")
selected_category = st.sidebar.selectbox(
    'Select a Pizza Category',
    all_category,
    key="category_selector")   

# --- KPI ROW ---
# Filter data based on selection from the sidebar
if selected_category == 'All':
    filtered_df = df
else:
    filtered_df = df[df['pizza_category'] == selected_category]

# Calculate KPIs from the filtered data
total_revenue = filtered_df['total_price'].sum()
total_orders = filtered_df['order_id'].nunique()
pizzas_sold = filtered_df['quantity'].sum()

# Create columns for the KPIs
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col2:
    st.metric("Total Orders", f"{total_orders}")
    
with col3:
    st.metric("Pizzas Sold", f"{pizzas_sold}")
st.markdown("---")


day_order = df[['day_number', 'day']].drop_duplicates().sort_values(by='day_number', ascending=True).day
month_order = df[['month_number', 'month']].drop_duplicates().sort_values(by='month_number', ascending=True).month
monthly_revenue = df.groupby(['month'])['total_price'].sum().reindex(month_order)

order_by_month = filtered_df.month.value_counts().reindex(month_order)
order_by_day = filtered_df.day.value_counts().reindex(day_order)
order_by_hour = filtered_df['hour'].value_counts().sort_index()


fig1, ax1 = create_countplot(df, y_plot='pizza_category', 
                             orient='v', 
                             order= df['pizza_category'].value_counts().sort_values(ascending=False).index,
                             xlabel_plot='Pizza Order',
                             ylabel_plot='Pizza Category',
                             plot_title= 'Pizza Sales Category')
fig3, ax3 = create_barplot(x_plot=order_by_day.index, 
                             y_plot=order_by_day.values,
                             orient='v', 
                             xlabel_plot='Day',
                             ylabel_plot='Total Order',
                             plot_title= 'Daily Sales Trend')
fig2, ax2 = create_lineplot(series_data=order_by_day, 
                            plot_title='Monthly Sales Trend',
                            xlabel_plot='Month',
                            ylabel_plot='Total Order')
fig4, ax4 = create_lineplot(series_data=order_by_hour, 
                            plot_title='Busiest Hour',
                            xlabel_plot='Hour',
                            ylabel_plot='Total Order')
fig5, ax5 = create_lineplot(series_data=monthly_revenue, 
                            plot_title='Monthly Revenue',
                            xlabel_plot='Month',
                            ylabel_plot='Total revenue')



c1, c2 = st.columns(2)
with c1:
    st.pyplot(fig4)
with c2:
    st.pyplot(fig3)


co1, co2 = st.columns(2)
with co1:
    st.pyplot(fig2)
with co2:
    st.pyplot(fig5)
