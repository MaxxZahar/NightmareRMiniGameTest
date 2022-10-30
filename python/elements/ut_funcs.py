def d1tod2(x: int, number_of_columns: int):
    return (x % number_of_columns, x // number_of_columns)


def d2tod1(x: tuple, number_of_columns: int):
    return x[0] + x[1] * number_of_columns
