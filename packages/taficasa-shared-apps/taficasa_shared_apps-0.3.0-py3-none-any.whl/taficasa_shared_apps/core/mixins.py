from typing import List, Tuple


class ModelChoiceMixin:
    """
    This mixin is used to extend python enums so
    they can be used in model choice fields.
    """

    @classmethod
    def as_choices(cls) -> List[Tuple[int, str]]:
        return list(map(lambda c: (c.value, c.name), cls))

    def as_choice(self) -> Tuple[int, str]:
        return (self.value, self.name)

    @classmethod
    def max_name_length(cls) -> int:
        raise NotImplementedError()
