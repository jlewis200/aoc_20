#!/usr/bin/env python3


def solve(pub_key_0, pub_key_1):
    loop_size_0 = get_loop_size(pub_key_0)
    return transform(pub_key_1, loop_size_0)


def transform(pub_key, loop_size):
    value = 1

    for _ in range(loop_size):
        value *= pub_key
        value %= 20201227

    return value


def get_loop_size(pub_key, subject_number=7):
    value = 1
    loops = 0

    while value != pub_key:
        value *= subject_number
        value %= 20201227
        loops += 1

    return loops


if __name__ == "__main__":
    assert solve(5764801, 17807724) == 14897079
    print(solve(18356117, 5909654))
