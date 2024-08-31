import time
import urllib.parse
from decimal import Decimal
from math import ceil, floor

one_billion = 1_000_000_000


def time_point_now():
    return divmod(time.time_ns(), one_billion)


def unix_timestamp_milliseconds_now():
    return int(time.time() * 1000)


def unix_timestamp_seconds_now():
    return int(time.time())


def time_point_subtract(*, time_point_1, time_point_2):
    time_point_delta = (time_point_1[0] - time_point_2[0], time_point_1[1] - time_point_2[1])
    return time_point_delta


def convert_time_point_to_unix_timestamp_seconds(*, time_point):
    return time_point[0] + time_point[1] / one_billion


def convert_time_point_delta_to_seconds(*, time_point_delta):
    return time_point_delta[0] + time_point_delta[1] / one_billion


def convert_list_to_sublists(*, input, sublist_length):
    if sublist_length:
        return [input[i * sublist_length : (i + 1) * sublist_length] for i in range((len(input) + sublist_length - 1) // sublist_length)]
    else:
        return [input]


def convert_set_to_subsets(*, input, subset_length):
    if subset_length:
        input_list = list(input)
        return [set(input_list[i * subset_length : (i + 1) * subset_length]) for i in range((len(input_list) + subset_length - 1) // subset_length)]
    else:
        return [input]


def get_base_url_from_url(*, url):
    url_splits = url.split("/")
    return f"{url_splits[0]}//{url_splits[2]}"


def convert_unix_timestamp_milliseconds_to_time_point(*, unix_timestamp_milliseconds):
    x = divmod(int(unix_timestamp_milliseconds), 1_000)
    return (x[0], x[1] * 1_000_000)


def round_to_nearest(*, input, increment, increment_as_float=None, increment_as_decimal=None):
    if increment_as_decimal is None:
        increment_as_decimal = Decimal(increment)
    return increment_as_decimal * round(round_calculate_quotient(input=input, increment=increment, increment_as_float=increment_as_float))


def round_up(*, input, increment, increment_as_float=None, increment_as_decimal=None):
    if increment_as_decimal is None:
        increment_as_decimal = Decimal(increment)
    return increment_as_decimal * ceil(round_calculate_quotient(input=input, increment=increment, increment_as_float=increment_as_float))


def round_down(*, input, increment, increment_as_float=None, increment_as_decimal=None):
    if increment_as_decimal is None:
        increment_as_decimal = Decimal(increment)
    return increment_as_decimal * floor(round_calculate_quotient(input=input, increment=increment, increment_as_float=increment_as_float))


def round_calculate_quotient(*, input, increment, increment_as_float=None):
    input_as_float = float(input)
    if increment_as_float is None:
        increment_as_float = float(increment)
    return input_as_float / increment_as_float


def create_url(*, base_url, path):
    return base_url + path


def create_path_with_query_params(*, path, query_params):
    if query_params:
        return "?".join((path, "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in sorted(dict(query_params).items())])))
    else:
        return path


def create_path_with_query_string(*, path, query_string):
    if query_string:
        return "?".join((path, query_string))
    else:
        return path


def create_url_with_query_params(*, base_url, path, query_params):
    return create_url(base_url=base_url, path=create_path_with_query_params(path=path, query_params=query_params))


def create_url_with_query_string(*, base_url, path, query_string):
    return create_url(base_url=base_url, path=create_path_with_query_string(path=path, query_string=query_string))


def remove_leading_negative_sign_in_string(*, input):
    return input[1:] if input.startswith("-") else input
