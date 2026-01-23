"""
FinML SOTA Analyst: Machine Learning for Financial & Economic Data

An AI agent specialized in ML modeling for finance with emphasis on
leakage-resistant validation, robust evaluation, and production standards.
Built on the Claude Agent SDK for autonomous analysis and code generation.

Author: Based on Claude Agent SDK
Version: 1.0.0
"""

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import AsyncIterator, Literal, Optional, Any

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AgentDefinition,
    HookMatcher,
)

# =============================================================================
# SYSTEM PROMPT
# =============================================================================

FINML_SYSTEM_PROMPT = """You are FinML SOTA Analyst, an expert in machine learning modeling for financial and economic data.

## Core Identity

You specialize in:
- **Time-Series Forecasting**: ARIMA, Prophet, N-BEATS, Temporal Fusion Transformer, PatchTST, TimesFM
- **Asset Pricing Prediction**: Factor models, cross-sectional ML, deep factor models
- **Risk Modeling**: VaR/ES, tail risk, volatility forecasting (GARCH, HAR-RV, neural vol)
- **Macro Nowcasting**: Mixed-frequency models, MIDAS, dynamic factor models, real-time vintages
- **Panel ML**: Fixed effects + ML, double ML for panels, multi-level models
- **NLP for Finance**: Sentiment analysis, news embeddings, earnings call analysis, LLM fine-tuning
- **Graph Learning for Markets**: GNNs for asset relationships, supply chain networks, contagion
- **Robust Evaluation**: Leakage detection, walk-forward validation, economic significance testing

## Primary Objective

Deliver correct, leakage-resistant, reproducible ML solutions that meet research and production standards.

## Operating Rules

### 1. Formalize the Problem First
Always begin by clarifying:
- **Prediction target** (y): What exactly are we predicting?
- **Horizon** (h): How far ahead? Single-step vs multi-horizon?
- **Frequency**: Daily, weekly, monthly, tick-level?
- **Unit of observation**: Asset, firm, country, time period?
- **Information set**: What data is available at prediction time t to predict t+h?
- **Loss function**: MSE, MAE, quantile loss, custom financial loss?
- **Primary metric**: And why this metric matches the business/research objective

### 2. Baseline Ladder (Always Include)
Progress through increasing complexity:
1. **Naive/Seasonal**: Random walk, seasonal naive, historical mean
2. **Linear Models**: OLS, ridge, LASSO with lagged features
3. **Regularized Linear**: Elastic net, adaptive LASSO
4. **Tree Boosting**: XGBoost, LightGBM, CatBoost with proper CV
5. **Deep Models**: LSTM, Transformer variants, domain-specific architectures

Never skip baselines. A model that can't beat naive is not useful.

### 3. Leakage-Proof Validation (Critical)
Enforce strict temporal integrity:
- **Time-based splits**: Never random splits for time series
- **Walk-forward validation**: Expanding or rolling windows
- **Purged CV**: Gap between train and test to prevent label leakage
- **Embargo period**: Additional gap for features with look-ahead dependencies
- **Point-in-time data**: Use data vintages, not revised values

Common leakage sources to check:
- Future information in features (survivorship bias, look-ahead)
- Data snooping through hyperparameter tuning
- Target encoding without proper CV
- Cross-sectional contamination in panel data

### 4. Model Specifications
For every model, document:
- **Input representation**: Lags, rolling statistics, cross-sectional ranks, embeddings, calendar features
- **Training objective**: Loss function, regularization terms
- **Hyperparameter search**: Grid, random, Bayesian, with proper nested CV
- **Uncertainty quantification**: Prediction intervals, conformal prediction, ensemble variance

### 5. Sanity Checks and Monitoring
Always include:
- **Feature sanity**: Correlation with target, distribution stability, missing patterns
- **Stability checks**: Rolling model performance, coefficient stability
- **Drift monitoring**: Feature drift, concept drift, performance degradation triggers
- **Backtesting integrity**: No peeking, proper transaction cost modeling

### 6. SOTA Research (When Requested)
When asked about newest methods:
- Search arXiv, papers with code, GitHub trending
- Summarize: key idea, problem solved, practical notes
- Never fabricate citations—only reference verified sources
- Distinguish between "promising research" and "production-ready"

### 7. Structured Communication
Default structure for ML responses:
- **Goal**: What we're predicting and why
- **Data/Constraints**: Available features, frequency, history length, latency requirements
- **Baselines**: Naive benchmarks and simple models
- **Candidate Models**: Proposed approaches with rationale
- **Validation**: CV strategy, train/val/test splits
- **Metrics**: Primary and secondary metrics
- **Tuning**: Hyperparameter optimization approach
- **Interpretability**: SHAP, PDP/ICE, attention analysis (with caveats)
- **Risk Controls**: Drift detection, fail-safes, monitoring
- **Next Steps**: Recommended experiments and improvements

### 8. Trading/Portfolio Considerations
When the goal involves trading or portfolio decisions:
- **Transaction costs**: Realistic estimates for asset class
- **Turnover**: Portfolio turnover and its impact on net returns
- **Slippage**: Market impact, bid-ask spread modeling
- **Backtest hygiene**: Walk-forward, out-of-sample, multiple testing adjustment
- **Economic significance**: Sharpe ratio, Sortino, max drawdown, not just accuracy
- **Capacity constraints**: How much capital can the strategy absorb?

## Domain-Specific Knowledge

### Time-Series Forecasting
- Classical: ARIMA, ETS, TBATS, VAR
- Modern: N-BEATS, N-HiTS, Temporal Fusion Transformer, PatchTST, Informer
- Foundation models: TimesFM, Chronos, Lag-Llama
- Ensemble methods: Stacking with proper CV

### Feature Engineering for Finance
- Price-based: Returns, log returns, realized volatility, momentum
- Volume-based: VWAP, volume profiles, order flow imbalance
- Cross-sectional: Ranks, z-scores, percentiles within peer groups
- Fundamental: Valuation ratios, quality metrics, growth indicators
- Alternative data: Sentiment, satellite, web traffic, credit card

### Validation Strategies
```
Standard Time-Series CV:
|---Train---|--Val--|     |---Train---|--Val--|
                         ^gap if needed

Walk-Forward:
|---Train---|Test|
   |---Train---|Test|
      |---Train---|Test|

Purged K-Fold for Panels:
|Train|Gap|Test|Gap|Train|  (purge overlapping labels)
```

### Evaluation Metrics
- Regression: RMSE, MAE, MAPE, SMAPE, MDA (directional accuracy)
- Classification: AUC, precision-recall, Brier score
- Financial: Sharpe, Sortino, Calmar, max drawdown, hit rate
- Calibration: Coverage of prediction intervals, PIT histogram

### Interpretability Caveats
- SHAP: Valid for tree models, approximate for deep models
- Attention weights: Do not equal importance—use integrated gradients
- Feature importance: Depends on correlation structure
- PDPs: Assume feature independence (often violated in finance)

## Code Standards

When providing code:
- Complete, runnable with clear dependencies
- Proper train/test splits enforced
- Reproducibility: Random seeds, version logging
- Error handling for common edge cases
- Modular design for production deployment

**Python packages**: pandas, numpy, scikit-learn, xgboost, lightgbm, pytorch, pytorch-forecasting, statsmodels, shap, optuna
**R packages**: tidymodels, xgboost, lightgbm, forecast, fable, timetk

## Personality

Direct, research-grade, practical. Strong opinions, loosely held—update based on evidence and evaluation. No hype without substance. If a method is oversold, say so."""


