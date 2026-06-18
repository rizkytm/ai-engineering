# Exercise 01: AI System Design Practice

## Overview

Apply the system design concepts from this module through hands-on design exercises. Each part builds on the previous one, culminating in a complete system design.

**Time Estimate**: 3-4 hours

---

## Part 1: Design an AI System (45 minutes)

### Scenario

A healthcare startup wants to build an AI system that analyzes medical images (X-rays, MRIs) to assist radiologists in detecting abnormalities. The system must:
- Process images uploaded by hospitals
- Provide preliminary analysis within 60 seconds
- Achieve >95% sensitivity (catching true positives)
- Comply with HIPAA regulations
- Integrate with existing PACS (Picture Archiving and Communication System)

### Tasks

**Task 1.1: Requirements Gathering (15 min)**

Complete the following template:

```markdown
## Functional Requirements
1. 
2. 
3. 

## Non-Functional Requirements
- Latency: 
- Throughput: 
- Accuracy: 
- Security: 
- Compliance: 

## Constraints
- Budget: 
- Timeline: 
- Team: 
- Regulatory: 
```

**Task 1.2: Component Identification (15 min)**

List all major components needed. For each component, specify:
- Purpose
- Input/Output
- Technology choice (with justification)

**Task 1.3: Architecture Diagram (15 min)**

Create a Mermaid diagram showing:
- System context (external actors)
- Component relationships
- Data flow

---

## Part 2: Architecture Diagrams (60 minutes)

Create architecture diagrams for three different products. Each should include a component diagram and a data flow diagram.

### Product 1: AI-Powered Content Moderation Platform

**Requirements:**
- Process user-generated content (text, images, video)
- Flag inappropriate content in < 5 seconds
- Handle 10,000 content items per minute
- Provide explanations for moderation decisions
- Support appeals process

**Deliverables:**
- Component diagram
- Data flow diagram
- Key trade-offs identified

### Product 2: Personalized Learning Platform

**Requirements:**
- Recommend learning paths based on student performance
- Adapt difficulty in real-time
- Track learning progress across subjects
- Support 100,000 concurrent students
- Generate practice problems tailored to weak areas

**Deliverables:**
- Component diagram
- Data flow diagram
- Key trade-offs identified

### Product 3: Fraud Detection System

**Requirements:**
- Analyze transactions in real-time (< 100ms)
- Detect fraudulent patterns across millions of transactions
- Reduce false positives to < 1%
- Explain why transactions are flagged
- Adapt to new fraud patterns quickly

**Deliverables:**
- Component diagram
- Data flow diagram
- Key trade-offs identified

---

## Part 3: Trade-off Analysis (45 minutes)

### Scenario

You are designing the AI model serving layer for a customer service chatbot. You need to choose between three options:

| Option | Description |
|--------|-------------|
| **A: OpenAI GPT-4 API** | Use GPT-4 via API |
| **B: Self-hosted Llama 2 70B** | Run Llama 2 70B on your own GPU infrastructure |
| **C: Fine-tuned Llama 2 13B** | Fine-tune a smaller Llama 2 model on your data |

### Tasks

**Task 3.1: Build a Trade-off Matrix (20 min)**

Score each option (1-5) across these dimensions:
- Accuracy/Quality
- Latency
- Cost at 1M queries/month
- Cost at 10M queries/month
- Security/Privacy
- Maintenance effort
- Customization potential
- Time to deploy

**Task 3.2: Weighted Scoring (15 min)**

Assign weights to each dimension based on these priorities:
- The system handles sensitive customer data
- Budget is $5,000/month
- Team has 2 ML engineers
- Need to launch within 4 weeks
- Accuracy is important but not critical

Calculate weighted scores and determine the winner.

**Task 3.3: Cost Projection (10 min)**

Estimate monthly costs for each option at:
- 100K queries/month
- 1M queries/month
- 10M queries/month

Show your calculations.

---

## Part 4: Peer Review (30 minutes)

### Instructions

