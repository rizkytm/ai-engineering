# Module 10 Resources: Prompt Engineering

## Official Guides

- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) — Comprehensive guide covering techniques, strategies, and best practices
- [Google Gemini Prompting Guide](https://ai.google.dev/docs/prompt_best_practices) — Gemini-specific prompt engineering recommendations
- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — Claude-focused techniques with practical examples
- [AWS Bedrock Prompt Engineering](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-engineering.html) — Enterprise prompt patterns for Bedrock models

## Research Papers

- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) — Wei et al., 2022. Foundational paper on CoT reasoning.
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — Brown et al., 2020. The GPT-3 paper demonstrating in-context learning.
- [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/abs/2205.11916) — Kojima et al., 2022. "Let's think step by step" paper.
- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) — Bai et al., 2022. System prompts for alignment.
- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401) — Lewis et al., 2020. Combining prompts with retrieval.
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) — Wang et al., 2023. Voting-based CoT improvement.

## Prompt Engineering Frameworks

- [LangChain Prompts](https://python.langchain.com/docs/concepts/prompt-templates/) — Prompt template library and composition tools
- [DSPy](https://dspy.ai/) — Programming framework for prompt optimization
- [PromptFlow (Azure)](https://learn.microsoft.com/en-us/azure/ai-studio/how-to-flow-build) — Visual prompt flow builder
- [Guardrails AI](https://www.guardrailsai.com/) — Output validation and guardrails for LLM prompts

## Tools and Utilities

- [PromptPerfect](https://promptperfect.jina.ai/) — AI-powered prompt optimization
- [LangSmith](https://smith.langchain.com/) — Prompt testing, evaluation, and monitoring
- [PromptLayer](https://www.promptlayer.com/) — Prompt versioning and analytics
- [Humanloop](https://humanloop.com/) — Prompt management platform for teams

## Tutorials and Courses

- [DeepLearning.AI: ChatGPT Prompt Engineering for Developers](https://www.deeplearning.ai/short-courses/chatgpt-prompt-engineering-for-developers/) — Free short course with Andrew Ng
- [Anthropic's Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — Jupyter notebook tutorial
- [Google's Prompt Design Strategies](https://ai.google.dev/docs/prompt_best_practices) — Best practices from Google

## Blog Posts and Articles

- [OpenAI: Techniques to Improve Reliability](https://platform.openai.com/docs/guides/prompt-engineering/strategy-improve-reliability) — Practical strategies for production prompts
- [Anthropic: Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Comprehensive overview of techniques
- [Chip Huyen: Prompt Engineering Guide](https://huyenchip.com/2023/03/15/prompt-engineering.html) — Technical deep dive
- [Lilian Weng: Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — Research-oriented overview

## Community Resources

- [Awesome ChatGPT Prompts](https://github.com/f/awesome-chatgpt-prompts) — Curated prompt templates
- [r/PromptEngineering](https://www.reddit.com/r/PromptEngineering/) — Reddit community
- [Prompt Engineering Guide (DAIR.AI)](https://www.promptingguide.ai/) — Open-source guide covering all major techniques

## Key Concepts Cheat Sheet

| Technique | When to Use | Token Cost | Accuracy |
|-----------|------------|------------|----------|
| Zero-shot | Simple tasks | Low | Medium |
| Few-shot | Complex format/domain | Medium | High |
| Chain-of-thought | Reasoning tasks | High | High |
| CoT + Few-shot | Complex + specific format | Very High | Very High |
| Self-consistency | Critical decisions | Very High | Highest |
| Tree-of-thought | Multi-path reasoning | Very High | High |

## Temperature Reference

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| 0.0 | Deterministic | Extraction, classification, code |
| 0.1-0.3 | Very consistent | Summarization, structured output |
| 0.4-0.7 | Balanced | General conversation, Q&A |
| 0.8-1.0 | Creative | Brainstorming, creative writing |
| 1.0+ | Very random | Diversity sampling |
