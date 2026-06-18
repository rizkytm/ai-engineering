# Module 10: Advanced Prompt Engineering & Context Management

## Learning Objectives

By the end of this module, you will be able to:

- Structure prompts using the Persona-Context-Task-Format framework
- Apply zero-shot, few-shot, and chain-of-thought prompting techniques
- Control LLM output through temperature, top-p, and max_tokens
- Build reusable prompt templates for classification, summarization, and extraction
- Implement production-grade prompt management for backend systems

---

## 1. Why Prompt Engineering Matters

Prompt engineering is not "just chatting with AI." It is a disciplined practice that determines the reliability, consistency, and quality of LLM outputs. In production systems, the prompt is the interface between your application logic and the model's behavior.

Poorly crafted prompts produce:
- Inconsistent output formats that break downstream parsers
- Hallucinations that propagate through data pipelines
- High latency from excessive retries and fallbacks
- Unpredictable costs from verbose or redundant responses

Well-engineered prompts produce:
- Deterministic output structures for reliable parsing
- Factual, grounded responses with reduced hallucination
- Token-efficient interactions that minimize cost
- Systematic behavior across diverse input types

**Core principle:** Treat prompts as code. Version them, test them, and iterate on them systematically.

---

## 2. Prompt Structure: The PCFT Framework

Every effective prompt contains four components:

### Persona
Defines who the model should act as. This constrains the model's knowledge domain and communication style.

```
You are a senior security analyst reviewing infrastructure code for vulnerabilities.
```

### Context
Provides background information the model needs to make informed decisions. This includes relevant data, constraints, and domain-specific knowledge.

```
The following code is part of a microservices architecture deployed on AWS EKS.
The service handles authentication tokens and PII data.
```

### Task
The specific action you want the model to perform. Be explicit about scope and boundaries.

```
Review the provided Terraform configuration and identify security misconfigurations.
Focus on: IAM permissions, network exposure, encryption at rest, and secret management.
```

### Format
Specifies the exact output structure. This eliminates ambiguity and ensures parseable responses.

```
Respond in JSON format:
{
  "findings": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "resource": "resource_name",
      "issue": "description of the misconfiguration",
      "recommendation": "specific remediation step"
    }
  ],
  "summary": "one paragraph overview"
}
```

### Complete Example

```
You are a senior security analyst reviewing infrastructure code for vulnerabilities.
The following code is part of a microservices architecture deployed on AWS EKS.
The service handles authentication tokens and PII data.

Review the provided Terraform configuration and identify security misconfigurations.
Focus on: IAM permissions, network exposure, encryption at rest, and secret management.

Respond in JSON format:
{
  "findings": [
    {
      "severity": "HIGH|MEDIUM|LOW",
      "resource": "resource_name",
      "issue": "description",
      "recommendation": "remediation step"
    }
  ],
  "summary": "one paragraph overview"
}

--- BEGIN TERRAFORM CODE ---
{{terraform_code}}
--- END TERRAFORM CODE ---
```

---

## 3. Prompting Techniques

### Zero-Shot Prompting
No examples provided. The model relies entirely on its pre-trained knowledge.

```
Classify the following customer review as positive, negative, or neutral.

Review: "The product arrived late and the packaging was damaged."
```

**When to use:** Simple, well-defined tasks where the model has strong pre-trained capability.

### Few-Shot Prompting
Provide examples that demonstrate the expected input-output mapping.

```
Classify customer reviews as positive, negative, or neutral.

Review: "Absolutely love this product, best purchase I've made this year!"
Classification: positive

Review: "The item works as described, nothing special."
Classification: neutral

Review: "Terrible quality, broke after two days of use."
Classification: negative

Review: "The product arrived late and the packaging was damaged."
Classification:
```

**When to use:** Tasks requiring specific output format, domain-specific classification, or when zero-shot produces inconsistent results.

### Chain-of-Thought (CoT) Prompting
Instruct the model to reason step-by-step before producing a final answer.

```
You are a financial analyst. Analyze the following quarterly report and determine
whether the company's financial health is improving, stable, or declining.

Quarterly data:
Q1: Revenue $2.1M, Expenses $1.8M, Debt $500K
Q2: Revenue $2.4M, Expenses $1.7M, Debt $450K

Think through this step-by-step:
1. Calculate profit margins for each quarter
2. Analyze the trend in expenses relative to revenue
3. Evaluate debt reduction progress
4. Synthesize findings into a final assessment

Provide your final answer as:
Assessment: [improving|stable|declining]
Confidence: [high|medium|low]
Reasoning: [2-3 sentence summary]
```

**When to use:** Complex reasoning tasks, mathematical problems, multi-step analysis, or when accuracy is more important than speed.

---

## 4. Output Control Parameters

### Temperature (0.0 - 2.0)
Controls randomness in token selection.

| Value | Behavior | Use Case |
|-------|----------|----------|
| 0.0 | Deterministic, always picks highest probability token | Data extraction, classification, code generation |
| 0.3 | Low randomness, mostly consistent | Summarization, structured output |
| 0.7 | Balanced creativity and coherence | General conversation, content generation |
| 1.0+ | High randomness, diverse outputs | Creative writing, brainstorming |

