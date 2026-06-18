# Module 18: Resources — AI Ethics, Safety & Model Strategy

---

## AI Ethics Frameworks and Guidelines

- **EU AI Act** — [https://artificialintelligenceact.eu/](https://artificialintelligenceact.eu/)
  - The most comprehensive AI regulation globally, risk-based classification system
- **NIST AI Risk Management Framework** — [https://www.nist.gov/artificialintelligence/risk-management-framework](https://www.nist.gov/artificialintelligence/risk-management-framework)
  - US voluntary framework for managing AI risks
- **OECD AI Principles** — [https://www.oecd.org/en/topics/sub-issues/responsible-artificial-intelligence.html](https://www.oecd.org/en/topics/sub-issues/responsible-artificial-intelligence.html)
  - International principles for trustworthy AI
- **UNESCO Recommendation on AI Ethics** — [https://www.unesco.org/en/artificialintelligence/ethics](https://www.unesco.org/en/artificialintelligence/ethics)
  - Global normative framework for AI ethics
- **Asilomar AI Principles** — [https://futureoflife.org/ai-principles/](https://futureoflife.org/ai-principles/)
  - 23 principles developed by AI researchers
- **ISO/IEC 42001** — AI management system standard
  - International standard for responsible AI management

---

## Prompt Injection and Security Research

- **OWASP Top 10 for LLM Applications** — [https://owasp.org/www-project-top-10-for-large-language-model-applications/](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
  - Comprehensive threat taxonomy for LLM-based applications
- **Prompt Injection Explained (Simon Willison)** — [https://simonwillison.net/2023/Apr/14/worst-that-can-happen/](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/)
  - Authoritative primer on prompt injection attacks
- **Not All Downloads Are Equal (Prompt Injection via Indirect Methods)** — [https://arxiv.org/abs/2302.12173](https://arxiv.org/abs/2302.12173)
  - Research paper on indirect prompt injection
- **Jailbreaking with Code (MIT)** — [https://arxiv.org/abs/2308.01825](https://arxiv.org/abs/2308.01825)
  - Research on adversarial attacks on code generation models
- **Garak: LLM Vulnerability Scanner** — [https://github.com/leondz/garak](https://github.com/leondz/garak)
  - Automated red-teaming for LLMs
- **PyRIT: PyRIT (Python Risk Identification Tool)** — [https://github.com/Azure/PyRIT](https://github.com/Azure/PyRIT)
  - Microsoft's tool for identifying generative AI risks

---

## Bias Detection and Fairness

- **AI Fairness 360 (IBM)** — [https://github.com/Trusted-AI/AIF360](https://github.com/Trusted-AI/AIF360)
  - Comprehensive toolkit for detecting and mitigating bias
- **Fairlearn (Microsoft)** — [https://github.com/fairlearn/fairlearn](https://github.com/fairlearn/fairlearn)
  - Toolkit for assessing and improving fairness of ML models
- **What-If Tool (Google)** — [https://pair-code.github.io/what-if-tool/](https://pair-code.github.io/what-if-tool/)
  - Interactive visual tool for exploring ML model behavior
- **Datasheets for Datasets** — [https://arxiv.org/abs/1803.09010](https://arxiv.org/abs/1803.09010)
  - Framework for documenting datasets
- **Model Cards for Model Reporting** — [https://arxiv.org/abs/1802.08137](https://arxiv.org/abs/1802.08137)
  - Framework for documenting model capabilities and limitations
- **The Hateful Memes Challenge (Facebook AI)** — [https://ai.meta.com/datasets/hateful-memes/](https://ai.meta.com/datasets/hateful-memes/)
  - Benchmark for multimodal hate detection

---

## Guardrails and Safety Tools

- **Guardrails AI** — [https://github.com/guardrails-ai/guardrails](https://github.com/guardrails-ai/guardrails)
  - Framework for validating and verifying LLM outputs
- **NeMo Guardrails (NVIDIA)** — [https://github.com/NVIDIA/NeMo-Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
  - Toolkit for adding programmable guardrails to LLM apps
- **LangChain Guardrails** — [https://python.langchain.com/docs/guides/safety/](https://python.langchain.com/docs/guides/safety/)
  - Built-in safety features in LangChain
- **Lakera Guard** — [https://www.lakera.ai/](https://www.lakera.ai/)
  - Real-time injection detection and content filtering
- **Rebuff: Prompt Injection Detector** — [https://github.com/rebuff/rebuff](https://github.com/rebuff/rebuff)
  - Self-hardening prompt injection detector
- **LLM Guard** — [https://github.com/protectai/llm-guard](https://github.com/protectai/llm-guard)
  - Toolkit for securing LLM interactions (Prompt Security)
- **Azure AI Content Safety** — [https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety](https://azure.microsoft.com/en-us/products/ai-services/ai-content-safety)
  - Microsoft's content moderation service

---

## Grounding and Hallucination

- **Chain-of-Verification (CoVe)** — [https://arxiv.org/abs/2309.11495](https://arxiv.org/abs/2309.11495)
  - Method for reducing hallucination through self-verification
- **Self-RAG** — [https://arxiv.org/abs/2310.11511](https://arxiv.org/abs/2310.11511)
  - Self-reflective RAG framework
- **FActScore** — [https://arxiv.org/abs/2305.14251](https://arxiv.org/abs/2305.14251)
  - Fine-grained atomic fact evaluation for long-form text
- **RAGAS** — [https://github.com/explodinggradients/ragas](https://github.com/explodinggradients/ragas)
  - Framework for evaluating RAG pipelines
- **Vectara Hallucination Leaderboard** — [https://github.com/vectara/hallucination-leaderboard](https://github.com/vectara/hallucination-leaderboard)
  - Benchmark comparing LLM hallucination rates
- **Grounding with Google Search** — [https://ai.google.dev/gemini-api/docs/grounding](https://ai.google.dev/gemini-api/docs/grounding)
  - Google's grounding API for OpenAI models

---

## Privacy and Compliance

- **NIST Privacy Framework** — [https://www.nist.gov/privacy-framework](https://www.nist.gov/privacy-framework)
  - Risk-based approach to privacy management
- **GDPR Compliance Guide (ICO)** — [https://ico.org.uk/for-organisations/direct-marking-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/](https://ico.org.uk/for-organisations/direct-marking-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/)
  - UK Information Commissioner's Office guidance
- **HIPAA for AI Systems** — [https://www.hhs.gov/hipaa/](https://www.hhs.gov/hipaa/)
  - US health data protection requirements
- **Privacy-Enhancing Technologies (PETs)** — [https://www.nist.gov/itl/applied-cryptography/privacy-enhancing-technologies-pets](https://www.nist.gov/itl/applied-cryptography/privacy-enhancing-technologies-pets)
  - NIST overview of PETs for AI systems
- **Differential Privacy** — [https://en.wikipedia.org/wiki/Differential_privacy](https://en.wikipedia.org/wiki/Differential_privacy)
  - Mathematical framework for privacy guarantees

---

## Open-Source Models and Self-Hosting

- **Hugging Face Model Hub** — [https://huggingface.co/models](https://huggingface.co/models)
  - Repository of open-source models
- **vLLM** — [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
  - High-throughput serving for LLMs
- **Ollama** — [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
  - Run LLMs locally with simple CLI
- **llama.cpp** — [https://github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp)
  - Efficient inference for LLaMA models in C++
- **Text Generation Inference (Hugging Face)** — [https://github.com/huggingface/text-generation-inference](https://github.com/huggingface/text-generation-inference)
  - Production-grade inference server
- **LocalAI** — [https://github.com/mudler/LocalAI](https://github.com/mudler/LocalAI)
  - Drop-in OpenAI API replacement for local models

---

## Responsible AI Development

- **Google's Responsible AI Practices** — [https://ai.google/responsibility/responsible-ai-practices/](https://ai.google/responsibility/responsible-ai-practices/)
  - Practical guidelines from Google
- **Microsoft Responsible AI Standard** — [https://learn.microsoft.com/en-us/ai/responsible-ai/](https://learn.microsoft.com/en-us/ai/responsible-ai/)
  - Microsoft's framework for responsible AI
- **Anthropic's Core Views on AI Safety** — [https://www.anthropic.com/research#702-core-views-on-ai-safety](https://www.anthropic.com/research#702-core-views-on-ai-safety)
  - Anthropic's approach to AI safety
- **OpenAI Safety Documentation** — [https://platform.openai.com/docs/guides/safety-best-practices](https://platform.openai.com/docs/guides/safety-best-practices)
  - Best practices from OpenAI
- **Responsible AI Course (Google)** — [https://www.coursera.org/learn/responsible-ai](https://www.coursera.org/learn/responsible-ai)
  - Free course on responsible AI development
- **AI Ethics: Global Perspectives (edX)** — [https://www.edx.org/learn/ai-ethics](https://www.edx.org/learn/ai-ethics)
  - Academic course on AI ethics across cultures

---

## Research Papers

- **On the Dangers of Stochastic Parrots (Bender et al., 2021)** — [https://dl.acm.org/doi/10.1145/3442188.3445922](https://dl.acm.org/doi/10.1145/3442188.3445922)
  - Foundational paper on risks of large language models
- **Do the Rewards Justify the Means? (Bostrom & Yudkowsky, 2014)** — [https://nickbostrom.com/ethics/aiethics.pdf](https://nickbostrom.com/ethics/aiethics.pdf)
  - Classic work on AI ethics and existential risk
- **Concrete Problems in AI Safety (Amodei et al., 2016)** — [https://arxiv.org/abs/1606.06565](https://arxiv.org/abs/1606.06565)
  - Practical AI safety research agenda
- **Scaling Laws for Neural Language Models (Kaplan et al., 2020)** — [https://arxiv.org/abs/2001.08361](https://arxiv.org/abs/2001.08361)
  - Understanding scaling implications for safety
- **Constitutional AI (Anthropic, 2022)** — [https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)
  - Training AI systems to be helpful, harmless, and honest
- **Sleeper Agents (Anthropic, 2024)** — [https://arxiv.org/abs/2401.05566](https://arxiv.org/abs/2401.05566)
  - Research on deceptive AI behavior and detection

---

## Tools and Libraries Summary

| Tool | Purpose | Link |
|------|---------|------|
| Guardrails AI | Output validation | [GitHub](https://github.com/guardrails-ai/guardrails) |
| NeMo Guardrails | Programmable safety | [GitHub](https://github.com/NVIDIA/NeMo-Guardrails) |
| AIF360 | Bias detection | [GitHub](https://github.com/Trusted-AI/AIF360) |
| Fairlearn | Fairness assessment | [GitHub](https://github.com/fairlearn/fairlearn) |
| Garak | LLM vulnerability scanning | [GitHub](https://github.com/leondz/garak) |
| PyRIT | Risk identification | [GitHub](https://github.com/Azure/PyRIT) |
| LLM Guard | Security toolkit | [GitHub](https://github.com/protectai/llm-guard) |
| RAGAS | RAG evaluation | [GitHub](https://github.com/explodinggradients/ragas) |
| vLLM | Model serving | [GitHub](https://github.com/vllm-project/vllm) |
| Rebuff | Injection detection | [GitHub](https://github.com/rebuff/rebuff) |
