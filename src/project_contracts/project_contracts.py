from contracts import new_contract


new_contract("non_empty_iterable", lambda iterable: len(iterable) > 0)
