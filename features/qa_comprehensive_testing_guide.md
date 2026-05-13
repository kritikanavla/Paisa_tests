# Comprehensive QA Testing Guide: Paisa System (Regular User Core)

This document provides a highly actionable, structured, and comprehensive testing framework for verifying regular user-facing areas of Paisa. It is designed to be utilized by freelance QA analysts to systematically test workflows, user experiences, visual integrity, and edge cases.

---

## 1. Testing Strategy & Priorities
- **Visual Integrity**: Verify modern dark mode aesthetics, glassmorphism (`backdrop-blur`), clear typography, and responsive scaling. Avoid raw, generic HTML layouts.
- **Micro-Interactions**: Confirm all hover transitions, click handlers, modals, sliders, and sidebar transitions operate smoothly.
- **Logical Synchronizations**: Ensure that portfolio values, ticker scores, and options setup details are logically consistent across pages to prevent "Recommendation Drift".

---

## 2. Feature-by-Feature Test Scenarios

### 2.1. Authentication & Onboarding Flow
Verify the user's initial entry path and automated onboarding interview.

- **Scenario A: First-time User Onboarding Intercept**
  1. Log in with a fresh user account that has no persona configured (`user.persona === null`).
  2. **Expected Behavior**: The system must intercept the default routing and redirect the user immediately to `/hunter` with `onboarding: true` in state.
  3. Verify that the AI Chat starts an interview by sending: *"Hello, I am ready to start my risk discovery interview. Please help me set up my persona."*

- **Scenario B: Quota Exhausted Intercept**
  1. Simulate a user account where `quota_exhausted: true`.
  2. **Expected Behavior**: System intercepts routing and redirects to `/quota-exhausted`. No sidebar navigation is accessible.

- **Scenario C: Standard Login & Verification**
  1. Test `/login` and `/verify-email` pages. Check field validation (empty email, invalid passwords).

---

### 2.2. Market Dashboard (`/`)
Verify portfolio health widgets, active positions, and AI autopilot.

- **Scenario A: System Guardrail Badge**
  1. Check the top-right macro safety badge under different market states.
  2. **Expected Behavior**: 
    - If `paisa_score` > 60: Badge displays "MARKET STABLE" (Green, with a subtle pulsing animation).
    - If `paisa_score` ≤ 60: Badge displays "HIGH VOLATILITY" (Red/Yellow, with a bounce animation).

- **Scenario B: Dashboard KPI Toggle**
  1. Locate the KPI Summary Cards (Total Exposure, Unrealized PnL, Winners, Actions Required).
  2. Click the visibility toggle icon (`showKpiCards`).
  3. **Expected Behavior**: Values within cards are blurred/hidden for privacy, and clicking again unhides them.

- **Scenario C: Active Trades Table & Expired Modal**
  1. Review the active positions grid. Confirm trades are grouped under `Ticker-Strategy` labels.
  2. Trigger a login with trades that have passed their expiration date.
  3. **Expected Behavior**: The `ExpiredTradesModal` triggers automatically upon loading the dashboard. Verify buttons: "Reconcile All" updates DB state, "Close Trade" closes position, and "Delete" removes the trade record.

- **Scenario D: Auto-Pilot Review Agent**
  1. Scroll to the "🤖 Auto-Pilot" section and click **"Run Portfolio Review"**.
  2. **Expected Behavior**: Terminal status changes to "running". Real-time logs are output to the terminal emulator screen. Sidebar navigation remains operational during background run.

---

### 2.3. Market Discovery & Scanner (`/discovery`)
Verify trade idea filters, presets, and scans.

- **Scenario A: Preset Filter Toggle (CRITICAL)**
  1. Click on a trade preset card (e.g., "Bullish"). Verify the picks table filters down.
  2. Click the **same active preset card again**.
  3. **Expected Behavior**: The preset card toggles off, clearing active filters and returning the picks list to the default scan view.

- **Scenario B: Advanced Filter Sliders**
  1. Expand the "Advanced Options" sidebar panel.
  2. Drag the Score slider, IV Rank slider, and Price Range selectors.
  3. **Expected Behavior**: Picks results table updates instantly based on live inputs without requiring a manual page refresh.

- **Scenario C: Single Ticker Refresh**
  1. Find a ticker in the Picks list and click the manual "Refresh" icon.
  2. **Expected Behavior**: A loader spinner appears next to the ticker. The ticker's data (e.g., expiration dates, price metrics) updates and persists to the database upon completion.

---

### 2.4. Deep Ticker Analysis (`/analysis`)
Verify ticker lookup, scores, charts, and AI Analyst drawers.

- **Scenario A: Empty / No Ticker State**
  1. Navigate directly to `/analysis` with no query parameters.
  2. **Expected Behavior**: Screen displays a centered `Info` icon with message: "No Ticker Selected. Search for a ticker in the header to start a deep analysis."

- **Scenario B: Interactive Price Chart & Probability Cones**
  1. Search for a liquid ticker (e.g., `AAPL` or `SPY`).
  2. Check the Price Chart with Standard Deviation / Probability Cones.
  3. **Expected Behavior**: Hovering over the chart reveals expected 7-day price envelopes (standard deviation bands) calculated dynamically using the stock's Implied Volatility (IV).

