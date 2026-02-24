import subprocess
import datetime
import os

result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
lines = result.stdout.split("\n")

users = []
user_process_count = {}

total_cpu = 0
total_mem = 0

max_cpu = 0
max_cpu_name = ""

max_mem = 0
max_mem_name = ""

for i in range(1, len(lines)):

    if lines[i] == "":
        continue

    parts = lines[i].split()

    user = parts[0]
    cpu = float(parts[2])
    mem = float(parts[3])
    command = " ".join(parts[10:])

    if user not in users:
        users.append(user)

    if user in user_process_count:
        user_process_count[user] += 1
    else:
        user_process_count[user] = 1

    total_cpu += cpu
    total_mem += mem

    if cpu > max_cpu:
        max_cpu = cpu
        max_cpu_name = command[:20]

    if mem > max_mem:
        max_mem = mem
        max_mem_name = command[:20]


report = "Отчёт о состоянии системы:\n"
report += "Пользователи системы: " + ", ".join(users) + "\n"
report += "Процессов запущено: " + str(len(lines) - 1) + "\n\n"

report += "Пользовательских процессов:\n"
for user in user_process_count:
    report += user + ": " + str(user_process_count[user]) + "\n"

report += "\nВсего памяти используется: " + str(round(total_mem, 1)) + "%\n"
report += "Всего CPU используется: " + str(round(total_cpu, 1)) + "%\n"
report += "Больше всего памяти использует: (" + max_mem_name + ")\n"
report += "Больше всего CPU использует: (" + max_cpu_name + ")\n"

print(report)

if not os.path.exists("output"):
    os.mkdir("output")

now = datetime.datetime.now()
filename = now.strftime("%d-%m-%Y-%H-%M-scan.txt")
filepath = "output/" + filename

file = open(filepath, "w", encoding="utf-8")
file.write(report)
file.close()

print("Отчёт сохранён в файл:", filepath)