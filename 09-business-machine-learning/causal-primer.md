# A short causal primer: from a score to an intervention

[Chapter 9](README.md) &nbsp;·&nbsp; [Shared delivery plan](delivery-plan.md)

Read this before the offer, price or retention guide. It helps you state the causal question and
its assumptions before choosing an estimator. The arithmetic below is made-up teaching data.

## Name the comparison

A prediction asks what is likely in the observed setting. A causal question asks what would
change if the same eligible people received a different action. Write the **estimand**: the
quantity you want to estimate, with its population, action, comparison and outcome horizon.

For example: “Among currently eligible subscribers, how does assigning this retention offer rather
than no contact change 30-day retained contribution per assigned account?” This policy comparison
is more useful than asking whether some model “reduces churn.”

For each account, imagine two potential outcomes: retention if assigned the offer, `Y(1)`, and
retention if assigned no contact, `Y(0)`. You see only one, so ordinary data never labels the
difference for one person. An average treatment effect compares the averages, and a conditional
effect compares them within a stated context. Neither tells you for certain which person would have
changed their decision.

## Worked lesson: risk and benefit answer different questions

Suppose a randomised, fully observed experiment gives these point estimates:

| Pre-assignment segment | Retained without offer | Retained with offer | Estimated retention difference |
| --- | --- | --- | --- |
| Higher risk | 70 of 100 | 80 of 100 | +10 percentage points |
| Lower risk | 90 of 100 | 90 of 100 | 0 percentage points |

With equal segment weights, the estimated average retention effect is `(0.10 + 0) / 2 = 0.05`.
Assume an extra retained account contributes 100 units and an offer costs 5 per assigned account,
with no other costs or interference between customers. The estimated extra contribution is:

- Higher risk: `0.10 × 100 - 5 = +5` per assigned account.
- Lower risk: `0 × 100 - 5 = -5` per assigned account.

These are point estimates, not promised gains. Report intervals at the assignment unit, check
guardrails, and confirm a policy's value on data you did not use to choose it. Real economics may
need contribution as the direct outcome, not retention times a constant. The churn guide explains
when high risk and benefit from the action disagree.

**Try it yourself.** An offer costs 12 instead of 5. What do the point estimates recommend?

<details>
<summary>Hint and explained answer</summary>

The two estimated gains become `10 - 12 = -2` and `0 - 12 = -12`. Under these assumptions, keep the
no-contact baseline for both segments. Better retention alone does not make an action profitable.
A capacity limit or uncertain effect can change the decision further.

</details>

## What randomization supplies—and what it still needs

Random assignment makes groups alike on average. Still check assignment logs, eligibility,
sample-ratio mismatch (unplanned group sizes), outcome coverage and the planned analysis horizon.
Analyse outcomes by original assignment for an **intention-to-treat** effect. Dropping failed
deliveries after assignment can leave different kinds of customers in each arm.

The comparison also needs a clear action and outcome, a real chance of receiving each compared
action, and a design for any interference or carryover (lasting effects of earlier actions).
Randomising one customer's price may change another's demand or use up shared stock. Choose the
assignment unit and interpret results accordingly.

## When assignment was not random

A **confounder** affects both who gets the action and the outcome. For example, an account manager
may target unhappy customers, who were already more likely to leave. A treated-versus-untreated
comparison then mixes that selection with the offer's effect.

A **mediator** is changed by the action and sits on a path to the outcome, such as post-offer
engagement. Adjusting for it usually changes the causal question and can bias a total-effect
analysis. A **collider** is a shared result of other variables, and conditioning on it can create a
false association. A diagram helps state these choices, but cannot prove the assumptions.

Observational adjustment usually needs a believable case that measured pre-action variables block
the relevant confounding. It also needs **overlap**: each compared action has a nonzero chance in
the contexts where the policy would choose it. If an action was never tried in a segment, a
flexible model can extrapolate a number without identifying that effect. Restrict the policy or
collect data.

The **propensity** is the probability that the assignment policy selects an action, given
recorded pre-action context. It differs from the predicted chance of a purchase. Estimated
propensities and outcome models are often called nuisance models, because the main target is the
effect or policy value, not their predictions.

**Cross-fitting** trains a nuisance model on other folds before scoring a fold. It can reduce some
overfitting, but cannot repair unmeasured confounding, unsupported actions or a wrong time or group
split. “Doubly robust” is a property under stated assumptions, so the design still matters. The
linked guides give each estimator's requirements.

## Before using an effect estimate

Write the estimand, assignment unit, clocks and outcome coverage. Say which identification
assumptions come from the design and which are your judgement. Keep simulation, past-data prediction
and measured intervention results apart. Then go to the [delivery plan](delivery-plan.md) and one
case: [offers](offer-recommendation.md), [prices](price-recommendation.md) or
[churn and retention](churn.md).

To go deeper, try [The Effect](https://theeffectbook.net/) and the
[metalearners paper](https://www.pnas.org/doi/10.1073/pnas.1804597116), both annotated in the
[chapter resources](resources/README.md).
