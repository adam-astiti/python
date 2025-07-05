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
st.image(r"Pizza Title.jpg", use_column_width=True)
st.title("KPI and Metrics")
st.markdown("---") # A subtle separator line

# --- SIDEBAR FILTERS ---
# Note: The text color on the sidebar is automatically handled by Streamlit,
# but we can override it with more specific CSS if needed.
st.sidebar.header("Dashboard Filters")
selected_category = st.sidebar.selectbox(
    'Select a Pizza Category',
    all_category,
    # The key is needed to uniquely identify this widget
    key="category_selector" 
)

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

revenue_by_category = df.groupby(['pizza_category'])['total_price'].sum().sort_values(ascending=False)
revenue_by_pizza = df.groupby(['pizza_name'])['total_price'].sum().sort_values(ascending=False).head(5)
pizza_sales = df['pizza_name'].value_counts().sort_values(ascending=False).head(5)


fig1, ax1 = create_countplot(df, y_plot='pizza_category', 
                             orient='v', 
                             order= df['pizza_category'].value_counts().sort_values(ascending=False).index,
                             xlabel_plot='Pizza Order',
                             ylabel_plot='',
                             plot_title= 'Best Seler Category')
fig2, ax2 = create_barplot(y_plot=revenue_by_category.index,
                           x_plot=revenue_by_category.values,
                           orient='h',
                           plot_title='Most Profitable Pizza Category (USD)',
                           xlabel_plot='Revenue $(USD)',
                           ylabel_plot='')
fig3, ax3 = create_barplot(y_plot=pizza_sales.index,
                           x_plot=pizza_sales.values,
                           orient='h',
                           plot_title='Best Seler Pizza',
                           xlabel_plot='Sales Count',
                           ylabel_plot='')
fig4, ax4 = create_barplot(y_plot=revenue_by_pizza.index,
                           x_plot=revenue_by_pizza.values,
                           orient='h',
                           plot_title='Most Profitable Pizza (USD)',
                           xlabel_plot='Revenue $(USD)',
                           ylabel_plot='')


co1, co2 = st.columns(2)
with co1:
    st.pyplot(fig1)
with co2:
    st.pyplot(fig2)

c1, c2 = st.columns(2)
with c1:
    st.pyplot(fig3)
with c2:
    st.pyplot(fig4)
