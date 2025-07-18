from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage
import time
import math
import random

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\samyn\Desktop\IC New Deign\build\build\assets\frame0")
RPM_ASSETS = OUTPUT_PATH / Path(r"C:\Users\samyn\Desktop\IC New Deign\build\build\assets\frame0\speed")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_rpm_assets(path: str) -> Path:
    return RPM_ASSETS / Path(path)

# Function to update the timer
def update_timer():
    global start_time
    current_time = time.time() - start_time
    minutes, seconds = divmod(int(current_time), 60)
    hours, minutes = divmod(minutes, 60)
    time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    canvas.itemconfig(timer_text, text=time_str)
    window.after(1000, update_timer)

def update_rpm_text_loc(rpm_value):
    if   rpm_value < 10:
        canvas.coords(engine_rpm, 215.2299993634224, 209.8755645751953)
    else:
        canvas.coords(engine_rpm, 179.2299993634224, 209.8755645751953)
    canvas.itemconfig(engine_rpm, text=str(rpm_value))

# Function to update RPM text with sinusoidal oscillation
def update_rpm_text():
    global start_time
    current_time = time.time() - start_time
    period = 5  # seconds for one complete oscillation
    amplitude = 14  # peak RPM value

    # Calculate RPM value using sine wave
    rpm_value = amplitude * (math.sin((2 * math.pi / period) * current_time) + 1) / 2

    # Round the value to ensure it reaches 14
    rpm_value = round(rpm_value)

    # Adjust position based on RPM value length
    update_rpm_text_loc(rpm_value)

    # Update RPM image based on rpm_value
    if rpm_value == 0:
        canvas.itemconfig(rpm_image_item, state='hidden')  # Hide the image when RPM is 0
    else:
        image_path = relative_to_rpm_assets(f"image_{rpm_value}.png")
        rpm_image = PhotoImage(file=image_path)
        canvas.itemconfig(rpm_image_item, image=rpm_image)
        canvas.rpm_image = rpm_image  # Prevent garbage collection
        canvas.itemconfig(rpm_image_item, state='normal')

    window.after(100, update_rpm_text)

# Function to update odometer text with dynamic positioning
def update_odometer_value(odometer_value):
    if odometer_value < 10:
        canvas.coords(odometer, 750.0, 105.00528717041016)
    else:
        canvas.coords(odometer, 715.0, 105.00528717041016)
    canvas.itemconfig(odometer, text=str(odometer_value))

# Function to update speed text with dynamic positioning
def update_speed_value(speed_value):
    if speed_value > 99:
        canvas.coords(speed_text, 389.7893647402525, 334.1695556640625)
    elif speed_value > 9:
        canvas.coords(speed_text, 420.7893647402525, 334.1695556640625)
    else:
        canvas.coords(speed_text, 450.7893647402525, 334.1695556640625)
    canvas.itemconfig(speed_text, text=str(speed_value))

# Function to update coolant temperature text with random values
def update_coolant_temperature():
    coolant_temp_value = random.randint(70, 120)
    canvas.itemconfig(coolant_temperature, text=f"{coolant_temp_value} c")
    window.after(1000, update_coolant_temperature)

# Function to update engine temperature text with random values
def update_engine_temperature():
    engine_temp_value = random.randint(20, 30)
    canvas.itemconfig(engine_temp_value_text, text=str(engine_temp_value))
    window.after(1000, update_engine_temperature)

# Function to update RPM, odometer, speed, coolant temperature, and engine temperature values
def update_values():
    odometer_value = random.randint(1, 99)
    speed_value = random.randint(0, 120)
    update_odometer_value(odometer_value)
    update_speed_value(speed_value)
    window.after(1000, update_values)

window = Tk()
window.geometry("800x480")
window.configure(bg="#FFFFFF")
window.overrideredirect(True)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=480,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(400.0, 240.0, image=image_image_1)

odometer = canvas.create_text(
    715.0, 105.00528717041016,
    anchor="nw",
    text="10",
    fill="#FFFFFF",
    font=("Inter", 63 * -1, "bold italic")
)

voltage = canvas.create_text(
    660.0, 197.415283203125,
    anchor="nw",
    text="12.2",
    fill="#FFFFFF",
    font=("Inter", 63 * -1, "bold italic")
)

coolant_temperature = canvas.create_text(
    552.3029013425112, 263.7500915527344,
    anchor="nw",
    text="105 c",
    fill="#FFFFFF",
    font=("Inter", 30 * -1, "bold italic")
)

engine_temp_value_text = canvas.create_text(
    710.3497271537781, 424.0625915527344,
    anchor="nw",
    text="25",
    fill="#FFFFFF",
    font=("Inter", 26 * -1, "bold italic")
)

engine_temp_subscript = canvas.create_text(
    745.3497271537781,
    421.0625915527344,
    anchor="nw",
    text="c",
    fill="#F24343",
    font=("Inter", 30 * -1, "bold italic")
)

timer_text = canvas.create_text(
    610.5551906526089, 24.599563598632812,
    anchor="nw",
    text="00:00:00",
    fill="#FFFFFF",
    font=("Inter", 44 * -1, "bold italic")
)

gear_position = canvas.create_text(
    23.95985282957554, 111.7099380493164,
    anchor="nw",
    text="N",
    fill="#37E148",
    font=("Inter", 52 * -1, "bold italic")
)

engine_rpm = canvas.create_text(
    179.2299993634224, 209.8755645751953,
    anchor="nw",
    text="0",
    fill="#FFFFFF",
    font=("Inter", 127 * -1, "bold italic")
)

speed_text = canvas.create_text(
    450.7893647402525, 334.1695556640625,
    anchor="nw",
    text="2",
    fill="#FFFFFF",
    font=("Inter", 103 * -1, "bold italic")
)

# Create an invisible image item for RPM images
rpm_image_item = canvas.create_image(400, 240, image=None)
canvas.itemconfig(rpm_image_item, state='hidden')  # Start as hidden

start_time = time.time()

update_timer()
update_values()
update_coolant_temperature()
update_engine_temperature()
update_rpm_text()

window.resizable(False, False)
window.mainloop()
