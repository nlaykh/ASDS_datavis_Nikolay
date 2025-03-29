# Hotel Booking Analysis

This repository contains a data visualization project analyzing hotel booking patterns to optimize strategies for Resort and City Hotels. The project is divided into two parts: the first part focuses on data cleaning and exploratory data analysis (EDA), while the second part delves into advanced visualizations and actionable insights using Plotly. The analysis explores lead times, stay durations, customer segments, revenue drivers, and cancellation risks, providing recommendations for hotel management to balance revenue and operational stability.

## Project Overview

The project uses a dataset of 86,726 hotel bookings to uncover patterns that can help Resort and City Hotels optimize their strategies. The analysis addresses key questions such as:
- When do guests book, and how far in advance?
- How long do they stay, and how does this vary by season?
- Who are the guests (customer segments)?
- What drives revenue (stay length and average daily rate)?
- Why and when do guests cancel their bookings?

### Part 1: Data Cleaning and Exploratory Data Analysis (EDA)
The first part of the project focuses on preparing the dataset for analysis and conducting initial exploratory data analysis.

#### Objectives:
- **Data Cleaning:** Handle missing values, correct data types, remove duplicates, and address inconsistencies in the dataset.
- **Exploratory Data Analysis (EDA):** Perform initial analysis to understand the dataset’s structure, distributions, and relationships between variables (e.g., lead time, stay duration, cancellations).
- **Visualizations:** Use Matplotlib and Seaborn to create static visualizations (e.g., histograms, bar charts, heatmaps) to identify patterns and trends.

#### Key Findings:
- Identified and handled missing values in columns like `children` and `country`.
- Corrected data types (e.g., converted `arrival_date` to datetime).
- Explored distributions of key variables like lead time and stay duration, revealing differences between Resort and City Hotels.
- Analyzed cancellation rates and their relationship with lead time, setting the stage for deeper analysis in Part 2.

### Part 2: Advanced Visualizations and Actionable Insights
The second part builds on the cleaned dataset to create interactive visualizations and derive actionable insights for hotel management.

#### Objectives:
- **Interactive Visualizations:** Use Plotly to create six interactive plots to explore booking patterns, customer segments, revenue drivers, and cancellation risks.
- **Narrative Development:** Tell a cohesive story through the visualizations, addressing key questions about guest behaviors and operational impacts.
- **Actionable Recommendations:** Provide tailored strategies for Resort and City Hotels to optimize revenue and minimize cancellation risks.

#### Key Sections and Visualizations:
1. **When Do Guests Book? (Lead Time Distribution):** Histogram showing lead time distribution by hotel type.
2. **How Long Do They Stay? (Stay Duration Patterns):** Bar chart of average stay length by month and hotel type.
3. **Who Are the Guests? (Booking Patterns by Market Segment):** Stacked bar chart of booking proportions by market segment.
4. **What Drives Revenue? (ADR and Stay Length):** Scatter plot of ADR vs. stay length, with point size reflecting revenue.
5. **Why Do Guests Cancel? (Cancellations by Lead Time and Hotel Type):** Boxplot of lead time by cancellation status and hotel type.
6. **When Are Cancellations Most Likely? (Cancellation Trends by Month):** Line chart of cancellation rates by month and hotel type.

#### Key Findings:
- **Resort Hotels:** Guests book further in advance (median ~50 days), stay longer in summer (e.g., August ~5.5 nights), often belong to group or leisure segments, and have higher cancellation risks with long lead times and in spring.
- **City Hotels:** Guests book closer to their stay (median ~30 days), have shorter and more consistent stays (~2.5-3.5 nights), include more corporate and online bookers, and face higher cancellation risks in spring (e.g., April ~35%).
- **Revenue Drivers:** Higher revenue is associated with longer stays and higher ADRs, with Resort Hotels benefiting from mid-length stays and City Hotels from volume.

#### Recommendations:
- **Resort Hotels:** Offer early-bird discounts, extended-stay packages in summer, group packages, premium pricing for mid-length stays, stricter cancellation policies for long lead times, and last-minute deals in summer.
- **City Hotels:** Focus on last-minute marketing, optimize room turnover, enhance online booking platforms, provide corporate amenities, offer competitive pricing for short stays, and use incentives (e.g., loyalty points) to reduce spring cancellations.

## Files
- `Project_NikolayKhachatryan.ipynb`: Jupyter notebook containing both Part 1 (data cleaning and EDA) and Part 2 (advanced visualizations and insights).
- `cleaned_hotel_bookings.csv`: The cleaned dataset used for the analysis. 

## How to Run
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NikolayKhachatryan/hotel-booking-analysis.git
