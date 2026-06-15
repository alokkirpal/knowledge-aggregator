from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class KnowledgeStoreState:
    """
    Shared state object that flows through the entire
    knowledge store generation pipeline.
    """

    # ==========================
    # User Input
    # ==========================

    user_query: str = ""

    # ==========================
    # Scope
    # ==========================

    scope: Dict[str, Any] = field(default_factory=dict)

    refined_scope: Dict[str, Any] = field(default_factory=dict)

    search_queries: List[str] = field(default_factory=list)

    # ==========================
    # Crawling
    # ==========================

    source_urls: List[str] = field(default_factory=list)

    documents: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================
    # Processing
    # ==========================

    chunks: List[Dict[str, Any]] = field(default_factory=list)

    relevant_chunks: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================
    # Topics
    # ==========================

    candidate_topics: List[Dict[str, Any]] = field(default_factory=list)

    canonical_topics: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================
    # Hierarchy
    # ==========================

    hierarchy: Dict[str, Any] = field(default_factory=dict)

    # ==========================
    # Knowledge Graph
    # ==========================

    knowledge_graph: Dict[str, Any] = field(default_factory=dict)

    # ==========================
    # Learning Path
    # ==========================

    learning_path: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================
    # Metadata
    # ==========================

    metadata: Dict[str, Any] = field(default_factory=dict)

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    # ==========================
    # Utility Methods
    # ==========================

    def add_error(self, message: str):
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings.append(message)

    def update_metadata(self, key: str, value: Any):
        self.metadata[key] = value

    def summary(self):

        return {
            "user_query": self.user_query,
            "num_search_queries": len(self.search_queries),
            "num_sources": len(self.source_urls),
            "num_documents": len(self.documents),
            "num_chunks": len(self.chunks),
            "num_relevant_chunks": len(self.relevant_chunks),
            "num_candidate_topics": len(self.candidate_topics),
            "num_canonical_topics": len(self.canonical_topics),
            "has_hierarchy": bool(self.hierarchy),
            "has_knowledge_graph": bool(self.knowledge_graph),
            "num_learning_steps": len(self.learning_path),
            "num_errors": len(self.errors),
            "num_warnings": len(self.warnings)
        }