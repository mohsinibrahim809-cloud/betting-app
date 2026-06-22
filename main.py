import streamlit as st
import json
import os

DB_FILE = "data.json"


def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


st.title("📊 Betting Web App (Mobile Friendly)")

data = load_data()

menu = st.sidebar.selectbox("Menu", ["Matches", "Add Match"])

if menu == "Add Match":
    name = st.text_input("Enter Match Name")

    if st.button("Add Match"):
        if name:
            data.append({"name": name, "bets": []})
            save_data(data)
            st.success("Match Added!")

if menu == "Matches":
    if not data:
        st.warning("No matches found")
    else:
        match_names = [m["name"] for m in data]
        selected = st.selectbox("Select Match", match_names)

        match_index = match_names.index(selected)

        st.subheader("Add Bet")

        amount = st.number_input("Bet Amount", min_value=0.0)
        odds = st.number_input("Odds", min_value=1.0)

        if st.button("Add Bet"):
            profit = amount * (odds - 1)

            data[match_index]["bets"].append({
                "amount": amount,
                "odds": odds,
                "profit": profit
            })

            save_data(data)
            st.success("Bet Added!")

        st.subheader("Bets")

        total_profit = 0

        for bet in data[match_index]["bets"]:
            st.write(
                f"💰 Amount: {bet['amount']} | "
                f"🎯 Odds: {bet['odds']} | "
                f"📈 Profit: {bet['profit']}"
            )
            total_profit += bet["profit"]

        st.info(f"Total Profit/Loss: {round(total_profit, 2)}")
