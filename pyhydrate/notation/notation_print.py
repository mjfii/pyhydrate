from typing import Any


def notation_print(notation: Any):
    """

    :param notation:
    :return:
    """
    print('=============================================================')
    print(f"<< REPR >>\n{repr(notation)}\n")
    print(f"<< STR/YAML >>\n{notation}\n")
    print(f"<< VALUE/CALL >>\n{notation()}\n")
    print(f"<< TYPE >>\n{notation.type}\n")
    print(f"<< ELEMENT >>\n{notation.element}\n")
    print(f"<< DEPTH >>\n{notation.depth}\n")
    print(f"<< MAP >>\n{notation.map}")
    print('=============================================================')


if __name__ == '__main__':
    pass
