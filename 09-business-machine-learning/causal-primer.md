# A short causal primer: from a score to an intervention

[Chapter 9](README.md) &nbsp;·&nbsp; [Shared delivery plan](delivery-plan.md)

Read this before the offer, price or retention guide. The goal is to state the causal question and
its assumptions before choosing an estimator. The arithmetic below is invented teaching data.

## Name the comparison

A prediction asks what outcome is likely in the observed setting. A causal question asks what
would change if the same eligible population received a different action. Write the **estimand**:
the quantity you want to estimate, including population, action, comparator and outcome horizon.

For example: “Among currently eligible subscribers, how does assigning this retention offer rather
than no contact change 30-day retained contribution per assigned account?” This specifies a policy
comparison. It is more useful than asking whether an unspecified model “reduces churn.”

For each account, imagine two potential outcomes: retention under offer assignment, `Y(1)`, and
retention under no-contact assignment, `Y(0)`. You observe one of them. Their difference for one
person is not directly labeled in ordinary data. An average treatment effect compares average
potential outcomes; a conditional effect compares them within a specified context. Neither tells
you with certainty which particular person would have changed their decision.

## Worked lesson: risk and benefit answer different questions

Suppose a randomized, fully observed experiment produces these point estimates:

| Pre-assignment segment | Retained without offer | Retained with offer | Estimated retention difference |
| --- | --- | --- | --- |
| Higher risk | 70 of 100 | 80 of 100 | +10 percentage points |
| Lower risk | 90 of 100 | 90 of 100 | 0 percentage points |

With equal segment weights, the estimated average retention effect is `(0.10 + 0) / 2 = 0.05`.
Assume an extra retained account contributes 100 units and an offer costs 5 per assigned account,
with no additional costs or interference. Estimated incremental contribution is:

- Higher risk: `0.10 × 100 - 5 = +5` per assigned account.
- Lower risk: `0 × 100 - 5 = -5` per assigned account.

These are point estimates, not guaranteed gains. Report intervals at the assignment unit, check
guardrails and avoid choosing a policy on the same data later used to confirm its value. Real
economics may require contribution as the direct outcome rather than multiplying retention by a
constant. The churn guide explains cases where high risk and intervention benefit disagree.

**Try it yourself.** An offer costs 12 instead of 5. What do the point estimates recommend?

<details>
<summary>Hint and explained answer</summary>

The two estimated gains become `10 - 12 = -2` and `0 - 12 = -12`. Under these assumptions, retain
the no-contact baseline for both segments. Better predicted retention does not automatically make
an intervention profitable. A capacity limit or uncertain effect can further change the decision.

</details>

## What randomization supplies—and what it still needs

Random assignment makes the assigned groups comparable in expectation. Check actual assignment
logging, eligibility, sample-ratio mismatch, outcome coverage and the planned analysis horizon.
Analyze outcomes by original assignment for an **intention-to-treat** effect. Excluding failed
deliveries after assignment can select different kinds of customers in each arm.

The comparison also needs a well-defined intervention and outcome, a relevant chance of receiving
each compared action, and a design addressing interference or carryover where present. Randomizing
one customer's price may affect another customer's demand or deplete shared stock; the assignment
unit and interpretation must reflect that system.

## When assignment was not random

A **confounder** affects both action assignment and outcome. For example, an account manager may
target dissatisfied customers, who were already more likely to leave. A treated-versus-untreated
comparison then mixes selection with the offer's effect.

A **mediator** is affected by the action and lies on a path to the outcome, such as post-offer
engagement. Adjusting for it generally changes the causal question and can bias a total-effect
analysis. A **collider** is a shared consequence of other variables; conditioning on it can create
a spurious association. A diagram helps state these choices, but does not prove the assumptions.

Observational adjustment usually needs a credible case that measured pre-action variables block
the relevant confounding, plus **overlap**: each compared action has a nonzero chance in the
contexts where the policy would choose it. If an action was never tried in a segment, a flexible
model can extrapolate a number without identifying that effect. Restrict the policy or collect data.

The **propensity** is the probability that the assignment policy selects an action given recorded
pre-action context. It is not the predicted probability that the customer purchases. Estimated
propensities and outcome models are often called nuisance models because the effect or policy
value, rather than those predictions, is the main target.

**Cross-fitting** trains a nuisance model on other folds before scoring a fold. It can reduce some
overfitting problems, but cannot repair unmeasured confounding, unsupported actions or a wrong
time/group split. “Doubly robust” is a property under stated assumptions, not permission to ignore
the design. Use the specific estimator's requirements in the linked guides.

## Before using an effect estimate

Write the estimand, assignment unit, clocks and outcome coverage. State which identification
assumptions come from the design and which remain judgments. Distinguish simulation, retrospective
prediction and measured intervention evidence. Then proceed to the [delivery plan](delivery-plan.md)
and one case: [offers](offer-recommendation.md), [prices](price-recommendation.md) or
[churn and retention](churn.md).

For deeper explanations, use [The Effect](https://theeffectbook.net/) and the
[metalearners paper](https://www.pnas.org/doi/10.1073/pnas.1804597116), already annotated in the
[chapter resources](resources/README.md).
