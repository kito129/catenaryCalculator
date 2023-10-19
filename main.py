import math

PI = math.pi


# *** SUPPORT FUNCTIONS  ***
def function_approximate(param, first_value, second_value, last_sub):
    return param * (
            (math.exp((first_value - second_value) / param) + math.exp(-(first_value - second_value) / param)) / 2 -
            (math.exp(second_value / param) + math.exp(-second_value / param)) / 2) - last_sub


def function_derivate_approximate(param, a, b):
    return -(math.exp((a - b) / param) - math.exp(-(a - b) / param)) / 2 - (
            math.exp(b / param) - math.exp(-b / param)) / 2


def arrow_calculator(campata, elevation_diff, param):
    return campata * (campata ** 2 + elevation_diff ** 2) ** 0.5 / (8 * param)


def angle_in_radiant(angle):
    return PI / 2 - PI / 200 * angle


def radiant_conversion(angle_a, angle_b):
    delta_angle = angle_a - angle_b
    if delta_angle < 0:
        radian_value = PI / 200 * (400 + delta_angle)
    else:
        radian_value = PI / 200 * delta_angle
    return radian_value


# *** MAIN FUNCTIONS  ***

def newton_rapshon_method(angle_hgr_radiant, angle_vgr_radiant, angle_h1_radiant, angle_v1_radiant,
                          angle_h2_radiant, angle_v2_radiant, angle_hd_radiant, angle_vd_radiant, span):
    alpha = (PI - angle_hd_radiant + angle_hgr_radiant) / 2
    iterationValue = (PI - angle_hd_radiant + angle_hgr_radiant) / 4
    param = 1000
    f2 = 1
    i = 1

    while abs(iterationValue) > 0.00000157:
        ag = span * math.sin(PI - angle_hd_radiant - alpha) / math.sin(angle_hd_radiant)
        ad = span * math.sin(alpha) / math.sin(angle_hd_radiant)
        yd = ad * math.tan(angle_vd_radiant) - ag * math.tan(angle_vgr_radiant)
        x1 = ag * math.sin(angle_h1_radiant) / math.sin(PI - angle_h1_radiant - alpha)
        a1 = x1 * math.sin(alpha) / math.sin(angle_h1_radiant)
        y1 = a1 * math.tan(angle_v1_radiant) - ag * math.tan(angle_vgr_radiant)
        x2 = ag * math.sin(angle_h2_radiant) / math.sin(PI - angle_h2_radiant - alpha)
        a2 = x2 * math.sin(alpha) / math.sin(angle_h2_radiant)
        y2 = a2 * math.tan(angle_v2_radiant) - ag * math.tan(angle_vgr_radiant)
        f1 = 1
        j = 1
        x0 = span / 2

        while abs(f1) > 0.005:
            x0 = span / 2
            fd = 1
            k = 1

            while abs(fd) > 0.05:

                fd = function_approximate(param, span, x0, yd)
                functionDerivate = function_derivate_approximate(param, span, x0)
                x0 = x0 - fd / functionDerivate

                if k == 15:
                    print("Newton-Raphson method did not converge")
                    param = 0
                k = k + 1

            f1 = function_approximate(param, x1, x0, y1)

            param = param * (param * ((math.exp((x1 - x0) / param) + math.exp(-(x1 - x0) / param)) / 2 - (
                    math.exp(x0 / param) + math.exp(-x0 / param)) / 2) - yd * x1 / span) / (
                            y1 - yd * x1 / span)

            if j == 15:
                print("Newton-Raphson method did not converge")
                param = 0

            j = j + 1

        f2 = function_approximate(param, x2, x0, y2)
        if f2 > 0:
            alpha = alpha + iterationValue
        else:
            alpha = alpha - iterationValue

        if i == 20:
            print("Newton-Raphson method did not converge")
            param = 0

        iterationValue = iterationValue / 2
        i = i + 1

    return param


