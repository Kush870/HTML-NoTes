# Import necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# 1. Data Collection
# Download historical data for a stock (e.g., Apple)
data = yf.download("AAPL", start="2015-01-01", end="2023-01-01")

# 2. Feature Engineering
# Calculate technical indicators
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()
data['RSI'] = ta.RSI(data['Close'], timeperiod=14)

# Drop rows with missing values
data = data.dropna()

# 3. Data Preprocessing
# Define features and target
X = data[['50_MA', '200_MA', 'RSI']].values
y = data['Close'].values

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets (80/20 split)
split_index = int(len(X_scaled) * 0.8)
X_train, X_test = X_scaled[:split_index], X_scaled[split_index:]
y_train, y_test = y[:split_index], y[split_index:]

# Reshape the data for LSTM (samples, timesteps, features)
X_train_reshaped = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test_reshaped = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# 4. Model Development
# Build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=False, input_shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train_reshaped, y_train, epochs=20, batch_size=32, validation_data=(X_test_reshaped, y_test))

# 5. Predictions
# Make predictions
y_pred = model.predict(X_test_reshaped)

# 6. Evaluation
# Plot actual vs predicted values
plt.figure(figsize=(14, 5))
plt.plot(y_test, label='Actual Prices')
plt.plot(y_pred.flatten(), label='Predicted Prices')
plt.title('Actual vs Predicted Stock Prices')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()

# Calculate returns (for Sharpe Ratio calculation)
returns = np.diff(y_test) / y_test[:-1]

# Calculate Sharpe Ratio
sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252)  # Annualized
print(f'Sharpe Ratio: {sharpe_ratio:.2f}')
