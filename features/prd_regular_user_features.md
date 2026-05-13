# Product Requirement Document (PRD): Paisa System (Regular User Core)

## 1. Introduction & Product Vision
Paisa is an advanced, AI-driven institutional-grade portfolio companion and strategy execution engine for retail options and stock traders. The platform empowers regular users by combining technical/fundamental scoring models, real-time market regime analysis, risk benchmarking stress-testing models, and an interactive conversational AI agent ("Hunter") into a single cohesive, high-performance dashboard.

The key design philosophy of Paisa is **visual excellence, transparency, and micro-interactivity**. Regular users are guided by robust guardrails, professional terminologies (with simple toggles), and real-time alerts to prevent "Recommendation Drift" and execution errors.

---

## 2. Core User Personas
1. **The Active Retail Trader**: Seeks daily high-conviction trade setups, fundamental-technical scores, and direct paper-trading execution.
2. **The Options Strategist**: Looks for advanced option structures (Spreads, Covered Calls, Cash-Secured Puts), IV metrics, Greeks, and automatic Exit Matrix triggers.
3. **The Risk-Averse Portfolio Manager**: Uses stress-testing scenarios (VIX spikes, market drops) to evaluate portfolio exposure and rebalance assets.

---

## 3. Scope of Regular User Features
This PRD focuses exclusively on features accessible to standard (non-admin) users. Administrative screens (e.g., user management, database overrides, system job runners) are excluded from this testing scope.

| Feature Area | Live Path | Key Sub-Components |
| :--- | :--- | :--- |
| **Authentication & Onboarding** | `/login`, `/verify-email` | Onboarding Interview, Login Validation |
| **Market Dashboard** | `/` | Macro Safety Badge, Active Trades, Sector Exposure, Portfolio Auto-Pilot Console, Expired Trades Modal |
| **Market Discovery / Scanner** | `/discovery` | Status Bar, Sidebar Filters, Presets, Today's Picks Grid |
| **Deep Ticker Analysis** | `/analysis` | Watchlist/Universe toggles, Metrics, Price Chart with Probability Cones, Operational Blueprint, AI Analyst drawer |
| **Options Engine** | `/options` | Option Chain setup, Exit Matrix, Greeks & Analytics, Bypass toggle |
| **Research Laboratory** | `/external-analysis` | Live vs. Isolated Lab, CSV Trade Import, Stress-Testing Sliders |
| **Agent Playbooks** | `/skills` | Strategy markdown registry and playbook viewer |
| **Scoring Methodology** | `/methodology` | Sector Weightings and factor allocation visualizations |

---

## 4. Detailed Feature Requirements

### 4.1. Authentication & Onboarding
- **Onboarding Interview**: 
  - **Requirement**: If a logged-in user does not have a defined trading persona (`user.persona`), the system must intercept and redirect them to `/hunter` with an onboarding state.
  - **Behavior**: An automated conversational onboarding flow must trigger immediately to help the user set up their risk profile.
  - **Verify Email**: A clean validation interface for confirming account activation.

### 4.2. Market Dashboard (`/`)
The main hub provides an instant overview of portfolio health, active exposures, and quick actions.
- **System Guardrail (Macro Safety Badge)**:
  - Displays a visual safety pill: "MARKET STABLE" (Green, pulse) if `paisa_score` > 60, or "HIGH VOLATILITY" (Yellow/Red, bounce) if ≤ 60.
- **Immediate Action Center**:
  - Highlights urgent alerts (e.g., stop-losses triggered, margin alerts) and active suggestions for immediate user approval.
- **Dashboard KPI Summary**:
  - Displays Total Exposure, Unrealized PnL, Winners (count), and Actions Required.
  - Features a toggle to show/hide KPI card values for privacy.
- **Active Trades Table**:
  - Lists current positions grouped by `Ticker-Strategy` (e.g., `AAPL-LONG_STOCK`).
  - Columns: Ticker, Position Type, Action, Entry Price, Current Price, Quantity, PnL, Alerts (e.g., STOP-LOSS, TIME-OUT, PAYCHECK, HOLD).
  - Actions: Manual Close Trade or Delete Trade.
- **Sector Exposure Chart**:
  - Displays sector distribution percentages with visual indicators of exposure risk (HIGH/LOW) and diversification state (OPTIMAL).
