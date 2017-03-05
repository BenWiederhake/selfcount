#!/usr/bin/env python3

# selfcount – binary numbers that count their own zeros: hilarity ensues
# Copyright (C) 2017  Ben Wiederhake
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import floor, log


def log2(v):
    # Not sure what base it uses, so ignore it.
    return log(v) / log(2)


# How many zeros does the binary value v with n bits have?
def zeros(v, n):
    assert v < n  # Technically, works also for any v < 2**n, but that would be a bit slower for large n.
    return n - bin(v).count("1")


def search(n):
    if n == 0:
        return {0: 0}
    elif n == 1:
        # One of the "log" steps doesn't work with n=1
        return dict()
    # n > 0
    # => v > 0
    # => v < n
    # => v >= n - floor(log2(n - 1)) - 1
    # And that's small enough to be searched
    # by brute force, even if n is large.
    start = n - floor(log2(n - 1)) - 1
    return {v: zeros(v, n) for v in range(start, n)}


def selves(n):
    return {v for (v, z) in search(n).items() if v == z}


USAGE_FMT = \
"""{prog} – binary numbers that count their own zeros: hilarity ensues
Usage: {prog} [N]
If no N is given, {prog} prints the set of bitwidths up to {upper}
that have such a self-describing number.
If N is given, then a short analysis of the bitwidth N is printed.

Running time and consumed memory is roughly logarithmic in N.
So this program has absolutely no problem to reason about bitwidths like 65535.

(Did you know?  The 65535-bit word representing 65522 has 65522 zeros.)"""

UPPER = 129

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        print("v and its zeros:", search(int(argv[1])))
        print("self-maps:", selves(int(argv[1])))
    elif len(argv) == 1:
        all_selves = {n: selves(n) for n in range(0, UPPER)}
        print({n for (n, s) in all_selves.items() if len(s) != 0})
    else:
        print(USAGE_FMT.format(prog=argv[0], upper=UPPER))
        exit(1)
