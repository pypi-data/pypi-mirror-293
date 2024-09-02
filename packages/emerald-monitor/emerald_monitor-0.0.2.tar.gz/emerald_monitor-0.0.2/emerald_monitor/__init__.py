import psutil
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from threading import Thread

class ResourceMonitor(Thread):

    def __init__(self, logging_interval=1):
        super().__init__()
        self.daemon = True  # Set as daemon to terminate with main program
        self.running = False
        self.epoch_time = []
        self.cpu_times = []  # List to store per-CPU time data (may not be per-core)
        self.memory_info = []
        self.kernel_process = psutil.Process()
        self.logging_interval = logging_interval

    def start_logging(self):
        # Check if already running to avoid conflicts
        if self.running:
            print("Monitoring already in progress.")
            return
        self.running = True
        self.start()  # Thread automatically calls run()

    def stop_logging(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                kernel_process = self.kernel_process
                self.epoch_time.append(time.time())
                self.cpu_times.append(kernel_process.cpu_times())
                self.memory_info.append(kernel_process.memory_info())

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                # Handle potential issues with the kernel process
                print(f"Error monitoring process with PID {self.kernel_process.pid}. Stopping logging.")
                break
            time.sleep(self.logging_interval)  # Use the set logging interval # s

    def get_logs(self):
        columns = ['epoch_time', 'elapsed_time', 'memory_rss', 'cpu_times_user', 'cpu_times_system', 'cpu_times_total']
        monitor_info = pd.DataFrame(np.ones([len(self.epoch_time), len(columns)]), columns=columns)
        for ii in range(0, len(self.epoch_time), 1):
            now_time = self.epoch_time[ii]
            gm_time = time.gmtime(now_time)

            numdec = 3
            dec_sec = f'0{np.round(gm_time.tm_sec + (now_time - np.floor(now_time)), numdec)}0'
            dec_sec = dec_sec.split('.')[0][-2:] + '.' + dec_sec.split('.')[1][:numdec]

            monitor_info.loc[ii, 'epoch_time'] = now_time
            monitor_info.loc[ii, 'elapsed_time'] = now_time - self.epoch_time[0]
            monitor_info.loc[ii, 'gm_year'] = gm_time.tm_year
            monitor_info.loc[ii, 'gm_month'] = gm_time.tm_mon
            monitor_info.loc[ii, 'gm_day'] = gm_time.tm_mday
            monitor_info.loc[ii, 'gm_time'] = f"{gm_time.tm_hour}:{gm_time.tm_min}:{dec_sec}"
            monitor_info.loc[ii, 'memory_rss'] = self.memory_info[ii].rss / (1024 ** 3)
            monitor_info.loc[ii, 'cpu_times_user'] = self.cpu_times[ii].user
            monitor_info.loc[ii, 'cpu_times_system'] = self.cpu_times[ii].system
            monitor_info.loc[ii, 'cpu_times_total'] = self.cpu_times[ii].user + self.cpu_times[ii].system

        return monitor_info

    def plot_logs(self, time_key='elapsed_time', figsize=(10, 5)):
        # time_key = 'epoch_time'
        monitor_info = self.get_logs()

        fig, axs = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=figsize)
        axs[0].plot(monitor_info[time_key], monitor_info.memory_rss, label="memory_rss", c='blue')
        axs[0].set_ylabel(f"memory usage (Gb)")

        axs[1].plot(monitor_info[time_key], monitor_info.memory_rss.diff(), label="memory_change", c='blue')
        axs[1].set_ylabel(f"memory usage change (Gb)")

        axs[2].plot(monitor_info[time_key], monitor_info.cpu_times_total, label='total', c="red")
        axs[2].plot(monitor_info[time_key], monitor_info.cpu_times_system, label='system', c="green")
        axs[2].plot(monitor_info[time_key], monitor_info.cpu_times_user, label='user', c="orange")
        axs[2].legend()
        axs[2].set_ylabel(f"cpu times")

        axs[3].plot(monitor_info[time_key], monitor_info.cpu_times_total.diff(), label="total_change", c='red')
        axs[3].plot(monitor_info[time_key], monitor_info.cpu_times_system.diff(), label="system_change", c='green')
        axs[3].plot(monitor_info[time_key], monitor_info.cpu_times_user.diff(), label="user_change", c='orange')
        axs[3].legend()
        axs[3].set_ylabel(f"cpu times change")

        axs[3].set_xlabel(f"{time_key} (s)")

        plt.tight_layout()
        plt.show()
        
