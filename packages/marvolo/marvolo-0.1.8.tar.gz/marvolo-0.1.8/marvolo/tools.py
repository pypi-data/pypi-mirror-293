import os
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


def split_jsonl(origin_file, output_dir, size, save_res=True):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    index = 0
    data = []
    with open(origin_file, "r") as f:
        for line in f:
            data.append(line)
            if len(data) >= size:
                with open(os.path.join(output_dir, f"{index}.jsonl"), "w") as f:
                    for d in data:
                        f.write(d)
                data = []
                index += 1

    if save_res and len(data) > 0:
        with open(os.path.join(output_dir, f"{index}.jsonl"), "w") as f:
            for d in data:
                f.write(d)
    data = []
