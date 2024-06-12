from tkinter import *
import requests
import json

root = Tk()
root.title("Air Quality Index")
color_lib = {"Good": "Green", "Moderate": "Yellow", "Unhealthy for Sensitive Groups": "Orange",
             "Unhealthy": "Red", "Very Unhealthy": "Purple", "Hazardous": "Maroon"}


class Weather:
    def __init__(self, master):
        self.master = master

        # initialising values for output data
        self.api_request = None
        self.api_content = None
        self.api_o3 = None
        self.api_pm25 = None
        self.api_pm10 = None
        self.api_display_area = None
        self.api_display_o3 = None
        self.api_display_pm25 = None
        self.api_display_pm10 = None
        self.display_label_area = None
        self.display_label_o3 = None
        self.display_label_pm25 = None
        self.display_label_pm10 = None

        # widgets for taking zipcode
        self.zipcode_label = Label(master, text="Enter zipcode : ", justify=LEFT, bg="Light Blue",
                                   font=("Times New Roman", 16))
        self.zipcode_label.grid(row=0, column=0, sticky="news")
        self.zipcode_entry = Entry(master, width=20)
        self.zipcode_entry.grid(row=0, column=1, sticky="news")
        self.zipcode_button = Button(master, text="Submit", font=("Times New Roman", 16),
                                     command=lambda: self.retrieve_data(str(self.zipcode_entry.get())))
        self.zipcode_button.grid(row=0, column=2, sticky="news")

    def retrieve_data(self, zipcode):
        self.api_o3 = None
        self.api_pm25 = None
        self.api_pm10 = None
        try:
            self.api_request = requests.get(
                "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode="
                + zipcode + "&distance=25&API_KEY=B928D096-7A6B-40FB-BB4E-2090AB4FCDBC")
            self.api_content = json.loads(self.api_request.content)
            # if api_content has items, then create widgets accordingly
            if self.api_content:
                # forgetting current labels to replace
                if self.display_label_o3:
                    self.display_label_o3.grid_forget()
                if self.display_label_pm25:
                    self.display_label_pm25.grid_forget()
                if self.display_label_pm10:
                    self.display_label_pm10.grid_forget()

                for content in self.api_content:
                    self.api_display_area = content["ReportingArea"] + ", " + content["StateCode"]
                    if "O3" in content.values():
                        self.api_o3 = content
                    elif "PM2.5" in content.values():
                        self.api_pm25 = content
                    elif "PM10" in content.values():
                        self.api_pm10 = content

                if self.api_o3:
                    self.api_display_o3 = "\nO3 Air Quality Index : " + str(self.api_o3["AQI"])
                    self.api_display_o3 += "\nEvaluation : Ozone Air Quality is " + str(self.api_o3["Category"]["Name"])

                    self.display_label_o3 = Label(self.master, text=self.api_display_o3, justify=LEFT,
                                                  bg=color_lib[self.api_o3["Category"]["Name"]], fg="White",
                                                  font=("Helvetica", 15))
                    self.display_label_o3.grid(row=2, column=0, sticky="we", columnspan=3)

                if self.api_pm25:
                    self.api_display_pm25 = "\nPM 2.5 Air Quality Index : " + str(self.api_pm25["AQI"])
                    self.api_display_pm25 += "\nEvaluation : PM 2.5 Air Quality is " + str(self.api_pm25["Category"][
                                                                                           'Name'])

                    self.display_label_pm25 = Label(self.master, text=self.api_display_pm25, justify=LEFT,
                                                    bg=color_lib[self.api_pm25["Category"]["Name"]], fg="White",
                                                    font=("Helvetica", 15))
                    self.display_label_pm25.grid(row=3, column=0, sticky="we", columnspan=3)

                if self.api_pm10:
                    self.api_display_pm10 = "\nPM 10 Air Quality Index : " + str(self.api_pm10["AQI"])
                    self.api_display_pm10 += "\nEvaluation : PM 10 Air Quality is " + str(self.api_pm10["Category"][
                                                                                           'Name'])
                    self.display_label_pm10 = Label(self.master, text=self.api_display_pm10, justify=LEFT,
                                                    bg=color_lib[self.api_pm10["Category"]["Name"]], fg="White",
                                                    font=("Helvetica", 15))
                    self.display_label_pm10.grid(row=4, column=0, sticky="we", columnspan=3)

                self.display_label_area = Label(self.master, text=self.api_display_area, justify=LEFT, bg="Light Blue",
                                                font=("Times New Roman", 18))
                self.display_label_area.grid(row=1, column=0, sticky="we", columnspan=3)

            else:
                self.display_label_area = Label(self.master, text="Zipcode unavailable", justify=LEFT, bg="Light Blue",
                                                font=("Times New Roman", 18))
                self.display_label_area.grid(row=1, column=0, sticky="we", columnspan=3)
                if self.display_label_o3:
                    self.display_label_o3.grid_forget()
                if self.display_label_pm25:
                    self.display_label_pm25.grid_forget()
                if self.display_label_pm10:
                    self.display_label_pm10.grid_forget()
        except requests.exceptions.RequestException as err:
            self.display_label_area = Label(self.master, text=str(err), justify=LEFT, bg="Light Blue",
                                            font=("Times New Roman", 18))
            self.display_label_area.grid(row=1, column=0, sticky="we", columnspan=3)
            if self.display_label_o3:
                self.display_label_o3.grid_forget()
            if self.display_label_pm25:
                self.display_label_pm25.grid_forget()
            if self.display_label_pm10:
                self.display_label_pm10.grid_forget()


w = Weather(root)
root.mainloop()
