# Financial Feature Engineering

Design and validate features for financial ML models.

## Input Required
- Prediction target and horizon
- Available raw data (OHLCV, fundamentals, alternative)
- Point-in-time constraints
- Cross-sectional vs time-series context

## Feature Categories

### 1. Price-Based Features

```python
# Returns
returns_1d = close.pct_change(1)
returns_5d = close.pct_change(5)
log_returns = np.log(close / close.shift(1))

# Momentum
momentum_20d = close / close.shift(20) - 1
momentum_60d = close / close.shift(60) - 1
momentum_252d = close / close.shift(252) - 1

# Mean Reversion
deviation_from_ma20 = close / close.rolling(20).mean() - 1
deviation_from_ma60 = close / close.rolling(60).mean() - 1

# Price levels
high_52w = close.rolling(252).max()
low_52w = close.rolling(252).min()
pct_from_high = (close - high_52w) / high_52w
```

### 2. Volume Features

```python
# Volume statistics
volume_ma20 = volume.rolling(20).mean()
volume_ratio = volume / volume_ma20
abnormal_volume = (volume - volume_ma20) / volume.rolling(20).std()

# Dollar volume
dollar_volume = close * volume
dollar_volume_ma = dollar_volume.rolling(20).mean()

# VWAP
vwap = (close * volume).rolling(20).sum() / volume.rolling(20).sum()
vwap_deviation = close / vwap - 1
```

### 3. Volatility Features

```python
# Realized volatility (annualized)
returns = close.pct_change()
vol_20d = returns.rolling(20).std() * np.sqrt(252)
vol_60d = returns.rolling(60).std() * np.sqrt(252)

# Parkinson volatility (high-low based)
parkinson = np.sqrt(1/(4*np.log(2)) * (np.log(high/low)**2))
parkinson_20d = parkinson.rolling(20).mean()

# Garman-Klass volatility
gk = 0.5*(np.log(high/low))**2 - (2*np.log(2)-1)*(np.log(close/open_))**2

# Volatility regime
vol_zscore = (vol_20d - vol_60d.rolling(60).mean()) / vol_60d.rolling(60).std()
```

### 4. Technical Indicators

```python
# RSI
delta = close.diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rsi = 100 - (100 / (1 + gain/loss))

# MACD
ema12 = close.ewm(span=12).mean()
ema26 = close.ewm(span=26).mean()
macd = ema12 - ema26
signal = macd.ewm(span=9).mean()
macd_hist = macd - signal

# Bollinger Bands
bb_mid = close.rolling(20).mean()
bb_std = close.rolling(20).std()
bb_upper = bb_mid + 2*bb_std
bb_lower = bb_mid - 2*bb_std
bb_pctb = (close - bb_lower) / (bb_upper - bb_lower)
```

### 5. Cross-Sectional Features

```python
# Ranks (0-1 scale)
def cross_sectional_rank(series):
    return series.rank(pct=True)

momentum_rank = df.groupby('date')['momentum_20d'].transform(cross_sectional_rank)
size_rank = df.groupby('date')['market_cap'].transform(cross_sectional_rank)

# Z-scores within peer group
def cross_sectional_zscore(series):
    return (series - series.mean()) / series.std()

vol_zscore_xs = df.groupby('date')['vol_20d'].transform(cross_sectional_zscore)

# Industry-adjusted
industry_mean = df.groupby(['date', 'industry'])['returns'].transform('mean')
industry_adjusted_return = df['returns'] - industry_mean
```

### 6. Fundamental Features

```python
# Valuation ratios (use lagged to avoid look-ahead)
pe_ratio = price / earnings_ttm.shift(1)  # Lag for reporting delay
pb_ratio = price / book_value.shift(1)
ps_ratio = market_cap / revenue_ttm.shift(1)

# Quality
roe = net_income_ttm / book_value.shift(4)  # Quarterly lag
roa = net_income_ttm / total_assets.shift(4)
gross_margin = gross_profit / revenue_ttm

# Growth
revenue_growth_yoy = revenue_ttm / revenue_ttm.shift(4) - 1
earnings_growth_yoy = earnings_ttm / earnings_ttm.shift(4) - 1
```

### 7. Calendar Features

```python
# Time dummies
day_of_week = date.dt.dayofweek
month = date.dt.month
quarter_end = date.dt.is_quarter_end.astype(int)

# Seasonal patterns
month_sin = np.sin(2 * np.pi * date.dt.month / 12)
month_cos = np.cos(2 * np.pi * date.dt.month / 12)

# Days to/from events
days_to_earnings = (next_earnings_date - date).dt.days
days_from_dividend = (date - last_dividend_date).dt.days
```

## Leakage Prevention Checklist

- [ ] All rolling calculations use `.shift(1)` after rolling
- [ ] Fundamental data lagged for reporting delay (45-90 days)
- [ ] Cross-sectional features computed within each date
- [ ] No future information in any feature
- [ ] Point-in-time data sources verified

## Feature Validation

```python
def validate_feature(feature, target, dates):
    """
    Validate a feature for quality and leakage.
    """
    results = {}
    
    # 1. Missing data
    results['missing_pct'] = feature.isna().mean()
    
    # 2. Correlation with target
    results['target_corr'] = feature.corr(target)
    
    # 3. Stability over time
    rolling_corr = feature.rolling(252).corr(target)
    results['corr_stability'] = rolling_corr.std()
    
    # 4. Autocorrelation (persistence)
    results['autocorr_1d'] = feature.autocorr(1)
    
    # 5. Distribution check
    results['skewness'] = feature.skew()
    results['kurtosis'] = feature.kurtosis()
    
    # 6. Leakage warning
    if abs(results['target_corr']) > 0.5:
        results['warning'] = "High correlation - check for leakage"
    
    return results
```

## Output
- Feature definitions with formulas
- Point-in-time documentation
- Validation statistics table
- Correlation matrix
- Recommended feature set
