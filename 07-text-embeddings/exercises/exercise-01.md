# Exercise 01: Text Embeddings Practice

## Part 1: Generate and Visualize Embeddings (20 min)

Using the OpenAI Embeddings API, complete the following tasks:

1. **Custom dataset**: Create a list of 15 sentences across 5 different topics (3 sentences per topic).

2. **Generate embeddings**: Use `genai.embed_content` to generate embeddings for all sentences.

3. **Visualize with PCA**: Use `sklearn.decomposition.PCA` to project embeddings to 2D. Create a scatter plot where each topic is a different color.

4. **Analysis**: 
   - Do sentences from the same topic cluster together?
   - Which topics are closest to each other in embedding space?
   - Which topics are furthest apart?

5. **t-SNE comparison**: Repeat the visualization using t-SNE. Does it produce better cluster separation than PCA?

## Part 2: Document Similarity Finder (25 min)

Build a complete document similarity system:

1. **Create a knowledge base**: Write 20+ short documents (1-2 sentences each) covering technical topics (e.g., Python errors, web frameworks, database concepts).

2. **Implement similarity search**: Create a function that:
   - Takes a query as input
   - Generates an embedding for the query
   - Computes cosine similarity with all documents
   - Returns the top 5 most similar documents

3. **Test with 10 queries**: 
   - 3 queries that should match well
   - 3 queries that should partially match
   - 4 queries with no good matches
   
4. **Precision analysis**: For the first 5 queries, count how many of the top 5 results are actually relevant. Calculate precision@5.

5. **Improve results**: Try these techniques and measure if precision improves:
   - Use `task_type="RETRIEVAL_QUERY"` for query embeddings
   - Use `task_type="RETRIEVAL_DOCUMENT"` for document embeddings
   - Change the number of results (top_k)

## Part 3: Embedding Quality Comparison (20 min)

Compare embedding quality across models:

1. **Install models**: Ensure `sentence-transformers` is installed with `all-MiniLM-L6-v2` and `all-mpnet-base-v2`.

2. **Create evaluation pairs**: Write 15 sentence pairs with expected similarity levels:
   - 5 pairs with high expected similarity
   - 5 pairs with medium expected similarity
   - 5 pairs with low expected similarity

3. **Compute similarities**: For each pair, compute cosine similarity using:
   - OpenAI text-embedding-3-small
   - MiniLM-L6-v2
   - MPNet-base-v2

4. **Compare accuracy**: 
   - Which model best distinguishes high from low similarity?
   - Which model has the most consistent rankings?
   - Create a table showing the results.

5. **Speed benchmark**: Time how long each model takes to embed 100 sentences. Which is fastest?

## Bonus: Simple Recommendation System (15 min)

Build a recommendation engine:

1. **Create a catalog**: Write 20+ "items" (articles, products, or courses) with short descriptions.

2. **Build recommendation function**: Given an item, recommend the 3 most similar items.

3. **Test recommendations**: 
   - Pick 5 items and get recommendations for each
   - Do the recommendations make sense?
   - Are there any surprising recommendations?

4. **Evaluate**: Rate each recommendation as "relevant", "partially relevant", or "not relevant". Calculate overall relevance rate.

---

## Submission

Save your code and analysis in this folder. Include:
- Your notebook(s) with all code
- A brief summary of your findings (1-2 paragraphs)
- Any interesting observations about embedding behavior
