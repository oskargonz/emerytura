import streamlit as st
import pandas as pd
from retirement_calc import calculate_retirement_age

st.title("💰 Kalkulator Wczesnej Emerytury")

current_age = st.number_input(
    "Obecny wiek", min_value=0, max_value=100, value=30, step=1
)
capital = st.number_input("Kapitał początkowy", min_value=0, value=300000, step=1000)
monthly_contrib = st.number_input(
    "Miesięczna inwestycja", min_value=0, value=5000, step=100
)
annual_return = (
    st.number_input("Średnia stopa zwrotu (%)", min_value=0.0, value=6.0, step=0.1)
)
annual_expenses = st.number_input(
    "Miesięczne wydatki", min_value=0, value=12000, step=100
)
projected_lifespan = st.number_input(
    "Przewidywany wiek śmierci", min_value=50, max_value=120, value=90, step=1
)
inflation = st.number_input("Roczna inflacja (%)", min_value=0.0, value=3.0, step=0.1)

if st.button("Policz"):
    with st.spinner('Obliczam wiek emerytury i tworzę wykresy... ⏳'):
        age, kapital_po_emeryturze, chart, capital_timeline, cost_timeline = calculate_retirement_age(
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
        
        # Capital over time chart
        if capital_timeline:
            st.subheader("📈 Kapitał w czasie")
            
            with st.spinner('Tworzę wykres kapitału w czasie...'):
                # Create DataFrame for the chart
                df = pd.DataFrame(capital_timeline)
                
                # Separate data by phase
                accumulation_data = df[df['phase'] == 'Accumulation'].set_index('age')['capital']
                retirement_data = df[df['phase'] == 'Retirement'].set_index('age')['capital']
                
                # Create chart data with both phases
                chart_data = pd.DataFrame({
                    'Faza akumulacji': accumulation_data,
                    'Faza emerytury': retirement_data
                })
                
                # Display the line chart with colored series
                st.line_chart(chart_data)
            
            # Add phase information
            st.write("**Legenda:**")
            col1, col2 = st.columns(2)
            with col1:
                st.write("🟢 **Faza akumulacji** - oszczędzanie do emerytury")
            with col2:
                st.write("🔴 **Faza emerytury** - wydawanie kapitału")
            
            # Show key milestones
            st.write("**Kluczowe punkty:**")
            retirement_capital = df[df['phase'] == 'Accumulation']['capital'].iloc[-1] if len(df[df['phase'] == 'Accumulation']) > 0 else 0
            st.write(f"• Kapitał w momencie przejścia na emeryturę: {retirement_capital:,.0f} PLN")
            max_capital = df['capital'].max()
            max_capital_age = df[df['capital'] == max_capital]['age'].iloc[0]
            st.write(f"• Maksymalny kapitał: {max_capital:,.0f} PLN w wieku {max_capital_age} lat")
        
        # Monthly costs over time chart
        if cost_timeline:
            st.subheader("💸 Miesięczne koszty w czasie (wpływ inflacji)")
            
            with st.spinner('Tworzę wykres kosztów w czasie...'):
                # Create DataFrame for the costs chart
                cost_df = pd.DataFrame(cost_timeline)
                
                # Separate data by phase for costs
                accumulation_costs = cost_df[cost_df['phase'] == 'Accumulation'].set_index('age')['monthly_cost']
                retirement_costs = cost_df[cost_df['phase'] == 'Retirement'].set_index('age')['monthly_cost']
                
                # Create chart data with both phases
                cost_chart_data = pd.DataFrame({
                    'Koszty podczas akumulacji': accumulation_costs,
                    'Koszty podczas emerytury': retirement_costs
                })
                
                # Display the line chart
                st.line_chart(cost_chart_data)
            
            # Show cost information
            st.write("**Informacje o kosztach:**")
            current_monthly_cost = annual_expenses
            retirement_monthly_cost = cost_df[cost_df['phase'] == 'Retirement']['monthly_cost'].iloc[0] if len(cost_df[cost_df['phase'] == 'Retirement']) > 0 else current_monthly_cost
            final_monthly_cost = cost_df[cost_df['phase'] == 'Retirement']['monthly_cost'].iloc[-1] if len(cost_df[cost_df['phase'] == 'Retirement']) > 0 else current_monthly_cost
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Obecne koszty miesięczne", f"{current_monthly_cost:,.0f} PLN")
            with col2:
                st.metric("Koszty w momencie emerytury", f"{retirement_monthly_cost:,.0f} PLN", 
                         f"+{((retirement_monthly_cost/current_monthly_cost-1)*100):,.1f}%")
            with col3:
                st.metric("Koszty na koniec życia", f"{final_monthly_cost:,.0f} PLN",
                         f"+{((final_monthly_cost/current_monthly_cost-1)*100):,.1f}%")
            
            st.info(f"💡 **Wpływ inflacji:** Przy inflacji {inflation}% rocznie, Twoje koszty życia będą rosły każdego roku. "
                   f"To oznacza, że za {age - current_age} lat będziesz potrzebować {retirement_monthly_cost:,.0f} PLN miesięcznie "
                   f"zamiast obecnych {current_monthly_cost:,.0f} PLN, aby utrzymać ten sam standard życia.")
            
        # Tworzenie wykresu danych z tabeli chart
        if chart:
            st.subheader("📊 Analiza scenariuszy emerytury")
            st.write("Wykres pokazuje w jakim wieku skończą się fundusze dla różnych wieków przejścia na emeryturę:")
            
            with st.spinner('Tworzę wykres scenariuszy emerytury...'):
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
            
            with st.spinner('Przygotowuję szczegółowe dane...'):
                # Tworzenie danych tabeli
                table_data = {
                    'Wiek przejścia na emeryturę': retirement_ages,
                    'Wiek wyczerpania funduszy': funds_depletion_ages,
                    'Lata na emeryturze': [funds_age - ret_age for ret_age, funds_age in chart]
                }
                st.dataframe(table_data)
    else:
        st.error("Z podanymi parametrami przejście na emeryturę nie jest możliwe 😞")
