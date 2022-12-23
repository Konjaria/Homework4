import random
import re
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from colors.colors import color_list
FILE_NAME = "data.xlsx"
try:
    with open(FILE_NAME, 'r') as reader:
        pass
except FileNotFoundError:
    messagebox.showinfo(title="File not Found", message="Please check corresponding file: {}".format(FILE_NAME))
    exit(1)
finally:

    def get_digits_only(lst, text):
        pattern = re.compile(r'^\d+$')
        digits_only = []
        for s in lst:
            if pattern.match(str(s)):
                digits_only.append(s)
            elif s not in err_:
                messagebox.showinfo(title="Oops.. some data is not valid",
                                    message=f"{s} is not valid {text}")
                err_.append(s)
        return digits_only


    def Unique(list1, digits_only=0, txt="input"):
        if digits_only == 1:
            list1 = get_digits_only(list1, txt)
        unique_list = []
        for x in list1:
            if x not in unique_list:  # I am not sure if it is correct, so I won't add there ' and x not in err_list'
                unique_list.append(x)
        return unique_list


    data = pd.read_excel(FILE_NAME)
    dataframe = data.to_dict(orient="records")
    BACKGROUND_COLOR = "#3C2A21"
    TEXT_COLOR = "#E5E5CB"
    random.shuffle(color_list)
    err_ = []
    unique_transports = Unique([text.lower() for text in data.Transport])
    unique_years = Unique(list(data.year), digits_only=1, txt="year")
    number_of_visits = {element: list.count(list(data.year), element) for element in unique_years}
    unique_countries = Unique(list(data.Country))
    POSSIBLE_INPUT = ["year", "number of visits", "country"]
    RUN_TIME = 0
    for element in unique_transports:
        POSSIBLE_INPUT.append(str(element).lower())


    def save_info():
        p1 = param_1.get().lower()
        p2 = param_2.get().lower()

        if p1 not in POSSIBLE_INPUT or p2 not in POSSIBLE_INPUT or p1 == p2 \
                or p1 == "year" and p2 != "number of visits" \
                or p1 == "number of visits" and p2 != "year" \
                or p1 == "country" and p2 not in unique_transports \
                or p1 not in unique_transports and p2 == "country":  # we have to build Bar chart over there
            messagebox.showinfo(title="Oops..", message="Unhandled Action, Please check the parameters\nPlease "
                                                        "make sure to use, number of visits with year and one of "
                                                        "the transport types along  country")
            return

        # Chart type is not provided
        elif chart_type_.get() == 0:
            messagebox.showwarning(title="Oops..", message="Chart type is not selected")
            return


        # Bar chart or Plot chart case but not both case
        elif chart_type_.get() == 1 or chart_type_.get() == 2:
            if (p1 == "year" or p1 == "number of visits") and (p2 == "year" or p2 == "number of visits"):
                # Bar chart
                if chart_type_.get() == 1:
                    df1 = data.groupby("year")["year"].count()
                    df1.plot(kind='bar')
                    plt.show()
                    plt.close()
                    return


                # Plot chart
                elif chart_type_.get() == 2:
                    x = list(dict(data.groupby("year")["year"].count()).values())
                    y = list(data["year"].unique())
                    plt.plot(x, y)
                    # Add labels to the plot chart
                    plt.xlabel("Year", labelpad=10)
                    plt.ylabel("Number of Visits")
                    plt.title("Number of Visits per year",
                              fontstyle="oblique",
                              fontfamily={"Arial", "sans-serif"},
                              c="#251749",
                              pad=10)
                    plt.show()
                    plt.close()
                    return


            elif not (not (not "country" != p1 or p1 in unique_transports) or not (
                    p2 in unique_transports or p2 == "country")):
                ttype = ""
                if p1 in unique_transports:
                    ttype += p1.title()
                else:
                    ttype += p2.title()
                x_axis = list(data['Country'].unique())
                y_axis = list(dict(data.groupby("Country")["Transport"].apply(lambda tr_type: (tr_type == ttype).sum())).values())


                # Bar chart
                if chart_type_.get() == 1:
                    plt.bar(x_axis, y_axis)
                    plt.xticks(x_axis, rotation=90)
                    plt.title(f"{ttype} Population ")
                    plt.xlabel("Countries", labelpad=10)
                    plt.ylabel(f"{ttype} usage")
                    plt.title(label=f"{ttype} in different countries")
                    plt.show()
                    plt.close()
                    return


                # Plot chart
                if chart_type_.get() == 2:
                    plt.plot(x_axis, y_axis, color="#D5CEA3", lw=2)
                    plt.scatter(x_axis, y_axis)
                    plt.xticks(x_axis, rotation=90)
                    plt.title(f"{ttype} Population",
                              fontstyle="oblique",
                              fontfamily={"Arial", "sans-serif"},
                              c="#251749",
                              pad=10
                              )
                    plt.show()
                    plt.close()
                    return


        # both plot and bar chart appears over there and implementation is omre like starting from 'scratch' rather
        # that the other ones
        elif chart_type_.get() == 3:

            global RUN_TIME
            RUN_TIME += 1
            if not (not (p1 == "year") and not (p1 == "number of visits")):

                if p2 == "year" or p2 == "number of visits":
                    # Create a figure with 2 subplots
                    fig, (ax1, ax2) = plt.subplots(1, 2)

                    x_axis1 = np.array(sorted(list(range(0, len(list(number_of_visits.keys())), 1))))  # year
                    y_axis1 = np.array(sorted(list(number_of_visits.values())))  # number of visits into each of the
                    # year
                    if RUN_TIME % 2 == 0:
                        ax1.bar(x_axis1, y_axis1, label=unique_years, color=color_list)
                        ax1.legend(loc='upper left', ncol=5)
                    else:
                        ax1.bar(x_axis1, y_axis1)
                    ax1.set_title("Bar chart - Number of Visits per year")
                    ax1.set_xlabel("Years")
                    ax1.set_ylabel("Number of Visits")
                    i = 0
                    for x_val, y_val in zip(x_axis1, y_axis1):
                        label1 = str(y_val)
                        ax1.text(x_val, y_val * 0.5, label1, ha='center', va='top', rotation=90, fontsize=7, )
                        i += 1

                    ax2.plot(x_axis1, y_axis1)
                    ax2.set_title("Plot chart - Number of Visits per year")
                    ax2.set_xlabel("Years")
                    ax2.set_ylabel("Number of Visits")
                    plt.show()
                    plt.close()

                elif not (not (not "country" != p1 or p1 in unique_transports) or not (
                        p2 in unique_transports or p2 == "country")):
                    actual_data = {element: 0 for element in unique_countries}

                    transport = ""
                    contre = ""
                    if p1 in unique_transports:
                        transport += str(p1)
                        contre += str(p2)
                    if p2 in unique_transports:
                        contre += str(p1)
                        transport += str(p2)

                    for curr_list in dataframe:
                        if curr_list["Transport"].lower() == transport:
                            actual_data[curr_list["Country"]] += 1

                    x_axis2 = np.array(sorted(list(range(1, len(actual_data.keys()) + 1, 1))))
                    y_axis2 = np.array(sorted(list(actual_data.values())))

                    # Create a figure with 2 subplots
                    fig, (ax1, ax2) = plt.subplots(1, 2)

                    ax1.bar(x_axis2, y_axis2)
                    ax1.set_title(f"Country: {contre} and Transport: {transport}")
                    ax1.set_xlabel("Countries", labelpad=10)
                    ax1.set_ylabel(f"{transport} usage")
                    ax1.set_title(label=f"{transport} in different countries",
                                  fontstyle="oblique",
                                  fontfamily={"Arial", "sans-serif"},
                                  c="#850000")

                    ax2.plot(x_axis2, y_axis2,
                             color="#D5CEA3",
                             lw=2)
                    ax2.scatter(x_axis2, y_axis2)
                    ax2.set_xlabel("Country")
                    ax2.set_ylabel(f"{transport} Usage")
                    ax2.set_title("{} usage in different countries".format(transport),
                                  fontstyle="oblique",
                                  fontfamily={"Arial", "sans-serif"},
                                  c="#251749",
                                  pad=10)
                    plt.show()
                    plt.close()
                    return

            elif not (not (not "country" != p1 or p1 in unique_transports) or not (
                    p2 in unique_transports or p2 == "country")):
                actual_data = {element: 0 for element in unique_countries}

                transport = ""
                contre = ""
                if p1 in unique_transports:
                    transport += str(p1)
                    contre += str(p2)
                if p2 in unique_transports:
                    contre += str(p1)
                    transport += str(p2)

                for curr_list in dataframe:
                    if curr_list["Transport"].lower() == transport:
                        actual_data[curr_list["Country"]] += 1

                x_axis2 = np.array(sorted(list(range(1, len(actual_data.keys()) + 1, 1))))
                y_axis2 = np.array(sorted(list(actual_data.values())))

                # Create a figure with 2 subplots
                fig, (ax1, ax2) = plt.subplots(1, 2)
                ax1.bar(x_axis2, y_axis2,
                        color=color_list[:len(x_axis2)],
                        )
                ax1.set_title(f"Country: {contre} and Transport: {transport}")
                ax1.set_xlabel("Countries", labelpad=10)
                ax1.set_ylabel(f"{transport} usage")
                ax1.set_title(label=f"{transport} in different countries",
                              fontstyle="oblique",
                              fontfamily={"Arial", "sans-serif"},
                              c="#850000")


                ax2.plot(x_axis2, y_axis2,
                         color="#D5CEA3",
                         lw=2)
                ax2.scatter(x_axis2, y_axis2)
                ax2.set_xlabel("Country")
                ax2.set_ylabel(f"{transport} Usage")
                ax2.set_title("{} usage in different countries".format(transport),
                              fontstyle="oblique",
                              fontfamily={"Arial", "sans-serif"},
                              c="#251749",
                              pad=10)
                plt.show()
                plt.close()
                return

    # ------------------------------ ui setup --------------------------------------
    # Build main window and set its geometry and fixed width and height
    window = tk.Tk()
    window.title("Visitors in different countries")
    window.geometry("600x600+0+0")
    window.resizable(False, False)
    window.config(padx=70, pady=70, bg=BACKGROUND_COLOR)

    # Draw a bit into the Canvas as well
    canvas = tk.Canvas(width=300, height=300, bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.create_text(100, 50, text="Visitors", font=("Ariel", 36, "italic"),
                       fill="#D5CEA3", anchor="center")
    # variables for text labels, that are actual parameters of our function
    parameter1 = tk.Label(text="Parameter 1:", fg=TEXT_COLOR, font=("Arial Black", 12, "bold"), bg=BACKGROUND_COLOR)
    parameter2 = tk.Label(text="Parameter 2:", fg=TEXT_COLOR, font=("Arial Black", 12, "bold"), bg=BACKGROUND_COLOR)

    # Combobox variables
    param_1_var = tk.StringVar()
    param_2_var = tk.StringVar()
    chart_type_ = tk.IntVar(window, 0)

    param_1 = ttk.Combobox(window, width=38, textvariable=param_1_var, values=['year', 'number of visits', 'country', 'air',
                                                                               'tunnel', 'sea'], )

    param_2 = ttk.Combobox(window, width=38, textvariable=param_2_var,
                           values=['year',
                                   'number of visits',
                                   'country',
                                   'air',
                                   'tunnel',
                                   'sea'],
                           )

    bar_type = tk.Radiobutton(width=10, text="Bar chart", bg='#D5CEA3',
                              fg="#1A120B", variable=chart_type_, value=1)

    plot_type = tk.Radiobutton(width=10, text="Plot chart", bg='#D5CEA3',
                               fg="#1A120B", variable=chart_type_, value=2)

    both_type = tk.Radiobutton(width=10, text="Both types", bg='#D5CEA3',
                               fg="#1A120B", variable=chart_type_, value=3,
                               selectcolor='white')

    save_button = tk.Button(width=38, text="Save", bg='#1A120B', fg="#D5CEA3",
                            command=save_info)

    # I've putted the parameters onto the window
    parameter1.grid(row=1, column=0)
    parameter2.grid(row=2, column=0, padx=5)
    param_1.grid(row=1, column=1)
    param_2.grid(row=2, column=1, padx=12)
    bar_type.grid(row=5, column=0, pady=10)
    plot_type.grid(row=5, column=1, pady=10)
    both_type.grid(row=6, column=0, pady=10)
    save_button.grid(row=7, column=1, columnspan=2,
                     pady=20, padx=15)
    canvas.grid(row=0, column=1)
    window.mainloop()