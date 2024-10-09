from graphviz import Digraph

# Create a new directed graph
dot = Digraph()

# Define nodes with descriptive names
dot.node("UserInput", "User Input\n(Customer Queries)")
dot.node("QueryProcessing", "Query Processing\n(Tokenization, Intent Detection)")
dot.node("RetrievalComponent", "Retrieval Component\n(Vector Search, Keyword Search)")
dot.node("RAGCombiner", "RAG Combiner\n(Combine Retrieved Content with Prompt)")
dot.node("GenerationComponent", "Generation Component\n(GPT-4, LLaMA)")
dot.node("FinalResponse", "Final Response\n(Generated Answer)")
dot.node("DataIngestion", "Data Ingestion\n(Databases, CSV, Emails)")
dot.node("Extraction", "Data Extraction\n(Text from Unstructured Sources)")
dot.node("Transformation", "Data Transformation\n(Splitting & Formatting)")
dot.node("ChunkingEmbedding", "Chunking and Embedding\n(Convert to Vectors)")
dot.node("Persistence", "Persistence\n(Maintain Dimension Consistency)")
dot.node("Refreshing", "Refreshing\n(Maintain Synchronization)")
dot.node("CloudInfrastructure", "Cloud Infrastructure\n(Deployment, Security)")
dot.node("EvaluationMetrics", "Evaluation Metrics\n(Feedback, Quality Assessment)")

# Define edges connecting the nodes
dot.edge("UserInput", "QueryProcessing", label="  User Interaction")
dot.edge("QueryProcessing", "RetrievalComponent", label="  Processed Query")
dot.edge("RetrievalComponent", "RAGCombiner", label="  Retrieved Documents")
dot.edge("RAGCombiner", "GenerationComponent", label="  Combined Input")
dot.edge("GenerationComponent", "FinalResponse", label="  Generated Response")

# Adding Data Pipeline components
dot.edge("UserInput", "DataIngestion", label="  Data Ingestion")
dot.edge("DataIngestion", "Extraction", label="  Source Data")
dot.edge("Extraction", "Transformation", label="  Extracted Text")
dot.edge("Transformation", "ChunkingEmbedding", label="  Transformed Data")
dot.edge("ChunkingEmbedding", "RetrievalComponent", label="  Embedded Vectors")
dot.edge("ChunkingEmbedding", "Persistence", label="  Maintain Vector Structure")
dot.edge("Persistence", "Refreshing", label="  Sync with Source Data")

# Adding Cloud Infrastructure
dot.edge("GenerationComponent", "CloudInfrastructure", label="  Deployment & Security")
dot.edge("FinalResponse", "EvaluationMetrics", label="  User Feedback")

dot.render("combined_rag_pipeline_diagram", format="png", cleanup=True)
