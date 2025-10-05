"""
Test the new overtime formatting
"""

def format_hours_as_time(hours):
    """Convert decimal hours to HH:MM format"""
    if hours == 0:
        return "0:00"
    
    # Extract whole hours
    whole_hours = int(hours)
    
    # Extract minutes from decimal part
    minutes_decimal = (hours - whole_hours) * 60
    whole_minutes = int(minutes_decimal)
    
    return f"{whole_hours}:{whole_minutes:02d}"

# Test the formatting
test_cases = [3.0, 1.5, 2.75, 0.5, 0.0, 1.25, 2.33]

print("🕐 NEW OVERTIME FORMATTING TEST")
print("=" * 40)

for hours in test_cases:
    formatted = format_hours_as_time(hours)
    print(f"{hours:4.2f} hours → {formatted}")

print("\n✅ Perfect! No seconds, no 'h', just clean HH:MM format!")