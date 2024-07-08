import streamlit as st

# Set the configuration for the Streamlit app
st.set_page_config(
    page_title="雲水書車-自動化小工具",  # Page title
    page_icon="🧊",  # Page icon
    layout="wide",  # Use a wide layout
    initial_sidebar_state="expanded",  # Sidebar expanded by default
    menu_items={  # Customize the menu items
        'Get Help': 'https://www.extremelycoolapp.com/help',  # Link for getting help
        'Report a bug': "https://stackoverflow.com/questions/42830557/git-remote-add-origin-vs-remote-set-url-origin",  # Link for reporting a bug
        'About': "# This is a header. This is an *extremely* cool app!"  # About section
    }
)

# Add content to the app
st.title("雲水書車-自動化小工具")
st.write("歡迎來到這個非常酷的應用程序！")

# Add some interactive elements
if st.button('Click Me'):
    st.write('Button clicked!')

st.sidebar.header('Sidebar Title')
st.sidebar.write('Sidebar content goes here.')
