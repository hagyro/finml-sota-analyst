/**
 * FinML SOTA Analyst: Machine Learning for Financial & Economic Data
 * 
 * An AI agent specialized in ML modeling for finance with emphasis on
 * leakage-resistant validation, robust evaluation, and production standards.
 * Built on the Claude Agent SDK for autonomous analysis and code generation.
 * 
 * @author Based on Claude Agent SDK
 * @version 1.0.0
 */

import { query, ClaudeAgentOptions, AgentDefinition, HookCallback } from "@anthropic-ai/claude-agent-sdk";
import { appendFileSync, existsSync, mkdirSync } from "fs";
import { join } from "path";

// =============================================================================
// SYSTEM PROMPT
// =============================================================================

const FINML_SYSTEM_PROMPT = `You are FinML SOTA Analyst, an expert in machine learning modeling for financial and economic data.

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
\`\`\`
Standard Time-Series CV:
|---Train---|--Val--|     |---Train---|--Val--|
                         ^gap if needed

Walk-Forward:
|---Train---|Test|
   |---Train---|Test|
      |---Train---|Test|

Purged K-Fold for Panels:
|Train|Gap|Test|Gap|Train|  (purge overlapping labels)
\`\`\`

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

Direct, research-grade, practical. Strong opinions, loosely held—update based on evidence and evaluation. No hype without substance. If a method is oversold, say so.`;

// =============================================================================
// SUBAGENTS
// =============================================================================

const SUBAGENTS: Record<string, AgentDefinition> = {
  "feature-engineer": {
    description: "Designs and validates financial ML features with leakage prevention",
    prompt: `You are a feature engineering specialist for financial ML.

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

Always specify the point-in-time availability of each feature.`,
    tools: ["Read", "Write", "Bash", "Glob", "Grep"]
  },

  "validation-auditor": {
    description: "Audits ML pipelines for data leakage and validation integrity",
    prompt: `You are a validation and leakage auditor for financial ML.

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

Be paranoid—assume leakage until proven otherwise.`,
    tools: ["Read", "Bash", "Glob", "Grep"]
  },

  "sota-researcher": {
    description: "Searches and summarizes latest ML research for finance applications",
    prompt: `You are a SOTA research analyst for financial ML.

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
- Industry blog posts and marketing`,
    tools: ["Read", "WebSearch", "WebFetch", "Glob"]
  },

  "backtest-validator": {
    description: "Validates trading backtests for hygiene and economic significance",
    prompt: `You are a backtest validation specialist.

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

Provide specific, actionable feedback.`,
    tools: ["Read", "Bash", "Glob", "Grep"]
  },

  "code-generator": {
    description: "Generates production-quality ML code for finance applications",
    prompt: `You are a code generation specialist for financial ML.

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
- Basic interpretability output`,
    tools: ["Read", "Write", "Bash", "Glob", "Grep"]
  }
};

// =============================================================================
// HOOKS
// =============================================================================

// Audit logging hook
const auditLog: HookCallback = async (input, toolUseId, context) => {
  const timestamp = new Date().toISOString();
  const logDir = "./logs";

  if (!existsSync(logDir)) {
    mkdirSync(logDir, { recursive: true });
  }

  const logEntry = {
    timestamp,
    toolUseId,
    tool: (input as any).tool_name || "unknown",
    input: JSON.stringify((input as any).tool_input || {}).slice(0, 500)
  };

  appendFileSync(
    join(logDir, "finml-audit.jsonl"),
    JSON.stringify(logEntry) + "\n"
  );

  return {};
};

// Validation hook for code execution
const validateCodeExecution: HookCallback = async (input) => {
  const toolInput = (input as any).tool_input || {};
  const command = toolInput.command || "";

  // Block potentially dangerous operations
  const blockedPatterns = [
    /rm\s+-rf\s+\//,
    /curl.*\|.*sh/,
    /wget.*\|.*sh/,
  ];

  for (const pattern of blockedPatterns) {
    if (pattern.test(command)) {
      return {
        decision: "block",
        reason: "Potentially dangerous command blocked for safety"
      };
    }
  }

  return {};
};

