import os
import json
from collections import defaultdict


def parse_log_line(line):
    parts = line.split()

    ip = parts[0]
    method = parts[5].strip('"')
    url = parts[6]
    time = parts[3].strip('[')
    duration = int(parts[-1])

    return ip, method, url, time, duration


def analyze_log(file_path):
    total_requests = 0
    methods = defaultdict(int)
    ip_count = defaultdict(int)
    slow_requests = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            total_requests += 1

            ip, method, url, time, duration = parse_log_line(line)

            methods[method] += 1
            ip_count[ip] += 1

            slow_requests.append((duration, method, url, ip, time))

    return total_requests, methods, ip_count, slow_requests


def get_top_ips(ip_count):
    sorted_ips = sorted(ip_count.items(), key=lambda x: x[1], reverse=True)
    return sorted_ips[:3]


def get_top_slowest(slow_requests):
    slow_requests.sort(reverse=True)
    return slow_requests[:3]


def create_result_dict(total, methods, top_ips, slowest):
    result = {
        "total_requests": total,
        "methods": dict(methods),
        "top_ips": [{"ip": ip, "count": count} for ip, count in top_ips],
        "top_slowest_requests": [
            {
                "method": method,
                "url": url,
                "ip": ip,
                "duration": duration,
                "time": time,
            }
            for duration, method, url, ip, time in slowest
        ],
    }

    return result


def save_json(file_name, data):
    json_name = file_name + "_result.json"

    with open(json_name, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def process_file(file_path):
    print(f"\nAnalyzing file: {file_path}")

    total, methods, ip_count, slow_requests = analyze_log(file_path)

    top_ips = get_top_ips(ip_count)
    slowest = get_top_slowest(slow_requests)

    result = create_result_dict(total, methods, top_ips, slowest)

    print(json.dumps(result, indent=4))

    file_name = os.path.basename(file_path)
    save_json(file_name, result)


def main(path):
    if os.path.isfile(path):
        process_file(path)

    elif os.path.isdir(path):
        for file in os.listdir(path):
            full_path = os.path.join(path, file)

            if os.path.isfile(full_path):
                process_file(full_path)

    else:
        print("Path not found")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <path_to_log_or_directory>")
    else:
        main(sys.argv[1])

