import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset with error handling
try:
    df = pd.read_csv("cleaned_hotel_bookings.csv")
    df['arrival_date'] = pd.to_datetime(df['arrival_date'])
    df['total_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    df['revenue'] = df['adr'] * df['total_stay']
except FileNotFoundError:
    raise FileNotFoundError("The file 'cleaned_hotel_bookings.csv' was not found. Please ensure it is in the project directory.")
except Exception as e:
    raise Exception(f"Error loading dataset: {str(e)}")

# Verify required columns exist
required_columns = ['hotel', 'lead_time', 'arrival_date', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adr', 'market_segment', 'is_canceled']
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

# Custom color mapping for accessibility and consistency
COLOR_MAP = {
    "Resort Hotel": "#1E90FF",  # Dodger Blue
    "City Hotel": "#FF4500"     # OrangeRed
}

# Helper function to create an empty plot with a message
def create_empty_plot(message):
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=20, color="#333333")
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=12, color="#333333"),
        showlegend=False
    )
    return fig

# Plot 1: Lead Time Distribution
def lead_time_distribution(hotel_type=None, lead_time_range=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        if lead_time_range:
            filtered_df = filtered_df[
                (filtered_df['lead_time'] >= lead_time_range[0]) &
                (filtered_df['lead_time'] <= lead_time_range[1])
            ]
        if filtered_df.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.histogram(
            filtered_df,
            x="lead_time",
            color="hotel",
            nbins=50,
            title="Distribution of Booking Lead Time by Hotel Type",
            labels={"lead_time": "Lead Time (Days)", "hotel": "Hotel Type"},
            marginal="box",
            opacity=0.7,
            color_discrete_map=COLOR_MAP
        )
        fig.update_layout(
            bargap=0.2,
            xaxis_title="Lead Time (Days)",
            yaxis_title="Number of Bookings",
            legend_title="Hotel Type",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 2: Stay Duration Patterns
def stay_duration_patterns(hotel_type=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        stay_by_month = filtered_df.groupby([filtered_df['arrival_date'].dt.strftime('%B'), 'hotel'])['total_stay'].mean().reset_index()
        stay_by_month = stay_by_month.rename(columns={'arrival_date': 'Month'})
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        stay_by_month['Month'] = pd.Categorical(stay_by_month['Month'], categories=month_order, ordered=True)
        stay_by_month = stay_by_month.sort_values(by='Month')
        if stay_by_month.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.bar(
            stay_by_month,
            x="Month",
            y="total_stay",
            color="hotel",
            barmode="group",
            title="Average Stay Duration by Month and Hotel Type",
            labels={"total_stay": "Average Stay Length (Nights)", "hotel": "Hotel Type"},
            color_discrete_map=COLOR_MAP
        )
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Average Stay Length (Nights)",
            legend_title="Hotel Type",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 3: Booking Patterns by Market Segment
def booking_patterns_market_segment(hotel_type=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        market_segment_dist = filtered_df.groupby(['hotel', 'market_segment']).size().reset_index(name='count')
        market_segment_dist['proportion'] = market_segment_dist.groupby('hotel')['count'].transform(lambda x: x / x.sum())
        if market_segment_dist.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.bar(
            market_segment_dist,
            x="proportion",
            y="hotel",
            color="market_segment",
            title="Proportion of Bookings by Market Segment and Hotel Type",
            labels={"proportion": "Proportion of Bookings", "hotel": "Hotel Type", "market_segment": "Market Segment"},
            orientation='h',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            xaxis_title="Proportion of Bookings",
            yaxis_title="Hotel Type",
            legend_title="Market Segment",
            barmode="stack",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 4: ADR vs. Stay Length
def adr_vs_stay_length(hotel_type=None, stay_length_range=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        if stay_length_range:
            filtered_df = filtered_df[
                (filtered_df['total_stay'] >= stay_length_range[0]) &
                (filtered_df['total_stay'] <= stay_length_range[1])
            ]
        if filtered_df.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.scatter(
            filtered_df,
            x="total_stay",
            y="adr",
            color="hotel",
            size="revenue",
            hover_data=["arrival_date", "is_canceled"],
            title="ADR vs. Stay Length: Revenue Impact by Hotel Type",
            labels={"total_stay": "Total Stay (Nights)", "adr": "Average Daily Rate ($)", "hotel": "Hotel Type"},
            color_discrete_map=COLOR_MAP
        )
        fig.update_layout(
            xaxis_title="Total Stay (Nights)",
            yaxis_title="Average Daily Rate ($)",
            legend_title="Hotel Type",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 5: Cancellations by Lead Time and Hotel Type
def cancellations_by_lead_time(hotel_type=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        if filtered_df.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.box(
            filtered_df,
            x="is_canceled",
            y="lead_time",
            color="hotel",
            title="Lead Time Distribution by Cancellation Status and Hotel Type",
            labels={"is_canceled": "Canceled (0 = No, 1 = Yes)", "lead_time": "Lead Time (Days)", "hotel": "Hotel Type"},
            category_orders={"is_canceled": [0, 1]},
            color_discrete_map=COLOR_MAP
        )
        fig.update_layout(
            xaxis_title="Cancellation Status",
            yaxis_title="Lead Time (Days)",
            legend_title="Hotel Type",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 6: Cancellation Trends by Month
def cancellation_trends_by_month(hotel_type=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        cancel_by_month = filtered_df.groupby([filtered_df['arrival_date'].dt.strftime('%B'), 'hotel'])['is_canceled'].mean().reset_index()
        cancel_by_month = cancel_by_month.rename(columns={'arrival_date': 'Month', 'is_canceled': 'Cancellation Rate'})
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        cancel_by_month['Month'] = pd.Categorical(cancel_by_month['Month'], categories=month_order, ordered=True)
        cancel_by_month = cancel_by_month.sort_values('Month')
        if cancel_by_month.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.line(
            cancel_by_month,
            x="Month",
            y="Cancellation Rate",
            color="hotel",
            title="Cancellation Rate by Month and Hotel Type",
            labels={"Cancellation Rate": "Cancellation Rate", "hotel": "Hotel Type"},
            color_discrete_map=COLOR_MAP
        )
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Cancellation Rate",
            legend_title="Hotel Type",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 7: Heatmap of Booking Trends by Month and Year
def booking_trends_heatmap(hotel_type=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        # Extract year and month
        filtered_df['year'] = filtered_df['arrival_date'].dt.year
        filtered_df['month'] = filtered_df['arrival_date'].dt.strftime('%B')
        month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        # Aggregate bookings by year and month
        heatmap_data = filtered_df.groupby(['year', 'month']).size().reset_index(name='booking_count')
        heatmap_data['month'] = pd.Categorical(heatmap_data['month'], categories=month_order, ordered=True)
        heatmap_data = heatmap_data.sort_values(['year', 'month'])
        if heatmap_data.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.density_heatmap(
            heatmap_data,
            x="month",
            y="year",
            z="booking_count",
            color_continuous_scale='Blues',
            title="Booking Trends by Month and Year",
            labels={"month": "Month", "year": "Year", "booking_count": "Number of Bookings"},
            text_auto=True
        )
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Year",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")

# Plot 8: Stacked Area Chart of Revenue Contribution by Market Segment
def revenue_by_market_segment(hotel_type=None):
    filtered_df = df.copy()
    try:
        if hotel_type and hotel_type != "All":
            filtered_df = filtered_df[filtered_df['hotel'] == hotel_type]
        # Aggregate revenue by market segment over time
        filtered_df['year_month'] = filtered_df['arrival_date'].dt.to_period('M').astype(str)
        revenue_data = filtered_df.groupby(['year_month', 'market_segment'])['revenue'].sum().reset_index()
        if revenue_data.empty:
            return create_empty_plot("No data available for the selected filters.")
        fig = px.area(
            revenue_data,
            x="year_month",
            y="revenue",
            color="market_segment",
            title="Revenue Contribution by Market Segment Over Time",
            labels={"year_month": "Year-Month", "revenue": "Revenue ($)", "market_segment": "Market Segment"},
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            xaxis_title="Year-Month",
            yaxis_title="Revenue ($)",
            legend_title="Market Segment",
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12, color="#333333"),
            showlegend=True
        )
        return fig
    except Exception as e:
        return create_empty_plot(f"Error generating plot: {str(e)}")