def print_1_to_n(n):
    if n==0:
        return
    small_out=print_1_to_n(n-1)
    print(n)