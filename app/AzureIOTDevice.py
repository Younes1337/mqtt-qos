import streamlit as st
import psutil
import time

# Streamlit app title
st.title("Real-time CPU, RAM, and Data Analysis")

# Initialize empty lists to store CPU and RAM data
cpu_data, ram_data, rtt_data = [], [], []

# Create a placeholder for the combined chart
combined_chart = st.line_chart(data={'Threshold': [90]})

# Create a placeholder for the RTT chart
rtt_chart = st.line_chart(data={'RTT (ms)': []})

with open('../total_data_sent_per_second.txt', 'r') as input_file, open('../output.txt', 'w') as output_file:
    lines = input_file.readlines()
    chunk_size = 3

    for i in range(0, len(lines), chunk_size):
        chunk = lines[i:i + chunk_size]
        values = [int(line.strip()) for line in chunk]
        sum_values = sum(values)
        avg_value = sum_values / 300 if values else 0

        output_file.write(f'{avg_value}\n')

# Create a placeholder for the new data analysis chart
data_analysis_chart = st.line_chart(data={'New Data Analysis': []})

cpu_display = st.empty()
ram_display = st.empty()
rtt_display = st.empty()

# Start the Streamlit loop
while True:
    # Read RTT values from the text file
    with open('../rtt_values.txt', 'r') as file:
        rtt_data = [float(line.strip()) * 1000 for line in file.readlines()]  # Convert seconds to milliseconds

    # Update RTT chart with the latest data
    rtt_chart.line_chart(data={'RTT (ms)': rtt_data})  # Display RTT in milliseconds

    # Fetch system resource usage
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent

    # Append data to respective lists
    cpu_data.append(cpu_percent)
    ram_data.append(ram_percent)

    # Update combined chart with CPU and RAM data
    combined_chart.line_chart(data={'CPU %': cpu_data, 'RAM %': ram_data, 'Threshold': [90] * len(cpu_data)})

    # Optional: Limit data points for smoother visualization
    if len(cpu_data) > 100:
        cpu_data.pop(0)
        ram_data.pop(0)

    cpu_display.markdown(f' Current CPU Usage: <span style="color:green;"> {cpu_percent}%</span>', unsafe_allow_html=True)
    ram_display.markdown(f'Current RAM Usage: <span style="color:green;"> {ram_percent}%</span>', unsafe_allow_html=True)
    rtt_display.markdown(f'Latest RTT: <span style="color:green;"> {rtt_data[-1] if rtt_data else "No RTT data available"} ms</span>', unsafe_allow_html=True)

    # Read data from the text file and perform analysis
    with open('../output.txt', 'r') as file:
        data_sent_per_second = [float(line.strip()) for line in file.readlines()]
        data_analysis_chart.line_chart(data={'New Data Analysis': data_sent_per_second})

        

    # Optional: Control refresh rate
    time.sleep(0.1)