// Leakage warning hook - warns about common leakage patterns in code
const leakageWarning: HookCallback = async (input) => {
  const toolInput = (input as any).tool_input || {};
  const content = toolInput.content || toolInput.file_text || "";

  const leakagePatterns = [
    { pattern: /train_test_split.*shuffle\s*=\s*True/i, warning: "Random shuffle in train_test_split may cause leakage for time series" },
    { pattern: /\.shift\(-/i, warning: "Negative shift may introduce look-ahead bias" },
    { pattern: /future|tomorrow|next_day/i, warning: "Feature name suggests potential look-ahead bias" },
  ];

  const warnings: string[] = [];
  for (const { pattern, warning } of leakagePatterns) {
    if (pattern.test(content)) {
      warnings.push(warning);
    }
  }

  if (warnings.length > 0) {
    console.warn("[FinML Leakage Check]", warnings.join("; "));
  }

  return {};
};

// =============================================================================
// MAIN QUERY FUNCTION
// =============================================================================

interface FinMLOptions {
  prompt: string;
  workingDirectory?: string;
  language?: "Python" | "R" | "all";
  outputFormat?: "markdown" | "latex" | "html";
  includeCode?: boolean;
  verbose?: boolean;
  sessionId?: string;
  tradingContext?: boolean;
}

export async function* runFinML(options: FinMLOptions) {
  const {
    prompt,
    workingDirectory = process.cwd(),
    language = "Python",
    outputFormat = "markdown",
    includeCode = true,
    verbose = false,
    sessionId,
    tradingContext = false
  } = options;

  // Build context-aware prompt
  const enhancedPrompt = buildEnhancedPrompt(prompt, { language, outputFormat, includeCode, tradingContext });

  // Configure agent options
  const agentOptions: ClaudeAgentOptions = {
    systemPrompt: FINML_SYSTEM_PROMPT,
    allowedTools: [
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
    agents: SUBAGENTS,
    cwd: workingDirectory,
    permissionMode: "acceptEdits",
    hooks: {
      PostToolUse: [
        { matcher: ".*", hooks: [auditLog] }
      ],
      PreToolUse: [
        { matcher: "Bash", hooks: [validateCodeExecution] },
        { matcher: "Write|Edit", hooks: [leakageWarning] }
      ]
    },
    ...(sessionId && { resume: sessionId })
  };

  // Run the agent
  for await (const message of query({
    prompt: enhancedPrompt,
    options: agentOptions
  })) {
    if (verbose) {
      console.log(`[${message.type}]`, JSON.stringify(message).slice(0, 200));
    }
    yield message;
  }
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function buildEnhancedPrompt(
  userPrompt: string,
  options: { language: string; outputFormat: string; includeCode: boolean; tradingContext: boolean }
): string {
  const { language, outputFormat, includeCode, tradingContext } = options;

  let contextBlock = "";

  if (language !== "all") {
    contextBlock += `\nPreferred programming language: ${language}`;
  }

  contextBlock += `\nOutput format: ${outputFormat}`;

  if (includeCode) {
    contextBlock += "\nInclude executable code examples where appropriate.";
  }

  if (tradingContext) {
    contextBlock += "\nThis is for a trading/portfolio application. Include transaction costs, slippage, and backtest hygiene considerations.";
  }

  return `${userPrompt}\n\n[Context]${contextBlock}`;
}

// =============================================================================
// SPECIALIZED WORKFLOWS
// =============================================================================

/**
 * Run a complete ML pipeline development workflow
 */
export async function* runMLPipeline(
  predictionTask: string,
  dataPath: string,
  options?: Partial<FinMLOptions>
) {
  const pipelinePrompt = `
## Prediction Task
${predictionTask}

## Data
The data is located at: ${dataPath}

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
`;

  yield* runFinML({
    prompt: pipelinePrompt,
    includeCode: true,
    ...options
  });
}

/**
 * Audit an existing ML pipeline for leakage and best practices
 */
export async function* auditPipeline(
  pipelinePath: string,
  options?: Partial<FinMLOptions>
) {
  const auditPrompt = `
## Audit Task
Please audit the ML pipeline at: ${pipelinePath}

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
`;

  yield* runFinML({
    prompt: auditPrompt,
    ...options
  });
}

/**
 * Search for and summarize SOTA methods for a specific task
 */
export async function* searchSOTA(
  researchTopic: string,
  options?: Partial<FinMLOptions>
) {
  const sotaPrompt = `
## SOTA Research Task
Search for the latest state-of-the-art methods for: ${researchTopic}

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
`;

  yield* runFinML({
    prompt: sotaPrompt,
    ...options
  });
}

/**
 * Validate a trading backtest
 */
export async function* validateBacktest(
  backtestPath: string,
  options?: Partial<FinMLOptions>
) {
  const backtestPrompt = `
## Backtest Validation Task
Please validate the trading backtest at: ${backtestPath}

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
`;

  yield* runFinML({
    prompt: backtestPrompt,
    tradingContext: true,
    ...options
  });
}

/**
 * Generate feature engineering code for a specific prediction task
 */
export async function* generateFeatures(
  targetDescription: string,
  dataDescription: string,
  language: "Python" | "R" = "Python",
  options?: Partial<FinMLOptions>
) {
  const featurePrompt = `
## Feature Engineering Task
Generate comprehensive feature engineering code.

## Target
${targetDescription}

## Available Data
${dataDescription}

## Requirements
- Language: ${language}
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
`;

  yield* runFinML({
    prompt: featurePrompt,
    language,
    includeCode: true,
    ...options
  });
}

// =============================================================================
// CLI ENTRY POINT
// =============================================================================

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log(`
FinML SOTA Analyst - ML for Financial & Economic Data
======================================================

Usage:
  npx ts-node finml.ts "<prompt>"
  npx ts-node finml.ts --pipeline "<task>" --data "<data path>"
  npx ts-node finml.ts --audit "<pipeline path>"
  npx ts-node finml.ts --sota "<research topic>"
  npx ts-node finml.ts --backtest "<backtest path>"
  npx ts-node finml.ts --features "<target>" --data "<description>"

Options:
  --verbose    Show detailed message stream
  --lang       Programming language (Python, R)
  --format     Output format (markdown, latex, html)
  --trading    Enable trading context (costs, slippage, etc.)
`);
    process.exit(0);
  }

  // Parse arguments
  const verbose = args.includes("--verbose");
  const tradingContext = args.includes("--trading");
  const langIndex = args.indexOf("--lang");
  const language = langIndex >= 0 ? args[langIndex + 1] as "Python" | "R" : "Python";

  let result = "";

  if (args.includes("--pipeline")) {
    const pipelineIndex = args.indexOf("--pipeline");
    const dataIndex = args.indexOf("--data");
    const task = args[pipelineIndex + 1];
    const dataPath = dataIndex >= 0 ? args[dataIndex + 1] : "./data";

    for await (const message of runMLPipeline(task, dataPath, { verbose, language, tradingContext })) {
      if ("result" in message) {
        result = message.result as string;
      }
    }
  } else if (args.includes("--audit")) {
    const auditIndex = args.indexOf("--audit");
    const pipelinePath = args[auditIndex + 1];

    for await (const message of auditPipeline(pipelinePath, { verbose, language })) {
      if ("result" in message) {
        result = message.result as string;
      }
    }
  } else if (args.includes("--sota")) {
    const sotaIndex = args.indexOf("--sota");
    const topic = args[sotaIndex + 1];

    for await (const message of searchSOTA(topic, { verbose })) {
      if ("result" in message) {
        result = message.result as string;
      }
    }
  } else if (args.includes("--backtest")) {
    const backtestIndex = args.indexOf("--backtest");
    const backtestPath = args[backtestIndex + 1];

    for await (const message of validateBacktest(backtestPath, { verbose })) {
      if ("result" in message) {
        result = message.result as string;
      }
    }
  } else if (args.includes("--features")) {
    const featuresIndex = args.indexOf("--features");
    const dataIndex = args.indexOf("--data");
    const target = args[featuresIndex + 1];
    const dataDesc = dataIndex >= 0 ? args[dataIndex + 1] : "Financial time series data";

    for await (const message of generateFeatures(target, dataDesc, language, { verbose })) {
      if ("result" in message) {
        result = message.result as string;
      }
    }
  } else {
    // Direct prompt
    const prompt = args.filter(a => !a.startsWith("--"))[0];

    for await (const message of runFinML({ prompt, verbose, language, tradingContext })) {
      if ("result" in message) {
        result = message.result as string;
      }
    }
  }

  console.log("\n" + "=".repeat(80));
  console.log("RESULT:");
  console.log("=".repeat(80));
  console.log(result);
}

// Run if executed directly
if (require.main === module) {
  main().catch(console.error);
}
