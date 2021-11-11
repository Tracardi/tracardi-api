import typing


def cast(list_of: list, type: typing.Type, return_original=False):
    for item in list_of:
        if return_original is True:
            yield type(**item), item
        else:
            yield type(**item)
