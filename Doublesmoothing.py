import numpy as np

# Double Exponential Smoothing Function
def double_exponential_smoothing(data, alpha, beta):
    # Initialize the first smoothed value and the first trend value
    S1 = [data[0]]  # Smoothed value for day 1 is the actual data for day 1
    S2 = [data[0]]  # Trend is initialized to the first data value as well
    forecast = [data[0]]  # Forecast starts as the first data value

    # Loop through the data starting from the second point
    for t in range(1, len(data)):
        # Calculate new smoothed value (level)
        new_S1 = alpha * data[t] + (1 - alpha) * (S1[t - 1] + S2[t - 1])
        S1.append(new_S1)

        # Calculate new trend value
        new_S2 = beta * (S1[t] - S1[t - 1]) + (1 - beta) * S2[t - 1]
        S2.append(new_S2)

        # Forecast for the next period
        new_forecast = S1[t] + S2[t]
        forecast.append(new_forecast)

    return forecast

# Function to forecast the next day
def forecast_next_day(forecast, S1_last, S2_last):
    # Forecast for the next day is the last smoothed value plus the last trend
    return S1_last + S2_last

# Function to calculate Mean Squared Error (MSE)
def mean_squared_error(actual, forecast):
    errors = [(actual[i] - forecast[i]) ** 2 for i in range(len(actual))]
    mse = np.mean(errors)
    return mse

# Function to find the best alpha and beta based on the lowest MSE
def adjust_alpha_beta(data, alphas, betas):
    best_alpha = None
    best_beta = None
    lowest_mse = float('inf')

    for alpha in alphas:
        for beta in betas:
            forecast = double_exponential_smoothing(data, alpha, beta)
            mse = mean_squared_error(data, forecast)
            if mse < lowest_mse:
                lowest_mse = mse
                best_alpha = alpha
                best_beta = beta

    return best_alpha, best_beta, lowest_mse

# Data: Customer visits per day in a restaurant (5 days)
data = [120, 130, 115, 125, 110]

# Initial alpha and beta values
alpha = 0.3
beta = 0.3

# Generate forecast using initial alpha and beta
forecast = double_exponential_smoothing(data, alpha, beta)

# Print the forecast for each day
print("Forecast for each day:")
for day in range(1, len(forecast) + 1):
    print(f"Day {day}: {forecast[day - 1]:.2f}")

# Forecast for the next (6th) day
forecast_day_6 = forecast_next_day(forecast, forecast[-1], forecast[-2])
print(f"\nForecast for Day 6: {forecast_day_6:.2f}")

# Calculate and print the Mean Squared Error (MSE)
mse = mean_squared_error(data, forecast)
print(f"\nMean Squared Error (MSE): {mse:.2f}")

# Test multiple alpha and beta values to find the best combination
alphas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
betas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

best_alpha, best_beta, lowest_mse = adjust_alpha_beta(data, alphas, betas)
print(f"\nBest alpha: {best_alpha}, Best beta: {best_beta}, with the lowest MSE: {lowest_mse:.2f}")
