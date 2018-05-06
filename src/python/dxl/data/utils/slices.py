def slices_from_ranges(ranges):
    pass


def _parse_single_str_slice(s):
    if ':' in s:
        splitted = s.split(':')
        splitted = [None if s == '' else int(s) for s in splitted]
        return slice(*splitted)
    else:
        return int(s)


def slices_from_str(slices_str: str):
    slices = slices_str[1:-1].split(',')
    return tuple(map(_parse_single_str_slice, slices))


__all__ = ['slices_from_ranges', 'slices_from_str']