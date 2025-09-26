import streamlit as st
from retirement_calc import calculate_retirement_age

st.title("💰 Kalkulator Wczesnej Emerytury")

current_age = st.number_input("Obecny wiek", min_value=0, max_value=100, value=30, step=1)
capital = st.number_input("Kapitał początkowy", min_value=0, value=100000, step=1000)
monthly_contrib = st.number_input("Miesięczna inwestycja", min_value=0, value=20000, step=1000)
annual_return = st.number_input("Średnia stopa zwrotu (%)", min_value=0.0, value=5.0, step=0.1) / 100
annual_expenses = st.number_input("Miesięczne wydatki", min_value=0, value=40000, step=1000)
projected_lifespan = st.number_input("Przewidywany wiek śmierci", min_value=50, max_value=120, value=90, step=1)
inflation = st.number_input("Roczna inflacja (%)", min_value=0.0, value=3.0, step=0.1)

if st.button("Policz"):
    age = calculate_retirement_age(obecny_wiek = current_age, miesieczna_wplata = monthly_contrib, roczny_zwrot_z_inwestycji = annual_return, wiek_smierci = projected_lifespan, inflacja = inflation, wartosc_emerytury = annual_expenses, kapital_startowy = capital) 
    st.success(f"Możesz przejść na emeryturę w wieku {age} lat 🎉")
