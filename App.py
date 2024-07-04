import os
import tkinter as tk
import tkinter.font as tkFont
from cryptography.fernet import Fernet
from pykeepass import PyKeePass
import requests


class App:
    """
    The aim of this tool is automating the subscription process for a new SendGrid SubUser.
    Its structure and functions are based on the available documentation about "Creating a new SendGrid subcription".

    This app hosts a Graphic User Interface to fill fields.
    It also hosts API-calling functions using these fields.

    The main function of this tool is command_create(), where all steps are listed in chronological order.
    """

    def __init__(self):
        """
        Displays the windows and subscription selection buttons.
        """

        # Setting the zoom parameter
        self.zoom = 2

        # Setting the window
        self.root = tk.Tk()
        self.root.title("New Sendgrid Subscription")
        self.width = 570 * self.zoom
        self.height = 390 * self.zoom
        self.screenwidth = self.root.winfo_screenwidth()
        self.screenheight = self.root.winfo_screenheight()
        self.alignstr = "%dx%d+%d+%d" % (
            self.width,
            self.height,
            (self.screenwidth - self.width) / 2,
            (self.screenheight - self.height) / 2,
        )
        self.root.geometry(self.alignstr)
        self.root.resizable(width=False, height=False)

        # Setting the subscription service variable
        self.service = "null"

        # Setting the Shared Service button
        self.radio_shared = tk.Button(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.radio_shared["font"] = self.ft
        self.radio_shared["fg"] = "#000000"
        self.radio_shared["justify"] = "center"
        self.radio_shared["text"] = "Shared subdomain"
        self.radio_shared.place(
            x=10 * self.zoom,
            y=10 * self.zoom,
            width=170 * self.zoom,
            height=25 * self.zoom,
        )
        self.radio_shared["command"] = self.command_shared
        self.radio_shared["state"] = tk.ACTIVE

        # Setting the Centrally Managed button
        self.radio_centrally = tk.Button(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.radio_centrally["font"] = self.ft
        self.radio_centrally["fg"] = "#000000"
        self.radio_centrally["justify"] = "center"
        self.radio_centrally["text"] = "Centrally managed"
        self.radio_centrally.place(
            x=190 * self.zoom,
            y=10 * self.zoom,
            width=170 * self.zoom,
            height=25 * self.zoom,
        )
        self.radio_centrally["command"] = self.command_centrally
        self.radio_centrally["state"] = tk.ACTIVE

        # Setting the Locally Managed button
        self.radio_locally = tk.Button(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.radio_locally["font"] = self.ft
        self.radio_locally["fg"] = "#000000"
        self.radio_locally["justify"] = "center"
        self.radio_locally["text"] = "Locally Managed"
        self.radio_locally.place(
            x=370 * self.zoom,
            y=10 * self.zoom,
            width=170 * self.zoom,
            height=25 * self.zoom,
        )
        self.radio_locally["command"] = self.command_locally
        self.radio_locally["state"] = tk.ACTIVE

        self.display = False

        self.root.mainloop()

    def display_fields(self):
        """
        Displays all labels and fields.
        """

        if self.display is True:
            return

        self.label_username = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_username["font"] = self.ft
        self.label_username["fg"] = "#000000"
        self.label_username["justify"] = "center"
        self.label_username["text"] = "Username"
        self.label_username.place(
            x=10 * self.zoom,
            y=40 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_username = tk.Entry(self.root)
        self.entry_username["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_username["font"] = self.ft
        self.entry_username["fg"] = "#000000"
        self.entry_username["justify"] = "center"
        self.entry_username.place(
            x=160 * self.zoom,
            y=40 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_username = self.entry_username

        self.label_password = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_password["font"] = self.ft
        self.label_password["fg"] = "#000000"
        self.label_password["justify"] = "center"
        self.label_password["text"] = "Password"
        self.label_password.place(
            x=10 * self.zoom,
            y=70 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_password = tk.Entry(self.root)
        self.entry_password["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_password["font"] = self.ft
        self.entry_password["fg"] = "#000000"
        self.entry_password["justify"] = "center"
        self.entry_password.place(
            x=160 * self.zoom,
            y=70 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_password = self.entry_password

        self.label_ip = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_ip["font"] = self.ft
        self.label_ip["fg"] = "#000000"
        self.label_ip["justify"] = "center"
        self.label_ip["text"] = "IP address"
        self.label_ip.place(
            x=10 * self.zoom,
            y=100 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_ip = tk.Entry(self.root)
        self.entry_ip["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_ip["font"] = self.ft
        self.entry_ip["fg"] = "#000000"
        self.entry_ip["justify"] = "center"
        self.entry_ip.place(
            x=160 * self.zoom,
            y=100 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_ip = self.entry_ip

        self.label_plan = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_plan["font"] = self.ft
        self.label_plan["fg"] = "#000000"
        self.label_plan["justify"] = "center"
        self.label_plan["text"] = "Subscription Plan"
        self.label_plan.place(
            x=10 * self.zoom,
            y=130 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_plan = tk.Entry(self.root)
        self.entry_plan["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_plan["font"] = self.ft
        self.entry_plan["fg"] = "#000000"
        self.entry_plan["justify"] = "center"
        self.entry_plan.place(
            x=160 * self.zoom,
            y=130 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_plan = self.entry_plan

        self.label_subdomain = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_subdomain["font"] = self.ft
        self.label_subdomain["fg"] = "#000000"
        self.label_subdomain["justify"] = "center"
        self.label_subdomain["text"] = "SubDomain"
        self.label_subdomain.place(
            x=10 * self.zoom,
            y=160 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_subdomain = tk.Entry(self.root)
        self.entry_subdomain["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_subdomain["font"] = self.ft
        self.entry_subdomain["fg"] = "#000000"
        self.entry_subdomain["justify"] = "center"
        self.entry_subdomain.place(
            x=160 * self.zoom,
            y=160 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_subdomain = self.entry_subdomain

        self.label_teammates = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_teammates["font"] = self.ft
        self.label_teammates["fg"] = "#000000"
        self.label_teammates["justify"] = "center"
        self.label_teammates["text"] = "Teammates"
        self.label_teammates.place(
            x=10 * self.zoom,
            y=190 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.label_teammates_details = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=8 * self.zoom)
        self.label_teammates_details["font"] = self.ft
        self.label_teammates_details["fg"] = "#000000"
        self.label_teammates_details["justify"] = "center"
        self.label_teammates_details["text"] = "(email, first name, last name)"
        self.label_teammates_details.place(
            x=10 * self.zoom,
            y=220 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_teammates_1 = tk.Entry(self.root)
        self.entry_teammates_1["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_teammates_1["font"] = self.ft
        self.entry_teammates_1["fg"] = "#000000"
        self.entry_teammates_1["justify"] = "center"
        self.entry_teammates_1.place(
            x=160 * self.zoom,
            y=190 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_teammates_1 = self.entry_teammates_1

        self.entry_teammates_2 = tk.Entry(self.root)
        self.entry_teammates_2["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_teammates_2["font"] = self.ft
        self.entry_teammates_2["fg"] = "#000000"
        self.entry_teammates_2["justify"] = "center"
        self.entry_teammates_2.place(
            x=160 * self.zoom,
            y=215 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_teammates_2 = self.entry_teammates_2

        self.entry_teammates_3 = tk.Entry(self.root)
        self.entry_teammates_3["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_teammates_3["font"] = self.ft
        self.entry_teammates_3["fg"] = "#000000"
        self.entry_teammates_3["justify"] = "center"
        self.entry_teammates_3.place(
            x=160 * self.zoom,
            y=240 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_teammates_3 = self.entry_teammates_3

        self.entry_teammates_4 = tk.Entry(self.root)
        self.entry_teammates_4["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_teammates_4["font"] = self.ft
        self.entry_teammates_4["fg"] = "#000000"
        self.entry_teammates_4["justify"] = "center"
        self.entry_teammates_4.place(
            x=160 * self.zoom,
            y=265 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_teammates_4 = self.entry_teammates_4

        self.entry_teammates_5 = tk.Entry(self.root)
        self.entry_teammates_5["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_teammates_5["font"] = self.ft
        self.entry_teammates_5["fg"] = "#000000"
        self.entry_teammates_5["justify"] = "center"
        self.entry_teammates_5.place(
            x=160 * self.zoom,
            y=290 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_teammates_5 = self.entry_teammates_5

        self.label_app_owner = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_app_owner["font"] = self.ft
        self.label_app_owner["fg"] = "#000000"
        self.label_app_owner["justify"] = "center"
        self.label_app_owner["text"] = "Application Owner Email"
        self.label_app_owner.place(
            x=10 * self.zoom,
            y=320 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_app_owner = tk.Entry(self.root)
        self.entry_app_owner["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_app_owner["font"] = self.ft
        self.entry_app_owner["fg"] = "#000000"
        self.entry_app_owner["justify"] = "center"
        self.entry_app_owner.place(
            x=160 * self.zoom,
            y=320 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_app_owner = self.entry_app_owner

        self.label_bus_contact = tk.Label(self.root)
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.label_bus_contact["font"] = self.ft
        self.label_bus_contact["fg"] = "#000000"
        self.label_bus_contact["justify"] = "center"
        self.label_bus_contact["text"] = "Business Contact Email"
        self.label_bus_contact.place(
            x=10 * self.zoom,
            y=350 * self.zoom,
            width=140 * self.zoom,
            height=25 * self.zoom,
        )

        self.entry_bus_contact = tk.Entry(self.root)
        self.entry_bus_contact["borderwidth"] = "1px"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.entry_bus_contact["font"] = self.ft
        self.entry_bus_contact["fg"] = "#000000"
        self.entry_bus_contact["justify"] = "center"
        self.entry_bus_contact.place(
            x=160 * self.zoom,
            y=350 * self.zoom,
            width=300 * self.zoom,
            height=25 * self.zoom,
        )
        self.entry_bus_contact = self.entry_bus_contact

        self.button_create = tk.Button(self.root)
        self.button_create["bg"] = "#6b6b6b"
        self.ft = tkFont.Font(family="Times", size=10 * self.zoom)
        self.button_create["font"] = self.ft
        self.button_create["fg"] = "#ffffff"
        self.button_create["justify"] = "center"
        self.button_create["text"] = "Create"
        self.button_create.place(
            x=480 * self.zoom,
            y=350 * self.zoom,
            width=70 * self.zoom,
            height=25 * self.zoom,
        )
        self.button_create["command"] = self.command_create

        self.display = True

    def command_shared(self):
        """
        Enables and disables the rights fields for a Shared Service subscription.
        """

        self.display_fields()
        self.service = "shared_subdomain"

        self.entry_username.config(state="normal")
        self.entry_username.delete(0, tk.END)

        self.entry_password.config(state="normal")
        self.entry_password.delete(0, tk.END)

        self.entry_ip.config(state="normal")
        self.entry_ip.delete(0, tk.END)
        self.entry_ip.insert(0, "149.72.22.107")
        self.entry_ip.config(state="readonly")

        self.entry_plan.config(state="normal")
        self.entry_plan.delete(0, tk.END)
        self.entry_plan.insert(0, "50000")
        self.entry_plan.config(state="readonly")

        self.entry_subdomain.config(state="normal")
        self.entry_subdomain.delete(0, tk.END)
        self.entry_subdomain.insert(0, "app.saint-gobain.com")
        self.entry_subdomain.config(state="readonly")

        self.entry_teammates_1.config(state="normal")
        self.entry_teammates_1.delete(0, tk.END)
        self.entry_teammates_1.config(state="readonly")

        self.entry_teammates_2.config(state="normal")
        self.entry_teammates_2.delete(0, tk.END)
        self.entry_teammates_2.config(state="readonly")

        self.entry_teammates_3.config(state="normal")
        self.entry_teammates_3.delete(0, tk.END)
        self.entry_teammates_3.config(state="readonly")

        self.entry_teammates_4.config(state="normal")
        self.entry_teammates_4.delete(0, tk.END)
        self.entry_teammates_4.config(state="readonly")

        self.entry_teammates_5.config(state="normal")
        self.entry_teammates_5.delete(0, tk.END)
        self.entry_teammates_5.config(state="readonly")

        self.entry_app_owner.config(state="normal")
        self.entry_app_owner.delete(0, tk.END)

        self.entry_bus_contact.config(state="normal")
        self.entry_bus_contact.delete(0, tk.END)

        self.radio_shared["background"] = "green"
        self.radio_centrally["background"] = "light grey"
        self.radio_locally["background"] = "light grey"

    def command_centrally(self):
        """
        Enables and disables the fields for a Centrally Managed subscription.
        """

        self.display_fields()
        self.service = "centrally_managed"

        self.entry_username.config(state="normal")
        self.entry_username.delete(0, tk.END)

        self.entry_password.config(state="normal")
        self.entry_password.delete(0, tk.END)

        self.entry_ip.config(state="normal")
        self.entry_ip.delete(0, tk.END)

        self.entry_plan.config(state="normal")
        self.entry_plan.delete(0, tk.END)

        self.entry_subdomain.config(state="normal")
        self.entry_subdomain.delete(0, tk.END)

        self.entry_teammates_1.config(state="normal")
        self.entry_teammates_1.delete(0, tk.END)

        self.entry_teammates_2.config(state="normal")
        self.entry_teammates_2.delete(0, tk.END)

        self.entry_teammates_3.config(state="normal")
        self.entry_teammates_3.delete(0, tk.END)

        self.entry_teammates_4.config(state="normal")
        self.entry_teammates_4.delete(0, tk.END)

        self.entry_teammates_5.config(state="normal")
        self.entry_teammates_5.delete(0, tk.END)

        self.entry_app_owner.config(state="normal")
        self.entry_app_owner.delete(0, tk.END)

        self.entry_bus_contact.config(state="normal")
        self.entry_bus_contact.delete(0, tk.END)

        self.radio_shared["background"] = "light grey"
        self.radio_centrally["background"] = "green"
        self.radio_locally["background"] = "light grey"

    def command_locally(self):
        """
        Enables and disables the fields for a Locally Managed subscription.
        """

        self.display_fields()
        self.service = "locally_managed"

        self.entry_username.config(state="normal")
        self.entry_username.delete(0, tk.END)

        self.entry_password.config(state="normal")
        self.entry_password.delete(0, tk.END)

        self.entry_ip.config(state="normal")
        self.entry_ip.delete(0, tk.END)

        self.entry_plan.config(state="normal")
        self.entry_plan.delete(0, tk.END)

        self.entry_subdomain.config(state="normal")
        self.entry_subdomain.delete(0, tk.END)

        self.entry_teammates_1.config(state="normal")
        self.entry_teammates_1.delete(0, tk.END)

        self.entry_teammates_2.config(state="normal")
        self.entry_teammates_2.delete(0, tk.END)

        self.entry_teammates_3.config(state="normal")
        self.entry_teammates_3.delete(0, tk.END)

        self.entry_teammates_4.config(state="normal")
        self.entry_teammates_4.delete(0, tk.END)

        self.entry_teammates_5.config(state="normal")
        self.entry_teammates_5.delete(0, tk.END)

        self.entry_app_owner.config(state="normal")
        self.entry_app_owner.delete(0, tk.END)

        self.entry_bus_contact.config(state="normal")
        self.entry_bus_contact.delete(0, tk.END)

        self.radio_shared["background"] = "light grey"
        self.radio_centrally["background"] = "light grey"
        self.radio_locally["background"] = "green"

    def command_create(self):
        """
        Is activated when the "Create" button is pressed. Starts all steps and functions of the script.
        """

        print(f"--- START --- ({self.service})\n")
        self.get_api_key()
        if (
            self.check_inputs()
            and not self.check_used_username()
            and not self.check_used_teammate()
        ):
            self.post_subuser()
            self.put_credits()
            self.store_subuser()
            self.assign_domain()
            self.create_api_key()
            if self.service != "locally_managed":
                self.store_api_key()
            if self.service != "shared_subdomain":
                if self.service == "centrally_managed":
                    self.create_teammates_read_only()
                if self.service == "locally_managed":
                    self.create_teammates_restricted_access()
            self.setup_alerts()
            self.validation_test()
            if self.service == "locally_managed":
                self.delete_subuser_api_key()

            self.popup("STATUS: End of process.")
            # TODO: wipe data function before creating another subuser
        print("--- END --- \n")

    def popup(self, message):
        """
        Creates a popup with a message.
        """

        popup = tk.Toplevel()

        # Create a label to display the message
        label = tk.Label(popup, text=message)
        label.pack(padx=10, pady=10)

        # Create a button to close the popup
        button = tk.Button(popup, text="Close", command=popup.destroy)
        button.pack()

        popup.width = 300
        popup.height = 70
        popup.alignstr = "%dx%d+%d+%d" % (
            popup.width,
            popup.height,
            (self.screenwidth - popup.width) / 2,
            (self.screenheight - popup.height) / 2,
        )
        popup.geometry(popup.alignstr)

    def check_inputs(self) -> bool:
        """
        Checks the fields' content to verify that all fields are filled.
        Also checks if the IP address format and Teammate format is correct.
        """

        print("STEP: Checking inputs content")
        print("- START: check_inputs()")

        if self.service == "null":
            self.popup("ERROR: Select a subscription type.")
            return False
        if (
            not self.entry_username.get()
            or self.entry_username.get() == ""
            or not self.entry_password.get()
            or self.entry_password.get() == ""
            or not self.entry_ip.get()
            or self.entry_ip.get() == ""
            or not self.entry_plan.get()
            or self.entry_plan.get() == ""
            or not self.entry_subdomain.get()
            or self.entry_subdomain.get() == ""
        ):
            self.popup("ERROR: Missing data.")
            return False
        if self.entry_ip.get().count(".") != 3:
            self.popup(
                "ERROR: Wrong data format in IP field. Must be a valid IP address format using dots."
            )
            return False
        if (
            (
                (self.entry_teammates_1.get().count(",") != 2)
                and (self.entry_teammates_1.get() != "")
            )
            or (
                (self.entry_teammates_2.get().count(",") != 2)
                and (self.entry_teammates_2.get() != "")
            )
            or (
                (self.entry_teammates_3.get().count(",") != 2)
                and (self.entry_teammates_3.get() != "")
            )
            or (
                (self.entry_teammates_4.get().count(",") != 2)
                and (self.entry_teammates_4.get() != "")
            )
            or (
                (self.entry_teammates_5.get().count(",") != 2)
                and (self.entry_teammates_5.get() != "")
            )
        ):
            self.popup(
                "ERROR: Wrong data format in Teammate field. Must use commas to separate ."
            )
            return False

        print("- SUCCESS: check_inputs() \n")
        return True

    def check_used_username(self) -> bool:
        """
        Checks if the username value already exists.
        """

        print("STEP: Checking if the username is available")
        print("- START: check_used_username()")

        # Check for existing username
        url = "https://api.sendgrid.com/v3/subusers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            for subuser in data:
                for field in subuser:
                    if self.entry_username.get() == subuser[field]:
                        self.popup("ERROR: Username already used.")
                        return True

        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

        print("- SUCCESS: check_used_username() \n")
        return False

    def check_used_teammate(self) -> bool:
        """
        Checks if the teammate value already exists.
        """

        print("STEP: Checking if the teammate is available")
        print("- START: check_used_teammate()")

        url = "https://api.sendgrid.com/v3/subusers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            subusers = response.json()

            for subuser in subusers:
                url = "https://api.sendgrid.com/v3/teammates"
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "on-behalf-of": subuser["username"],
                }

                try:
                    response = requests.get(url=url, headers=headers)
                    response.raise_for_status()
                    teammates = response.json()
                except requests.exceptions.HTTPError as errh:
                    print(f"Http Error: {errh} \n")
                    print(response.text)
                except requests.exceptions.ConnectionError as errc:
                    print(f"Error Connecting: {errc} \n")
                    print(response.text)
                except requests.exceptions.Timeout as errt:
                    print(f"Timeout Error: {errt} \n")
                    print(response.text)
                except requests.exceptions.RequestException as err:
                    print(f"Oops: Something Else {err} \n")
                    print(response.text)

                for teammate in teammates["result"]:
                    if (self.entry_teammates_1.get()) and (
                        self.entry_teammates_1 != ""
                    ):
                        teammate1 = self.entry_teammates_1.get()
                        teammate1 = teammate1.replace("(", "")
                        teammate1 = teammate1.replace(")", "")
                        teammate1 = teammate1.replace(" ", "")
                        teammate1 = teammate1.split(",")
                        if teammate["email"] == teammate1[0]:
                            print(f"- ERROR: {teammate1[0]} is already used. \n")
                            self.popup(f"ERROR: {teammate1[0]} is already used.")
                            return True
                    if (self.entry_teammates_2.get()) and (
                        self.entry_teammates_2 != ""
                    ):
                        teammate2 = self.entry_teammates_2.get()
                        teammate2 = teammate2.replace("(", "")
                        teammate2 = teammate2.replace(")", "")
                        teammate2 = teammate2.replace(" ", "")
                        teammate2 = teammate2.split(",")
                        if teammate["email"] == teammate2[0]:
                            print(f"- ERROR: {teammate2[0]} is already used. \n")
                            self.popup(f"ERROR: {teammate2[0]} is already used.")
                            return True
                    if (self.entry_teammates_3.get()) and (
                        self.entry_teammates_3 != ""
                    ):
                        teammate3 = self.entry_teammates_3.get()
                        teammate3 = teammate3.replace("(", "")
                        teammate3 = teammate3.replace(")", "")
                        teammate3 = teammate3.replace(" ", "")
                        teammate3 = teammate3.split(",")
                        if teammate["email"] == teammate3[0]:
                            print(f"- ERROR: {teammate3[0]} is already used. \n")
                            self.popup(f"ERROR: {teammate3[0]} is already used.")
                            return True
                    if (self.entry_teammates_4.get()) and (
                        self.entry_teammates_4 != ""
                    ):
                        teammate4 = self.entry_teammates_4.get()
                        teammate4 = teammate4.replace("(", "")
                        teammate4 = teammate4.replace(")", "")
                        teammate4 = teammate4.replace(" ", "")
                        teammate4 = teammate4.split(",")
                        if teammate["email"] == teammate4[0]:
                            print(f"- ERROR: {teammate4[0]} is already used. \n")
                            self.popup(f"ERROR: {teammate4[0]} is already used.")
                            return True
                    if (self.entry_teammates_5.get()) and (
                        self.entry_teammates_5 != ""
                    ):
                        teammate5 = self.entry_teammates_5.get()
                        teammate5 = teammate5.replace("(", "")
                        teammate5 = teammate5.replace(")", "")
                        teammate5 = teammate5.replace(" ", "")
                        teammate5 = teammate5.split(",")
                        if teammate["email"] == teammate5[0]:
                            print(f"- ERROR: {teammate5[0]} is already used. \n")
                            self.popup(f"ERROR: {teammate5[0]} is already used.")
                            return True

        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

        print("- SUCCESS: check_used_teammate() \n")
        return False

    def get_api_key(self):
        """
        Retrieve the script's API key from SendGrid's dedicated KeePass.
        """

        print("STEP: Retrieving the script API key")
        print("- START: get_api_key()")

        # Get KeePass' password from the encrypted file
        dir = os.path.dirname(__file__)
        filepath = os.path.join(dir, "sendgrid_keepass_password_key")
        with open(filepath, "rb") as key_file:
            key = key_file.read()

        filepath = os.path.join(dir, "sendgrid_keepass_password")
        with open(filepath, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        f = Fernet(key)
        decrypted_data = f.decrypt(encrypted_data)

        self.keepass_password = decrypted_data.decode()

        # Open the KeePass
        filepath = os.path.join(dir, "sendgrid_keepass.kdbx")
        keepass = PyKeePass(filepath, self.keepass_password)

        # Get the API Key from the KeePass
        entry = keepass.find_entries(title="sendgrid-portal", first=True)
        self.api_key = entry.password
        print("- SUCCESS: get_api_key() \n")

    def post_subuser(self):
        """
        Creates a new SubUser.
        """

        print("STEP: Creating the subuser")
        print("- START: post_subuser()")

        url = "https://api.sendgrid.com/v3/subusers"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "username": self.entry_username.get(),
            "email": "sgem.report@saint-gobain.com",
            "ips": [self.entry_ip.get()],
            "password": self.entry_password.get(),
        }
        try:
            response = requests.post(url=url, headers=headers, json=body)
            response.raise_for_status()
            print("- SUCCESS: post_subuser() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

    def put_credits(self):
        """
        Sets the recurring credits value for the SubUser.
        """

        print("STEP: Setting credits")
        print("- START: put_credits()")

        url = (
            "https://api.sendgrid.com/v3/subusers/"
            + self.entry_username.get()
            + "/credits"
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "type": "recurring",
            "reset_frequency": "monthly",
            "total": self.entry_plan.get(),
        }
        try:
            response = requests.put(url=url, headers=headers, json=body)
            response.raise_for_status()
            print("- SUCCESS: put_credits() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

    def store_subuser(self):
        """
        Stores the SubUser's data in SendGrid's KeePass.
        """

        print("STEP: Storing subuser in KeePass")
        print("- START: store_subuser()")

        dir = os.path.dirname(__file__)
        keepass_path = os.path.join(dir, "sendgrid_keepass.kdbx")
        self.keepass = PyKeePass(keepass_path, password=self.keepass_password)
        try:
            self.keepass.add_entry(
                destination_group=self.keepass.root_group,
                title=self.entry_username.get(),
                username=self.entry_username.get(),
                password=self.entry_password.get(),
                icon="5",
                url="https://app.sendgrid.com/",
            )
            self.keepass.save()
            print("- SUCCESS: store_subuser() \n")
        except Exception as e:
            print(f"ERROR: {e} \n")

    def assign_domain(self):
        """
        Assignes the SubDomain to the SubUser.
        """

        print("STEP: Assigning subdomain")
        print("- START: assign_domain()")

        # Get self.domain_id from self.entry_subdomain.get()
        url = "https://api.sendgrid.com/v3/whitelabel/domains"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            for d in data:
                if d["domain"] == self.entry_subdomain.get():
                    self.domain_id = d["id"]
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

        # Assign domain using self.domain_id:
        url = f"https://api.sendgrid.com/v3/whitelabel/domains/{self.domain_id}/subuser"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        body = {"username": self.entry_username.get()}
        try:
            response = requests.post(url=url, headers=headers, json=body)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            print("- SUCCESS: assign_domain() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

    def create_api_key(self):
        """
        Creates an API key for the SubUser.
        """

        print("STEP: Creating subuser's API key")
        print("- START: create_api_key()")

        url = "https://api.sendgrid.com/v3/api_keys"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "on-behalf-of": self.entry_username.get(),
        }
        body = {"name": self.entry_username.get() + "-API01"}

        try:
            response = requests.post(url=url, headers=headers, json=body)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            self.subuser_api_key = data["api_key"]
            self.subuser_api_key_name = data["name"]
            self.subuser_api_key_id = data["api_key_id"]
            print("- SUCCESS: create_api_key() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

    def store_api_key(self):
        """
        Stores the SubUser's API key in SendGrid's KeePass.
        """

        print("STEP: Storing subuser's API key")
        print("- START: store_api_key()")

        dir = os.path.dirname(__file__)
        keepass_path = os.path.join(dir, "sendgrid_keepass.kdbx")
        self.keepass = PyKeePass(keepass_path, password=self.keepass_password)
        try:
            self.keepass.add_entry(
                destination_group=self.keepass.root_group,
                title=self.subuser_api_key_name,
                username=self.subuser_api_key_name,
                password=self.subuser_api_key,
                icon="0",
            )
            self.keepass.save()
            print("- SUCCESS: store_api_key() \n")
        except Exception as e:
            print(f"ERROR: {e} \n")

    def create_teammates_read_only(self):
        """
        Creates new Teammates with Read-Only access for the SubUser.
        """

        print("STEP: Creating Read-Only teammates")
        print("- START: create_teammates_read_only()")

        url = "https://api.sendgrid.com/v3/sso/teammates"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "on-behalf-of": self.entry_username.get(),
        }
        scopes = [
            "alerts.read",
            "asm.groups.read",
            "ips.warmup.read",
            "ips.pools.read",
            "ips.pools.ips.read",
            "ips.read",
            "mail_settings.read",
            "mail_settings.bcc.read",
            "mail_settings.address_whitelist.read",
            "mail_settings.footer.read",
            "mail_settings.forward_spam.read",
            "mail_settings.plain_content.read",
            "mail_settings.spam_check.read",
            "mail_settings.bounce_purge.update",
            "mail_settings.forward_bounce.read",
            "partner_settings.read",
            "partner_settings.new_relic.read",
            "partner_settings.sendwithus.read",
            "tracking_settings.read",
            "tracking_settings.click.read",
            "tracking_settings.subscription.read",
            "tracking_settings.open.read",
            "tracking_settings.google_analytics.read",
            "user.webhooks.event.settings.read",
            "user.webhooks.event.test.read",
            "user.webhooks.parse.settings.read",
            "stats.read",
            "stats.global.read",
            "categories.stats.read",
            "categories.stats.sums.read",
            "devices.stats.read",
            "clients.stats.read",
            "clients.phone.stats.read",
            "clients.tablet.stats.read",
            "clients.webmail.stats.read",
            "clients.desktop.stats.read",
            "geo.stats.read",
            "mailbox_providers.stats.read",
            "browsers.stats.read",
            "user.webhooks.parse.stats.read",
            "templates.read",
            "templates.versions.read",
            "user.account.read",
            "user.credits.read",
            "user.email.read",
            "user.profile.read",
            "user.profile.update",
            "user.timezone.read",
            "user.username.read",
            "user.settings.enforced_tls.read",
            "api_keys.read",
            "categories.read",
            "mail_settings.template.read",
            "mail.batch.read",
            "user.scheduled_sends.read",
            "access_settings.whitelist.read",
            "access_settings.activity.read",
            "suppression.read",
            "messages.read",
            "email_testing.read",
            # "sender_verification_eligible",
            # "2fa_exempt",
            # "2fa_required",
        ]

        if (self.entry_teammates_1.get()) and (self.entry_teammates_1 != ""):
            teammate1 = self.entry_teammates_1.get()
            teammate1 = teammate1.replace("(", "")
            teammate1 = teammate1.replace(")", "")
            teammate1 = teammate1.replace(" ", "")
            teammate1 = teammate1.split(",")

            body = {
                "email": teammate1[0],
                "first_name": teammate1[1],
                "last_name": teammate1[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_2.get()) and (self.entry_teammates_2 != ""):
            teammate2 = self.entry_teammates_2.get()
            teammate2 = teammate2.replace("(", "")
            teammate2 = teammate2.replace(")", "")
            teammate2 = teammate2.replace(" ", "")
            teammate2 = teammate2.split(",")

            body = {
                "email": teammate2[0],
                "first_name": teammate2[1],
                "last_name": teammate2[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_3.get()) and (self.entry_teammates_3 != ""):
            teammate3 = self.entry_teammates_3.get()
            teammate3 = teammate3.replace("(", "")
            teammate3 = teammate3.replace(")", "")
            teammate3 = teammate3.replace(" ", "")
            teammate3 = teammate3.split(",")

            body = {
                "email": teammate3[0],
                "first_name": teammate3[1],
                "last_name": teammate3[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_4.get()) and (self.entry_teammates_4 != ""):
            teammate4 = self.entry_teammates_4.get()
            teammate4 = teammate4.replace("(", "")
            teammate4 = teammate4.replace(")", "")
            teammate4 = teammate4.replace(" ", "")
            teammate4 = teammate4.split(",")

            body = {
                "email": teammate4[0],
                "first_name": teammate4[1],
                "last_name": teammate4[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_5.get()) and (self.entry_teammates_5 != ""):
            teammate5 = self.entry_teammates_5.get()
            teammate5 = teammate5.replace("(", "")
            teammate5 = teammate5.replace(")", "")
            teammate5 = teammate5.replace(" ", "")
            teammate5 = teammate5.split(",")

            body = {
                "email": teammate5[0],
                "first_name": teammate5[1],
                "last_name": teammate5[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        print("- SUCCESS: create_teammates_read_only() \n")

    def create_teammates_restricted_access(self):
        """
        Creates new Teammates with Restricted access for the SubUser.
        """

        print("STEP: Creating Restricted-Access teammates")
        print("- START: create_teammates_restricted_access()")

        url = "https://api.sendgrid.com/v3/sso/teammates"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "on-behalf-of": self.entry_username.get(),
        }

        scopes = [
            "alerts.create",
            "alerts.read",
            "alerts.update",
            "alerts.delete",
            "asm.groups.create",
            "asm.groups.read",
            "asm.groups.update",
            "asm.groups.delete",
            "ips.warmup.create",
            "ips.warmup.read",
            "ips.warmup.update",
            "ips.warmup.delete",
            "ips.pools.create",
            "ips.pools.read",
            "ips.pools.update",
            "ips.pools.delete",
            "ips.pools.ips.create",
            "ips.pools.ips.read",
            "ips.pools.ips.update",
            "ips.pools.ips.delete",
            "ips.read",
            "mail.send",
            "mail_settings.read",
            "mail_settings.bcc.read",
            "mail_settings.bcc.update",
            "mail_settings.address_whitelist.read",
            "mail_settings.address_whitelist.update",
            "mail_settings.footer.read",
            "mail_settings.footer.update",
            "mail_settings.forward_spam.read",
            "mail_settings.forward_spam.update",
            "mail_settings.plain_content.read",
            "mail_settings.plain_content.update",
            "mail_settings.spam_check.read",
            "mail_settings.spam_check.update",
            "mail_settings.bounce_purge.read",
            "mail_settings.bounce_purge.update",
            "mail_settings.forward_bounce.read",
            "mail_settings.forward_bounce.update",
            "partner_settings.read",
            "partner_settings.new_relic.read",
            "partner_settings.new_relic.update",
            "partner_settings.sendwithus.read",
            "partner_settings.sendwithus.update",
            "tracking_settings.read",
            "tracking_settings.click.read",
            "tracking_settings.click.update",
            "tracking_settings.subscription.read",
            "tracking_settings.subscription.update",
            "tracking_settings.open.read",
            "tracking_settings.open.update",
            "tracking_settings.google_analytics.read",
            "tracking_settings.google_analytics.update",
            "user.webhooks.event.settings.create",
            "user.webhooks.event.settings.read",
            "user.webhooks.event.settings.update",
            "user.webhooks.event.settings.delete",
            "user.webhooks.event.test.create",
            "user.webhooks.event.test.read",
            "user.webhooks.event.test.update",
            "user.webhooks.parse.settings.create",
            "user.webhooks.parse.settings.read",
            "user.webhooks.parse.settings.update",
            "user.webhooks.parse.settings.delete",
            "stats.read",
            "stats.global.read",
            "categories.stats.read",
            "categories.stats.sums.read",
            "devices.stats.read",
            "clients.stats.read",
            "clients.phone.stats.read",
            "clients.tablet.stats.read",
            "clients.webmail.stats.read",
            "clients.desktop.stats.read",
            "geo.stats.read",
            "mailbox_providers.stats.read",
            "browsers.stats.read",
            "templates.create",
            "templates.read",
            "templates.update",
            "templates.delete",
            "templates.versions.create",
            "templates.versions.read",
            "templates.versions.update",
            "templates.versions.delete",
            "templates.versions.activate.create",
            "user.account.read",
            "user.credits.read",
            "user.email.read",
            "user.profile.read",
            "user.profile.update",
            "user.timezone.read",
            "user.timezone.update",
            "user.username.read",
            "user.settings.enforced_tls.read",
            "user.settings.enforced_tls.update",
            "api_keys.create",
            "api_keys.read",
            "api_keys.update",
            "api_keys.delete",
            "categories.create",
            "categories.read",
            "categories.update",
            "categories.delete",
            "mail_settings.template.read",
            "mail_settings.template.update",
            "mail.batch.create",
            "mail.batch.read",
            "mail.batch.update",
            "mail.batch.delete",
            "user.scheduled_sends.create",
            "user.scheduled_sends.read",
            "user.scheduled_sends.update",
            "user.scheduled_sends.delete",
            "access_settings.whitelist.create",
            "access_settings.whitelist.read",
            "access_settings.whitelist.update",
            "access_settings.whitelist.delete",
            "access_settings.activity.read",
            "suppression.create",
            "suppression.read",
            "suppression.update",
            "suppression.delete",
            "messages.read",
            "design_library.read",
            "design_library.create",
            "design_library.update",
            "design_library.delete",
            "email_testing.read",
            "email_testing.write",
            # "sender_verification_eligible",
            # "2fa_exempt",
            # "2fa_required",
        ]

        if (self.entry_teammates_1.get()) and (self.entry_teammates_1 != ""):
            teammate1 = self.entry_teammates_1.get()
            teammate1 = teammate1.replace("(", "")
            teammate1 = teammate1.replace(")", "")
            teammate1 = teammate1.replace(" ", "")
            teammate1 = teammate1.split(",")

            body = {
                "email": teammate1[0],
                "first_name": teammate1[1],
                "last_name": teammate1[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_2.get()) and (self.entry_teammates_2 != ""):
            teammate2 = self.entry_teammates_2.get()
            teammate2 = teammate2.replace("(", "")
            teammate2 = teammate2.replace(")", "")
            teammate2 = teammate2.replace(" ", "")
            teammate2 = teammate2.split(",")

            body = {
                "email": teammate2[0],
                "first_name": teammate2[1],
                "last_name": teammate2[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_3.get()) and (self.entry_teammates_3 != ""):
            teammate3 = self.entry_teammates_3.get()
            teammate3 = teammate3.replace("(", "")
            teammate3 = teammate3.replace(")", "")
            teammate3 = teammate3.replace(" ", "")
            teammate3 = teammate3.split(",")

            body = {
                "email": teammate3[0],
                "first_name": teammate3[1],
                "last_name": teammate3[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_4.get()) and (self.entry_teammates_4 != ""):
            teammate4 = self.entry_teammates_4.get()
            teammate4 = teammate4.replace("(", "")
            teammate4 = teammate4.replace(")", "")
            teammate4 = teammate4.replace(" ", "")
            teammate4 = teammate4.split(",")

            body = {
                "email": teammate4[0],
                "first_name": teammate4[1],
                "last_name": teammate4[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        if (self.entry_teammates_5.get()) and (self.entry_teammates_5 != ""):
            teammate5 = self.entry_teammates_5.get()
            teammate5 = teammate5.replace("(", "")
            teammate5 = teammate5.replace(")", "")
            teammate5 = teammate5.replace(" ", "")
            teammate5 = teammate5.split(",")

            body = {
                "email": teammate5[0],
                "first_name": teammate5[1],
                "last_name": teammate5[2],
                "scopes": scopes,
            }

            try:
                response = requests.post(url=url, headers=headers, json=body)
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print(f"Http Error: {errh} \n")
                print(response.text)
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc} \n")
                print(response.text)
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt} \n")
                print(response.text)
            except requests.exceptions.RequestException as err:
                print(f"Oops: Something Else {err} \n")
                print(response.text)

        print("- SUCCESS: create_teammates_restricted_access() \n")

    def setup_alerts(self):
        """
        Re-sets the default alert for the SubUser.
        """

        print("STEP: Setting the alerts")
        print("- START: setup_alerts()")

        # Get the alert id from the created subuser
        url = "https://api.sendgrid.com/v3/alerts"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "on-behalf-of": self.entry_username.get(),
        }

        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            data = response.json()
            alert_id = data[0]["id"]
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

        # Update the alert
        url = f"https://api.sendgrid.com/v3/alerts/{alert_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "on-behalf-of": self.entry_username.get(),
        }
        if self.entry_app_owner.get() and self.entry_bus_contact.get():
            body = {
                "email_to": f"sgem.report@saint-gobain.com, {self.entry_app_owner.get()}, {self.entry_bus_contact.get()}",
                "percentage": 80,
            }
        if self.entry_app_owner.get() and not self.entry_bus_contact.get():
            body = {
                "email_to": f"sgem.report@saint-gobain.com, {self.entry_app_owner.get()}",
                "percentage": 80,
            }
        if not self.entry_app_owner.get() and self.entry_bus_contact.get():
            body = {
                "email_to": f"sgem.report@saint-gobain.com, {self.entry_bus_contact.get()}",
                "percentage": 80,
            }
        if not self.entry_app_owner.get() and not self.entry_bus_contact.get():
            body = {
                "email_to": "sgem.report@saint-gobain.com",
                "percentage": 80,
            }

        try:
            response = requests.patch(url=url, headers=headers, json=body)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            print("- SUCCESS: setup_alerts() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

    def validation_test(self):
        """
        Executes a validation test to confirm the SubUser creation and the working status of it's API key.
        Sends a mail from the SubUser username and SubDomain name to the SendGrid team.
        """

        print("STEP: Validating the subuser's API key")
        print("- START: validation_test()")

        # Send a mail using the Subuser's API Key and show its details
        url = "https://api.sendgrid.com/v3/mail/send"
        headers = {"Authorization": f"Bearer {self.subuser_api_key}"}
        body = {
            "personalizations": [
                {
                    "to": [
                        # TODO: Replace comments before deploy
                        # {"email": "DL-Workplace-CloudSMTPService@saint-gobain.com"},
                        {"email": "gilles.meunier@saint-gobain.com"},
                    ],
                },
            ],
            "from": {
                "email": f"{self.entry_username.get()}@{self.entry_subdomain.get()}"
            },
            "subject": f"Subuser creation - {self.entry_username.get()}",
            "content": [
                {
                    "type": "text/plain",
                    "value": f"Validation test is succesful for {self.entry_username.get()} subscription.",
                }
            ],
        }

        try:
            response = requests.post(url=url, headers=headers, json=body)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            print("- SUCCESS: validation_test() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)

    def delete_subuser_api_key(self):
        """
        Deletes the previously created SubUser's API key.
        """

        print("STEP: Deleting the subuser's API key")
        print("- START: delete_subuser_api_key()")

        url = f"https://api.sendgrid.com/v3/api_keys/{self.subuser_api_key_id}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "on-behalf-of": self.entry_username.get(),
        }

        try:
            response = requests.delete(url=url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            print("- SUCCESS: delete_subuser_api_key() \n")
        except requests.exceptions.HTTPError as errh:
            print(f"Http Error: {errh} \n")
            print(response.text)
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc} \n")
            print(response.text)
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt} \n")
            print(response.text)
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else {err} \n")
            print(response.text)


if __name__ == "__main__":
    """
    Starts the App.__init__() function when the file is executed.
    """

    app = App()
