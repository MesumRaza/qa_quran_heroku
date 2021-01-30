mkdir -p ~/.streamlit/

pip install git+https://github.com/deepset-ai/haystack.git
pip install urllib3==1.25.4
echo "\
[general]\n\
email = \"juan.ciro@premexcorp.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

