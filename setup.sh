mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"aithrabouty@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor=\"#529AEF\"\n\
backgroundColor=\"#F1F5FB\"\n\
secondaryBackgroundColor=\"#FFFFFF\"\n\
textColor=\"#252733\"\n\
font=\"sans serif\"\n\
[global]\n\
dataFrameSerialization = \"legacy\"\n\
" > ~/.streamlit/config.toml