# =============================================================================
# SUBAGENTS
# =============================================================================

SUBAGENTS = {
    "feature-engineer": AgentDefinition(
        description="Designs and validates financial ML features with leakage prevention",
        prompt="""You are a feature engineering specialist for financial ML.

Your responsibilities:
- Design informative features from raw financial data
- Ensure no look-ahead bias or data leakage
- Recommend appropriate transformations (logs, ranks, z-scores)
- Suggest rolling window calculations with proper alignment
- Identify potential multicollinearity issues
- Validate feature distributions and stability over time

For each feature:
1. Clear definition and economic rationale
2. Calculation formula with time alignment
3. Expected relationship with target
4. Potential issues (missing data, outliers, regime changes)

Always specify the point-in-time availability of each feature.""",
        tools=["Read", "Write", "Bash", "Glob", "Grep"]
    ),

    "validation-auditor": AgentDefinition(
        description="Audits ML pipelines for data leakage and validation integrity",
        prompt="""You are a validation and leakage auditor for financial ML.

Your job is to identify:
- Data leakage (look-ahead bias, survivorship bias)
- Improper cross-validation (random splits for time series)
- Target leakage (features derived from target)
- Cross-sectional contamination in panel models
- Overfitting from hyperparameter tuning
- Multiple testing issues (data snooping)

For each issue:
1. Describe the specific leakage mechanism
2. Quantify potential impact on results
3. Provide corrected implementation
4. Suggest validation tests to detect the issue

Be paranoid—assume leakage until proven otherwise.""",
        tools=["Read", "Bash", "Glob", "Grep"]
    ),

    "sota-researcher": AgentDefinition(
        description="Searches and summarizes latest ML research for finance applications",
        prompt="""You are a SOTA research analyst for financial ML.

When asked about new methods:
1. Search arXiv, Papers With Code, GitHub
2. Identify relevant recent papers (last 2 years)
3. Summarize: core idea, claimed improvements, limitations
4. Assess practical applicability for finance
5. Find open-source implementations if available
6. Note computational requirements and complexity

Never fabricate citations. If you can't verify a reference, say so.
Distinguish clearly between:
- Peer-reviewed published work
- Preprints with empirical validation
- Theoretical proposals
- Industry blog posts and marketing""",
        tools=["Read", "WebSearch", "WebFetch", "Glob"]
    ),

    "backtest-validator": AgentDefinition(
        description="Validates trading backtests for hygiene and economic significance",
        prompt="""You are a backtest validation specialist.

Evaluate trading backtests for:
1. **Data integrity**: Point-in-time data, survivorship bias
2. **Execution realism**: Transaction costs, slippage, market impact
3. **Statistical validity**: Enough observations, multiple testing
4. **Economic significance**: Risk-adjusted returns, drawdowns
5. **Robustness**: Parameter sensitivity, regime dependence

Red flags to identify:
- Unrealistic Sharpe ratios (>2 is suspicious for most strategies)
- Cherry-picked time periods
- Overfitted parameters
- Missing transaction costs
- Ignoring capacity constraints

Provide specific, actionable feedback.""",
        tools=["Read", "Bash", "Glob", "Grep"]
    ),

    "code-generator": AgentDefinition(
        description="Generates production-quality ML code for finance applications",
        prompt="""You are a code generation specialist for financial ML.

Your outputs must be:
- Correct and runnable without modification
- Leakage-free with proper temporal splits
- Well-documented with clear variable names
- Include validation and sanity checks
- Production-ready with error handling
- Reproducible with fixed random seeds

Standards:
- Python: Use sklearn pipelines, proper CV, type hints
- Time series: Always use TimeSeriesSplit or custom walk-forward
- Features: Document point-in-time availability
- Metrics: Include both ML metrics and financial metrics

Always include:
- Data loading and preprocessing
- Feature engineering with comments
- Model training with proper CV
- Evaluation on held-out test set
- Basic interpretability output""",
        tools=["Read", "Write", "Bash", "Glob", "Grep"]
    )
}


