def calculate_retirement_age(
    obecny_wiek,
    miesieczna_wplata,
    roczny_zwrot_z_inwestycji,
    wiek_smierci,
    inflacja,
    wartosc_emerytury,
    kapital_startowy,
):
    """
    Oblicza wiek, w którym można przejść na emeryturę.

    Args:
        obecny_wiek: obecny wiek osoby
        miesieczna_wplata: średnia miesięczna wpłata do inwestycji
        roczny_zwrot_z_inwestycji: roczny zwrot z inwestycji (w procentach, np. 6 dla 6%)
        wiek_smierci: przewidywany wiek śmierci
        inflacja: roczna inflacja (w procentach, np. 3 dla 3%)
        wartosc_emerytury: miesięczna wartość emerytury (w dzisiejszych pieniądzach)
        kapital_startowy: początkowy kapitał

    Returns:
        wiek_emerytury: wiek, w którym można przejść na emeryturę, lub None jeśli niemożliwe
    """

    # Konwersja procentów na wartości dziesiętne
    zwrot = roczny_zwrot_z_inwestycji / 100
    inflacja_dec = inflacja / 100
    chart = []

    # Sprawdzamy każdy możliwy wiek emerytury
    for wiek_emerytury in range(obecny_wiek, wiek_smierci):
        kapital = kapital_startowy

        # Faza akumulacji (do wieku emerytury)
        lata_akumulacji = wiek_emerytury - obecny_wiek
        for rok in range(lata_akumulacji):
            # Wpłaty uwzględniające inflację
            wplata_roczna = miesieczna_wplata * 12 * ((1 + inflacja_dec) ** rok)
            kapital = kapital * (1 + zwrot) + wplata_roczna

        # Faza emerytury (od wieku emerytury do śmierci)
        lata_emerytury = wiek_smierci - wiek_emerytury
        kapital_po_emeryturze = kapital

        for rok in range(lata_emerytury):
            # Wypłata emerytury uwzględniająca inflację
            wyplata_roczna = (
                wartosc_emerytury * 12 * ((1 + inflacja_dec) ** (lata_akumulacji + rok))
            )
            kapital_po_emeryturze = kapital_po_emeryturze * (1 + zwrot) - wyplata_roczna

            # Jeśli kapitał spadnie poniżej zera, ten wiek emerytury nie jest możliwy
            if kapital_po_emeryturze < 0:
                chart.append((wiek_emerytury, wiek_emerytury + rok))
                break
        if kapital_po_emeryturze > 0:
            return wiek_emerytury, kapital_po_emeryturze, chart

    return None, None  # Niemożliwe przejście na emeryturę z podanymi parametrami


# # Przykład użycia
# if __name__ == "__main__":
#     wiek_emerytury, kapital_po_emeryturze, chart = oblicz_wiek_emerytury(
#         obecny_wiek=30,
#         miesieczna_wplata=5000,
#         roczny_zwrot_z_inwestycji=6,
#         wiek_smierci=90,
#         inflacja=3,
#         wartosc_emerytury=12000,
#         kapital_startowy=300000
#     )

#     if wiek_emerytury:
#         print(f"Możesz przejść na emeryturę w wieku: {wiek_emerytury} lat")
#         print(f"To oznacza {wiek_emerytury - 30} lat oszczędzania")
#         print(f"Kapitał po śmierci: {kapital_po_emeryturze}")
#     else:
#         print("Z podanymi parametrami przejście na emeryturę nie jest możliwe")
