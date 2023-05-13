import random

def induce_err(in_str, error_probability):
    chk = random.random() * 100

    if chk > error_probability:
        return in_str

    idx = (int)(random.random() * 1000) % len(in_str)
    f_bit = '*'
    if in_str[idx] == '0':
        f_bit = '1'
    else:
        f_bit = '0'

    out_str = in_str[: idx] + f_bit + in_str[idx + 1:]
    return out_str


if __name__ == "__main__":
    data = "1001010"
    print("Initial : ", data)
    print("Final : ", induce_err(data, 10))