# =============================================================================
# HOOKS
# =============================================================================

async def audit_log(input_data: dict, tool_use_id: str, context: Any) -> dict:
    """Log all tool usage for audit purposes."""
    timestamp = datetime.now().isoformat()
    log_dir = Path("./logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": timestamp,
        "tool_use_id": tool_use_id,
        "tool": input_data.get("tool_name", "unknown"),
        "input": json.dumps(input_data.get("tool_input", {}))[:500]
    }

    log_file = log_dir / "finml-audit.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {}


async def validate_code_execution(input_data: dict, tool_use_id: str, context: Any) -> dict:
    """Validate bash commands before execution."""
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    # Block potentially dangerous operations
    blocked_patterns = [
        r"rm\s+-rf\s+/",
        r"curl.*\|.*sh",
        r"wget.*\|.*sh",
    ]

    for pattern in blocked_patterns:
        if re.search(pattern, command):
            return {
                "decision": "block",
                "reason": "Potentially dangerous command blocked for safety"
            }

    return {}


async def leakage_warning(input_data: dict, tool_use_id: str, context: Any) -> dict:
    """Warn about common leakage patterns in code."""
    tool_input = input_data.get("tool_input", {})
    content = tool_input.get("content", "") or tool_input.get("file_text", "")

    leakage_patterns = [
        (r"train_test_split.*shuffle\s*=\s*True", "Random shuffle in train_test_split may cause leakage for time series"),
        (r"\.shift\(-", "Negative shift may introduce look-ahead bias"),
        (r"future|tomorrow|next_day", "Feature name suggests potential look-ahead bias"),
    ]

    warnings = []
    for pattern, warning in leakage_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            warnings.append(warning)

    if warnings:
        print(f"[FinML Leakage Check] {'; '.join(warnings)}")

    return {}


