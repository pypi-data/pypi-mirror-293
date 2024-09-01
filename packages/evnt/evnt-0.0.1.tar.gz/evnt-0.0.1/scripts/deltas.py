#!/bin/env python
from pathlib import Path

import evnt



def print_components():
    csmip_archive = Path("dat/58658_007_20210426_10.09.54.P.zip")

    station = evnt.csmip.read_event(csmip_archive)

    for motion in station.motions.values():
        print(motion)
        for name,component in motion.components.items():
            print("\t", name)
            peak_accel = component.accel["peak_value"]
            peak_time  = component.accel["peak_time"]
            print(f"\t\tpeak accel: {peak_accel} (time = {peak_time})")
            print("\t\t", component.accel.data[0])





if __name__ == "__main__":
    print_components()





