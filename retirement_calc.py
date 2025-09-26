def calculate_retirement_age(
    current_age,
    monthly_contribution,
    annual_investment_return,
    death_age,
    inflation,
    retirement_value,
    starting_capital,
):
    """
    Calculates the age at which one can retire.

    Args:
        current_age: current age of the person
        monthly_contribution: average monthly contribution to investments
        annual_investment_return: annual investment return (in percentage, e.g., 6 for 6%)
        death_age: expected age of death
        inflation: annual inflation (in percentage, e.g., 3 for 3%)
        retirement_value: monthly retirement value (in today's money)
        starting_capital: initial capital

    Returns:
        retirement_age: age at which one can retire, or None if impossible
    """

    # Convert percentages to decimal values
    return_rate = annual_investment_return / 100
    inflation_dec = inflation / 100
    chart = []

    # Check each possible retirement age
    for retirement_age in range(current_age, death_age):
        capital = starting_capital
        current_timeline = []  # Track capital for this retirement scenario
        cost_timeline = []  # Track monthly costs over time

        # Accumulation phase (until retirement age)
        accumulation_years = retirement_age - current_age
        for year in range(accumulation_years):
            # Contributions accounting for inflation
            annual_contribution = monthly_contribution * 12 * ((1 + inflation_dec) ** year)
            capital = capital * (1 + return_rate) + annual_contribution
            current_timeline.append({
                'age': current_age + year + 1,
                'capital': capital,
                'phase': 'Accumulation'
            })
            # Track monthly costs during accumulation (assumed to be retirement_value adjusted for inflation)
            monthly_cost_inflated = retirement_value * ((1 + inflation_dec) ** year)
            cost_timeline.append({
                'age': current_age + year + 1,
                'monthly_cost': monthly_cost_inflated,
                'phase': 'Accumulation'
            })

        # Retirement phase (from retirement age to death)
        retirement_years = death_age - retirement_age
        capital_after_retirement = capital

        for year in range(retirement_years):
            # Retirement withdrawal accounting for inflation
            annual_withdrawal = (
                retirement_value * 12 * ((1 + inflation_dec) ** (accumulation_years + year))
            )
            monthly_withdrawal = annual_withdrawal / 12
            capital_after_retirement = capital_after_retirement * (1 + return_rate) - annual_withdrawal
            current_timeline.append({
                'age': retirement_age + year + 1,
                'capital': max(0, capital_after_retirement),  # Don't show negative capital
                'phase': 'Retirement'
            })
            cost_timeline.append({
                'age': retirement_age + year + 1,
                'monthly_cost': monthly_withdrawal,
                'phase': 'Retirement'
            })

            # If capital falls below zero, this retirement age is not possible
            if capital_after_retirement < 0:
                chart.append((retirement_age, retirement_age + year))
                break
        
        if capital_after_retirement > 0:
            return retirement_age, capital_after_retirement, chart, current_timeline, cost_timeline

    return None, None, None, None, None  # Impossible to retire with given parameters


# # Example usage
# if __name__ == "__main__":
#     retirement_age, capital_after_retirement, chart = calculate_retirement_age(
#         current_age=30,
#         monthly_contribution=5000,
#         annual_investment_return=6,
#         death_age=90,
#         inflation=3,
#         retirement_value=12000,
#         starting_capital=300000
#     )

#     if retirement_age:
#         print(f"Możesz przejść na emeryturę w wieku: {retirement_age} lat")
#         print(f"To oznacza {retirement_age - 30} lat oszczędzania")
#         print(f"Kapitał po śmierci: {capital_after_retirement}")
#     else:
#         print("Z podanymi parametrami przejście na emeryturę nie jest możliwe")
