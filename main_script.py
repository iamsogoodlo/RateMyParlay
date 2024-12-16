import webscraper as ws 
# Main script
while True:
    try:
        first_name = input("Player first name: ")
        last_name = input("Player last name: ")
        name = ws.player_name(first_name, last_name)
        url = ws.create_url_player(name)
        df = ws.scrape_player_stats(url)
        break
    except Exception as e:
        print(f"Error fetching player stats: {e}. Please try again.")

while True:
    try:
        bet_type = input("What is your bet type: ").lower()
        times_true = ws.take_leg(bet_type, df)
        if times_true is not None:
            leg_rating = ws.rate_leg(times_true)
            print(f"Leg rating: {leg_rating}")
            break
    except Exception as e:
        print(f"Error evaluating leg: {e}. Please try again.")

while True:
    try:
        odds = input("Odds of bet (+/-): ")
        amt_wagered = input("How much did you wager: ")
        ev = ws.calculate_expected_value(odds, amt_wagered)
        if ev:
            print("Expected Value Calculation:", ev)
            break
    except Exception as e:
        print(f"Error calculating expected value: {e}. Please try again.")
