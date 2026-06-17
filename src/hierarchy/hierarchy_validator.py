import json


def validate_node(node):

    if not node.get("name"):
        raise ValueError("Node missing name")

    children = node.get("children", [])

    names = []

    for child in children:

        child_name = child["name"]

        if child_name in names:
            raise ValueError(
                f"Duplicate child: {child_name}"
            )

        names.append(child_name)

        validate_node(child)


def validate_hierarchy(path):

    with open(path, "r", encoding="utf-8") as f:
        hierarchy = json.load(f)

    validate_node(hierarchy)

    print("Hierarchy validation passed")


if __name__ == "__main__":

    validate_hierarchy(
        "data/output/topic_hierarchy_v1.json"
    )