import re


class ScopeBuilder:

    def __init__(self):
        pass

    def build(self, user_query):

        normalized = user_query.lower().strip()

        tokens = re.findall(
            r"[A-Za-z0-9]+",
            normalized
        )

        return {

            "raw_query": user_query,

            "normalized_query": normalized,

            "tokens": tokens

        }


if __name__ == "__main__":

    builder = ScopeBuilder()

    print(

        builder.build(

            "Science Olympiad Solar System 2026"

        )

    )