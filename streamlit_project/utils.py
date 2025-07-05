import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



# --- CUSTOM CSS STYLING ---
# This is the "secret sauce" where we apply your color palette.
# I've mapped your color requests to the correct Streamlit elements.

def css_load():
    css = """
    <style>
        /* --- GENERAL STYLING --- */
        /* Main app background */
        .stApp {
            background-color: #ffffff; 
        }

        /* --- SIDEBAR STYLING --- */
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #fdd8d8;
        }

        /* Sidebar font */
        [data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
            color: #ffffff; /* Dark grey text for readability on white */
            font-family: 'Verdana', sans-serif; /* A clean, professional font */
            font-size: 30px;
        }

        /* Sidebar header font */
        [data-testid="stSidebar"] .st-emotion-cache-1lcbmx1 {
            color: #ffffff;
            font-family: 'Verdana', sans-serif;
        }


        /* --- KPI CARD STYLING --- */
        /* KPI Metric card style */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 2px solid #FFFFFF;
            border-radius: 15px; /* More rounded corners */
            padding: 20px;
            /* Adding the shadow you wanted */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        /* KPI value text */
        [data-testid="stMetricValue"] {
            color: #333333;
            font-weight: bold;
        }

        /* KPI label text */
        [data-testid="stMetricLabel"] {
            color: #333333;
        }

        /* --- PLOT STYLING --- */
        /* This targets the container that holds your Matplotlib/Seaborn plots */
        [data-testid="stImage"] {
            border-radius: 20px; /* Rounded corners for the plot container */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Shadow for the plot container */
            border: 2px solid #FFFFFF; /* A white border to make it pop */
        }

    </style>
    """
    return st.markdown(css, unsafe_allow_html=True)


# --- DATA LOADING (Cached) ---
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv(r"D:\python\streamlit_project\Raw_data_pizza_sales.csv")
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    df['month_number'] = df['order_date'].dt.month
    df['day'] = df['order_date'].dt.day_name()
    df['day_number'] = df['order_date'].dt.day_of_week
    df['order_time'] = pd.to_datetime(df['order_time'])
    df['hour'] = df['order_time'].dt.hour
    return df

df = load_and_clean_data()


def create_lineplot(series_data, plot_title, color_line= '#CC0000', xlabel_plot='', ylabel_plot=''):
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(x=series_data.index, y=series_data.values, ax=ax, color=color_line, linewidth=5, marker='o', markersize=15, palette='black')
    ax.set_title(plot_title, fontweight='bold', fontsize=20)
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    plt.xlabel(xlabel_plot, fontweight='bold', fontsize=15)
    plt.ylabel(ylabel_plot, fontweight='bold', fontsize=15)
    plt.grid(True, linestyle= '--', alpha=0.6)
    plt.tight_layout()
    return fig, ax

def create_countplot(plot_data, x_plot=None, y_plot=None, orient='h', plot_title='', order = None, color_bar= '#CC0000', xlabel_plot='', ylabel_plot=''):
    fig, ax = plt.subplots(figsize=(10,5))
    sns.countplot(data=plot_data, y=y_plot, x=x_plot, ax=ax, color=color_bar, orient=orient, order= order)
    ax.set_title(plot_title, fontdict={'fontweight': 'bold', 'fontsize' : 20})
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    plt.xlabel(xlabel_plot, fontweight='bold', fontsize=15)
    plt.ylabel(ylabel_plot, fontweight='bold', fontsize=15)
    plt.tight_layout()
    return fig, ax

def create_barplot(plot_data=None, x_plot=None, y_plot=None, orient='v', plot_title='', order = None, color_bar= '#CC0000', xlabel_plot='', ylabel_plot=''):
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=plot_data, y=y_plot, x=x_plot, ax=ax, color=color_bar, order= order, orient=orient)
    ax.set_title(plot_title, fontdict={'fontweight': 'bold', 'fontsize' : 20})
    fig.patch.set_alpha(0.0)
    ax.patch.set_alpha(0.0)
    plt.xlabel(xlabel_plot, fontweight='bold', fontsize=15)
    plt.ylabel(ylabel_plot, fontweight='bold', fontsize=15)
    plt.tight_layout()
    return fig, ax