class QueryGenerator:

    def __init__(self):
        pass

    def generate(self, refined_scope):

        scope = refined_scope["scope"]

        topic = scope["topic"]
        domain = scope["domain"]
        year = scope["year"]

        queries = []

        if domain:

            queries.append(
                f"{domain} {topic}"
            )

        if domain and year:

            queries.append(
                f"{domain} {topic} {year}"
            )

            queries.append(
                f"{domain} {topic} rules {year}"
            )

            queries.append(
                f"{domain} {topic} syllabus {year}"
            )

            queries.append(
                f"{domain} {topic} study guide {year}"
            )

            queries.append(
                f"{domain} {topic} wiki"
            )

            queries.append(
                f"{domain} {topic} practice test {year}"
            )

        return list(set(queries))


if __name__ == "__main__":

    from scope.scope_builder import ScopeBuilder
    from scope.scope_refiner import ScopeRefiner

    builder = ScopeBuilder()
    refiner = ScopeRefiner()

    scope = builder.build_scope(
        "Science Olympiad Solar System 2026"
    )

    refined = refiner.refine(scope)

    generator = QueryGenerator()

    queries = generator.generate(refined)

    for q in queries:
        print(q)