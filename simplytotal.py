from pickle import FALSE
from readline import get_current_history_length
import simplygo
from pprint import pprint
import streamlit as st 
import pandas as pd 
import numpy as np 
from decimal import Decimal

state = st.session_state 

def get_card_info(rider):
        cards = rider.get_card_info()
        card_list = []
        for card in cards: 
            card_list.append({card["Description"], card["UniqueCode"]})
        return card_list
    
def get_txn_from_range(rider, card_code, start_date, end_date):
    txns = rider.get_transactions(card_code, start_date, end_date)
    hist = txns["Histories"]
    fare_arr = []
    # pprint(hist)
    
    for item in hist: 
        entry = item
        if 'PostedDate' not in entry.keys():
            fare_arr.append(entry['Fare'])
        # Make sure item has no PostedDate entries
    
    total = sum_total_txns(fare_arr)
    return total 
    
def sum_total_txns(arr):
    # Remove dollar signs and cast fare (str) into floats 
    fares = [fare.lstrip("$") for fare in arr]
    clean_fares = [Decimal(fare) for fare in fares]
    total = sum(clean_fares)
    return total 

st.title("Total up your SimplyGo transactions")
st.write("Because SimplyGo's website won't do this for some reason")

st.header("1. Log in to your SimplyGo account")
with st.form("login", clear_on_submit=True): 
    # Save user + pw in session state
    state['user_val'] = st.text_input("Username (Phone number / email)")
    state['password_val'] = st.text_input("Password")
    
    submitted = st.form_submit_button("Submit")

st.header("2. Get the unique code associated with your cards")

if submitted:
    st.write("Take note of the unique code linked to each card!")
    global rider 
    state.rider = simplygo.Ride(state.user_val, state.password_val)
    st.write(get_card_info(state.rider))

st.header("3. Retrieve transactions for a specific card")

with st.form("transactions", clear_on_submit=False):
    card_code = st.text_input("Your card's unique code")
    start_date = st.text_input("Start date in DD-MM-YYYY format")
    end_date = st.text_input("End date in DD-MM-YYYY format")
    submitted = st.form_submit_button("Submit")

st.header("4. Get the total amount of transactions for the date range specified")
if start_date and end_date: 
    with st.spinner("Please wait, we are fetching your transactions"):
        total = get_txn_from_range(state.rider, card_code, start_date, end_date)
        st.write(f"Your total spent from {start_date} to {end_date} is ${total}")

