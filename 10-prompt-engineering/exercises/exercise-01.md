# Module 10 Exercise: Advanced Prompt Engineering

## Instructions

Complete all parts below. Use the OpenAI API for testing. Submit your completed notebook files.

---

## Part 1: Rewrite Bad Prompts (PCFT Framework)

Rewrite each of the following prompts using the Persona-Context-Task-Format framework. For each, identify what's missing and explain how the rewrite improves it.

### 1.1

```
Look at this data and tell me what's wrong.
```

**Input data:**
```
2024-01-15, 250 units, $12,500, Region A
2024-01-16, 0 units, $0, Region A
2024-01-17, 310 units, $15,500, Region A
2024-01-18, -20 units, $-1,000, Region A
2024-01-19, 280 units, $14,000, Region A
```

**Your rewrite:**

```python
# Write your PCFT prompt here
```

**What was missing:** (explain)

---

### 1.2

```
Summarize this article.
```

**Article:** The global semiconductor shortage that began in 2020 has forced automakers to cut production by an estimated 7.7 million vehicles in 2021, according to AlixPartners. The shortage has been exacerbated by increased demand for consumer electronics during the pandemic, trade tensions between the US and China, and a fire at a key Japanese factory. Major automakers including Ford, GM, and Toyota have all announced production cuts. The shortage is expected to ease by mid-2023 as new fabrication plants come online.

**Your rewrite:**

```python
# Write your PCFT prompt here
```

**What was missing:** (explain)

---

### 1.3

```
Write code for user authentication.
```

**Your rewrite:**

```python
# Write your PCFT prompt here
```

**What was missing:** (explain)

---

### 1.4

```
Analyze sentiment.
```

**Input:** "The product works great when it works, but it crashes at least twice a day. Support was helpful but the issue keeps coming back."

**Your rewrite:**

```python
# Write your PCFT prompt here
```

**What was missing:** (explain)

---

### 1.5

```
Make this better.
```

**Code:**
```python
def get_users(db):
    result = db.execute("SELECT * FROM users")
    return result
```

**Your rewrite:**

```python
# Write your PCFT prompt here
```

**What was missing:** (explain)

---

## Part 2: Few-Shot vs Zero-Shot Comparison

### 2.1 Task

Classify customer support emails into categories: `TECHNICAL`, `BILLING`, `FEATURE`, `ACCOUNT`.

### 2.2 Zero-Shot Prompt

Write a zero-shot classification prompt and run it on these 5 test cases:

```python
test_cases = [
    "My invoice shows $99 but I was charged $149",
    "The API returns 500 errors on the /users endpoint",
    "Can you add support for exporting to PDF?",
    "I forgot my password and the reset link isn't working",
    "The dashboard loads very slowly today",
]
```

### 2.3 Few-Shot Prompt

Write a few-shot prompt with 4 examples covering each category, then run it on the same 5 test cases.

### 2.4 Comparison

Create a comparison table and answer:

| Case | Zero-Shot Result | Few-Shot Result | Consistent? |
|------|------------------|-----------------|-------------|
| 1    |                  |                 |             |
| 2    |                  |                 |             |
| 3    |                  |                 |             |
| 4    |                  |                 |             |
| 5    |                  |                 |             |

**Which technique was more consistent? Why?**

(Write your answer here)

---

## Part 3: Classification Prompt Template

### 3.1 Build a reusable classification template

Create a Python class `ClassificationTemplate` that:
- Takes categories and a role as constructor arguments
- Has a `classify(text)` method that renders the prompt and returns the category
- Handles empty/invalid input gracefully (returns "UNCLASSIFIED")
- Validates the model's output against known categories

### 3.2 Test with different domain

Use your template to classify **technical error messages** into severity levels:
- `CRITICAL`: System down, data loss
- `HIGH`: Major feature broken
- `MEDIUM`: Minor feature broken
- `LOW`: Cosmetic issue

Test cases:
```python
error_messages = [
    "Database connection pool exhausted, all requests failing",
    "User avatar not displaying on profile page",
    "Typo in error message on login page",
    "Payment processing returning 503 errors",
    "Search results slightly misaligned on mobile",
    "Authentication service unreachable, users cannot log in",
]
```

### 3.3 Code

```python
# Write your ClassificationTemplate class and test code here
```

---

## Part 4: Summarization Prompt Template

### 4.1 Build a summarization template

Create a `SummarizationTemplate` class that supports:
- Multiple summary styles: `executive`, `technical`, `bullet`
- Configurable length (short, medium, long)
- Optional context/audience parameter

### 4.2 Test with a meeting transcript

Test your template with this sample:

```
Meeting: Sprint Retrospective - June 2024

Attendees: Sarah (PM), Mike (Tech Lead), Lisa (Designer), Tom (Backend)

Key Discussion Points:
1. Sprint velocity dropped 15% from previous sprint. Main cause: unexpected production incident took 2 engineers offline for 3 days.
2. New onboarding flow shipped successfully. User activation increased 23%.
3. API response times degraded after last deployment. Need to investigate caching layer.
4. Design system update blocked by lack of engineering resources.
5. Team morale concerns raised by Tom - excessive overtime in last 2 sprints.

Action Items:
- Mike: Investigate API caching issue (due next Tuesday)
- Lisa: Create design system prioritization doc
- Sarah: Discuss resource allocation with leadership
- Tom: Document the overtime concerns formally
```

### 4.3 Code

```python
# Write your SummarizationTemplate class and test code here
# Generate all three summary styles and compare
```

---

## Part 5: Chain-of-Thought for Complex Reasoning

### 5.1 Build a CoT prompt

Write a chain-of-thought prompt that analyzes a system architecture diagram description and identifies potential failure points.

Input:
```
Architecture:
- Frontend: React SPA hosted on CDN
- API Gateway: Kong, routes to 3 microservices
- Auth Service: Node.js, PostgreSQL, handles JWT tokens
- Order Service: Python, MongoDB, processes orders
- Notification Service: Go, Redis queues, sends emails/SMS
- Database: PostgreSQL (primary) + MongoDB replica set
- Cache: Redis cluster (3 nodes)
- Message Queue: RabbitMQ

Recent issues:
- Intermittent 503 errors during peak hours
- Some users receiving duplicate order confirmations
- Authentication token validation slow (>2s)
```

### 5.2 Requirements

Your CoT prompt should guide the model through:
1. Identifying all single points of failure
2. Analyzing data flow between services
3. Assessing the impact of each component failing
4. Prioritizing fixes by severity

### 5.3 Code

```python
# Write your CoT prompt and test it here
```

---

## Bonus: Edge Case Handling

### Challenge

Create a prompt system that handles ALL of the following edge cases gracefully:

1. **Empty input** → Return a structured error response
2. **Input in wrong language** → Detect and respond appropriately
3. **Input too long** → Truncate intelligently and note the truncation
4. **Ambiguous input** → Request clarification or provide best guess with confidence
5. **Contradictory input** → Flag the contradiction and ask for resolution

### Requirements

- Single prompt template that handles all cases
- Structured JSON output for all responses
- No unhandled exceptions

### Code

```python
# Write your edge-case-handling prompt system here
# Test with examples of each edge case
```

---

## Submission

Submit the following files:
1. This exercise file with all code blocks completed
2. Your notebook files from the exercises above
3. A brief reflection (3-5 sentences) on what surprised you about prompt engineering
