#!/bin/bash
# Install dependencies if not already installed (quick check)
# pip install -r requirements.txt

echo "Starting Little KITEs Tracker..."
echo "To access from your mobile, connect to the same Wi-Fi and use the 'Network URL' shown below."
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
