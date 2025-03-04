import csv
from datetime import datetime, timezone
import random
import time

random.seed(40351)

AZ_STEP = 10
EL_STEP = 10

# AZ_STEP = 1
# EL_STEP = 1


def calc_amplitude(azimuth, elevation):
    distance = (azimuth**2 + elevation**2) ** 0.5
    # return distance
    return -50 - distance * 1 + random.gauss(0, 5)


def generate_fake_data(delay, filename):
    azimuth = -80
    azimuth_direction = AZ_STEP
    elevation = -80
    elevation_direction = EL_STEP
    amplitude = calc_amplitude(azimuth, elevation)
    cut_index = 0  # Initialize cut_index

    # Write header
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "index",
                "timestamp",
                "azimuth",
                "elevation",
                "amplitude",
                "cut_index",
            ],
            dialect="unix",
        )
        writer.writeheader()

    index = 0
    while True:
        timestamp = datetime.now(timezone.utc).isoformat()
        amplitude = calc_amplitude(azimuth, elevation)
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "index",
                    "timestamp",
                    "azimuth",
                    "elevation",
                    "amplitude",
                    "cut_index",
                ],
                dialect="unix",
            )
            data = {
                "index": index,
                "timestamp": timestamp,
                "azimuth": azimuth,
                "elevation": elevation,
                "amplitude": amplitude,
                "cut_index": cut_index,  # Add cut_index to data
            }
            print(f"[{index=}] Writing {data}")
            writer.writerow(data)

        azimuth += azimuth_direction
        if azimuth > 80 or azimuth < -80:
            azimuth_direction *= -1
            azimuth += azimuth_direction
            elevation += elevation_direction
            cut_index += 1  # Increment cut_index when elevation changes
            if elevation > 80 or elevation < -80:
                elevation_direction *= -1
                elevation += elevation_direction

        index += 1
        time.sleep(delay)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        delay = float(sys.argv[1])
    else:
        delay = 2.5
    filename = "./data/fake_data.csv"
    generate_fake_data(delay, filename)
    print(f"Generating data indefinitely and saving to {filename}")