# =============================================================================
# MAIN QUERY FUNCTION
# =============================================================================

Language = Literal["Python", "R", "all"]
OutputFormat = Literal["markdown", "latex", "html"]


async def run_finml(
    prompt: str,
    working_directory: Optional[str] = None,
    language: Language = "Python",
    output_format: OutputFormat = "markdown",
    include_code: bool = True,
    verbose: bool = False,
    session_id: Optional[str] = None,
    trading_context: bool = False,
) -> AsyncIterator[Any]:
    """
    Run FinML agent with the given prompt.

    Args:
        prompt: The user's ML/finance question or task
        working_directory: Working directory for file operations
        language: Preferred programming language for code
        output_format: Format for output (markdown, latex, html)
        include_code: Whether to include executable code examples
        verbose: Whether to print detailed message stream
        session_id: Optional session ID to resume
        trading_context: Whether this is for trading/portfolio decisions

    Yields:
        Message objects from the agent
    """
    if working_directory is None:
        working_directory = os.getcwd()

    # Build context-aware prompt
    enhanced_prompt = _build_enhanced_prompt(
        prompt,
        language=language,
        output_format=output_format,
        include_code=include_code,
        trading_context=trading_context
    )

    # Configure agent options
    agent_options = ClaudeAgentOptions(
        system_prompt=FINML_SYSTEM_PROMPT,
        allowed_tools=[
            "Read",
            "Write",
            "Edit",
            "Bash",
            "Glob",
            "Grep",
            "WebSearch",
            "WebFetch",
            "Task",
            "AskUserQuestion"
        ],
        agents=SUBAGENTS,
        cwd=working_directory,
        permission_mode="acceptEdits",
        hooks={
            "PostToolUse": [HookMatcher(matcher=".*", hooks=[audit_log])],
            "PreToolUse": [
                HookMatcher(matcher="Bash", hooks=[validate_code_execution]),
                HookMatcher(matcher="Write|Edit", hooks=[leakage_warning])
            ]
        },
    )

    if session_id:
        agent_options.resume = session_id

    # Run the agent
    async for message in query(
        prompt=enhanced_prompt,
        options=agent_options
    ):
        if verbose:
            print(f"[{message.type}]", str(message)[:200])
        yield message


def _build_enhanced_prompt(
    user_prompt: str,
    language: str,
    output_format: str,
    include_code: bool,
    trading_context: bool
) -> str:
    """Build an enhanced prompt with context information."""
    context_parts = []

    if language != "all":
        context_parts.append(f"Preferred programming language: {language}")

    context_parts.append(f"Output format: {output_format}")

    if include_code:
        context_parts.append("Include executable code examples where appropriate.")

    if trading_context:
        context_parts.append(
            "This is for a trading/portfolio application. "
            "Include transaction costs, slippage, and backtest hygiene considerations."
        )

    context_block = "\n".join(context_parts)

    return f"{user_prompt}\n\n[Context]\n{context_block}"


# =============================================================================
# SPECIALIZED WORKFLOWS
# =============================================================================

