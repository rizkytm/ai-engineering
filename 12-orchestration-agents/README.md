# Module 12: AI Orchestration & Multi-Agent Workflows

## Overview

Simple LLM calls handle single-turn tasks. Real AI systems need orchestration: managing chains of LLM calls, routing through tools, maintaining state, and coordinating multiple agents. This module covers LangChain for composable chains, tool calling for external function access, and LangGraph for stateful, multi-step workflows.

## Learning Objectives

By the end of this module, you will be able to:

- Build composable LLM chains using LangChain Expression Language (LCEL)
- Add memory and state to conversational systems
- Define and connect tools that LLMs can call autonomously
- Build stateful workflows with LangGraph (nodes, edges, conditional routing)
- Implement human-in-the-loop patterns
- Design multi-agent architectures

---

## 1. Orchestration in AI Systems

### Why Orchestration?

A single prompt + LLM call works for simple tasks. But production systems require:

- **Multi-step reasoning** — break a complex task into steps, each handled by a different LLM call or tool
- **Conditional logic** — route to different paths based on intermediate results
- **Tool access** — let the LLM call external APIs, databases, calculators
- **State management** — track context across multiple interactions
- **Error handling** — retry, fallback, or escalate when steps fail

Orchestration is the layer that manages this complexity.

### The Spectrum of Complexity

```
Simple Prompt → Chain → Dynamic Chain → Graph → Multi-Agent System
     ↑                                                              ↑
  One call                                                    Many actors
```

| Pattern | Description | Example |
|---------|-------------|---------|
| Single call | One prompt → one LLM response | Chat, classification |
| Sequential chain | Output of step N feeds into step N+1 | RAG pipeline |
| Dynamic chain | Model decides which tools/steps to use | Tool-calling agent |
| Stateful graph | Nodes, edges, cycles, human-in-the-loop | Complex workflows |
| Multi-agent | Multiple autonomous agents collaborate | Research team |

---

## 2. LangChain: Chains, Memory, Prompt Templating

### What is LangChain?

LangChain is a framework for building applications powered by LLMs. It provides:

- **LCEL (LangChain Expression Language)** — declarative chain composition using the `|` pipe operator
- **Prompt Templates** — reusable, parameterized prompts
- **Memory** — state management across interactions
- **Integrations** — connectors for LLMs, tools, vector stores

### LangChain Expression Language (LCEL)

LCEL composes runnables using the pipe operator `|`. Each runnable accepts an input and returns an output.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatChatOpenAI

model = ChatChatOpenAI(model="gpt-4o-mini")

# Simple chain: prompt → model → parser
chain = ChatPromptTemplate.from_template("Tell me about {topic}") | model | StrOutputParser()

result = chain.invoke({"topic": "quantum computing"})
```

### Composing Chains

Chains compose into larger chains:

```python
# Two-step chain
generate = ChatPromptTemplate.from_template("Write a short poem about {topic}") | model | StrOutputParser()
summarize = ChatPromptTemplate.from_template("Summarize this poem in one sentence:\n{poem}") | model | StrOutputParser()

# Compose: generate → summarize
full_chain = {"poem": generate} | summarize
result = full_chain.invoke({"topic": "ocean"})
```

### RunnableParallel

`RunnableParallel` runs multiple runnables concurrently, returning a dict:

```python
from langchain_core.runnables import RunnableParallel

# Run two chains in parallel
parallel = RunnableParallel(
    joke=ChatPromptTemplate.from_template("Tell a joke about {topic}") | model | StrOutputParser(),
    fact=ChatPromptTemplate.from_template("Share a fact about {topic}") | model | StrOutputParser()
)

result = parallel.invoke({"topic": "space"})
# result = {"joke": "...", "fact": "..."}
```

### RunnablePassthrough

`RunnablePassthrough` passes its input through unchanged, useful for adding context:

```python
from langchain_core.runnables import RunnablePassthrough

# Add "original" key alongside processed output
chain = RunnableParallel(
    original=RunnablePassthrough(),
    processed=ChatPromptTemplate.from_template("Rewrite this formally: {text}") | model | StrOutputParser()
)

