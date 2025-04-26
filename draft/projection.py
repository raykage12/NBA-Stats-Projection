from sklearn.linear_model import LinearRegression
import numpy as np

class PlayerProjection:
    def predict_next_game_points(self, df):
        # Sort games from oldest to newest
        df = df.sort_values(by='GAME_DATE').reset_index(drop=True)
        
        # Prepare the data for Linear Regression (using game number as the feature)
        df['GAME_NUMBER'] = np.arange(1, len(df) + 1)
        X = df['GAME_NUMBER'].values.reshape(-1, 1)  # Feature (game number)
        y = df['PTS'].values  # Target (points scored)

        # Train Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict the next game (21st game)
        next_game = np.array([[len(df) + 1]])  # Next game number (21)
        predicted_pts = model.predict(next_game)[0]

        # Calculate Standard Error of Estimate (SEE)
        residuals = y - model.predict(X)  # Calculate residuals
        SEE = np.sqrt(np.sum(residuals**2) / (len(df) - 2))  # Standard Error of Estimate
        min_projected_pts = predicted_pts - SEE
        max_projected_pts = predicted_pts + SEE 

        print(f"Predicted points for the next game: {predicted_pts:.2f}")
        print(f"Standard Error: {SEE:.2f}")
        print(f"Projected with Standard Error: {min_projected_pts:.0f} - {max_projected_pts:.0f}")
        
        return predicted_pts, SEE