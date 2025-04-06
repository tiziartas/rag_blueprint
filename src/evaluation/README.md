# Evaluation Module

This module implements comprehensive evaluation capabilities for RAG systems, combining quality metrics assessment with observability tracking.

## Supported Evaluation Metrics

Faithfulness • Answer Relevancy • Context Precision • Context Recall • Harmfulness

## Supported Judge Embedding Models and Judge Large Language Models

Embedding models from [Embedding](/src/embedding/README.md) • LLMs from [Augmentation](/src/augmentation/README.md)


## Architecture

<div align="center">
  <img src="/res/readme/Evaluation.png" width="600">
  <p><em>Figure 1: High-level architecture evaluation process.</em></p>
</div>

### Core Components

- **Ragas Evaluator**: Evaluate RAG performance using Ragas metrics
- **Langfuse Evaluator**: Combines **Ragas Evaluator** with evaluation datasets

### Human Feedback Based Evaluation

<div align="center">
  <img src="/res/readme/Human_feedback.png" width="800">
  <p><em>Figure 2: High-level of evaluation based on human feedback.</em></p>
</div>

Integration between [Chainlit](https://chainlit.io/) and [Langfuse](https://langfuse.com/) building evaluation datasets based on the user feeback regarding the system answers. On top of that maintainers of the system can build their custom datasets e.g. manual datasets, which will help measure system's perfomance.
