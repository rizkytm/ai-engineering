# Exercise 01 — RAG Pipeline Practice

## Setup

```bash
cp ../.env.example .env
# Add your keys:
# OPENAI_API_KEY=your_key
# PINECONE_API_KEY=your_key
```

---

## Part 1: Build a Basic RAG Pipeline

Build a RAG pipeline from scratch using LangChain and Pinecone.

**Steps:**

1. Load a text document using `TextLoader` or create documents inline
2. Split text into chunks using `RecursiveCharacterTextSplitter` (chunk_size=500, chunk_overlap=100)
3. Initialize `ChatOpenAIEmbeddings` with `text-embedding-004`
4. Create a Pinecone index and store the chunks using `PineconeVectorStore.from_documents()`
5. Build a retrieval chain using `RetrievalQA` , with OpenAI
6. Test with 3 different queries

**Skeleton:**

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatOpenAIEmbeddings, ChatChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Load documents
# loader = TextLoader("your_document.txt")
# documents = loader.load()

# 2. Split into chunks
# splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
# chunks = splitter.split_documents(documents)

# 3. Embeddings
# embeddings = ChatOpenAIEmbeddings(model="models/text-embedding-004")

# 4. Vector store
# vector_store = PineconeVectorStore.from_documents(
#     documents=chunks, embedding=embeddings,
#     index_name="exercise-rag", namespace="docs"
# )

# 5. RAG chain
# llm = ChatChatOpenAI(model="gpt-4o-mini", temperature=0)
# prompt = PromptTemplate(...)
# chain = RetrievalQA.from_chain_type(...)

# 6. Test
# result = chain.invoke({"query": "Your question here"})
```

**Verify:** Your pipeline returns grounded answers and lists source documents.

---

## Part 2: Experiment with Chunk Sizes

Compare how chunk size affects retrieval quality.

**Steps:**

1. Take a single document (at least 2000 characters)
2. Split it with 3 different chunk sizes: 200, 500, 1000
3. For each size, embed and store in separate Pinecone namespaces
4. Run the same 5 test queries against each
5. Compare which chunks retrieve the most relevant content

**Test queries (adapt to your document):**

```python
test_queries = [
    "What is the main topic?",
    "How does [specific concept] work?",
    "What are the benefits?",
    "What are the requirements?",
    "How do I get started?"
]
```

**Deliverable:** A comparison showing which chunk size retrieved the best results for each query and why.

---

## Part 3: Add Metadata Filtering

Enhance retrieval by adding and filtering on metadata.

**Steps:**

1. When creating documents, add metadata fields: `source`, `topic`, `date`
2. Store all documents in Pinecone with metadata
3. Query with metadata filters to narrow results:
   ```python
   results = vector_store.similarity_search(
       "query", k=3,
       filter={"topic": "specific_topic"}
   )
   ```
4. Test filtering by different fields
5. Compare filtered vs unfiltered retrieval quality

**Example metadata:**

```python
doc = Document(
    page_content="...",
    metadata={
        "source": "documentation",
        "topic": "getting-started",
        "date": "2024-01-15"
    }
)
```

---

## Part 4: Optimize RAG Prompts

Compare different prompt templates for answer quality.

**Create 3 prompt variations:**

1. **Minimal:** Just context and question
2. **Structured:** Include instructions to cite sources and handle unknowns
3. **Chain-of-thought:** Ask the model to reason through the context before answering

```python
# Minimal
minimal = PromptTemplate(
    template="Context: {context}\nQuestion: {question}\nAnswer:",
    input_variables=["context", "question"]
)

# Structured
structured = PromptTemplate(
    template=\"\"\"Answer using ONLY the provided context.
If the context doesn't contain enough info, say so.
Cite which part of the context supports your answer.

Context: {context}
Question: {question}
Answer:\"\"\",
    input_variables=["context", "question"]
)

# Chain-of-thought
cot = PromptTemplate(
    template=\"\"\"Answer the question based on the context.

Step 1: Identify relevant information in the context.
Step 2: Reason through the information.
Step 3: Provide your answer.

Context: {context}
Question: {question}
Answer:\"\"\",
    input_variables=["context", "question"]
)
```

**Evaluate:** Which prompt produces the most accurate and grounded answers?

---

## Bonus: Build a RAG Chatbot

Build an interactive RAG chatbot with a chat history.

**Requirements:**

1. Accept user input in a loop
2. Maintain conversation history (last 5 exchanges)
3. Include conversation history in the prompt for context-aware answers
4. Display retrieved sources alongside answers
5. Handle graceful exit

**Skeleton:**

```python
from langchain_core.messages import HumanMessage, AIMessage

chat_history = []

def chat(question):
    # Format chat history
    history_str = "\\n".join(
        f"{'Human' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
        for m in chat_history[-10:]
    )
    
    # RAG with history
    prompt_with_history = f\"\"\"Chat history:
{history_str}

Context: {context}

Question: {question}
Answer:\"\"\"
    
    # Get answer, update history
    # ...
    pass

# Interactive loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    response = chat(user_input)
    print(f"Bot: {response}")
```

**Stretch goals:**
- Add a `/sources` command to show what documents were retrieved
- Add a `/clear` command to reset history
- Stream responses token by token
- Add a simple Gradio or Streamlit UI

---

## Submission Checklist

- [ ] Part 1: RAG pipeline returns grounded answers
- [ ] Part 2: Chunk size comparison with analysis
- [ ] Part 3: Metadata filtering works correctly
- [ ] Part 4: Prompt comparison with evaluation
- [ ] Bonus: Interactive chatbot (if attempted)
