#!/usr/bin/env python

import json
import re
import sys


class Recording(object):

    def __init__(self, desc, lines):
        self.desc = desc
        self.lines = lines

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r", encoding='utf-8') as f:
            desc = json.loads(f.readline())
            lines = []
            for line in f.readlines():
                lines.append(json.loads(line))
            return cls(desc, lines)

    def write(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            desc_line = json.dumps(self.desc) + "\n"
            f.write(desc_line)
            for line in self.lines:
                line = json.dumps(line) + "\n"
                f.write(line)

    def add_offset(self, offset):
        for line in self.lines:
            line[0] = line[0] + offset

    def limit_idle_time(self, idle_time_limit, match):
        last_time_old = 0
        last_time_new = 0
        for line in self.lines:
            if match and not match.search(line[2]):
                continue
            curr_time_old = line[0]
            diff = curr_time_old - last_time_old
            diff = min(diff, idle_time_limit)
            curr_time_new = last_time_new + diff
            line[0] = curr_time_new
            last_time_old = curr_time_old
            last_time_new = curr_time_new


def main():
    op = sys.argv[1]
    if op == "add-offset":
        # Add an offset to all timestamps in a recording.
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
        offset = float(sys.argv[4])
        r = Recording.from_file(input_filename)
        r.add_offset(offset)
        r.write(output_filename)
    elif op == "limit-idle-time":
        # Limit idle time in a recording.
        input_filename = sys.argv[2]
        output_filename = sys.argv[3]
        idle_time_limit = float(sys.argv[4])
        if len(sys.argv) > 5:
             match = re.compile(sys.argv[5])
        else:
             match = None
        r = Recording.from_file(input_filename)
        r.limit_idle_time(idle_time_limit, match)
        r.write(output_filename)
    elif op == "-h":
        print("asciinema video editor")
        print("Usage:")
        print("  {} add-offset <input file> <output file> <offset>".format(sys.argv[0]))
        print("  {} limit-idle-time <input file> <output file> <idle time limit> [<regex>]".format(sys.argv[0]))
    else:
        raise Exception("Unexpected operation: {}".format(op))


if __name__ == "__main__":
    main()
