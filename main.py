import subprocess
import datetime
import os
from collections import defaultdict


def get_process_lines():
    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    return result.stdout.split("\n")


def analyze_processes(lines):
    users = set()
    user_process_count = defaultdict(int)

    total_cpu = 0
    total_mem = 0

    max_cpu = 0
    max_cpu_name = ""

    max_mem = 0
    max_mem_name = ""

    process_count = 0

    for line in lines[1:]:
        if not line:
            continue

        parts = line.split()

        if len(parts) < 11:
            continue

        process_count += 1

        user = parts[0]
        cpu = float(parts[2])
        mem = float(parts[3])
        command = " ".join(parts[10:])

        users.add(user)
        user_process_count[user] += 1

        total_cpu += cpu
        total_mem += mem

        if cpu > max_cpu:
            max_cpu = cpu
            max_cpu_name = command[:20]

        if mem > max_mem:
            max_mem = mem
            max_mem_name = command[:20]

    return {
        "users": users,
        "user_process_count": user_process_count,
        "total_cpu": total_cpu,
        "total_mem": total_mem,
        "max_cpu_name": max_cpu_name,
        "max_mem_name": max_mem_name,
        "process_count": process_count,
    }


def build_report(stats):
    report = "Отчёт о состоянии системы:\n"
    report += "Пользователи системы: " + ", ".join(stats["users"]) + "\n"
    report += "Процессов запущено: " + str(stats["process_count"]) + "\n\n"

    report += "Пользовательских процессов:\n"
    for user, count in stats["user_process_count"].items():
        report += f"{user}: {count}\n"

    report += "\nВсего памяти используется: " + str(round(stats["total_mem"], 1)) + "%\n"
    report += "Всего CPU используется: " + str(round(stats["total_cpu"], 1)) + "%\n"
    report += "Больше всего памяти использует: (" + stats["max_mem_name"] + ")\n"
    report += "Больше всего CPU использует: (" + stats["max_cpu_name"] + ")\n"

    return report


def save_report(report):
    if not os.path.exists("output"):
        os.mkdir("output")

    now = datetime.datetime.now()
    filename = now.strftime("%d-%m-%Y-%H-%M-scan.txt")
    filepath = os.path.join("output", filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write(report)

    return filepath


def main():
    lines = get_process_lines()
    stats = analyze_processes(lines)
    report = build_report(stats)

    print(report)

    filepath = save_report(report)
    print("Отчёт сохранён в файл:", filepath)


if __name__ == "__main__":
    main()