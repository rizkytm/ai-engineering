# Module 07: Resources & References

## Official Documentation

- [OpenAI Embeddings API](https://ai.google.dev/docs/embeddings) — Official Google documentation
- [text-embedding-004 Model Card](https://ai.google.dev/docs/models#text-embedding-004) — Model specifications and capabilities
- [OpenAI Platform](https://platform.openai.com/) — Get your OpenAI API key
- [sentence-transformers Documentation](https://www.sbert.net/) — Python library for sentence embeddings

## Pre-trained Embedding Models

| Model | Dims | Speed | Use Case |
|-------|------|-------|----------|
| [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | 384 | Fast | General-purpose, lightweight |
| [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) | 768 | Medium | Best quality-speed balance |
| [BGE-large-en](https://huggingface.co/BAAI/bge-large-en-v1.5) | 1024 | Slow | High accuracy retrieval |
| [paraphrase-multilingual-MiniLM](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 384 | Fast | Multilingual support |

## Vector Databases

- [Pinecone](https://pinecone.io/) — Managed vector database
- [Weaviate](https://weaviate.io/) — Open-source vector search
- [Qdrant](https://qdrant.tech/) — High-performance vector DB
- [FAISS](https://github.com/facebookresearch/faiss) — Facebook's similarity search library
- [ChromaDB](https://www.trychroma.com/) — Lightweight embedded vector DB

## Visualization Tools

- [TensorFlow Embedding Projector](https://projector.tensorflow.org/) — Interactive 2D/3D visualization
- [t-SNE Interactive](https://distill.pub/2016/misread-tsne/) — Understanding t-SNE
- [UMAP Documentation](https://umap-learn.readthedocs.io/) — Alternative to t-SNE

## Papers & Articles

- [Efficient Estimation of Word Representations (Word2Vec)](https://arxiv.org/abs/1301.3781) — Original Word2Vec paper
- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) — BERT paper (contextual embeddings)
- [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084) — Sentence embeddings paper
- [The Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/) — Visual explanation of embeddings
- [How to Create Custom Embeddings](https://www.pinecone.io/learn/series/ann/custom-embeddings/) — Custom embedding guide

## Tutorials & Guides

- [Gemini Embeddings Tutorial](https://ai.google.dev/docs/embeddings_quickstart) — Quick start guide
- [Sentence-Transformers Getting Started](https://www.sbert.net/docs/training/overview.html) — Training custom models
- [Understanding Embeddings (Pinecone)](https://www.pinecone.io/learn/embeddings/) — Comprehensive embeddings guide
- [FAISS Getting Started](https://github.com/facebookresearch/faiss/wiki/Getting-started) — Similarity search at scale

## Tools Mentioned

| Tool | Link | Purpose |
|------|------|---------|
| OpenAI Platform | [platform.openai.com](https://platform.openai.com) | OpenAI API key |
| sentence-transformers | [sbert.net](https://www.sbert.net) | Local embeddings |
| scikit-learn | [scikit-learn.org](https://scikit-learn.org) | PCA, t-SNE, metrics |
| FAISS | [github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss) | Fast similarity search |
| Matplotlib | [matplotlib.org](https://matplotlib.org) | Visualization |
