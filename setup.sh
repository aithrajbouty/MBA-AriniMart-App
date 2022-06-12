mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
[theme]\n\
primaryColor='#529AEF'\n\
backgroundColor='#F1F5FB'\n\
secondaryBackgroundColor='#FFFFFF'\n\
textColor='#252733'\n\
font="sans serif"\n\
[global]\n\
dataFrameSerialization = "legacy"\n\
\n\
" > ~/.streamlit/config.toml