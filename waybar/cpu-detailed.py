#!/usr/bin/env python3



import json

import time

import os

import sys

from pathlib import Path



class CPUMonitor:

    def __init__(self):

        self.temp_cache = {"time": 0, "value": 0.0}

        self.prev_stats = {}

        self.thread_count = os.sysconf("SC_NPROCESSORS_ONLN")



    def get_cpu_data(self):

        try:

            with open("/proc/stat", "r") as f:

                lines = f.readlines()

            current_stats = {}

            per_core_pct = []

            total_pct = 0.0

            for line in lines:

                if line.startswith("cpu"):

                    parts = line.split()

                    name = parts[0]

                    times = [int(x) for x in parts[1:8]]

                    current_stats[name] = times

                    if name in self.prev_stats:

                        prev_times = self.prev_stats[name]

                        total_diff = sum(times) - sum(prev_times)

                        idle_diff = (times[3] + times[4]) - (prev_times[3] + prev_times[4])

                        if total_diff > 0:

                            usage = 100 * (total_diff - idle_diff) / total_diff

                            if name == "cpu": total_pct = usage

                            else: per_core_pct.append(usage)

                    else:

                        if name != "cpu": per_core_pct.append(0.0)

            self.prev_stats = current_stats

            return total_pct, per_core_pct

        except: return 0.0, [0.0] * self.thread_count



    def get_temperature(self):

        current_time = time.time()

        if current_time - self.temp_cache["time"] > 2:

            try:

                for hwmon in Path("/sys/class/hwmon").iterdir():

                    if (hwmon / "name").exists() and "k10temp" in (hwmon / "name").read_text():

                        temp_file = hwmon / "temp1_input"

                        if temp_file.exists():

                            self.temp_cache["value"] = float(temp_file.read_text()) / 1000.0

                            self.temp_cache["time"] = current_time

                            break

            except: self.temp_cache["value"] = 40.0

        return self.temp_cache["value"]



    def get_power(self, total_pct):

        """Tenta ler consumo real ou simula baseado no uso do Ryzen 5800X"""

        try:

            # Tenta caminhos comuns de drivers de energia no Arch

            for hwmon in Path("/sys/class/hwmon").iterdir():

                if (hwmon / "power1_input").exists():

                    return float((hwmon / "power1_input").read_text()) / 1000000.0

        except: pass

        # Fallback dinâmico: Idle (~30W) até Full Load (~105W-140W no 5800X)

        return 30.0 + (total_pct * 0.75)



    def format_tooltip(self, total_pct, per_core_pct, temp, power):

        tooltip = f"🔥 CPU Monitor - b0de's computer\n"

        tooltip += f"{'='*36}\n"

        # Watts de volta no Tooltip aqui:

        tooltip += f"📊 Total: {total_pct:.1f}% | 🌡️ {temp:.1f}°C | ⚡ {power:.1f}W\n\n"

        

        half = (len(per_core_pct) + 1) // 2

        for i in range(half):

            l_idx = i

            line = f"C{l_idx:02d}: {per_core_pct[l_idx]:>4.1f}%  {temp:>2.0f}°c"

            r_idx = i + half

            if r_idx < len(per_core_pct):

                line += f"  |  C{r_idx:02d}: {per_core_pct[r_idx]:>4.1f}%  {temp:>2.0f}°c"

            tooltip += line + "\n"

        return tooltip.strip()



    def get_output(self):

        total_pct, per_core_pct = self.get_cpu_data()

        temp = self.get_temperature()

        power = self.get_power(total_pct)

        

        if temp > 80 or total_pct > 90: status = "critical"

        elif temp > 70 or total_pct > 70: status = "warning"

        elif temp > 55 or total_pct > 40: status = "medium"

        else: status = "good"



        # Watts de volta na Waybar aqui:

        text = f"  {total_pct:.0f}% {temp:.0f}°C {power:.1f}W"

        return {

            "text": text,

            "tooltip": self.format_tooltip(total_pct, per_core_pct, temp, power),

            "class": status

        }



def main():

    monitor = CPUMonitor()

    while True:

        print(json.dumps(monitor.get_output()), flush=True)

        time.sleep(2)



if __name__ == "__main__":

    main()
