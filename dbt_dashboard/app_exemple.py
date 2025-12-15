import streamlit as st

# Set the title of your application
st.title("Hello Streamlit World! 👋")

# Add some simple text
st.write("This is a basic Streamlit app.") [0.12]

# Add a button widget and logic
if st.button("Say Hello"):
    st.write("Hello there!")

# Add a text input widget
user_input = st.text_input("Enter your name", "Visitor")
st.write(f"Welcome, {user_input}!")

# Add a slider and display its value
x = st.slider("Select a number", 0, 100, 25)
st.write("The current number is", x)
