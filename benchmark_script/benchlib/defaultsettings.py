#!/usr/bin/env python3
import os
import sys


def get_default_settings():

    settings = {}
    settings["target"] = []
    settings["template"] = "./fio-job-template.fio"
    settings["engine"] = "/home/ubuntu/spdk/build/fio/spdk_nvme"
    settings["mode"] = ["write"]
    settings["iodepth"] = [1, 2, 4, 8, 16, 32]
    settings["numjobs"] = [1, 2]
    settings["block_size"] = ["512", "4096", "65536"]
    settings["direct"] = 1
    settings["size"] = None
    settings["precondition"] = False
    settings["precondition_template"] = "precondition.fio"
    settings["precondition_repeat"] = False
    settings["entire_device"] = False
    settings["ss"] = False
    settings["ss_dur"] = None
    settings["ss_ramp"] = None
    settings["rwmixread"] = None
    settings["runtime"] = 60
    settings["loops"] = 1
    settings["time_based"] = False
    settings["extra_opts"] = []
    settings["loginterval"] = 500
    settings["mixed"] = []
    settings["invalidate"] = 1
    settings["loop_items"] = [
        "mode",
        "iodepth",
        "numjobs",
        "block_size",
    ]
    settings["filter_items"] = [
        "filter_items",
        "loop_items",
        "dry_run",
        "mixed",
        "quiet",
    ]
    return settings


def check_settings(settings):
    """Some basic error handling."""
    if not os.path.exists(settings["template"]):
        print()
        print(f"The specified template {settings['template']} does not exist.")
        print()
        sys.exit(6)

    # if settings["type"] != "device" and not settings["size"]:
    #     print()
    #     print("When the target is a file or directory, --size must be specified.")
    #     print()
    #     sys.exit(4)

    if settings["type"] == "directory":
        for item in settings["target"]:
            if not os.path.exists(item):
                print(
                    f"\nThe target directory ({item}) doesn't seem to exist.\n")
                sys.exit(5)

    for mode in settings["mode"]:
        if mode in settings["mixed"]:
            if settings["rwmixread"]:
                settings["loop_items"].append("rwmixread")
            else:
                print(
                    "\nIf a mixed (read/write) mode is specified, please specify --rwmixread\n"
                )
                sys.exit(6)
        else:
            settings["filter_items"].append("rwmixread")
