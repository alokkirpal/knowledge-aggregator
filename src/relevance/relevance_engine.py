class RelevanceEngine:

    def score(
        self,
        chunk,
        refined_scope
    ):

        text = chunk.lower()

        score = 0

        for keyword in refined_scope["must_include"]:

            if keyword.lower() in text:
                score += 10

        for keyword in refined_scope["must_exclude"]:

            if keyword.lower() in text:
                score -= 10

        return score