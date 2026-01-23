# Data Leakage Audit

Systematic audit for data leakage in ML pipelines.

## Leakage Types

### 1. Look-Ahead Bias (Temporal Leakage)

**Definition**: Using information not available at prediction time.

**Common Sources**:
- Future values in feature calculation
- Using revised data instead of real-time vintages
- Incorrect lag specification
- Target encoding without proper CV

**Detection**:
```python
# Check feature timestamps
for col in features.columns:
    # Feature date should be <= prediction date
    assert all(feature_dates[col] <= prediction_dates)

# Check for negative shifts
# BAD: df['feature'] = df['target'].shift(-1)  # Uses future!
# GOOD: df['feature'] = df['target'].shift(1)   # Uses past
```

### 2. Target Leakage

**Definition**: Features derived from or correlated with the target through a causal path that wouldn't exist at prediction time.

**Examples**:
- Including the target (or proxy) as a feature
- Features that are consequences of the target
- Labels from the future

**Detection**:
```python
# Suspiciously high correlation
for col in features.columns:
    corr = np.corrcoef(features[col], target)[0,1]
    if abs(corr) > 0.9:
        print(f"WARNING: {col} has {corr:.2f} correlation with target")
```

### 3. Train-Test Contamination

**Definition**: Information from test set influencing training.

**Common Sources**:
- Fitting scalers on full data
- Feature selection on full data
- Hyperparameter tuning without nested CV
- Random train/test splits for time series

**Correct Pattern**:
```python
# BAD
scaler.fit(X_all)  # Sees test data!
X_train_scaled = scaler.transform(X_train)

# GOOD
scaler.fit(X_train)  # Only sees train
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### 4. Cross-Sectional Contamination (Panel Data)

**Definition**: Information leaking across entities due to overlapping time periods.

**When It Matters**:
- Predictions for multiple assets at same time
- Overlapping return windows
- Cross-sectional features using contemporaneous data

**Solution**: Purged/Embargoed CV
```python
# Purge: Remove train samples with labels overlapping test
# Embargo: Additional gap after purge

from sklearn.model_selection import TimeSeriesSplit

class PurgedKFold:
    def __init__(self, n_splits, purge_gap):
        self.n_splits = n_splits
        self.purge_gap = purge_gap
    
    def split(self, X, y, times):
        # Implementation removes overlapping samples
        ...
```

### 5. Survivorship Bias

**Definition**: Only including entities that survived to the end of the sample.

**Impact**: Overstates returns (losers disappear)

**Detection**:
```python
# Check if any assets appear, disappear, or change
assets_by_date = df.groupby('date')['asset_id'].apply(set)
for i in range(1, len(assets_by_date)):
    dropped = assets_by_date.iloc[i-1] - assets_by_date.iloc[i]
    if dropped:
        print(f"Assets dropped on {assets_by_date.index[i]}: {dropped}")
```

## Audit Checklist

### Feature Engineering
- [ ] All features use only past information
- [ ] Rolling calculations exclude current observation
- [ ] Point-in-time data sources verified
- [ ] No features derived from target

### Validation Setup
- [ ] Time-based splits (no random shuffle)
- [ ] Gap/embargo for overlapping labels
- [ ] Scalers fit on train only
- [ ] Feature selection in CV fold

### Data Quality
- [ ] No survivorship bias
- [ ] Consistent universe definition
- [ ] Missing data handled before splitting

### Code Review
- [ ] No `.shift(-n)` with negative n
- [ ] No `future`, `next`, `forward` in feature names
- [ ] Train/test separation before any fitting
- [ ] Proper datetime handling

## Automated Checks

```python
def audit_pipeline(X_train, X_test, y_train, y_test, times_train, times_test):
    issues = []
    
    # Check temporal ordering
    if times_train.max() >= times_test.min():
        issues.append("CRITICAL: Train times overlap with test")
    
    # Check for perfect predictors
    for col in X_train.columns:
        corr = np.corrcoef(X_train[col], y_train)[0,1]
        if abs(corr) > 0.95:
            issues.append(f"CRITICAL: {col} nearly perfectly predicts target")
    
    # Check distribution shift
    for col in X_train.columns:
        ks_stat, p_val = ks_2samp(X_train[col], X_test[col])
        if p_val < 0.001:
            issues.append(f"WARNING: {col} has distribution shift (p={p_val:.4f})")
    
    return issues
```

## Output
- List of identified leakage issues
- Severity ranking (critical/high/medium/low)
- Specific code locations
- Corrected implementations
- Estimated impact on results
