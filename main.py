import math


def calculator(angle_hsx_radiant, angle_vsx_radiant, angle_h1_radiant, angle_v1_radiant,
               angle_h2_radiant, angle_v2_radiant, angle_hd_radiant, angle_vd_radiant, span):
    pi = math.pi
    alpha = (pi - angle_hd_radiant + angle_hsx_radiant) / 2
    vgr = pi / 2 - pi / 200 * angle_vsx_radiant
    iterationValue = (pi - angle_hd_radiant + angle_hsx_radiant) / 4
    param = 1000
    f2 = 1
    i = 1

    while abs(iterationValue) > 0.00000157:
        ag = span * math.sin(pi - angle_hd_radiant - alpha) / math.sin(angle_hd_radiant)
        ad = span * math.sin(alpha) / math.sin(angle_hd_radiant)
        yd = ad * math.tan(angle_vd_radiant) - ag * math.tan(vgr)
        x1 = ag * math.sin(angle_h1_radiant) / math.sin(pi - angle_h1_radiant - alpha)
        a1 = x1 * math.sin(alpha) / math.sin(angle_h1_radiant)
        y1 = a1 * math.tan(angle_v1_radiant) - ag * math.tan(vgr)
        x2 = ag * math.sin(angle_h2_radiant) / math.sin(pi - angle_h2_radiant - alpha)
        a2 = x2 * math.sin(alpha) / math.sin(angle_h2_radiant)
        y2 = a2 * math.tan(angle_v2_radiant) - ag * math.tan(vgr)
        f1 = 1
        j = 1

        while abs(f1) > 0.005:
            x0 = span / 2
            fd = 1
            k = 1

            while abs(fd) > 0.05:

                fd = param * ((math.exp((span - x0) / param) + math.exp(-(span - x0) / param)) / 2 -
                              (math.exp(x0 / param) + math.exp(-x0 / param)) / 2) - yd

                functionDerivate = -(math.exp((span - x0) / param) - math.exp(-(span - x0) / param)) / 2 - (
                        math.exp(x0 / param) - math.exp(-x0 / param)) / 2

                x0 = x0 - fd / functionDerivate

                if k == 15:
                    print("Newton-Raphson method did not converge")
                    param = 0
                k = k + 1

            f1 = param * ((math.exp((x1 - x0) / param) + math.exp(-(x1 - x0) / param)) / 2 - (
                    math.exp(x0 / param) + math.exp(-x0 / param)) / 2) - y1

            param = param * (param * ((math.exp((x1 - x0) / param) + math.exp(-(x1 - x0) / param)) / 2 - (
                    math.exp(x0 / param) + math.exp(-x0 / param)) / 2) - yd * x1 / span) / (
                            y1 - yd * x1 / span)

            if j == 15:
                param = 0

            j = j + 1

        if param == 0:
            break

        f2 = param * ((math.exp((x2 - x0) / param) + math.exp(-(x2 - x0) / param)) / 2 - (
                math.exp(x0 / param) + math.exp(-x0 / param)) / 2) - y2

        if f2 > 0:
            alpha = alpha + iterationValue
        else:
            alpha = alpha - iterationValue

        if i == 20:
            param = 0

        iterationValue = iterationValue / 2
        # i = i + 1

    return param


def calculate_params_in_radiant(len, hsx, vsx, h1, v1, h2, v2, h3, v3, hd, vd):
    # some constants
    pi = math.pi
    hgr = 0
    vgr = pi / 2 - pi / 200 * vsx

    # radiant conversion
    if hd < hsx:
        hdr = pi / 200 * (400 + hd - hsx)
    else:
        hdr = pi / 200 * (hd - hsx)
    vdr = pi / 2 - pi / 200 * vd

    if h1 < hsx:
        h1r = pi / 200 * (400 + h1 - hsx)
    else:
        h1r = pi / 200 * (h1 - hsx)
    v1r = pi / 2 - pi / 200 * v1

    if h2 < hsx:
        h2r = pi / 200 * (400 + h2 - hsx)
    else:
        h2r = pi / 200 * (h2 - hsx)
    v2r = pi / 2 - pi / 200 * v2

    # print(vdr, v1r, v2r)
    param1 = calculator(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, len)

    if h3 < hsx:
        h2r = pi / 200 * (400 + h3 - hsx)
    else:
        h2r = pi / 200 * (h3 - hsx)

    v2r = pi / 2 - pi / 200 * v3

    # print(vdr, v1r, v2r)
    param2 = calculator(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, len)

    if h2 < hsx:
        h1r = pi / 200 * (400 + h2 - hsx)
    else:
        h1r = pi / 200 * (h2 - hsx)

    v1r = pi / 2 - pi / 200 * v2

    # print(vdr, v1r, v2r)
    param3 = calculator(hgr, vgr, h1r, v1r, h2r, v2r, hdr, vdr, len)

    ecart_type = math.sqrt(
        (3 * (param1 ** 2 + param2 ** 2 + param3 ** 2) - (param1 + param2 + param3) ** 2) / (3 * (3 - 1)))

    # result calculation
    average = (param1 + param2 + param3) / 3

    if average == 0:
        arrow = 0
    else:
        arrow = len * (len ** 2 + average ** 2) ** 0.5 / (8 * average)

    return param1, param2, param3, arrow, average


# Example usage
temperature = 7.0
elevation_difference = -2.5
span_lenght = 389.50
angle_hsx = 0.100
angle_vsx = 94.058
angle_h1 = 30.038
angle_v1 = 93.871
angle_h2 = 63.971
angle_v2 = 92.708
angle_h3 = 90.801
angle_v3 = 91.907
angle_hd = 121.841
angle_vd = 90.464

param12, param13, param23, result, media = calculate_params_in_radiant(span_lenght, angle_hsx, angle_vsx, angle_h1,
                                                                       angle_v1, angle_h2, angle_v2, angle_h3, angle_v3,
                                                                       angle_hd, angle_vd)

# AVERAGE CALCULATIONS
if media == 0:
    media_arrow = 0
    delta = 0
else:
    media_arrow = span_lenght * (span_lenght ** 2 + elevation_difference ** 2) ** 0.5 / (8 * media)
    delta = (media_arrow - result) / result

print("VISTA 1-2")
print("\tparam:", format(param12, '.3f'))
print("\tarrow:", format(param13, '.3f'))
print()
print("VISTA 2-3")
print("\tparam:", format(param23, '.3f'))
print("\tarrow:", format(param13, '.3f'))
print()
print("VISTA 1-2")
print("\tparam:", format(param13, '.3f'))
print("\tarrow:", format(param13, '.3f'))
print()
print("MEDIA")
print("\tparam:", format(media, '.3f'))
print("\tarrow:", format(media_arrow, '.3f'))

print()
print("RESULT")
print("\tresult:", format(result, '.3f'))
print("\tdelta:", format(delta, '.3f'), "%")
