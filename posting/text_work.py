import re

def convert_premium_to_short(premium_text):
    # Find each stock section
    stock_sections = re.findall(r'(\d️⃣[^🔥]+?)(?=\d️⃣|\Z)', premium_text, re.DOTALL)
    
    formatted_parts = []
    
    for section in stock_sections:
        # Extract ticker symbol
        ticker_match = re.search(r'\(([$][A-Z]+)\)', section)
        if not ticker_match:
            continue
        ticker = ticker_match.group(1)
        
        # Extract emoji
        emoji_match = re.search(r'\) ([\u2600-\u27BF\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF])', section)
        emoji = emoji_match.group(1) if emoji_match else ""
        
        # Extract buy range
        buy_match = re.search(r'Buy \$([\d\.]+)–\$([\d\.]+)', section)
        buy_range = f"${buy_match.group(1)}–${buy_match.group(2)}" if buy_match else ""
        
        # Extract target
        target_match = re.search(r'Target: \$([\d\.]+) \(([\d\.]+)%', section)
        target = f"${target_match.group(1)} ({target_match.group(2)}%)" if target_match else ""
        
        # Extract stop
        stop_match = re.search(r'Stop \$([\d\.]+) \(([\d\.]+)%', section)
        stop = f"${stop_match.group(1)} ({stop_match.group(2)}%)" if stop_match else ""
        
        # Extract intraday percentage
        intraday_match = re.search(r'Change from Open: \+([\d\.]+)%', section)
        intraday = f"+{intraday_match.group(1)}% intraday" if intraday_match else ""
        
        # Extract notes
        notes_match = re.search(r'Note: (Confirm [^\.]+)', section)
        notes = notes_match.group(1) if notes_match else ""
        
        # Extract chart URL
        chart_match = re.search(r'Chart: (https://[^\s]+)', section)
        chart_url = chart_match.group(1) if chart_match else ""
        
        # Format post part
        formatted_part = (
            f"🚀 {ticker} Momentum! {emoji}\n"
            f"Buy: {buy_range} | Target: {target} | Stop: {stop}\n"
            f"{intraday}, {notes}. 📈\n"
            f"Chart: {chart_url}"
        )
        
        formatted_parts.append(formatted_part)
    
    if(len(formatted_parts) == 0):
        return ""
    
    return "\n\n".join(formatted_parts) + "\n\nFor informational purposes only, not financial advice."
