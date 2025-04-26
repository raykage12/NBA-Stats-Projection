import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
import time
import os


class NBAStats:
    def get_player_id(self, full_name):
        player_dict = players.find_players_by_full_name(full_name)
        return player_dict[0]['id'] if player_dict else None

    def get_games(self, player_id, season, season_type):
        time.sleep(1)  # avoid rate limit
        log = playergamelog.PlayerGameLog(player_id=player_id, season=season, season_type_all_star=season_type)
        df = log.get_data_frames()[0]
        return df[['GAME_DATE', 'MATCHUP', 'PTS']]

    def get_last_20_combined_games(self, player_id, season):
        regular_df = self.get_games(player_id, season, 'Regular Season')
        playoffs_df = self.get_games(player_id, season, 'Playoffs')
        
        combined = pd.concat([regular_df, playoffs_df])
        combined['GAME_DATE'] = pd.to_datetime(combined['GAME_DATE'])
        combined = combined.sort_values(by='GAME_DATE', ascending=False)
        return combined.head(20)
    
    # Never called in main function. Do not currently want to save anything but keep for future use
    def save_to_csv(self, df, player_name):
        os.makedirs("players", exist_ok=True)
        filename = os.path.join("players", player_name.replace(" ", "_").lower() + "_last_20_all_games.csv")
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")