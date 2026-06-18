# Module 12: Exercises

## Prerequisites

- Set `OPENAI_API_KEY` in your `.env` file
- Install dependencies: `pip install langchain langchain-core langchain-community langgraph openai langchain-openai`

---

## Part 1: Build a LangChain Chain

Build a chain that takes a topic and produces a structured learning guide with:
- A title
- 3 key concepts (each as a separate LLM call)
- A summary combining all concepts

**Requirements:**
- Use LCEL pipe operators (`|`)
- Use `ChatPromptTemplate` for all prompts
- Use `RunnableParallel` to generate the 3 concepts concurrently
- Use `StrOutputParser` to extract text
- Compose everything into a single chain

**Expected behavior:**
```
Input: {"topic": "Neural Networks"}
→ Parallel: concept1, concept2, concept3 generated simultaneously
→ Summary combining all 3
→ Final output with title + concepts + summary
```

**Starter code:**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_google_genai import ChatChatOpenAI

model = ChatChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# Build the chain here
```

---

## Part 2: Tool Calling with 3 Custom Tools

Create 3 custom tools and let the model choose which one to call:

1. **`get_weather`** — takes a city name, returns simulated weather data
2. **`convert_currency`** — takes amount + from_currency + to_currency, returns converted amount
3. **`calculate_bmi`** — takes weight_kg and height_m, returns BMI value and category

**Requirements:**
- Decorate each function with `@tool` from `langchain_core.tools`
- Include proper docstrings (the model uses these to decide which tool to call)
- Bind all tools to the model using `model.bind_tools()`
- Test with these queries:
  - "What's the weather in Tokyo?"
  - "Convert 100 USD to EUR"
  - "My weight is 70kg and height is 1.75m, what's my BMI?"
  - "What's 15 * 23 + 7?" (should NOT call any tool)
- Print `response.tool_calls` to verify the model selects the right tool

**Starter code:**
```python
from langchain_core.tools import tool
from langchain_google_genai import ChatChatOpenAI

model = ChatChatOpenAI(model="gpt-4o-mini")

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Simulated weather data
    pass

# Define 2 more tools here

tools = [get_weather, convert_currency, calculate_bmi]
model_with_tools = model.bind_tools(tools)

# Test queries
queries = [
    "What's the weather in Tokyo?",
    "Convert 100 USD to EUR",
    "My weight is 70kg and height is 1.75m, what's my BMI?",
    "What's 15 * 23 + 7?"
]

for q in queries:
    response = model_with_tools.invoke(q)
    print(f"Query: {q}")
    print(f"Tool calls: {response.tool_calls}\n")
```

---

## Part 3: LangGraph Workflow with Conditional Logic

Build a LangGraph workflow for a **customer support classifier**:

```
              ┌─────────────┐
              │  Classify   │
              │   Intent    │
              └──────┬──────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     ┌─────────┐ ┌────────┐ ┌──────────┐
     │ Billing │ │Technical│ │ General  │
     │  Agent  │ │ Support │ │   FAQ    │
     └────┬────┘ └────┬───┘ └────┬─────┘
          │          │           │
          └──────────┼───────────┘
                     ▼
              ┌─────────────┐
              │   Respond   │
              └─────────────┘
```

**State:**
```python
from typing import TypedDict, Literal

class SupportState(TypedDict):
    user_message: str
    intent: str  # "billing", "technical", "general"
    response: str
```

**Requirements:**
- Create a `classify_intent` node that uses the LLM to classify the user message
- Create separate nodes for `billing_agent`, `technical_agent`, `general_faq`
- Use a conditional edge from `classify_intent` to route to the correct agent
- Create a `respond` node that formats the final output
- Test with 3 different user messages (one per intent)
- Use `StateGraph` and `MemorySaver` for checkpointing

**Starter code:**
```python
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatChatOpenAI

model = ChatChatOpenAI(model="gpt-4o-mini")

class SupportState(TypedDict):
    user_message: str
    intent: str
    response: str

# Build the graph here
```

---

## Part 4: Design a Multi-Step Agent System (Paper Design)

Design a **research assistant** agent system on paper (or in text) that:

1. Takes a research question from the user
2. Detects the intent: is it a factual lookup, a comparison, or an opinion/analysis?
3. Routes to the appropriate sub-agent:
   - **Factual Lookup Agent** — uses a search tool, returns concise answer
   - **Comparison Agent** — uses search, structures output as a comparison table
   - **Analysis Agent** — uses search + LLM reasoning, provides a nuanced analysis
4. Formats the response with sources

**Your design should include:**
- A state diagram showing all nodes and edges
- The state schema (what fields flow through the graph)
- Descriptions of each node's logic
- The routing function (how intent determines the path)
- At least one place where human-in-the-loop could be useful (and why)

**Deliverables:** A markdown file or diagram describing the full system.

---

## Bonus: Build a Simple Multi-Agent System

Extend Part 3 to implement a **two-agent system**:

1. **Writer Agent** — takes a topic, writes a draft paragraph
2. **Editor Agent** — receives the draft, critiques it, and provides an improved version

**Requirements:**
- Use LangGraph with a `StateGraph`
- The Writer generates first, then the Editor refines
- Add a conditional edge: if the Editor's critique score is below a threshold, loop back to the Writer for revision (max 3 iterations)
- Track the iteration count in state
- Print each iteration's output

**Expected flow:**
```
Writer → Editor → (score < 7?) → Writer → Editor → (score < 7?) → Writer → Editor → Final Response
```

**State schema:**
```python
class DraftState(TypedDict):
    topic: str
    draft: str
    critique: str
    score: int
    iteration: int
```

---

## Self-Check

After completing the exercises, verify:

- [ ] Part 1: Chain produces structured output with parallel concept generation
- [ ] Part 2: Model selects the correct tool for each query
- [ ] Part 3: Graph routes to the correct agent based on intent classification
- [ ] Part 4: Design document includes state schema, nodes, edges, and routing logic
- [ ] Bonus: Writer-Editor loop converges within 3 iterations

## Solutions

Try to solve each exercise before checking solutions. If you get stuck:
1. Re-read the README.md theory section
2. Check the notebook examples for patterns
3. Consult the [resources.md](../resources.md) for documentation links
