import csv
import json
import io
import re
from datetime import datetime

csv_text = """Account Number,Account Name,Symbol,Description,Quantity,Last Price,Last Price Change,Current Value,Today's Gain/Loss Dollar,Today's Gain/Loss Percent,Total Gain/Loss Dollar,Total Gain/Loss Percent,Percent Of Account,Cost Basis Total,Average Cost Basis,Type
Z26865567,Individual - TOD,SPAXX**,HELD IN MONEY MARKET,,,,$29312.12,,,,,40.12%,,,Cash,
Z26865567,Individual - TOD,AAPL,APPLE INC,11.482,$276.83,-$3.31,$3178.56,-$38.01,-1.19%,+$979.38,+44.53%,4.35%,$2199.18,$191.53,Margin,
Z26865567,Individual - TOD,ACHR,ARCHER AVIATION INC COM CL A,106.114,$5.77,-$0.10,$612.27,-$10.62,-1.71%,-$191.89,-23.87%,0.84%,$804.16,$7.58,Margin,
Z26865567,Individual - TOD,AMD,ADVANCED MICRO DEVICES INC,0.004,$341.54,-$19.00,$1.36,-$0.08,-5.27%,+$0.97,+250.29%,0.00%,$0.39,$97.50,Margin,
Z26865567,Individual - TOD,AMZN,AMAZON.COM INC,15.748,$272.05,+$3.79,$4284.24,+$59.68,+1.41%,+$1983.64,+86.22%,5.86%,$2300.60,$146.09,Margin,
Z26865567,Individual - TOD,ATYR,ATYR PHARMA INC COM NEW,100,$0.8429,+$0.0094,$84.29,+$0.94,+1.12%,-$188.38,-69.09%,0.12%,$272.67,$2.73,Margin,
Z26865567,Individual - TOD,CMG,CHIPOTLE MEXICAN GRILL INC,114.702,$31.98,-$1.00,$3668.16,-$114.71,-3.04%,-$995.10,-21.34%,5.02%,$4663.26,$40.66,Margin,
Z26865567,Individual - TOD,CZR,CAESARS ENTERTAINMENT INC NEW COM,101.018,$27.41,-$0.97,$2768.90,-$97.99,-3.42%,-$106.77,-3.72%,3.79%,$2875.67,$28.47,Margin,
Z26865567,Individual - TOD, -CZR270319C30,CZR MAR 19 2027 $30 CALL,-1,$3.00,+$0.01,-$300.00,-$1.00,-0.34%,-$70.67,-30.82%,-0.41%,$229.33,$2.29,Margin,
Z26865567,Individual - TOD,DIS,DISNEY WALT CO COM,0.095,$101.31,-$1.77,$9.62,-$0.17,-1.72%,+$1.11,+13.09%,0.01%,$8.51,$89.58,Margin,
Z26865567,Individual - TOD,F,FORD MTR CO DEL COM,64.585,$11.50,-$0.38,$742.72,-$24.55,-3.20%,+$108.12,+17.03%,1.02%,$634.60,$9.83,Margin,
Z26865567,Individual - TOD,GOOGL,ALPHABET INC CAP STK CL A,24.966,$383.25,-$2.44,$9568.21,-$60.92,-0.64%,+$6036.36,+170.91%,13.10%,$3531.85,$141.47,Margin,
Z26865567,Individual - TOD,KO,COCA-COLA CO,5.679,$78.19,-$0.39,$444.04,-$2.22,-0.50%,+$36.80,+9.03%,0.61%,$407.24,$71.71,Margin,
Z26865567,Individual - TOD,LYFT,LYFT INC CL A COM,100,$14.06,-$0.36,$1406.00,-$36.00,-2.50%,-$801.66,-36.32%,1.92%,$2207.66,$22.08,Margin,
Z26865567,Individual - TOD,MSFT,MICROSOFT CORP,6.678,$413.62,-$0.82,$2762.15,-$5.48,-0.20%,+$647.74,+30.63%,3.78%,$2114.41,$316.62,Margin,
Z26865567,Individual - TOD,NVDA,NVIDIA CORPORATION COM,17,$198.48,+$0.03,$3374.16,+$0.51,+0.01%,+$3142.87,+1358.84%,4.62%,$231.29,$13.61,Margin,
Z26865567,Individual - TOD,SBUX,STARBUCKS CORP COM USD0.001,2,$104.97,-$0.93,$209.94,-$1.86,-0.88%,+$42.01,+25.01%,0.29%,$167.93,$83.97,Margin,
Z26865567,Individual - TOD,SPY,STATE STREET SPDR S&P 500 ETF UNITS,3.914,$718.01,-$2.64,$2810.29,-$10.34,-0.37%,+$607.41,+27.57%,3.85%,$2202.88,$562.82,Margin,
Z26865567,Individual - TOD,STZ,CONSTELLATION BRANDS INC COM USD0.01 CLASS A,3.882,$148.14,-$4.68,$575.07,-$18.17,-3.07%,-$65.84,-10.28%,0.79%,$640.91,$165.10,Margin,
Z26865567,Individual - TOD,UNH,UNITEDHEALTH GROUP INC,20.148,$370.75,+$1.97,$7469.87,+$39.69,+0.53%,+$1443.56,+23.95%,10.23%,$6026.31,$299.10,Margin,
Z26865567,Individual - TOD,WOLF,WOLFSPEED INC COMMON STOCK,2,$35.94,-$0.82,$71.88,-$1.64,-2.24%,-$228.12,-76.04%,0.10%,$300.00,$150.00,Margin,
81424,H&R BLOCK RETIREMENT SAVINGS PLAN,92202V534,VANGUARD TARGET 2050,128.519,$132.41,+$0.10,$17017.07,$0.00,0.00%,+$2462.58,+16.92%,100.00%,$14554.49,$113.25,,"""

def parse_fidelity_row(row):
    symbol = row['Symbol'].strip()
    if not symbol or symbol.startswith('SPAXX') or symbol.endswith('**'):
        return None
    
    # Handle option symbols like " -CZR270319C30"
    is_option = False
    clean_symbol = symbol.lstrip('-').strip()
    if re.search(r'\d{6}[CP]\d+', clean_symbol):
        is_option = True
        # Extraction logic could be more complex but we'll use symbol as is for now
        
    qty_str = row['Quantity'].replace(',', '')
    qty = float(qty_str) if qty_str else 0.0
    
    price_str = row['Average Cost Basis'].replace('$', '').replace(',', '')
    price = float(price_str) if price_str and price_str != 'n/a' else 0.0
    
    action = "Buy" if qty >= 0 else "Sell"
    
    return {
        "ticker": clean_symbol if not is_option else clean_symbol[:4].strip(), # Simple ticker extraction for options
        "date": "2026-05-04",
        "action": action,
        "quantity": abs(qty),
        "price": price,
        "strategy": "Fidelity Import"
    }

f = io.StringIO(csv_text)
reader = csv.DictReader(f)
trades = []
for row in reader:
    trade = parse_fidelity_row(row)
    if trade:
        trades.append(trade)

print(json.dumps(trades, indent=4))
