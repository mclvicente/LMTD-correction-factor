
import math

CONFIGURATIONS = [
    (1, "1-2"),
    (2, "2-4"),
    (3, "3-6"),
    (4, "4-8"),
    (5, "5-10"),
    (6, "6-12"),
]

def calculate_P_R(T1, T2, t1, t2):
    """Calculate P and R from the four terminal temperatures."""
    P = (t2 - t1) / (T1 - t1)
    R = (T1 - T2) / (t2 - t1)
    return P, R


def _validate_P_R(P, R):
    if not (0 <= P < 1):
        raise ValueError(f"P={P:.4f} must be in the range [0, 1).")
    if R < 0:
        raise ValueError(f"R={R:.4f} must be >= 0.")


def ft_one_shell(P, R):
    """Ft for one shell pass, two tube passes (1-2 configuration)."""
    _validate_P_R(P, R)
    if P <= 1e-12:
        return 1.0


    if abs(R - 1.0) < 1e-6:
        numerator = P * math.sqrt(2) / (1 - P)
        arg_num = 2 - P * (2 - math.sqrt(2))
        arg_den = 2 - P * (2 + math.sqrt(2))
        if arg_den <= 0:
            raise ValueError ("P,R combination is out of the physical range for this configuration.")
        return numerator / math.log(arg_num / arg_den)

    S = math.sqrt(R ** 2 + 1)
    arg_num = 2 / P - 1 - R + S
    arg_den = 2 / P - 1 - R - S
    if arg_den <= 0:
        raise ValueError("P,R combination is out of the physical range for this configuration.")

    numerator = S * math.log((1 - P) / (1 - R * P))
    denominator = (R - 1) * math.log(arg_num / arg_den)
    return numerator / denominator


def _equivalent_P1(P, R, N):
    """Equivalent per-shell effectiveness for N shells in series."""
    if abs(R - 1.0) < 1e-6:
        return P / (N - (N - 1) * P)
    base = (1 - P * R) / (1 - P)
    if base <= 0:
        raise ValueError("P,R,N combination is out of the physical range.")
    W = base ** (1.0 / N)
    return (W - 1) / (W - R)


def ft_n_shells(P, R, N):
    """Ft for N shells in series, 2N tube passes total (N-2N configuration)."""
    _validate_P_R(P, R)
    if N < 1:
        raise ValueError("N must be >= 1.")
    if P <= 1e-12:
        return 1.0
    P1 = _equivalent_P1(P, R, N)
    return ft_one_shell(P1, R)


def configuration_table(P, R):
    
    results = {}
    for N, label in CONFIGURATIONS:
        try:
            results[label] = ft_n_shells(P, R, N)
        except (ValueError, ZeroDivisionError):
            results[label] = None
    return results


print(" T for hot fluid and t for cold fluid; subscripts 1 and 2 refer to in and out, respectively.")
print(" Enter all temperatures in the same units, independent the system SI or English.")

T1 = float(input("Please enter T1 (hot fluid in): "))
T2 = float(input("Please enter T2 (hot fluid out): "))
t1 = float(input("Please enter t1 (cold fluid in): "))
t2 = float(input("Please enter t2 (cold fluid out): "))

P, R = calculate_P_R(T1, T2, t1, t2)
print(f"P = {P:.4f}   R = {R:.4f}\n")

print(f"{'Configuration':<15}{'Ft':>10}")
print("-" * 25)
results = configuration_table(P, R)
for label, F in results.items():
    value = f"{F:.8f}" if F is not None else "invalid"
    print(f"{label:<15}{value:>10}")