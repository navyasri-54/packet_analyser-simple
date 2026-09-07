import streamlit as st
import pandas as pd
import random
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Packet Analyzer",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 Simple Network Packet Analyzer")
st.caption("A clean, real-time dashboard visualizing network interface traffic streams.")
st.markdown("---")

# 2. Initialize Session Memory for Packet logs
if "packet_logs" not in st.session_state:
    st.session_state.packet_logs = []

# 3. Sidebar Controls
st.sidebar.header("⚙️ Controls")
is_sniffing = st.sidebar.toggle("Start Sniffing Engine", value=True)
speed = st.sidebar.slider("Capture Delay (seconds)", 0.5, 3.0, 1.0)

if st.sidebar.button("Clear Log History"):
    st.session_state.packet_logs = []
    st.rerun()

# 4. Mock Packet Generation Function
def capture_packet():
    protocols = ["TCP", "UDP", "HTTP", "DNS"]
    ips = ["192.168.1.50", "10.0.0.4", "8.8.8.8", "142.250.190.46"]
    
    proto = random.choice(protocols)
    sizes = {"TCP": random.randint(54, 1500), "UDP": random.randint(42, 512), "HTTP": random.randint(300, 2500), "DNS": random.randint(60, 150)}
    
    return {
        "Time": time.strftime("%H:%M:%S"),
        "Protocol": proto,
        "Source IP": random.choice(ips),
        "Destination IP": random.choice(ips),
        "Size (Bytes)": sizes[proto],
        "Port": random.randint(80, 443)
    }

# Continuously append packets if toggle is active
if is_sniffing:
    pkt = capture_packet()
    st.session_state.packet_logs.append(pkt)
    # Keep the log history at a maximum of 50 items for browser stability
    if len(st.session_state.packet_logs) > 50:
        st.session_state.packet_logs.pop(0)

# Create DataFrame
df = pd.DataFrame(st.session_state.packet_logs)

# 5. Live UI Rendering Components
if not df.empty:
    # KPI metrics row
    col1, col2, col3 = st.columns(3)
    col1.metric("Packets Captured", len(df))
    col2.metric("Avg Packet Size", f"{int(df['Size (Bytes)'].mean())} Bytes")
    col3.metric("Most Active Protocol", df["Protocol"].mode().iloc[0])
    
    st.markdown("---")
    
    # Visual Breakdown Layout Grid
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.subheader("📊 Protocol Count Breakdown")
        proto_counts = df["Protocol"].value_counts()
        st.bar_chart(proto_counts)
        
    with right_col:
        st.subheader("📋 Real-time Traffic Ledger")
        # Display latest packet arrays at the top of the dataframe chart grid view
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.info("Awaiting incoming traffic. Toggle 'Start Sniffing Engine' on the sidebar to observe data packets.")

# 6. Infinite Loop Window Auto-Refresh Trigger
if is_sniffing:
    time.sleep(speed)
    st.rerun()
