import os
import streamlit as st
import streamlit_nested_layout
import requests
import json


###
### Helper functions
###
def jsonify(response):
    result_dict = json.loads(response.text)[0]
    return result_dict


def fetch_data(type):
    ### prepare API key and URL
    with st.spinner("Working..."):
        api_key = os.getenv["RAPID_API_KEY"]
        api_url = f"https://api.api-ninjas.com/v1/{type}"

        ### invoke API and get the response
        response = requests.get(url=api_url, headers={"X-Api-Key": api_key})
        if response.status_code == requests.codes.ok:
            data = jsonify(response)
            status = "OK"
        else:
            data = {"code": response.status_code, "message": response.text}
            status = "ERROR"
    return status, data


def display(text, font="sans-serif", color="white", size="25px"):
    st.markdown(
        f'<p style="font-family:{font}; color:{color}; font-size: {size};">{text}</p>',
        unsafe_allow_html=True,
    )


def render_about_tab():
    """Render the this page"""
    with open("assets/about.md", "r") as f:
        text = f.read()
    st.markdown(text, unsafe_allow_html=True)


def show_dadkokes():
    ### Dad Jokes
    st.image("assets/dadjokes-logo.png", width=180)
    with st.expander("Expand me to laugh out loud...", expanded=False):
        if st.button("Get me a Dad Joke >>>"):
            status, data = fetch_data("dadjokes")
            if status == "OK":
                joke = data["joke"]
                display(text=joke + " 🤣 🤣 🤣", color="#FFD580")
            elif status == "ERROR":
                msg = f"({data['code']}): {data['message']}"
                st.error(msg)


def show_riddles():
    ### Riddles section
    st.divider()
    st.image("assets/riddles-logo.png", width=180)
    with st.expander("Find out how smart are u...", expanded=False):
        if st.button("Test Me >>>"):
            status, data = fetch_data("riddles")
            if status == "OK":
                title, question, answer = (
                    data["title"],
                    data["question"],
                    data["answer"],
                )
                st.markdown("## Title:")
                display(title, color="#ffffe0")
                st.markdown("## Question:")
                display(question, color="#ADD8E6")
                with st.expander("Reveal Answer >>>", expanded=False):
                    st.markdown("## Answer")
                    display(answer, color="#90EE90")
            elif status == "ERROR":
                msg = f"({data['code']}): {data['message']}"
                st.error(msg)


def show_facts():
    ### Facts section
    st.divider()
    st.image("assets/facts-logo.png", width=180)
    with st.expander("Test your GK...", expanded=False):
        if st.button("Give me a fact >>>"):
            status, data = fetch_data("facts")
            if status == "OK":
                fact = data["fact"]
                display(fact, color="#FFB6C1")
            elif status == "ERROR":
                msg = f"({data['code']}): {data['message']}"
                st.error(msg)


def show_trivia():
    ### Trivia section
    st.divider()
    st.image("assets/trivia-logo.png", width=180)
    with st.expander("Not a trivial task...", expanded=False):
        if st.button("Show me a trivia >>>"):
            status, data = fetch_data("trivia")
            if status == "OK":
                title, question, answer = (
                    data["category"],
                    data["question"],
                    data["answer"],
                )
                st.markdown("## Category")
                display(title, color="#CBC3E3")
                st.markdown("## Question")
                display(question, color="#DF00FF")
                with st.expander("Reveal Answer >>>", expanded=False):
                    st.markdown("## Answer")
                    display(answer, color="#90EE90")
            elif status == "ERROR":
                msg = f"({data['code']}): {data['message']}"
                print(msg)


def render_activity_tab():
    show_dadkokes()
    show_riddles()
    show_facts()
    show_trivia()
    st.divider()


###
### App entry point
###
if __name__ == "__main__":
    ### page heading, logo and app banner
    st.set_page_config(page_title="API Fun App", page_icon="assets/app-logo.gif")
    col1, col2 = st.columns(2)
    col1.title("A Fun app with The Ninja API")
    col2.image("assets/app-logo.gif")

    ### create tabs
    tab_about, tab_activity = st.tabs(["ABOUT 👋", "ACTIVITY ✒️"])

    ### render tabs
    with tab_about:
        render_about_tab()

    with tab_activity:
        render_activity_tab()
