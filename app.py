import streamlit as st
from retirement_calc import calculate_retirement_age

st.title("💰 Kalkulator Wczesnej Emerytury")

current_age = st.number_input(
    "Obecny wiek", min_value=0, max_value=100, value=30, step=1
)
capital = st.number_input("Kapitał początkowy", min_value=0, value=100000, step=1000)
monthly_contrib = st.number_input(
    "Miesięczna inwestycja", min_value=0, value=20000, step=1000
)
annual_return = (
    st.number_input("Średnia stopa zwrotu (%)", min_value=0.0, value=5.0, step=0.1)
)
annual_expenses = st.number_input(
    "Miesięczne wydatki", min_value=0, value=40000, step=1000
)
projected_lifespan = st.number_input(
    "Przewidywany wiek śmierci", min_value=50, max_value=120, value=90, step=1
)
inflation = st.number_input("Roczna inflacja (%)", min_value=0.0, value=3.0, step=0.1)

if st.button("Policz"):
    age, kapital_po_emeryturze, chart = calculate_retirement_age(
        current_age=current_age,
        monthly_contribution=monthly_contrib,
        annual_investment_return=annual_return,
        death_age=projected_lifespan,
        inflation=inflation,
        retirement_value=annual_expenses,
        starting_capital=capital,
    )
    
    if age:
        st.success(f"Możesz przejść na emeryturę w wieku {age} lat 🎉")
        st.info(f"Kapitał pozostały po śmierci: {kapital_po_emeryturze:,.0f} PLN")
        
        # Tworzenie wykresu danych z tabeli chart
        if chart:
            st.subheader("📊 Analiza scenariuszy emerytury")
            st.write("Wykres pokazuje w jakim wieku skończą się fundusze dla różnych wieków przejścia na emeryturę:")
            
            # Przygotowanie danych do wykresu
            retirement_ages = [item[0] for item in chart]
            funds_depletion_ages = [item[1] for item in chart]
            
            # Tworzenie DataFrame dla wykresu
            chart_data = {
                'Wiek przejścia na emeryturę': retirement_ages,
                'Wiek wyczerpania funduszy': funds_depletion_ages
            }
            
            # Wykres liniowy
            st.line_chart(chart_data, x='Wiek przejścia na emeryturę', y='Wiek wyczerpania funduszy')
            
            # Dodatkowa tabela z danymi
            st.subheader("📋 Szczegółowe dane")
            
            # Tworzenie danych tabeli
            table_data = {
                'Wiek przejścia na emeryturę': retirement_ages,
                'Wiek wyczerpania funduszy': funds_depletion_ages,
                'Lata na emeryturze': [funds_age - ret_age for ret_age, funds_age in chart]
            }
            st.dataframe(table_data)
    else:
        st.error("Z podanymi parametrami przejście na emeryturę nie jest możliwe 😞")
