import subprocess
import os



BASE = os.path.dirname(os.path.abspath(__file__))

subprocess.run(['python', os.path.join(BASE, '0kreiraj_tablice.py')])
subprocess.run(['python', os.path.join(BASE, '1skupovi.py')])
subprocess.run(['python', os.path.join(BASE, '2modeli.py')])
subprocess.run(['python', os.path.join(BASE, '3kategorije.py')])
subprocess.run(['python', os.path.join(BASE, '4karakteristike.py')])
