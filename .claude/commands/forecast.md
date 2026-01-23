# Time-Series Forecasting Pipeline

Build a complete time-series forecasting model with proper validation.

## Input Required
- Prediction target (y) and horizon (h)
- Data frequency (daily, weekly, monthly, etc.)
- Available features and history length
- Loss function / primary metric
- Latency requirements (if production)

## Pipeline Steps

### 1. Problem Formalization
```
- Target: y_{t+h} = ?
- Information set: I_t = {y_{t}, y_{t-1}, ..., X_t, ...}
- Metric: RMSE / MAE / MAPE / Direction accuracy / Custom
```

### 2. Data Exploration
- Summary statistics by time period
- Missing data patterns
- Stationarity tests (ADF, KPSS)
- Seasonality detection
- Outlier identification

### 3. Baseline Models
1. **Naive**: y_{t+h} = y_t (random walk)
2. **Seasonal Naive**: y_{t+h} = y_{t-s+h}
3. **Historical Mean**: y_{t+h} = mean(y)
4. **Drift**: y_{t+h} = y_t + h * trend

### 4. Feature Engineering
- Lags: y_{t-1}, y_{t-2}, ..., y_{t-p}
- Rolling statistics: mean, std, min, max (windows: 5, 10, 20, 60)
- Calendar: day_of_week, month, quarter, is_holiday
- Exponential smoothing features
- Fourier terms for seasonality

**Leakage Check**: All features use only t and earlier!

### 5. Model Candidates
```
Linear:     Ridge, LASSO, Elastic Net
Tree:       XGBoost, LightGBM, CatBoost
Sequence:   LSTM, GRU, Temporal Fusion Transformer
Foundation: TimesFM, Chronos (if applicable)
```

### 6. Validation Strategy
```
Walk-Forward (recommended):
|---Train (60%)---|Val (20%)---|Test (20%)|
Expanding or rolling window

TimeSeriesSplit:
- n_splits = 5
- gap = h (horizon) to prevent leakage
```

### 7. Hyperparameter Tuning
- Use validation fold(s) only
- Nested CV for unbiased estimates
- Optuna / RandomizedSearch with proper CV

### 8. Evaluation
| Metric | Formula | When to Use |
|--------|---------|-------------|
| RMSE | √(mean((y-ŷ)²)) | Standard, sensitive to outliers |
| MAE | mean(|y-ŷ|) | Robust to outliers |
| MAPE | mean(|y-ŷ|/|y|) | Scale-independent |
| MDA | mean(sign(Δy) == sign(Δŷ)) | Direction matters |

### 9. Interpretability
- Feature importance (SHAP for tree models)
- Forecast decomposition
- Residual analysis
- Confidence/prediction intervals

### 10. Production Considerations
- Retraining frequency
- Drift monitoring (feature and target)
- Fallback strategy
- Latency requirements

## Output
- Model comparison table
- Best model with uncertainty estimates
- Feature importance ranking
- Residual diagnostics
- Runnable code