result = chain.invoke({"text": "hey whats up"})
# result = {"original": {"text": "hey whats up"}, "processed": "..."}
```

### Prompt Templates

Templates with variables for dynamic prompts:

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Basic template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    ("human", "{question}")
])

# Few-shot template
examples = [{"input": "Hi", "output": "Hello! How can I help?"}]
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}")
])
few_shot = FewShotChatMessagePromptTemplate(example_prompt=example_prompt, examples=examples)
```

### Adding Memory

Memory stores conversation history for multi-turn interactions:

```python
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Manual memory with MessagesPlaceholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | model | StrOutputParser()

# Maintain history manually
history = []
result1 = chain.invoke({"input": "Hi, my name is Alice", "history": history})
history.append(HumanMessage(content="Hi, my name is Alice"))
history.append(AIMessage(content=result1))
result2 = chain.invoke({"input": "What's my name?", "history": history})
```

For automatic memory, use `ConversationBufferMemory` with `ConversationChain`, though LCEL with manual history is more transparent and flexible.

---

## 3. Linear Chains vs Dynamic Orchestration

### Linear Chains

Linear chains follow a fixed sequence: A → B → C. Predictable, easy to debug.

```
Input → Prompt → LLM → Parser → Output
```

Use for: RAG pipelines, structured extraction, classification pipelines.

### Dynamic Orchestration

The model decides what to do next based on the input. The workflow is not predetermined.

```
Input → LLM → [Tool call? → Tool → LLM] or [Direct response?] → Output
```

Use for: Agents, chatbots with tool access, research assistants.

The key difference: in linear chains, you define the flow. In dynamic orchestration, the model chooses the flow.

---

## 4. LangGraph: Stateful Orchestration

### What is LangGraph?

LangGraph is a library from LangChain for building stateful, multi-actor applications with LLMs. It models workflows as graphs where:

- **Nodes** are functions that do work (call LLMs, run tools, process data)
- **Edges** connect nodes and define the flow
- **State** is a shared object passed through the graph

LangGraph is ideal when you need cycles, conditional logic, or human-in-the-loop.

### Core Concepts

#### State

State is a typed dictionary that flows through the graph. Each node reads from and writes to it.

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    messages: Annotated[list, "Chat messages"]
    next_step: str
