
saldo: float = 3311
wydatki: float = 1000
przychody: float = 0

burn_rate: float = wydatki
runaway: float = saldo / burn_rate

line = "=" * 40
line_thin = "-" * 40

print(f"""
{line}
💰 BUDGET CHECK — kwiecień 2026
{line}
Saldo startowe:         {saldo:.2f} zł
Wydatki miesięczne:     {wydatki:.2f} zł
Przychody miesięczne:   {przychody:.2f} zł
{line_thin}
Burn rate:              {burn_rate:.2f} zł/mies
Runaway:                {runaway:.1f} miesięcy
{line_thin}
Za 1 miesiąc:           {(saldo - burn_rate * 1):.2f} zł
Za 3 miesiące:          {(saldo - burn_rate * 3):.2f} zł
Za 6 miesięcy:          {(saldo - burn_rate * 6):.2f} zł ⚠️
{line}
""")