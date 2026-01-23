# Backtest Validation Protocol

Comprehensive validation of a trading strategy backtest.

## Input Required
- Strategy description and logic
- Backtest code or results
- Data source and period
- Asset class and trading frequency

## Validation Checklist

### 1. Data Integrity

**Point-in-Time Data**
- [ ] No look-ahead bias in data
- [ ] Using as-reported data, not revised
- [ ] Proper handling of announcement dates

**Survivorship Bias**
- [ ] Includes delisted securities
- [ ] Handles mergers, bankruptcies, spinoffs
- [ ] Universe defined at each rebalance date

**Corporate Actions**
- [ ] Dividends adjusted correctly
- [ ] Splits/reverse splits handled
- [ ] Stock distributions accounted for

### 2. Execution Realism

**Transaction Costs**
```
Asset Class          Typical Cost (bps)
-----------------------------------------
Large Cap Equities   5-15 bps
Small Cap Equities   20-50 bps
ETFs                 2-10 bps
Futures              1-5 bps
FX Spot              2-10 bps
Bonds (IG)           10-30 bps
Bonds (HY)           30-100 bps
```

**Slippage Model**
- [ ] Market impact considered
- [ ] Bid-ask spread included
- [ ] Volume constraints respected

**Fill Assumptions**
- [ ] No trading at close if signal uses close
- [ ] Partial fills for large orders
- [ ] Realistic execution prices

### 3. Statistical Validity

**Sample Size**
- [ ] Sufficient independent observations
- [ ] Multiple market regimes covered
- [ ] At least 3-5 years for daily strategies

**Multiple Testing**
- [ ] Adjusted for variants tested
- [ ] False discovery rate controlled
- [ ] Reported p-values corrected

**Out-of-Sample**
- [ ] True holdout period exists
- [ ] No "peeking" at test period
- [ ] Walk-forward validation used

### 4. Performance Metrics

**Risk-Adjusted Returns**
```python
sharpe_ratio = (returns.mean() - rf) / returns.std() * np.sqrt(252)
sortino_ratio = (returns.mean() - rf) / returns[returns < 0].std() * np.sqrt(252)
calmar_ratio = cagr / max_drawdown
```

**Drawdown Analysis**
- Maximum drawdown
- Average drawdown duration
- Recovery time distribution

**Consistency**
- Rolling Sharpe stability
- Win rate by period
- Profit factor (gross profit / gross loss)

### 5. Robustness Tests

**Parameter Sensitivity**
- Vary key parameters ±20%
- Check for cliff effects
- Ensure smooth degradation

**Regime Analysis**
- Performance in bull/bear markets
- High/low volatility periods
- Different interest rate environments

**Bootstrap Analysis**
```python
# Bootstrap confidence interval for Sharpe
n_bootstrap = 10000
sharpes = []
for _ in range(n_bootstrap):
    sample = np.random.choice(returns, size=len(returns), replace=True)
    sharpes.append(sample.mean() / sample.std() * np.sqrt(252))
ci_95 = np.percentile(sharpes, [2.5, 97.5])
```

### 6. Red Flags

| Warning Sign | Typical Threshold |
|--------------|-------------------|
| Sharpe > 2.5 | Suspicious for most strategies |
| Max DD < 5%  | Likely overfitted or unrealistic |
| Win rate > 70% | Check for look-ahead |
| 100% invested always | Missing cash drag |
| No losing years | Cherry-picked period |

### 7. Capacity Analysis

- Estimate market impact for target AUM
- Calculate days to build/unwind position
- Assess strategy capacity ceiling

## Output
- Validation summary (pass/fail/warning)
- Specific issues with locations
- Corrected estimates where applicable
- Recommendations for improvement