- **Auto-Pilot Portfolio Review**:
  - Features a terminal emulator (`AgentTerminal`) that runs a portfolio review job. On-screen messages are printed line-by-line representing live-agent analysis.
- **Expired Trades Modal**:
  - Triggers automatically upon login if active trades have passed their expiry date (or after 4:00 PM EST on expiry day). Offers Reconcile All, Delete, or Close.

### 4.3. Market Discovery & Scanner (`/discovery`)
Provides today's high-conviction trade setups based on active daily sweeps.
- **Live Scanner Status**: Displays whether the backend daily scanner is idle or active (updating in real time).
- **Discovery Filters**:
  - Text search by ticker, sliders for score thresholds, price ranges, and checkboxes (e.g., hide high cap, elite mismatch only, exclude speculative).
  - **Filter Presets**: Quick buttons (e.g., "Bullish", "High Conviction"). *Clicking an already active preset must toggle it off*, returning filters to default states.
- **Today's Picks Table**:
  - Displays the ticker, name, recommended strategy (e.g., `BULL_PUT_SPREAD`), Paisa score, current price, and expected returns.
  - Includes a manual "Refresh" icon on individual tickers to update simulated option expiration dates immediately.

### 4.4. Deep Ticker Analysis (`/analysis`)
Allows deep quantitative and qualitative analysis of any individual asset.
- **Header Stats**: Shows active price, stock score, and lets users add the ticker to their Watchlist or Core Universe.
- **Score Transparency & Rationale**:
  - Displays a concise summary explanation for the score.
  - Lists every scoring rule applied (e.g., "+10 pts: High growth margins").
- **Price Chart & Probability Cones**:
  - An interactive visual representing standard-deviation price envelopes (7-day expected moves) calculated using implied volatility (IV).
- **Operational Blueprint**:
  - Pre-computed trade execution blueprint (e.g., buying stock or writing option spread legs).
  - Includes a "Record Trade" button to log the trade directly into paper trading.
- **Ticker AI Chat Drawer**:
  - A sliding right drawer offering a context-grounded AI analyst chat focused strictly on the selected ticker.

### 4.5. Options Engine (`/options`)
Advanced option strategy generator.
- **No-Trade State with Bypass**:
  - If a ticker does not meet default risk parameters, displays a "No Trade" card explaining why.
  - Users can toggle a **"Bypass Filter"** checkbox to generate a strategy blueprint anyway.
- **Fidelity Chain Link**: Direct deep link to the option chain page for the specific ticker on Fidelity.
- **Exit Matrix**:
  - Generates clear, mathematical triggers for closing the position (e.g., "Close at 50% max profit", "Stop-loss at 100% credit").
  - Users can click "Generate Blueprint" to establish these exit benchmarks.

### 4.6. Research Laboratory (`/external-analysis`)
An isolated risk sandbox and live stress-testing tool.
- **Sandbox Toggle**: Toggle between "Live Portfolio" (stress-testing actual holdings) and "Research Lab" (an isolated sandbox).
- **CSV Trade Ingestor**: Users can paste CSV records of trades, view an import preview table, and commit them to the Research Lab sandbox.
- **Stress-Testing Sliders**:
  - Sliders for Market Crash/Move % (0% to -50%) and VIX Spike % (0% to +100%).
  - Dynamically recalculates portfolio drawdown, health scores, and beta-equivalent exposures.
- **Actionable Rebalancing Suggestions**: Provides actionable rebalancing cards. Clicking any card opens the Lab Chat pre-loaded with advice queries.

### 4.7. Agent Playbooks & Scoring Methodology
- **Agent Playbooks (`/skills`)**: Users can view the system's markdown-based strategy playbooks (Registry sidebar and markdown render preview tab).
- **Scoring Methodology (`/methodology`)**: Displays interactive factor cards and percentage weights applied to each market sector (e.g., Technology sector places 40% weight on P/E ratio, 30% on Momentum, etc.).

---

## 5. Non-Functional Requirements
- **Modern Premium Aesthetic**: The application must utilize a modern sleek dark mode, tailored HSL color palettes, subtle glassmorphism (`backdrop-blur`), and hover transitions. No plain default browser elements.
- **Responsive Layout**: Seamless layouts across desktop and mobile devices.
- **SEO Elements**:
  - Descriptive page titles and meta-descriptions.
  - Structured semantic HTML hierarchy (`<h1>` down to `<h4>`).
  - Unique HTML element IDs for accurate cross-browser interactive testing.
