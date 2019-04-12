def log_error_on_duplicates(ordered_pairs):
    current_dict = {}
    for key, value in ordered_pairs:
        if key in current_dict:
            print("duplicate key: %r" % (key,))
        else:
            current_dict[key] = value
    return current_dict
