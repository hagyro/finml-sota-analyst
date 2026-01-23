# FinML SOTA Analyst

**Machine Learning for Financial & Economic Data** — Leakage-resistant, production-grade ML powered by Claude Agent SDK

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Node 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

---

## Overview

FinML SOTA Analyst is an AI agent specialized in machine learning for financial and economic data. Built on the [Claude Agent SDK](https://docs.anthropic.com/en/docs/agent-sdk/overview), it provides autonomous ML pipeline development with strict emphasis on:

- **Leakage Prevention**: Systematic detection and prevention of data leakage
- **Proper Validation**: Time-based splits, walk-forward, purged/embargoed CV
- **Production Standards**: Reproducible, monitored, deployment-ready code
- **SOTA Research**: Real-time search for latest methods with verified citations

### Key Capabilities

| Capability | Description |
|------------|-------------|
| **Baseline Ladder** | Always compares naive → linear → tree → deep models |
| **Leakage Auditing** | Automated detection of look-ahead bias, survivorship, contamination |
| **Walk-Forward Validation** | Proper temporal CV with purging and embargo |
| **Backtest Validation** | Transaction costs, slippage, economic significance |
| **SOTA Search** | arXiv/GitHub search with implementation notes |
| **Feature Engineering** | Point-in-time validated financial features |

### Domain Expertise

- **Time-Series Forecasting**: ARIMA, Prophet, N-BEATS, TFT, PatchTST, TimesFM
- **Asset Pricing**: Factor models, cross-sectional ML, deep factors
- **Risk Modeling**: VaR/ES, volatility (GARCH, HAR-RV, neural)
- **Macro Nowcasting**: MIDAS, DFM, real-time vintages
- **Panel ML**: FE + ML, double ML, multi-level
- **NLP for Finance**: Sentiment, embeddings, earnings calls
- **Graph Learning**: GNNs for markets, supply chains, contagion

---

## Installation

### Prerequisites

1. **Claude Code Runtime** (required):
   ```bash
   # macOS/Linux/WSL
   curl -fsSL https://claude.ai/install.sh | bash
   
   # Homebrew
   brew install --cask claude-code
   
   # Windows
   winget install Anthropic.ClaudeCode
   ```

2. **API Key**:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

### Python

```bash
cd finml

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install base package
pip install -e .

# With ML packages
pip install -e ".[ml]"

# With deep learning
pip install -e ".[ml,deep]"

# With finance data packages
pip install -e ".[ml,finance]"
```

### TypeScript

```bash
cd finml
npm install
npm run build
```

---

## Quick Start

### Python

```python
import asyncio
from finml import run_finml

async def main():
    async for message in run_finml(
        prompt="How do I forecast daily stock volatility using ML?",
        language="Python",
        include_code=True
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### TypeScript

```typescript
import { runFinML } from "./src/finml";

async function main() {
  for await (const message of runFinML({
    prompt: "How do I forecast daily stock volatility using ML?",
    language: "Python",
    includeCode: true
  })) {
    if ("result" in message) {
      console.log(message.result);
    }
  }
}

main();
```

### CLI

```bash
# Direct prompt
python src/finml.py "How do I prevent look-ahead bias in time series CV?"

# Full pipeline
python src/finml.py --pipeline "Predict 5-day forward returns" --data ./prices.csv

# Audit existing code
python src/finml.py --audit ./ml_pipeline/

# Search SOTA methods
python src/finml.py --sota "transformer models for financial time series"

# Validate backtest
python src/finml.py --backtest ./strategy/ --trading

# Generate features
python src/finml.py --features "Next-day returns" --data "Daily OHLCV, 2015-2024"
```

---

## Architecture

### Project Structure

```
finml/
├── src/
│   ├── finml.ts              # TypeScript implementation
│   └── finml.py              # Python implementation
├── .claude/
│   ├── skills/
│   │   └── FINML.md          # Skill definition
│   └── commands/
│       ├── forecast.md       # Time-series forecasting workflow
│       ├── backtest.md       # Backtest validation protocol
│       ├── leakage.md        # Leakage audit checklist
│       └── features.md       # Feature engineering guide
├── tests/
├── logs/                     # Audit logs (auto-created)
├── package.json
├── pyproject.toml
└── README.md
```

### Subagents

| Subagent | Purpose | Tools |
|----------|---------|-------|
| `feature-engineer` | Design leakage-free features | Read, Write, Bash, Glob, Grep |
| `validation-auditor` | Audit for leakage and CV issues | Read, Bash, Glob, Grep |
| `sota-researcher` | Search latest ML research | Read, WebSearch, WebFetch, Glob |
| `backtest-validator` | Validate trading backtests | Read, Bash, Glob, Grep |
| `code-generator` | Generate production ML code | Read, Write, Bash, Glob, Grep |

### Hooks

- **Audit Logging**: All tool calls logged to `logs/finml-audit.jsonl`
- **Command Validation**: Dangerous commands blocked
- **Leakage Warning**: Common leakage patterns flagged in code

---

## Slash Commands

Pre-built workflows for common tasks:

| Command | Description |
|---------|-------------|
| `/forecast` | Complete time-series forecasting pipeline |
| `/backtest` | Trading backtest validation protocol |
| `/leakage` | Systematic leakage audit |
| `/features` | Financial feature engineering guide |

---

## Validation Framework

### Walk-Forward Validation

```
Expanding Window:
|---Train (60%)---|Val|Test|
|------Train (70%)-----|Val|Test|
|--------Train (80%)--------|Val|Test|

Rolling Window:
|---Train (fixed)---|Val|Test|
   |---Train (fixed)---|Val|Test|
      |---Train (fixed)---|Val|Test|
```

### Purged K-Fold (for Panel Data)

```
|Train|Gap|Test|Gap|Train|

Gap = max(prediction_horizon, feature_lookback)
```

### Leakage Prevention Checklist

- [ ] Time-based splits only (no random shuffle)
- [ ] Features use only past information
- [ ] Scalers/encoders fit on train only
- [ ] Hyperparameter tuning uses nested CV
- [ ] Point-in-time data sources verified
- [ ] No survivorship bias

---

## Output Format

```markdown
## Goal
[What we're predicting and why]

## Data/Constraints
[Features, frequency, history, latency requirements]

## Baselines
[Naive, seasonal, linear benchmarks]

## Candidate Models
[Proposed models with rationale]

## Validation
[CV strategy: walk-forward, purged, etc.]

## Metrics
| Model | RMSE | MAE | MDA | Sharpe* |
|-------|------|-----|-----|---------|
| Naive | 0.02 | ... | ... | ...     |
| ...   | ...  | ... | ... | ...     |

## Tuning
[Hyperparameter optimization approach]

## Interpretability
[SHAP, feature importance with caveats]

## Risk Controls
[Drift monitoring, fail-safes]

## Code
[Complete, runnable implementation]

## Next Steps
[Recommended experiments]
```

---

## Examples

### Example 1: Volatility Forecasting

```python
prompt = """
I want to forecast next-day realized volatility for S&P 500 stocks.

Data: Daily OHLCV, 2010-2024, 500 stocks
Target: RV_{t+1} = sqrt(sum of squared 5-min returns)
Horizon: 1 day ahead

What's the best approach?
"""

async for msg in run_finml(prompt=prompt, language="Python"):
    if hasattr(msg, "result"):
        print(msg.result)
```

### Example 2: Cross-Sectional Return Prediction

```python
prompt = """
Build a model to predict monthly stock returns in the cross-section.

Data: Monthly returns, Fama-French factors, firm characteristics
Universe: Russell 1000
Target: Next month excess return
Evaluation: Information coefficient, spread returns

Need proper CV for overlapping monthly returns.
"""

async for msg in run_finml(prompt=prompt, trading_context=True):
    ...
```

### Example 3: Pipeline Audit

```bash
python src/finml.py --audit ./my_ml_pipeline/

# Output includes:
# - Leakage issues found
# - CV problems identified
# - Code corrections suggested
# - Estimated impact on results
```

---

## Metrics Reference

### ML Metrics

| Metric | Formula | Use Case |
|--------|---------|----------|
| RMSE | √(mean((y-ŷ)²)) | Standard regression |
| MAE | mean(\|y-ŷ\|) | Robust to outliers |
| MAPE | mean(\|y-ŷ\|/\|y\|) | Scale-independent |
| MDA | mean(sign(Δy)==sign(Δŷ)) | Direction accuracy |

### Financial Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Sharpe | (μ - rf) / σ × √252 | > 0.5 decent, > 1.0 good |
| Sortino | (μ - rf) / σ_down × √252 | > 1.0 good |
| Calmar | CAGR / MaxDD | > 1.0 good |
| Max Drawdown | max peak-to-trough | < 20% typically |

---

## Best Practices

### For Time Series

1. **Never random shuffle** — use TimeSeriesSplit
2. **Respect temporal order** — train before test always
3. **Gap for label leakage** — add embargo equal to horizon
4. **Check stationarity** — transform if needed
5. **Start with baselines** — beat naive first

### For Trading Strategies

1. **Realistic costs** — include transaction costs, slippage
2. **Out-of-sample** — true holdout, not just CV
3. **Multiple testing** — adjust for strategies tested
4. **Economic significance** — Sharpe > 0.5, not just p < 0.05
5. **Capacity check** — can you trade this size?

### For Production

1. **Monitor drift** — feature and target distributions
2. **Retraining schedule** — based on performance decay
3. **Fallback strategy** — when model fails
4. **Logging** — all predictions and features
5. **Version control** — models, data, code

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "SDK not found" | `pip install claude-agent-sdk` |
| "API key missing" | `export ANTHROPIC_API_KEY=...` |
| "Leakage warning" | Check logs, review flagged code |
| Import errors | Activate venv: `source venv/bin/activate` |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built on the [Claude Agent SDK](https://docs.anthropic.com/en/docs/agent-sdk/overview) by Anthropic.

Financial ML methodology informed by best practices from quantitative finance research and industry.
