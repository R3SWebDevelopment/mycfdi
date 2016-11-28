def collapse_white_spaces(value=None):
    value_retorned = None
    if value is not None and value.__class__ is str and value.strip():
        value_retorned = value.strip()
    return value_retorned