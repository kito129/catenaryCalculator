import math
import tkinter as tk
import openpyxl

PI = math.pi
ITERATION_ALPHA = 0.00000157
F1_MAX = 0.005
FD_MAX = 0.05


# *** SUPPORT FUNCTIONS  ***
def function_approximate(param, a_, b_, sub):
    return param * (
            (math.exp((a_ - b_) / param) + math.exp(-(a_ - b_) / param)) / 2 -
            (math.exp(b_ / param) + math.exp(-b_ / param)) / 2) - sub


def function_derivate_approximate(param, a, b):
    return -(math.exp((a - b) / param) - math.exp(-(a - b) / param)) / 2 - (
            math.exp(b / param) - math.exp(-b / param)) / 2


def arrow_calculator(campata, elevation_diff, param):
    # sag = campata * (1 - math.sqrt(1 - (elevation_diff ** 2) / campata ** 2))
    return campata * math.sqrt(campata ** 2 + elevation_diff ** 2) / (8 * param)


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
                          angle_h2_radiant, angle_v2_radiant, angle_hd_radiant, angle_vd_radiant, span, feedback):

    alpha = (PI - angle_hd_radiant + angle_hgr_radiant) / 2
    iteration_alpha = (PI - angle_hd_radiant + angle_hgr_radiant) / 4
    param = 1000
    f2 = 1
    i = 1
    # my add
    fd = feedback

    while abs(iteration_alpha) > ITERATION_ALPHA:
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
        while abs(f1) > F1_MAX:
            x0 = span / 2
            fd = 1
            k = 1
            while abs(fd) > FD_MAX:
                fd = function_approximate(param, span, x0, yd)
                functionDerivate = function_derivate_approximate(param, span, x0)
                x0 = x0 - fd / functionDerivate
                if k == 15:
                    print("Newton-Raphson method did not converge")
                    param = 0
                k = k + 1
            f1 = function_approximate(param, x1, x0, y1)
            param = param * (param * ((math.exp((x1 - x0) / param) + math.exp(-(x1 - x0) / param)) / 2 - (
                    math.exp(x0 / param) + math.exp(-x0 / param)) / 2) - yd * x1 / span) / (y1 - yd * x1 / span)
            if j == 15:
                print("Newton-Raphson method did not converge")
                param = 0
            j = j + 1
        f2 = function_approximate(param, x2, x0, y2)
        if f2 > 0:
            alpha = alpha + iteration_alpha
        else:
            alpha = alpha - iteration_alpha
        if i == 20:
            print("Newton-Raphson method did not converge")
            param = 0
        iteration_alpha = iteration_alpha / 2
        i = i + 1

    return param, fd


def calculate_params(campata, hg, vg, h1, v1, h2, v2, h3, v3, hd, vd, elevation_diff):
    hg_r = 0
    vg_r = PI / 2 - PI / 200 * vg

    # radiant conversion
    hd_r = radiant_conversion(hd, hg)
    vd_r = angle_in_radiant(vd)
    h1_r = radiant_conversion(h1, hg)
    v1_r = angle_in_radiant(v1)
    h2_r = radiant_conversion(h2, hg)
    v2_r = angle_in_radiant(v2)

    feedback = 1
    param1, feedback = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r, v2_r, hd_r, vd_r, campata, feedback)

    h2_r = radiant_conversion(h3, hg)
    v2_r = angle_in_radiant(v3)
    param2, feedback = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r, v2_r, hd_r, vd_r, campata, feedback)

    h1_r = radiant_conversion(h2, hg)
    v1_r = angle_in_radiant(v2)
    param3, feedback = newton_rapshon_method(hg_r, vg_r, h1_r, v1_r, h2_r, v2_r, hd_r, vd_r, campata, feedback)

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


# *** GET DATA FUNCTIONS  ***
def get_temperature():
    temp = float(input("Insert temperature: "))
    while temp < -10 or temp > 30:
        print("Temperature must be between -10 and 30")
        temp = float(input("Insert temperature: "))
    return temp


def get_elevation_difference():
    elevation_difference = float(input("Insert elevation difference: "))
    while elevation_difference < -1000 or elevation_difference > 1000:
        print("Elevation difference must be between -1000 and 1000")
        elevation_difference = float(input("Insert elevation difference: "))
    return elevation_difference


def get_span_length():
    span_length = float(input("Insert campata: "))
    while span_length < -1000 or span_length > 1000:
        print("Campata must be between -1000 and 1000")
        span_length = float(input("Insert span length: "))
    return span_length


