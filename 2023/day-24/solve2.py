from sympy import symbols, Eq, solve


hailstones = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""


TEST_AREA = (7, 27)

TEST_AREA = (200000000000000, 400000000000000)
hailstones = open("input.txt", "r").read().strip()


hailstones = [h.strip().split(" @ ") for h in hailstones.splitlines() if h.strip()]
hailstones = [
    (tuple(map(int, h[0].split(","))), tuple(map(int, h[1].split(","))))
    for h in hailstones
]


def system_eq(coefficients):
    ai, bi, ci, di, ei, fi, t1, t2, t3 = symbols("ai bi ci di ei fi t1 t2 t3")
    a0, b0, c0, d0, e0, f0 = coefficients[0]
    a1, b1, c1, d1, e1, f1 = coefficients[1]
    a2, b2, c2, d2, e2, f2 = coefficients[2]

    eqs = [
        Eq(a0 * t1 + b0, ai * t1 + bi),
        Eq(c0 * t1 + d0, ci * t1 + di),
        Eq(e0 * t1 + f0, ei * t1 + fi),
        Eq(a1 * t2 + b1, ai * t2 + bi),
        Eq(c1 * t2 + d1, ci * t2 + di),
        Eq(e1 * t2 + f1, ei * t2 + fi),
        Eq(a2 * t3 + b2, ai * t3 + bi),
        Eq(c2 * t3 + d2, ci * t3 + di),
        Eq(e2 * t3 + f2, ei * t3 + fi),
    ]

    return solve(eqs)


def get_coefficients(hailstones):
    coefficients = [zip(h2, h1) for h1, h2 in hailstones]
    unpacked_coeffs = []
    for coeffs in coefficients:
        e = []
        for c in coeffs:
            for k in c:
                e.append(k)
        unpacked_coeffs.append(e)
    return unpacked_coeffs


result = system_eq(get_coefficients(hailstones))
print(result[0])
a, b, c, d, e, f = list(result[0].values())[:6]
print("result:", b + d + f)