```

#### Nodes

Nodes are Python functions that receive state and return state updates.

```python
def call_model(state: AgentState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def use_tool(state: AgentState):
    # process tool call
    return {"messages": [tool_result]}
```

#### Edges

Edges connect nodes. They can be:

- **Fixed** — always go from node A to node B
- **Conditional** — choose the next node based on state

```python
from langgraph.graph import END

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", use_tool)
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
graph.add_edge("tools", "agent")
```

### Human-in-the-Loop

LangGraph supports interrupting execution for human review:

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = compiled_graph(checkpointer=checkpointer)

# Run until interrupted
result = graph.invoke(input_state, config={"configurable": {"thread_id": "1"}})

# Human reviews and approves
graph.update_state(config, {"messages": [HumanMessage("Approved")]})
result = graph.invoke(None, config=config)
```

---

## 5. Tool Calling: Connecting External Functions to LLMs

### What is Tool Calling?

Tool calling lets an LLM request the execution of external functions. The model generates a structured call (function name + arguments), your code executes it, and the result is fed back to the model.

This is the foundation of AI agents — the model can reason about what it needs and request the right tool.

### Defining Tools

With LangChain, tools are Python functions decorated with `@tool`:

```python
from langchain_core.tools import tool

@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

@tool
def search(query: str) -> str:
    """Search for information about a topic."""
    # In production, call a real search API
    return f"Search results for: {query}"
```

### Connecting Tools to LLM

Bind tools to the model so it knows what's available:

```python
tools = [calculate, search]
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke("What is 15 * 23?")
# response.tool_calls = [{"name": "calculate", "args": {"expression": "15 * 23"}}]
```

### Tool Execution Loop

The pattern for tool calling:

1. User sends a message
2. LLM decides which tool(s) to call
3. Code executes the tool(s)
4. Tool results are added to the conversation
5. LLM generates a final response using the results

This loop is what LangGraph automates.

---

## 6. Building Multi-Step Workflows

### Intent Detection → Retrieval → Prompt → Tool Calling

A real-world workflow combines multiple patterns:

```
User Input
    ↓
Intent Detection (LLM classifies the request)
    ↓
Route:
  ├─ General question → Direct LLM response
  ├─ Knowledge question → RAG retrieval → LLM with context
  └─ Action request → Tool calling → LLM with results
    ↓
Response to user
```

### Example: Research Assistant

```python
class ResearchState(TypedDict):
    query: str
    intent: str
    context: list
    answer: str

def detect_intent(state):
    response = model.invoke(f"Classify this query: {state['query']}")
    return {"intent": response.content}

def route(state):
    if "factual" in state["intent"].lower():
        return "retrieve"
    return "direct_answer"

def retrieve_context(state):
    docs = vectorstore.similarity_search(state["query"])
    return {"context": docs}

def generate_answer(state):
    context = "\n".join([doc.page_content for doc in state["context"]])
    response = model.invoke(f"Context: {context}\n\nQuestion: {state['query']}")
    return {"answer": response.content}
```

---

## 7. Agent Architectures

### ReAct (Reasoning + Acting)

The ReAct pattern interleaves reasoning and action:

```
Thought: I need to find the population of France
Action: search("population of France 2024")
Observation: France has approximately 68 million people
Thought: I now have the answer
Response: France has approximately 68 million people
```

LangGraph makes this explicit — each iteration is a node in the graph.

### Function Calling Agents

Modern LLMs (Gemini, GPT-4) have native function calling. The agent:

1. Receives the user message
2. Generates tool calls (if needed)
3. Receives tool results
4. Generates the final answer

This is simpler than ReAct for most use cases.

### Multi-Agent Systems

Multiple specialized agents collaborate on a task:

- **Router Agent** — classifies intent, delegates to specialists
- **Research Agent** — gathers information using search tools
- **Coding Agent** — writes and executes code
- **Review Agent** — evaluates outputs from other agents

Communication patterns:

- **Sequential** — Agent A finishes, passes result to Agent B
- **Parallel** — Multiple agents work simultaneously, results merged
- **Supervisor** — A coordinator agent manages others

---

## 8. Tool Calling , with OpenAI

Gemini supports tool calling natively. With LangChain:

```python
from langchain_google_genai import ChatChatOpenAI

model = ChatChatOpenAI(model="gpt-4o-mini")
model_with_tools = model.bind_tools([calculate, search])

# Model generates structured tool calls
response = model_with_tools.invoke("What's the square root of 144?")
print(response.tool_calls)
# [{'name': 'calculate', 'args': {'expression': '144 ** 0.5'}}]
```

---

## Key Takeaways

| Concept | What It Does |
|---------|-------------|
| LCEL | Compose chains with `\|` pipe operator |
| RunnableParallel | Run multiple chains concurrently |
| RunnablePassthrough | Pass input through unchanged |
| Memory | Store conversation history |
| Tools | External functions the LLM can call |
| LangGraph | Stateful graphs with nodes, edges, cycles |
| State | Typed dict flowing through the graph |
| Conditional edges | Dynamic routing based on state |
| Human-in-the-loop | Pause for human review/approval |
| Multi-agent | Multiple agents collaborating |

---

## Prerequisites

Before starting this module, ensure you have:

- ✅ Module 11 (RAG) — understanding of retrieval chains
- ✅ Python environment with `langchain`, `langchain-core`, `langchain-community`, `langgraph`, `openai`
- ✅ `OPENAI_API_KEY` set in `.env`

## Environment Setup

```bash
# Install dependencies
pip install langchain langchain-core langchain-community langgraph openai langchain-openai

# Set your API key
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Module Contents

| File | Description |
|------|-------------|
| [notebooks/01-langchain-basics.ipynb](notebooks/01-langchain-basics.ipynb) | LCEL, chains, prompts, memory |
| [notebooks/02-tool-calling.ipynb](notebooks/02-tool-calling.ipynb) | Defining tools, Gemini tool calling |
| [notebooks/03-langgraph-workflow.ipynb](notebooks/03-langgraph-workflow.ipynb) | StateGraph, nodes, edges, HITL |
| [exercises/exercise-01.md](exercises/exercise-01.md) | Practice problems |
| [resources.md](resources.md) | External references |

## Next Module

→ [Module 13: AI Backend & API](../13-ai-backend-api/) — FastAPI, Pydantic, LLM integration
