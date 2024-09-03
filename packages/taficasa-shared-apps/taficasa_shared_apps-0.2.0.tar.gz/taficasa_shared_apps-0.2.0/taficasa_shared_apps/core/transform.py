from typing import Any, Dict, List


def transform_list(data: List, id_field: str) -> Dict[str, Any]:
    """
    This function takes a list of objects and transforms them into
    objects where the key is the id (noted by the id_field) and the
    value is the object
    """

    transformed_data = {}
    for entity in data:
        entity_id = entity[id_field]
        transformed_data[entity_id] = entity
    return transformed_data
