from projection import PlayerProjection
from nbastats import NBAStats

if __name__ == "__main__":
    while True:
        try:
            stats = NBAStats()
            projection = PlayerProjection()
            player_name = input("\nEnter player full name (e.g., 'Luka Doncic'): ")        
            player_id = stats.get_player_id(player_name)
            if player_id:
                season = input("Enter season (e.g., '2024-25'):  ")
                print("Searching...\n")
                df = stats.get_last_20_combined_games(player_id, season)  ###### Adjust season as needed #########
                print("Last 20 games:\n", df)
                #save_to_csv(df, player_name)
                predicted_pts, SEE = projection.predict_next_game_points(df)
            else:
                print("Player not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please check the player name and/or season selected are in correct format")
        # Ask if the user wants to check another player    
        cont = input("\nDo you want to check another player? ('y' to continue): ").strip().lower()
        if cont != 'y':
            break
    print("Program Exited")
