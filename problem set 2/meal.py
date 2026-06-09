def main():
    time_str = input("What time is it? ")
    time_float = convert(time_str)
    
    if 7.0 <= time_float <= 8.0:
        print("breakfast time")
    elif 12.0 <= time_float <= 13.0:
        print("lunch time")
    elif 18.0 <= time_float <= 19.0:
        print("dinner time")
    else:
        # Temporary test line to see if it's working
        print(f"(Debug: Converted to {time_float:.2f} hours, which is not a meal time)")

def convert(time):
    # Standardize input to lowercase and remove outer spaces
    time = time.lower().strip()
    
    if "p.m." in time or "pm" in time:
        time = time.replace("p.m.", "").replace("pm", "").strip()
        hours, minutes = time.split(":")
        hours = float(hours)
        if hours != 12:
            hours += 12
        return hours + float(minutes) / 60.0
    
    elif "a.m." in time or "am" in time:
        time = time.replace("a.m.", "").replace("am", "").strip()
        hours, minutes = time.split(":")
        hours = float(hours)
        if hours == 12:
            hours = 0
        return hours + float(minutes) / 60.0
        
    else:
        hours, minutes = time.split(":")
        return float(hours) + float(minutes) / 60.0

if __name__ == "__main__":
    main()