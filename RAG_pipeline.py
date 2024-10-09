from graphviz import Digraph

dot = Digraph()

dot.attr(ranksep="1.0", nodesep="1.0")

dot.node("User Input", "User Input\n(Customer Queries)", shape="box")
dot.node(
    "Query Processing",
    "Query Processing\n(Tokenization, Intent Detection)",
    shape="box",
)
dot.node(
    "Retrieval Component",
    "Retrieval Component\n(Vector Search, Keyword Search)",
    shape="box",
)
dot.node(
    "RAG Combiner", "RAG Combiner\n(Combine Retrieved Content with Prompt)", shape="box"
)
dot.node("Generation Component", "Generation Component\n(GPT-4, LLaMA)", shape="box")
dot.node("Final Response", "Final Response\n(Generated Answer)", shape="box")
dot.node("Data Ingestion", "Data Ingestion\n(Databases, CSV, Emails)", shape="box")
dot.node(
    "Data Extraction", "Data Extraction\n(Text from Unstructured Sources)", shape="box"
)
dot.node(
    "Data Transformation", "Data Transformation\n(Splitting & Formatting)", shape="box"
)
dot.node(
    "Chunking and Embedding",
    "Chunking and Embedding\n(Convert to Vectors)",
    shape="box",
)
dot.node("Persistence", "Persistence\n(Maintain Dimension Consistency)", shape="box")
dot.node("Refreshing", "Refreshing\n(Maintain Synchronization)", shape="box")
dot.node(
    "Cloud Infrastructure", "Cloud Infrastructure\n(Deployment, Security)", shape="box"
)
dot.node(
    "Evaluation Metrics",
    "Evaluation Metrics\n(Feedback, Quality Assessment)",
    shape="box",
)

dot.edge("User Input", "Query Processing", label="  User Interaction")
dot.edge("Query Processing", "Retrieval Component", label="  Processed Query")
dot.edge("Retrieval Component", "RAG Combiner", label="  Retrieved Documents")
dot.edge("RAG Combiner", "Generation Component", label="  Combined Input")
dot.edge("Generation Component", "Final Response", label="  Generated Response")

# Adding Data Pipeline components
dot.edge("User Input", "Data Ingestion", label="  Data Ingestion")
dot.edge("Data Ingestion", "Data Extraction", label="  Source Data")
dot.edge("Data Extraction", "Data Transformation", label="  Extracted Text")
dot.edge("Data Transformation", "Chunking and Embedding", label="  Transformed Data")
dot.edge("Chunking and Embedding", "Retrieval Component", label="  Embedded Vectors")
dot.edge("Chunking and Embedding", "Persistence", label="  Maintain Vector Structure")
dot.edge("Persistence", "Refreshing", label="  Sync with Source Data")

# Adding Cloud Infrastructure
dot.edge(
    "Generation Component", "Cloud Infrastructure", label="  Deployment & Security"
)
dot.edge("Final Response", "Evaluation Metrics", label="  User Feedback")


dot.render("combined_rag_pipeline_diagram", format="png", cleanup=True)
