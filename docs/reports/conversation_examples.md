# Conversational Intent & Routing Reference Guide

This document describes the query routing and conversational classification rules used in the ACIS GraphRAG Assistant.

---

## 🚦 Intent Routing Matrix

To optimize retrieval latency and prevent irrelevant code entities from matching conversational queries, a lightweight gatekeeper classifies incoming questions.

| Intent Category | Query Patterns / Examples | Pipeline Action | Predefined Response / Output |
| :--- | :--- | :--- | :--- |
| **Greeting** | `hi`, `hello`, `hey`, `good morning`, `good evening` | **Bypass** (Zero retrieval, zero LLM calls) | Welcomes the user and details what the GraphRAG service can answer with examples. |
| **Small Talk** | `thanks`, `thank you`, `how are you`, `who are you` | **Bypass** (Zero retrieval, zero LLM calls) | Provides friendly conversational answers. |
| **Help Request** | `help`, `examples`, `what can you do` | **Bypass** (Zero retrieval, zero LLM calls) | Lists system usage capabilities and query ideas. |
| **Code Query** | `what is BODY`, `make_vertex()`, `SPAposition` | **Retrieve** (Vector + Lexical + Graph) | Full GraphRAG response with structured evidence. |
| **Workflow Query** | `how does variable radius blending work`, `explain journaling` | **Retrieve** (Vector + Lexical + Graph) | Full GraphRAG response with structured evidence. |
| **Relationship Query** | `which classes inherit ENTITY`, `class diagram of BODY` | **Retrieve** (Vector + Lexical + Graph) | Full GraphRAG response with structured evidence. |

---

## 💬 Predefined Response Specifications

### 1. Greetings Response
When a query matches a greeting keyword, the system immediately returns:
```text
Hello! I am the ACIS GraphRAG Assistant.

I can answer questions about:

• Classes
• Methods
• Inheritance
• Call Graphs
• Parameters
• Return Types
• Modeling Workflows

Example Questions:
- What is BODY?
- What is SPAposition?
- Which classes inherit ENTITY?
- How does variable radius blending work?
```

### 2. Help Response
When a user requests help or system usage options:
```text
I am the ACIS GraphRAG Assistant, designed to help you navigate and query the ACIS geometric modeling kernel.

You can ask me questions like:
• "What is BODY?" (class definitions & attributes)
• "What is SPAposition?" (struct definitions & components)
• "Which classes inherit ENTITY?" (inheritance & hierarchy)
• "How does variable radius blending work?" (modeling workflow details)
• "How are topology changes tracked?" (procedural call tree exploration)
```

### 3. Small Talk Responses
Standard conversational answers for social queries:
- **Thank you / Thanks**: `"You're welcome! Let me know if you need help exploring the ACIS codebase."`
- **How are you**: `"I'm doing well, thank you! How can I assist you with the ACIS codebase today?"`
- **Who are you / What are you**: `"I am the ACIS GraphRAG Assistant, trained on the structure and documentation of the ACIS geometric modeling kernel."`

---

## ⚡ Mixed Query & Override Rules

A major risk in static classifiers is a false positive—mistakenly treating a technical query as a greeting because it starts with a social token. 

### 1. Codebase Keyword Override
If the input query contains any of the following terms, it is **always** classified as `retrieval`, bypassing all conversational routes:
`body`, `spaposition`, `entity`, `blend`, `blending`, `journal`, `journaling`, `inherit`, `inherits`, `class`, `method`, `function`, `struct`, `enum`, `api`, `edge`, `face`, `wire`, `lump`, `shell`, `vertex`, `topology`, `call`, `attribute`, `relationship`, `parent`, `return`, `outcome`, `spaposition_array`, `history_stream`, `acisjournal`, `attrib_var_blend`

### 2. C++ Syntax Override
If the query contains:
- `::` (scoping operator)
- `()` (method invocation parentheses)
It is routed directly to GraphRAG.

### 3. Mixed Examples:
- **"Hello, what is BODY?"**
  - Contains `hello` (greeting) and `body` (override keyword).
  - **Result:** Classified as `retrieval`.
- **"hi, explain journaling"**
  - Contains `hi` (greeting) and `journaling` (override keyword).
  - **Result:** Classified as `retrieval`.
- **"help with blending"**
  - Contains `help` (help) and `blending` (override keyword).
  - **Result:** Classified as `retrieval`.
