from pprint import pprint

from scope.scope_builder import ScopeBuilder
from scope.scope_refiner import ScopeRefiner
from search.query_generator import QueryGenerator

from pipeline.state import KnowledgeStoreState

class KnowledgeStoreBuilder:

    def __init__(self):

        self.scope_builder = ScopeBuilder()
        self.scope_refiner = ScopeRefiner()
        self.query_generator = QueryGenerator()

    def initialize_state(self, user_query):

        return {

            "user_query": user_query,

            "scope": None,

            "refined_scope": None,

            "search_queries": [],

            "documents": [],

            "chunks": [],

            "relevant_chunks": [],

            "candidate_topics": [],

            "canonical_topics": [],

            "hierarchy": None,

            "knowledge_graph": None

        }

    def build_scope(self, state):

        state["scope"] = self.scope_builder.build_scope(
            state["user_query"]
        )

        return state

    def refine_scope(self, state):

        state["refined_scope"] = self.scope_refiner.refine(
            state["scope"]
        )

        return state

    def generate_queries(self, state):

        state["search_queries"] = self.query_generator.generate(
            state["refined_scope"]
        )

        return state

    ##################################################
    ## Future pipeline stages
    ##################################################

    def acquire_documents(self, state):

        # TODO

        return state

    def process_documents(self, state):

        # TODO

        return state

    def filter_relevance(self, state):

        # TODO

        return state

    def extract_topics(self, state):

        # TODO

        return state

    def canonicalize_topics(self, state):

        # TODO

        return state

    def generate_hierarchy(self, state):

        # TODO

        return state

    def build_graph(self, state):

        # TODO

        return state

    ##################################################

    def build(self, user_query):

        state = self.initialize_state(
            user_query
        )

        state = self.build_scope(
            state
        )

        state = self.refine_scope(
            state
        )

        state = self.generate_queries(
            state
        )

        state = self.acquire_documents(
            state
        )

        state = self.process_documents(
            state
        )

        state = self.filter_relevance(
            state
        )

        state = self.extract_topics(
            state
        )

        state = self.canonicalize_topics(
            state
        )

        state = self.generate_hierarchy(
            state
        )

        state = self.build_graph(
            state
        )

        return state


if __name__ == "__main__":

    from pipeline.state import KnowledgeStoreState

state = KnowledgeStoreState(
    user_query=user_query
)

    pprint(state)