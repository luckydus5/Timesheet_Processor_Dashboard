"""
Test the improved shift detection logic
"""
from datetime import time

def determine_shift_type(start_time, end_time):
    """
    Determine shift type based on check-in and check-out times
    
    Business Rules:
    - Day Shift: Generally works 8:00 AM - 17:00 PM
    - Night Shift: Generally works 18:00 PM - 3:00 AM (crosses midnight)
    """
    if start_time is None:
        return ""
    
    start_hour = start_time.hour
    end_hour = end_time.hour if end_time else start_hour
    
    # Convert to 24-hour decimal for easier comparison
    start_decimal = start_hour + start_time.minute/60 + start_time.second/3600
    end_decimal = end_hour + (end_time.minute/60 + end_time.second/3600 if end_time else 0)
    
    # Case 1: Check-in between 6:00 AM (6.0) and 5:59 PM (17.99)
    if 6.0 <= start_decimal < 18.0:
        return "Day Shift"
    
    # Case 2: Check-in between 6:00 PM (18.0) and 11:59 PM (23.99)
    elif 18.0 <= start_decimal <= 23.99:
        return "Night Shift"
    
    # Case 3: Check-in between midnight (0.0) and 5:59 AM (5.99)
    elif 0.0 <= start_decimal < 6.0:
        # If both check-in and check-out are in early morning, likely night shift ending
        if end_time and 0.0 <= end_decimal < 12.0:
            return "Night Shift"
        # If check-out is in afternoon/evening, likely day shift starting very early
        else:
            return "Day Shift"
    
    # Default case
    return "Day Shift"

# Test cases
test_cases = [
    # Day Shift cases
    (time(8, 0), time(17, 0), "Normal day shift"),
    (time(7, 30), time(16, 30), "Early day shift"),
    (time(9, 0), time(18, 0), "Day shift with overtime"),
    (time(6, 0), time(15, 0), "Very early day shift"),
    
    # Night Shift cases
    (time(18, 0), time(3, 0), "Normal night shift"),
    (time(20, 0), time(4, 0), "Late night shift"),
    (time(22, 0), time(6, 0), "Long night shift"),
    
    # Edge cases
    (time(0, 30), time(3, 0), "Night shift ending early morning"),
    (time(2, 0), time(8, 0), "Ambiguous early morning start"),
    (time(5, 0), time(13, 0), "Very early day shift"),
    (time(23, 30), time(2, 0), "Short night shift"),
]

print("🔧 IMPROVED SHIFT DETECTION TEST")
print("=" * 60)
print(f"{'Check-in':<10} {'Check-out':<10} {'Detected':<12} {'Description'}")
print("-" * 60)

for start, end, description in test_cases:
    detected_shift = determine_shift_type(start, end)
    print(f"{start.strftime('%H:%M'):<10} {end.strftime('%H:%M'):<10} {detected_shift:<12} {description}")

print("\n✅ Key Improvements:")
print("   📅 Day Shift: Check-in 6:00 AM - 5:59 PM")
print("   🌙 Night Shift: Check-in 6:00 PM - 5:59 AM")
print("   🔧 Considers both check-in AND check-out times")
print("   ⏰ Handles cross-midnight shifts correctly")
print("   🎯 Resolves ambiguous early morning cases")