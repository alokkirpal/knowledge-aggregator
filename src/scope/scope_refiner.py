class ScopeRefiner:

    def __init__(self):
        pass

    def refine(self, scope):

        refined = {

            "scope": scope,

            "goal":

                "Build a structured knowledge store",

            "focus":

                scope["raw_query"],

            "search_intent":

                f"Find authoritative resources "
                f"about {scope['raw_query']}",

            "relevance_policy":

                "Keep information directly "
                "relevant to the user query. "
                "Discard tangential information."

        }

        return refined


if __name__ == "__main__":

    from scope_builder import ScopeBuilder

    builder = ScopeBuilder()

    scope = builder.build(

        "Science Olympiad Solar System 2026"

    )

    refiner = ScopeRefiner()

    pprint(

        refiner.refine(scope)

    )