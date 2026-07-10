"""
LaundryBot V6

State Machine Parser
"""

import re


def split_jobs(text):

    jobs = []

    current = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # เจอ JOB ใหม่
        if re.match(r"JOB\d{4}-\d+", line):

            if current:
                jobs.append(current)

            current = [line]

        else:

            if current:
                current.append(line)

    if current:
        jobs.append(current)

    return jobs