### Top-P (Nucleus Sampling)
Controls diversity by considering only tokens whose cumulative probability reaches the threshold.

- **top_p = 0.1:** Only the most probable tokens are considered
- **top_p = 0.9:** Broader range of tokens, more diverse output
- **top_p = 1.0:** All tokens considered

**Best practice:** Adjust either temperature or top-p, not both simultaneously.

### Max Tokens
Limits the maximum length of the response. Set this explicitly in production to:
- Control API costs
- Prevent runaway outputs
- Ensure consistent response parsing

```
response = client.generate(
    prompt=prompt,
    temperature=0.3,
    top_p=0.9,
    max_tokens=512
)
```

---

## 5. System Prompts

System prompts define the model's behavior for the entire conversation. They are the foundation of consistent, production-grade interactions.

### Why System Prompts Matter

In backend systems, you cannot rely on users to provide good context. The system prompt:
- Establishes baseline behavior that persists across turns
- Defines output format requirements
- Sets domain-specific constraints
- Prevents off-topic or unsafe responses

### System Prompt Structure

```
You are [ROLE]. You [PRIMARY_FUNCTION].

Rules:
1. [Constraint 1]
2. [Constraint 2]
3. [Constraint 3]

Output format:
[Explicit format specification]

When you don't know the answer:
[Behavior for uncertainty]
```

### Example: Customer Support Agent

```
You are a customer support agent for CloudScale, a cloud infrastructure provider.

Rules:
1. Only answer questions about CloudScale products and services
2. Never share internal pricing algorithms or competitor comparisons
3. Escalate to human support for billing disputes over $500
4. Always provide the ticket number format: CS-XXXXX

Output format:
Response: [helpful answer]
Action Required: [none|escalate|follow-up]
Ticket Number: CS-XXXXX

When you don't know the answer:
Response: "I don't have specific information about that. Let me connect you with a specialist who can help."
Action Required: escalate
```

---

## 6. Prompt Patterns for Backend Systems

Production prompts differ from experimentation prompts. They require:

### Consistency
The same input should always produce structurally identical output.

```python
# Production prompt with fixed output structure
SYSTEM_PROMPT = """
Analyze the input text and return a JSON object with exactly these fields:
- sentiment: one of ["positive", "negative", "neutral"]
- confidence: float between 0.0 and 1.0
- keywords: list of exactly 3 strings
- summary: string, max 50 words

Do not include any text outside the JSON object.
"""
```

### Error Handling
Design prompts that degrade gracefully.

```python
SYSTEM_PROMPT = """
Analyze the customer feedback and extract structured data.

If the input is empty or unreadable, return:
{"error": "invalid_input", "message": "Input text could not be processed"}

If the input is in a language you cannot process, return:
{"error": "unsupported_language", "message": "Input language not supported"}

Otherwise, return:
{
  "sentiment": "positive|negative|neutral",
  "category": "product|service|support|billing",
  "urgency": "low|medium|high",
  "summary": "one sentence summary"
}
"""
```

### Token Efficiency
Minimize prompt tokens while maintaining quality.

```python
# Verbose (wasteful)
prompt = """
I would like you to please analyze the following customer feedback and tell me
what the sentiment is. The feedback might be positive, negative, or neutral.
Please also identify the main category it falls into and provide a brief summary.
"""

# Efficient (production)
prompt = """
Analyze customer feedback.
Return JSON: {"sentiment": "positive|negative|neutral", "category": "product|service|support", "summary": "string"}
"""
```

---

## 7. Output Formatting and Consistency

### JSON Output
Always specify the exact schema and use system-level instructions to prevent markdown wrapping.

```
Respond with a valid JSON object. No markdown, no code fences, no explanation.
```

### Structured Lists
For list-based outputs, specify the exact number of items and their format.

```
Extract exactly 5 key themes from the text.
Return as a numbered list:
1. [theme]: [one sentence explanation]
2. [theme]: [one sentence explanation]
...
```

### Controlled Vocabulary
Constrain outputs to predefined values to ensure downstream compatibility.

```
Classify the document into exactly one category:
- TECHNICAL: code, APIs, architecture, DevOps
- BUSINESS: revenue, growth, strategy, market
- LEGAL: compliance, regulation, contracts, liability
- HR: hiring, culture, performance, benefits

Return only the category name, nothing else.
```

---

## Summary

| Concept | Key Takeaway |
|---------|--------------|
| PCFT Framework | Persona, Context, Task, Format — always include all four |
| Zero-Shot | Simple tasks, no examples needed |
| Few-Shot | Complex tasks, specific output format |
| Chain-of-Thought | Reasoning tasks, multi-step analysis |
| Temperature | 0.0 for extraction, 0.3 for summarization, 0.7+ for creative |
| System Prompts | Define behavior, constraints, and format for entire session |
| Production Prompts | Consistent, error-handling, token-efficient |

---

## Next Steps

- **Notebook 01:** Practice prompt structure with the PCFT framework
- **Notebook 02:** Compare prompting techniques across real examples
- **Notebook 03:** Build production-ready prompt templates
- **Exercise 01:** Hands-on practice with all techniques