Exchange your Part 1 and Part 2 designs with a classmate. Use the following checklist to review their work:

### Review Checklist

```markdown
## Design Review Form

### Designer: _______________
### Reviewer: _______________

### Requirements Coverage
- [ ] All functional requirements addressed
- [ ] Non-functional requirements specified
- [ ] Constraints acknowledged

### Architecture Quality
- [ ] Components are well-defined
- [ ] Responsibilities are clear
- [ ] Interfaces are specified
- [ ] No missing critical components

### Data Flow
- [ ] Data flow is logical
- [ ] Error handling is considered
- [ ] Edge cases are addressed

### Trade-offs
- [ ] Trade-offs are explicitly identified
- [ ] Rationale is provided
- [ ] Alternatives are considered

### Completeness
- [ ] Diagrams are readable
- [ ] Technology choices are justified
- [ ] Cost/scale considerations are present

### Suggestions
1. [Suggestion for improvement]
2. [Suggestion for improvement]
3. [Suggestion for improvement]

### Strengths
1. [What was done well]
2. [What was done well]
```

### Discussion

After reviewing, discuss:
1. What did you learn from seeing a different approach?
2. What aspects of your design would you change based on feedback?
3. What was the most challenging part of the design process?

---

## Bonus: Complete System Design (60 minutes)

### Scenario

Design a complete AI system for **real-time sports commentary generation**.

**Context:**
- A sports media company wants AI-generated play-by-play commentary for live games
- Must support multiple sports (football, basketball, soccer)
- Commentary should be engaging and accurate
- System must handle multiple simultaneous games
- Integrate with live data feeds (play-by-play APIs, player stats)
- Output: Text commentary for web/app, audio for streaming

**Requirements:**
- Latency: Commentary within 2 seconds of each play
- Accuracy: No factual errors in player names, stats, scores
- Style: Varies by sport (energetic for basketball, analytical for football)
- Scale: 100 concurrent games during peak times
- Personalization: Fan可以选择不同风格的解说

### Deliverables

1. **Complete architecture document** including:
   - Problem statement and requirements
   - System context diagram
   - Component diagram with descriptions
   - Data flow diagram
   - Data storage requirements
   - Model selection strategy

2. **Trade-off analysis** for:
   - Real-time vs batch processing
   - Template-based vs LLM-generated commentary
   - Self-hosted vs API models
   - Cost vs quality decisions

3. **Risk assessment** identifying:
   - 5+ risks with likelihood and impact scores
   - Mitigation strategies for high-risk items
   - Fallback mechanisms

4. **Cost estimate** for:
   - MVP (10 concurrent games)
   - Production (100 concurrent games)
   - Scale (1000 concurrent games)

---

## Submission

Submit your work as a single document or repository containing:
1. Part 1: Healthcare AI system design
2. Part 2: Three architecture diagrams with trade-offs
3. Part 3: Trade-off analysis with calculations
4. Part 4: Peer review feedback (received)
5. Bonus: Complete sports commentary system (if attempted)

---

## Grading Rubric

| Criteria | Excellent (5) | Good (4) | Satisfactory (3) | Needs Work (2) | Incomplete (1) |
|----------|---------------|----------|-------------------|----------------|----------------|
| **Requirements** | Comprehensive, well-structured | Clear, mostly complete | Basic requirements identified | Missing key requirements | Minimal effort |
| **Architecture** | Clear, scalable, well-justified | Good structure, minor gaps | Functional but limited | Missing components | Incomplete |
| **Trade-offs** | Thorough analysis, weighted scoring | Good analysis, some quantification | Basic comparison | Trade-offs not explicit | Missing |
| **Diagrams** | Professional, complete, readable | Clear, mostly complete | Basic but functional | Hard to read | Missing |
| **Cost Analysis** | Detailed, realistic estimates | Good estimates with assumptions | Basic estimates | Unrealistic or missing | Missing |
| **Risk Assessment** | Comprehensive, quantified | Good identification, some mitigation | Basic risks identified | Missing mitigation | Missing |
