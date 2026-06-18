# Exercise 01: AI Landscape & Architecture

## Part 1: AI Taxonomy (10 min)

Answer these questions (short answers):

1. What's the difference between AI, ML, and Deep Learning?
2. Is ChatGPT a Deep Learning model or a Machine Learning model? Explain.
3. Name one example of rule-based AI still used in production today.
4. What makes a model "generative" vs "discriminative"?

## Part 2: Role Mapping (10 min)

For each task, identify which role (Data Scientist, ML Engineer, AI System Engineer) would own it:

| Task | Role |
|------|------|
| Cleaning a messy dataset | |
| Building a training pipeline on Kubernetes | |
| Integrating an LLM API into a FastAPI backend | |
| A/B testing model performance in production | |
| Creating visualizations for stakeholder presentation | |
| Setting up Docker containers for model serving | |
| Fine-tuning a pre-trained model on custom data | |
| Designing a RAG architecture for a chatbot | |

## Part 3: Architecture Analysis (15 min)

Pick ONE of these AI products and create a complete architecture diagram:

- **Option A**: AI-powered email composer (like Gmail Smart Compose)
- **Option B**: Image search system (like Google Reverse Image Search)
- **Option C**: Code review assistant (like CodeRabbit)

For your chosen product:

1. Draw the architecture using the 6-layer framework
2. List the specific technology for each layer (real or reasonable assumptions)
3. Identify the most expensive component (in terms of API calls or compute)
4. Identify the highest latency component
5. What data would this system need to store?

## Part 4: API Exploration (15 min)

Using the OpenAI API:

1. Send 3 different prompts and record the token usage for each
2. What happens when you set `temperature=0.0` vs `temperature=1.0`?
3. Try to make the model return a numbered list. How consistent is the format?
4. What error do you get with an invalid API key? (Try a fake key)

## Bonus Challenge

Sketch an architecture diagram for an **AI-powered customer support system** that:
- Answers questions from a company's knowledge base
- Can escalate to a human agent
- Remembers previous conversations
- Tracks cost per conversation

Draw this as a Mermaid diagram (paste into [mermaid.live](https://mermaid.live)).

---

## Submission

Save your answers in this folder or in your notes. There are no "right" answers for the architecture exercises — the goal is to practice thinking in layers.
