def entry_id(entry):
    for field in ['id', 'link']:
        ret = getattr(entry, field, None)
        if ret:
            return ret
    raise Exception('no id field found in entry: {}'.format(entry))
