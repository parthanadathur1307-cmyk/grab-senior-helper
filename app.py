import streamlit as st

# Setting the title of the application
st.title('Senior Helper App')

# Writing a brief description
st.write('This application is designed to assist senior citizens with various tasks and information.')

# Creating sections for different functionalities
st.header('Features')

# Example features
st.subheader('1. Medication Reminders')
st.write('Set reminders for medication intake.')

st.subheader('2. Appointment Scheduling')
st.write('Manage and schedule appointments.')

st.subheader('3. Emergency Contact')
st.write('Quick access to emergency contacts.')

# Displaying a simple input form
st.header('Feedback')
name = st.text_input('Enter your name:')
feedback = st.text_area('Your feedback:')
if st.button('Submit'):
    st.success('Thank you for your feedback!')