- **Scenario C: Score Transparency Panel**
  1. Scroll to "Score Transparency".
  2. **Expected Behavior**: Displays a detailed rule log showing positive or negative point contributors (e.g., "+10 pts: High growth margins") explaining how the total score was derived.

- **Scenario D: Ticker AI Chat Drawer**
  1. Click the floating action button with the `MessageSquare` icon in the bottom-right.
  2. **Expected Behavior**: A slide-out right drawer appears preloaded with context about the selected ticker. Ask: *"What is the core risk factor of this ticker?"* and check response grounding.

- **Scenario E: Operational Blueprint Recording**
  1. Scroll to "Operational Blueprint" and click **"Record Trade"**.
  2. **Expected Behavior**: Position is logged to paper trading. Navigate to the `/` (Dashboard) page to verify the position has populated correctly.

---

### 2.5. Options Engine (`/options`)
Verify options structures, exit matrices, and bypass switches.

- **Scenario A: No-Trade State & Bypass Switch**
  1. Search for a highly volatile speculative ticker (e.g., `GME` or `AMC`).
  2. **Expected Behavior**: If risk bounds are exceeded, system returns a "No Trade" state with a clear card detailing why.
  3. Check the **"Bypass Filter"** checkbox and search again.
  4. **Expected Behavior**: The system overrides safety filters and generates a standard options blueprint anyway.

- **Scenario B: Exit Matrix Generation**
  1. Review a generated options setup.
  2. Click **"Generate Blueprint"** inside the Exit Matrix panel.
  3. **Expected Behavior**: Displays mathematically computed exit rules (e.g., profit targets, stop-losses, or DTE milestones).

---

### 2.6. Research Laboratory (`/external-analysis`)
Verify isolated sandboxing, CSV imports, and macro stress testing.

- **Scenario A: Live vs. Sandbox Laboratory Toggle**
  1. Toggle between **"Live Portfolio"** and **"Research Lab"**.
  2. **Expected Behavior**: Live Portfolio displays active trades. Research Lab displays a clean state prompting for CSV upload if empty, or showing isolated sandbox assets.

- **Scenario B: Stress-Testing Sliders**
  1. Under the Research Lab view with active trades, locate the "Market Move %" and "VIX Spike %" sliders.
  2. Drag the Market Move slider to `-10%` or `-20%`, and VIX Spike to `+50%`.
  3. **Expected Behavior**: The Portfolio Health score drops, beta-delta equivalents update, and "Projected Drawdown" updates in real time based on stress-test modeling.

- **Scenario C: Rebalancing Recommendations to Chat**
  1. Under "Actionable Insights", find a rebalancing suggestion card and click it.
  2. **Expected Behavior**: The floating AI Chat drawer opens in the sidebar pre-populated with a detailed query regarding that recommendation.

---

## 3. Reference Datasets & Templates for Testing

### 3.1. Valid & Invalid Tickers
- **Valid Liquid Tickers**: `SPY`, `AAPL`, `MSFT`, `NVDA`, `QQQ` (Should yield strong scores, options chains, and full technical metrics).
- **Speculative Tickers**: `GME`, `AMC` (Use to test "No-Trade State" and "Bypass Filter" switches in the Options Engine).
- **Invalid Tickers**: `XYZ123`, `NULL` (Use to verify robust error-boundary handling).

### 3.2. Research Lab Sample CSV Template
Utilize these templates to verify the CSV import parsing in `/external-analysis`.

```csv
ticker,action,entry_price,quantity,trade_type,expiry
AAPL,BUY,175.50,100,STOCK,
MSFT,SELL,415.00,2,OPTION,2026-06-19
NVDA,BUY,850.00,10,STOCK,
```

**Invalid CSV Parsing Test Input (Malformed columns)**:
```csv
ticker;action;price;quantity
AAPL;BUY;175.50;100
```
*(Verify that the parser catches the delimiter mismatch or column deficiency gracefully, printing a clean validation warning rather than a system crash).*

---

## 4. Verification & Defect Checklists

Freelance analysts should copy this markdown block to organize and report testing results.

### 4.1. Visual & Interactive Checklist
- [ ] **Dark Mode Styling**: No bright white flashes or plain backgrounds.
- [ ] **Backdrop Blurs**: Sidebar overlays and modals utilize `backdrop-blur` for a glassmorphism feel.
- [ ] **Button States**: Hovering highlights buttons; clicking triggers immediate visual feedback or loading spinner.
- [ ] **Sliders**: Sliders operate smoothly with numerical readouts updating instantaneously.

### 4.2. Functional Checklist
- [ ] **First-time Onboarding Intercept**: Persona-less accounts are successfully redirected to `/hunter`.
- [ ] **Preset Filter Toggle**: Preset filters in Discovery toggle off on a second click.
- [ ] **Bypass Switch**: Options Engine generates setups for speculative stocks when Bypass is checked.
- [ ] **CSV parser**: Correctly handles option contracts with explicit expirations and stocks with null expirations.
- [ ] **Expired Trades**: Dashboard displays modal overlay if positions have passed their expiry date.
- [ ] **Ticker AI Drawer**: Chat is context-aware and includes the selected ticker's name.