def get_angle(title):
    print("Getting angle: ", title)
    angle = float(input("Insert angle: "))
    while angle <= 0 or angle >= 400:
        print("Hsx must be between 0 and 400")
        angle = float(input("Insert angle: "))
    return angle


def get_freccia_tab():
    freccia_tab = float(input("Insert freccia tab: "))
    return freccia_tab


# *** GUI  ***

def get_white_data(white_data_entry):
    white_data = white_data_entry.get()

    # Save the white data to the Excel file
    wb = openpyxl.load_workbook("FILE DI VERIFICA DI REGOLAZIONE DI UN CAVO CON METODO PAPOTOSELT.xlsx")
    ws = wb["Foglio1"]

    ws.cell(row=11, column=2).value = white_data

    wb.save("FILE DI VERIFICA DI REGOLAZIONE DI UN CAVO CON METODO PAPOTOSELT.xlsx")



# *** MAIN  ***
def main():

    print("**** FUNE CALCULATOR ****")
    print("**** author: kito129 ****")
    print()
    # GUI
    # root = tk.Tk()

    # instructions = tk.Label(root, text="Enter the white data:")
    # instructions.pack()

    # white_data_entry = tk.Entry(root)
    # white_data_entry.pack()

    # submit_button = tk.Button(root, text="Submit", command=lambda: get_white_data(white_data_entry))
    # submit_button.pack()

    #root.mainloop()

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

    if input("Do you want to insert data? yes: input, no: use default data (y/n)") == "y":
        # function that get this data from user with validation
        temperature = get_temperature()
        elevation_difference = get_elevation_difference()
        span_length = get_span_length()
        angle_hsx = get_angle("Hsx")
        angle_vsx = get_angle("Vsx")
        angle_h1 = get_angle("H1")
        angle_v1 = get_angle("V1")
        angle_h2 = get_angle("H2")
        angle_v2 = get_angle("V2")
        angle_h3 = get_angle("H3")
        angle_v3 = get_angle("V3")
        angle_hd = get_angle("Hdx")
        angle_vd = get_angle("Vdx")
        freccia_tab = get_freccia_tab()
    else:
        print("--> Using default data")
        print()

    # print params
    print("INPUT DATA")
    print("\ttemperature:", temperature, "°C")
    print("\televation difference:", elevation_difference, "m")
    print("\tcampata:", span_length, "m")
    print()
    print("\tHsx:", format(angle_hsx, '.4f'),"°")
    print("\tVsx:", format(angle_vsx, '.4f'),"°")
    print()
    print("\tH1:", format(angle_h1, '.4f'),"°")
    print("\tV1:", format(angle_v1, '.4f'),"°")
    print()
    print("\tH2:", format(angle_h2, '.4f'),"°")
    print("\tV2:", format(angle_v2, '.4f'),"°")
    print()
    print("\tH3:", format(angle_h3, '.4f'),"°")
    print("\tV3:", format(angle_v3, '.4f'),"°")
    print()
    print("\tHdx:", format(angle_hd, '.4f'),"°")
    print("\tVdx:", format(angle_vd, '.4f'),"°")

    # calculate and display results
    param12, param13, param23, result, media, arrow1, arrow2, arrow3, error = \
        calculate_params(span_length, angle_hsx, angle_vsx, angle_h1, angle_v1, angle_h2, angle_v2, angle_h3,
                         angle_v3, angle_hd, angle_vd, elevation_difference)

    print()
    print("**** RESULTS  ****")

    print("A) VISTA 1-2")
    print("\tparam:", format(param12, '.4f'))
    print("\tarrow:", format(arrow1, '.4f'))

    print()
    print("B) VISTA 2-3")
    print("\tparam:", format(param23, '.4f'))
    print("\tarrow:", format(arrow3, '.4f'))

    print()
    print("C) VISTA 1-3")
    print("\tparam:", format(param13, '.4f'))
    print("\tarrow:", format(arrow2, '.4f'))

    print("\033[1m")
    print("MEDIA")
    print("\tparam:", format(media, '.4f'))
    print("\tarrow:", format(result, '.4f'))
    print("\033[0m")

    print()
    print("RESULT")
    print("\tFreccia Tab:", format(freccia_tab, '.4f'))
    print("\tdelta :", format((result - freccia_tab), '.4f'))
    print("\033[1m", "\tdelta % :", format((result - freccia_tab) / freccia_tab, '.4f'), "%", "\033[0m")
    print("\terror  :", format(error, '.4f'))


    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