async def run_ml_pipeline(
    prediction_task: str,
    data_path: str,
    language: Language = "Python",
    verbose: bool = False,
    trading_context: bool = False,
) -> AsyncIterator[Any]:
    """
    Run a complete ML pipeline development workflow.

    Args:
        prediction_task: Description of the prediction task
        data_path: Path to the data file
        language: Preferred programming language
        verbose: Whether to print detailed messages
        trading_context: Whether this is for trading/portfolio

    Yields:
        Message objects from the agent
    """
    pipeline_prompt = f"""
## Prediction Task
{prediction_task}

## Data
The data is located at: {data_path}

## Required Analysis
Please develop a complete ML pipeline following this workflow:

1. **Problem Formalization**: Define y, h, frequency, information set, and metrics
2. **Data Exploration**: Load data, examine structure, check for issues
3. **Feature Engineering**: Design leakage-free features with documentation
4. **Baseline Models**: Implement naive, linear, and simple ML baselines
5. **Advanced Models**: Train tree boosting and/or deep learning models
6. **Validation**: Set up proper walk-forward or purged CV
7. **Evaluation**: Compare all models on primary and secondary metrics
8. **Interpretability**: SHAP or equivalent analysis with caveats
9. **Production Notes**: Monitoring, drift detection, retraining triggers

Provide complete, runnable code and interpret all results.
"""

    async for message in run_finml(
        prompt=pipeline_prompt,
        language=language,
        verbose=verbose,
        include_code=True,
        trading_context=trading_context
    ):
        yield message


async def audit_pipeline(
    pipeline_path: str,
    language: Language = "Python",
    verbose: bool = False,
) -> AsyncIterator[Any]:
    """
    Audit an existing ML pipeline for leakage and best practices.

    Args:
        pipeline_path: Path to the pipeline code
        language: Preferred programming language
        verbose: Whether to print detailed messages

    Yields:
        Message objects from the agent
    """
    audit_prompt = f"""
## Audit Task
Please audit the ML pipeline at: {pipeline_path}

Evaluate for:
1. **Data Leakage**: Look-ahead bias, survivorship bias, target leakage
2. **Validation Integrity**: Proper time-based splits, purging, embargo
3. **Feature Quality**: Point-in-time availability, stability, multicollinearity
4. **Model Selection**: Appropriate models for the problem, proper tuning
5. **Evaluation**: Correct metrics, statistical significance, economic significance
6. **Production Readiness**: Error handling, monitoring, reproducibility

For each issue found:
- Severity (critical / important / minor)
- Specific location in code
- Explanation of the problem
- Corrected implementation

Be thorough and skeptical.
"""

    async for message in run_finml(
        prompt=audit_prompt,
        language=language,
        verbose=verbose
    ):
        yield message


async def search_sota(
    research_topic: str,
    verbose: bool = False,
) -> AsyncIterator[Any]:
    """
    Search for and summarize SOTA methods for a specific task.

    Args:
        research_topic: Topic to search for
        verbose: Whether to print detailed messages

    Yields:
        Message objects from the agent
    """
    sota_prompt = f"""
## SOTA Research Task
Search for the latest state-of-the-art methods for: {research_topic}

Please:
1. Search arXiv, Papers With Code, and relevant GitHub repositories
2. Identify the top 3-5 recent methods (last 2 years)
3. For each method, provide:
   - Paper title and venue (if published)
   - Core innovation and claimed improvements
   - Practical implementation considerations
   - Available code repositories
   - Computational requirements
   - Applicability to financial data (with caveats)

4. Provide a comparative summary table
5. Recommend which methods to try first and why

Only include verified references. Clearly mark preprints vs. peer-reviewed.
"""

    async for message in run_finml(
        prompt=sota_prompt,
        verbose=verbose
    ):
        yield message


async def validate_backtest(
    backtest_path: str,
    verbose: bool = False,
) -> AsyncIterator[Any]:
    """
    Validate a trading backtest for hygiene and economic significance.

    Args:
        backtest_path: Path to the backtest code/results
        verbose: Whether to print detailed messages

    Yields:
        Message objects from the agent
    """
    backtest_prompt = f"""
## Backtest Validation Task
Please validate the trading backtest at: {backtest_path}

Evaluate:
1. **Data Integrity**
   - Point-in-time data used?
   - Survivorship bias addressed?
   - Corporate actions handled?

2. **Execution Realism**
   - Transaction costs modeled?
   - Slippage/market impact included?
   - Realistic fill assumptions?

3. **Statistical Validity**
   - Sufficient observations?
   - Multiple testing adjustment?
   - Out-of-sample validation?

4. **Performance Metrics**
   - Risk-adjusted returns (Sharpe, Sortino)
   - Drawdown analysis
   - Turnover and capacity

5. **Robustness**
   - Parameter sensitivity
   - Regime analysis
   - Bootstrap confidence intervals

Provide specific, actionable feedback with code corrections where needed.
"""

    async for message in run_finml(
        prompt=backtest_prompt,
        trading_context=True,
        verbose=verbose
    ):
        yield message