def calculate_params(campata, hg, vg, h1, v1, h2, v2, h3, v3, hd, vd, elevation_diff):
    # a = Cells(D30)
    # hg = Cells(D31)
    # vg = ...
    # h1 =
    # v1 =
    # h2 =
    # v2 =
    # h3 =
    # v3 =
    # hd =
    # vd = Cells(D40)

    hg_r = 0
    vg_r = PI / 2 - PI / 200 * vg

    # radiant conversion
    hd_r = radiant_conversion(hd, hg)
    h1_r = radiant_conversion(h1, hg)
    h2_r = radiant_conversion(h2, hg)
    # vd, v1 and v2 radiant conversion
    vd_r = angle_in_radiant(vd)
    v1_r = angle_in_radiant(v1)
    v2_r = angle_in_radiant(v2)

    param1 = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r, v2_r, hd_r, vd_r, campata)

    h2_r = radiant_conversion(h3, hg)
    v2_r = angle_in_radiant(v3)
    param2 = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r, v2_r, hd_r, vd_r, campata)

    h1_r = radiant_conversion(h2, hg)
    v1_r = angle_in_radiant(v2)
    param3 = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r, v2_r, hd_r, vd_r, campata)

    # result calculation
    parametro_media = (param1 + param2 + param3) / 3

    if parametro_media == 0:
        arrow_media = 0
    else:
        arrow_media = arrow_calculator(campata, elevation_diff, parametro_media)

    arr1 = arrow_calculator(campata, elevation_diff, param1)
    arr2 = arrow_calculator(campata, elevation_diff, param2)
    arr3 = arrow_calculator(campata, elevation_diff, param3)

    ecart_type = math.sqrt(
        (3 * (param1 ** 2 + param2 ** 2 + param3 ** 2) - (param1 + param2 + param3) ** 2) / (3 * (3 - 1)))

    if ecart_type > 1000:
        print("ecart_type > 1000", "**** ERROR ****")
        parametro_media = 0
        arrow_media = 0

    return param1, param2, param3, arrow_media, parametro_media, arr1, arr2, arr3, ecart_type


# *** MAIN  ***

if __name__ == '__main__':
    temperature = 7.0
    elevation_difference = -2.5
    span_length = 389.50
    angle_hsx = 0.100
    angle_vsx = 94.0580
    angle_h1 = 30.0380
    angle_v1 = 93.8710
    angle_h2 = 63.9710
    angle_v2 = 92.7080
    angle_h3 = 90.8010
    angle_v3 = 91.9070
    angle_hd = 121.8410
    angle_vd = 90.4640
    freccia_tab = 13.5000

    param12, param13, param23, result, media, arrow1, arrow2, arrow3, error = \
        calculate_params(span_length, angle_hsx, angle_vsx, angle_h1, angle_v1, angle_h2, angle_v2, angle_h3,
                         angle_v3, angle_hd, angle_vd, elevation_difference)

    # return param1, param2, param3, arrowMedia, parametro_media, arr1, arr2, arr3, ecart_type

    print("INPUT DATA")
    print("\ttemperature:", temperature, "°C")
    print("\televation difference:", elevation_difference, "m")
    print("\tspan lenght:", span_length, "m")
    print()
    print("\tHsx:", format(angle_hsx, '.4f'), "°")
    print("\tVsx:", format(angle_vsx, '.4f'), "°")
    print()
    print("\tH1:", format(angle_h1, '.4f'), "°")
    print("\tV1:", format(angle_v1, '.4f'), "°")
    print()
    print("\tH2:", format(angle_h2, '.4f'), "°")
    print("\tV2:", format(angle_v2, '.4f'), "°")
    print()
    print("\tH3:", format(angle_h3, '.4f'), "°")
    print("\tV3:", format(angle_v3, '.4f'), "°")
    print()
    print("\tHdx:", format(angle_hd, '.4f'), "°")
    print("\tVdx:", format(angle_vd, '.4f'), "°")

    print()
    print("**** RESULTS  ****")

    print("A) VISTA 1-2")
    print("\tparam:", format(param12, '.4f'))
    print("\tarrow:", format(arrow1, '.4f'))

    print()
    print("B) VISTA 2-3")
    print("\tparam:", format(param23, '.4f'))
    print("\tarrow:", format(arrow2, '.4f'))

    print()
    print("C) VISTA 1-3")
    print("\tparam:", format(param13, '.4f'))
    print("\tarrow:", format(arrow3, '.4f'))

    print("\033[1m")
    print("MEDIA")
    print("\tparam:", format(media, '.4f'))
    print("\tarrow:", format(result, '.4f'))
    print("\033[0m")

    print()
    print("RESULT")
    print("\tFreccia Tab:", format(freccia_tab, '.4f'))
    print("\tdelta ° :", format((result - freccia_tab), '.4f'), "°")
    print("\033[1m", "\tdelta % :", format((result - freccia_tab) / freccia_tab, '.4f'), "%", "\033[0m")
