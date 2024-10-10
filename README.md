## Customer Review Analysis & Retrieval-Augmented Generation (RAG) Pipeline
## Project Overview
This project demonstrates a proof-of-concept for analyzing customer review data and building a diagram for Retrieval-Augmented Generation pipeline to generate context-aware, high-quality responses for customer support. 

## Main Tasks:

### 1 – Data Advisory
This exercise is based on a sample of Amazon customer reviews. You should aim to spend around 3-4
hours on it. We are interested in your abilities as a Data Scientist as well as understanding how you
consider the business context in your work.
1.1 – Description of Dataset
You can find here a sample of customer reviews of health and personal care products. It contains the
following fields:
1. rating – the review rating (from 1 to 5)
2. title – the headline title
3. text – the review body text
4. images – product images (empty list)
5. asin – Amazon Standard Identification Number
6. parent_asin – the parent Amazon Standard Identification Number
7. user_id – a unique identifier for the customer
8. timestamp - the date on which the review was left
9. helpful_vote – the number of times the review has been “upvoted” by other users
10. verified_purchase – information about whether the user bought the product or not
1.2 – Description of Task
Scenario: Amazon is committed to improving its products catalogue and services by leveraging
customer feedback. The company has amassed a large dataset of customer reviews, which includes
information on review text, ratings, creation dates, and more. The management team wants to gain
insights into the main topics discussed in these reviews and to understand the overall trends to
improve their products and take strategic decisions.
You have been asked to identify trending topics in the reviews and analyze what these trends might
reveal about the company’s business. Collaborating with a cross-functional team, you are developing
a data-driven model to extract and summarize themes in review text. The goal is to identify key
topics and trends within the reviews and summarize the findings in a way that is accessible and
actionable for relevant stakeholders, by
- Creating a brief project plan to meet the requirements. Consider potential business
development opportunities.
- Implementing a POC model
o Analyzing and summarizing the main characteristics of the data
o Selecting and applying a model to identify topics and trends within the review text
o Identifying an output that may be of interest to stakeholders
- Summarizing the results of the analysis in an engaging way suitable for stakeholders

### 2 – Retrieval-Augmented Generation (RAG)
This exercise is a starting point for a discussion about GenAI. You should aim to spend around 1-2
hours on this task as it is not an implementation exercise.
2.1 – Description of Task
Your task is to outline a design of the key components of a RAG pipeline that can be used to improve
the quality and relevance of responses in customer support interactions. The focus of this exercise is
on your understanding of the architecture, components, and workflow rather than on the actual
implementation.
You can use some of the following discussion points as help:
- Overall architecture of a RAG pipeline.
- The interaction between retrieval and generation components.
- Query processing steps (e.g. tokenization).
- Choice of generative model (e.g. GPT-4, Llama 3).
- Challenges, considerations, and evaluation metrics.
- Potential improvements and future enhancements for a RAG pipeline.
- Ethical implications of using GenAI in customer interactions.
