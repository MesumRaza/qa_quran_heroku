mkdir -p ~/.streamlit/

pipenv install https://download.pytorch.org/whl/cpu/torch-1.7.0%2Bcpu-cp36-cp36m-linux_x86_64.whl
pip install git+https://github.com/deepset-ai/haystack.git
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
