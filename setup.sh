mkdir -p ~/.streamlit/
echo "[theme]
primaryColor=’#529AEF’
backgroundColor=’#F1F5FB’
secondaryBackgroundColor=’#FFFFFF’
font = ‘sans serif’
[global]
dataFrameSerialization = ’legacy’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml