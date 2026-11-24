# Rubric v0

Eight criteria, equal weight, scale 1-5. The machine-readable version is [`rubric.json`](rubric.json) (same content).

## Scoring rules

- Every score must cite at least one verbatim quote from the candidate's transcript.
- A criterion the candidate never addressed is "status": "missing" with score: null. In the overall average it counts as 1.
- Overall = mean of the 8 criteria, rounded to one decimal.
- Half points (x.5) are allowed.
- No scoring of voice tone, accent, emotion or confidence. Only what was said.

## Criteria

### `clarify_goal`: Clarifying the goal and the context

**Definition:** Establishes what success means and the context (company, product, constraints) before designing anything.

- **Level 1:** Starts designing immediately, or asks no questions, or asks only generic ones that change nothing.
- **Level 3:** Asks several relevant questions and restates the goal, but does not use the answers to shape the rest of the answer.
- **Level 5:** Asks targeted questions on goal, users, constraints and timeline, restates the goal in one sentence, and visibly uses the answers later.

**What counts as evidence:** Questions asked in the Clarify stage; a restated goal; later references to facts the interviewer gave.

### `user_segment`: Choosing and justifying a user segment

**Definition:** Names distinct user segments, picks one, and justifies the choice with reasons.

- **Level 1:** Treats 'users' as one group, or names a segment with no reason for choosing it.
- **Level 3:** Names two or more segments and picks one, with a reason that is partly generic.
- **Level 5:** Compares segments on size, pain and value to the business, picks one explicitly, and says who is deliberately left out and why.

**What counts as evidence:** Segment lists; the words used to choose between them; any mention of who is excluded.

### `pain_points`: Finding and prioritising pain points

**Definition:** Identifies concrete pain points of the chosen segment and ranks them.

- **Level 1:** Lists features or generic problems with no link to the chosen user.
- **Level 3:** Lists several real pain points for the segment but does not rank them or says why one matters most.
- **Level 5:** Describes specific pain points in the user's own situation, ranks them by severity and frequency, and picks the top one with a reason.

**What counts as evidence:** Descriptions of the user's day or workflow; explicit ranking language; the reason given for the top pain.

### `solutions`: Solution quality and creativity

**Definition:** Proposes solutions that address the top pain point, with some range and originality.

- **Level 1:** Offers one obvious or vague idea that does not clearly address a stated pain point.
- **Level 3:** Offers two or three solutions that address the pain point, mostly conventional, with limited detail on how they work.
- **Level 5:** Offers a small set of distinct solutions tied to the top pain, explains how each works for the user, includes at least one non-obvious idea, and picks one to build first.

**What counts as evidence:** Named solutions; how each is linked to a pain point; which one is chosen first and why.

### `tradeoffs`: Trade-offs and prioritisation

**Definition:** Weighs options against cost, risk and impact and makes a clear choice.

- **Level 1:** Does not mention any downside or alternative; everything is presented as good.
- **Level 3:** Mentions trade-offs or risks but decides without comparing them, or lists them without a conclusion.
- **Level 5:** Compares options on impact, effort and risk, states what is given up, makes a decision, and says what would change it.

**What counts as evidence:** Phrases such as 'instead of', 'the cost is', 'I would not do'; a stated decision rule; risks named with a response.

### `metrics`: Success metrics

**Definition:** Defines how success is measured, including a primary metric and guardrails.

- **Level 1:** No metrics, or only vanity numbers with no link to the goal.
- **Level 3:** Names a reasonable primary metric but no guardrails, or no definition of how it is measured.
- **Level 5:** Defines one primary (north-star) metric linked to the goal, defines it precisely, adds guardrail metrics, and says what result would count as success.

**What counts as evidence:** The metric names; their definitions; any guardrails or targets; the link back to the stated goal.

### `structure`: Structure and communication

**Definition:** Communicates in a clear, logical order that the interviewer can follow.

- **Level 1:** Jumps between topics, with no stated plan, and the interviewer has to piece the answer together.
- **Level 3:** Has a recognisable order but loses it at times, or skips signposting and summaries.
- **Level 5:** States a plan up front, signposts each part, keeps to the order within the time, and ends with a concise summary of the recommendation.

**What counts as evidence:** Opening plan statements; transitions between parts; the closing summary. Judge only what was said, not delivery.

### `pushback`: Handling pushback

**Definition:** Responds to challenge with reasoning, adjusting where warranted and holding firm where justified.

- **Level 1:** Gets defensive, repeats the claim, or drops the position at the first challenge without a reason.
- **Level 3:** Answers the challenge but with partial reasoning, or changes position without explaining why.
- **Level 5:** Engages with the specific challenge, concedes what is valid, defends what is justified with evidence or logic, and updates the answer coherently.

**What counts as evidence:** The candidate's replies in the Pushback stage and to any interruption; whether the reply addresses the actual challenge.
