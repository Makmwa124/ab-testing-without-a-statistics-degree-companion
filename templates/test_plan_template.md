# A/B test plan

**Test name**

Short, specific name

**Owner / decision maker**



**Analyst**



**Planned dates**

Start (Monday) to end (Sunday), whole weeks

**1. Hypothesis**

We believe [change] for [users] will [effect] because [reason].

**2. Primary metric**

Name, exact definition (numerator / denominator), time window, unit (per user).

**3. Guardrail metrics**

Metric | threshold (e.g. load time no worse than +0.10 s). Always include the sample ratio check (p >= 0.001).

**4. Secondary metrics**

For explanation only; they don't decide the test.

**5. Unit of randomisation and trigger**

Who is randomised, where exposure is logged (same point in both groups).

**6. Sample size and duration**

Baseline | MDE (relative) | alpha | power | users per group | eligible users per day | days | whole weeks.

**7. Analysis method**

Test used, cap for revenue (chosen from historical data), CUPED covariate if any, sequential looks if any.

**8. Segments of interest**

At most two, each with a reason. Everything else is exploratory.

**9. Decision rule**

Win: ...   Loss: ...   Inconclusive: ...

**10. Risks and notes**

Overlapping tests, unusual dates, dependencies.
