from tables import IsDescription, Float32Col, UInt32Col


def pytable_hit_class(padding_size, is_coincidence):
    if is_coincidence:
        nb_features = 8
    else:
        nb_features = 4

    class Hits(IsDescription):
        hits = Float32Col([padding_size, nb_features])
        first_hit_index = UInt32Col()
        padded_size = UInt32Col()
    return Hits
