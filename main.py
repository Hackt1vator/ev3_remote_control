from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent
from ev3dev2.sensor.lego import TouchSensor

# Motoren initialisieren
motor_a = LargeMotor(OUTPUT_A)
motor_b = LargeMotor(OUTPUT_B)

# Touch Sensor initialisieren
touch_sensor = TouchSensor()

# Funktion zum Vorwärtsfahren
def vorwaerts():
    motor_a.on_for_seconds(SpeedPercent(50), 2)
    motor_b.on_for_seconds(SpeedPercent(50), 2)

# Funktion zum Anhalten
def anhalten():
    motor_a.off()
    motor_b.off()

# Hauptprogramm
try:
    while not touch_sensor.is_pressed:
        vorwaerts()
    anhalten()

except KeyboardInterrupt:
    anhalten()


