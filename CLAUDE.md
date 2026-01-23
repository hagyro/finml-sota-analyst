# FinML SOTA Analyst Project Context

## Overview
FinML SOTA Analyst is an AI agent for machine learning in financial and economic data. It emphasizes leakage prevention, proper validation, and production standards.

## Design Principles

1. **Leakage Prevention First**: Assume leakage until proven otherwise
2. **Baseline Ladder**: Always compare naive → linear → tree → deep
3. **Temporal Integrity**: Time-based splits, walk-forward, purged CV
4. **Economic Significance**: Not just statistical metrics
5. **Reproducibility**: Seeds, versions, documentation

## Key Components

### System Prompt
Located in `src/finml.ts` and `src/finml.py`. Contains:
- Core identity and specializations
- 8 operating rules
- Domain-specific knowledge
- Code standards

### Subagents
Five specialized agents:
- `feature-engineer`: Leakage-free feature design
- `validation-auditor`: CV and leakage auditing
- `sota-researcher`: arXiv/GitHub search
- `backtest-validator`: Trading backtest validation
- `code-generator`: Production ML code

### Slash Commands
Pre-built workflows:
- `/forecast` - Time-series forecasting pipeline
- `/backtest` - Backtest validation protocol
- `/leakage` - Systematic leakage audit
- `/features` - Feature engineering guide

## Code Conventions

### Python Preferences
- sklearn pipelines for preprocessing
- TimeSeriesSplit or custom walk-forward
- XGBoost/LightGBM for tree models
- PyTorch for deep learning
- SHAP for interpretability
- Optuna for hyperparameter tuning

### Validation Patterns
```python
# CORRECT: Time-based split
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5, gap=horizon)

# WRONG: Random split for time series
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, shuffle=True)  # LEAKAGE!
```

### Feature Engineering
```python
# CORRECT: Use only past information
feature = price.shift(1).rolling(20).mean()  # t-1 to t-20

# WRONG: Look-ahead
feature = price.shift(-1)  # Uses future!
```

## Testing

Run tests with:
```bash
pytest tests/ -v
```

## Common Workflows

### Adding a New Model Type
1. Add to system prompt knowledge section
2. Update baseline ladder if applicable
3. Add validation considerations
4. Include interpretability notes

### Modifying Validation Logic
1. Update validation-auditor subagent
2. Add to leakage.md slash command
3. Update hooks if automated checks needed

## Leakage Checklist

Always verify:
- [ ] No `.shift(-n)` with negative n
- [ ] Scalers fit on train only
- [ ] No random shuffle for time series
- [ ] Point-in-time data sources
- [ ] Purge/embargo for overlapping labels
- [ ] No survivorship bias

## References

- Agent SDK docs: https://docs.anthropic.com/en/docs/agent-sdk/overview
- Financial ML: Lopez de Prado "Advances in Financial ML"
- Time Series: Hyndman & Athanasopoulos "Forecasting: Principles and Practice"
