import subprocess
import time
from datetime import datetime


interval_min = 120

start_time = time.time()
run_time = datetime.now()


def run_one_check():
    script_folder = "C:\\Users\\charl\\Google Drive\\10. Coding\\201707 Dell Outlet Stock Check with Python\\"
    subprocess.call(['py','-3',script_folder + 'Dell_Outlet_Stock_Checker_v1.py'])
    subprocess.call(['py','-2',script_folder + 'Send_Email_v1.py'])

while True:
  print("scan completed at " + str(run_time))
  print("next scan scheduled in " + str(interval_min) + " mins")
  print
  time.sleep((60.0 - ((time.time() - start_time) % 60.0)) * interval_min)