async def generate_features(
    target_description: str,
    data_description: str,
    language: Language = "Python",
    verbose: bool = False,
) -> AsyncIterator[Any]:
    """
    Generate feature engineering code for a specific prediction task.

    Args:
        target_description: Description of prediction target
        data_description: Description of available data
        language: Programming language for code
        verbose: Whether to print detailed messages

    Yields:
        Message objects from the agent
    """
    feature_prompt = f"""
## Feature Engineering Task
Generate comprehensive feature engineering code.

## Target
{target_description}

## Available Data
{data_description}

## Requirements
- Language: {language}
- All features must be point-in-time (no look-ahead)
- Include feature documentation (name, formula, rationale)
- Add sanity checks for each feature
- Include feature stability analysis over time
- Generate correlation matrix with target

Categories to consider:
1. Price/return-based features
2. Volume/liquidity features
3. Volatility features
4. Momentum/trend features
5. Cross-sectional features (if applicable)
6. Calendar/seasonal features

The code should be modular and production-ready.
"""

    async for message in run_finml(
        prompt=feature_prompt,
        language=language,
        verbose=verbose,
        include_code=True
    ):
        yield message


# =============================================================================
# CLI ENTRY POINT
# =============================================================================

async def main():
    """CLI entry point for FinML."""
    import argparse

    parser = argparse.ArgumentParser(
        description="FinML SOTA Analyst - ML for Financial & Economic Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python finml.py "How do I forecast stock volatility?"
  python finml.py --pipeline "Predict next-day returns" --data ./prices.csv
  python finml.py --audit ./ml_pipeline/
  python finml.py --sota "transformer models for time series"
  python finml.py --backtest ./strategy/
  python finml.py --features "5-day forward returns" --data "Daily OHLCV, 2015-2024"
        """
    )

    parser.add_argument("prompt", nargs="?", help="Direct prompt for FinML")
    parser.add_argument("--pipeline", help="Prediction task for full pipeline")
    parser.add_argument("--audit", help="Path to pipeline to audit")
    parser.add_argument("--sota", help="Research topic to search")
    parser.add_argument("--backtest", help="Path to backtest to validate")
    parser.add_argument("--features", help="Target for feature engineering")
    parser.add_argument("--data", help="Data path or description")
    parser.add_argument("--lang", choices=["Python", "R"], default="Python",
                        help="Programming language (default: Python)")
    parser.add_argument("--format", choices=["markdown", "latex", "html"], default="markdown",
                        help="Output format (default: markdown)")
    parser.add_argument("--trading", action="store_true",
                        help="Enable trading context (costs, slippage)")
    parser.add_argument("--verbose", action="store_true", help="Show detailed messages")

    args = parser.parse_args()

    result = ""

    if args.pipeline:
        data_path = args.data or "./data"
        async for message in run_ml_pipeline(
            args.pipeline, data_path, args.lang, args.verbose, args.trading
        ):
            if hasattr(message, "result"):
                result = message.result

    elif args.audit:
        async for message in audit_pipeline(args.audit, args.lang, args.verbose):
            if hasattr(message, "result"):
                result = message.result

    elif args.sota:
        async for message in search_sota(args.sota, args.verbose):
            if hasattr(message, "result"):
                result = message.result

    elif args.backtest:
        async for message in validate_backtest(args.backtest, args.verbose):
            if hasattr(message, "result"):
                result = message.result

    elif args.features:
        data_desc = args.data or "Financial time series data"
        async for message in generate_features(
            args.features, data_desc, args.lang, args.verbose
        ):
            if hasattr(message, "result"):
                result = message.result

    elif args.prompt:
        async for message in run_finml(
            args.prompt,
            language=args.lang,
            output_format=args.format,
            verbose=args.verbose,
            trading_context=args.trading
        ):
            if hasattr(message, "result"):
                result = message.result
    else:
        parser.print_help()
        return

    print("\n" + "=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
