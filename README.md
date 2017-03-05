# selfcount

## Introduction by example

Let's look at the binary, 8-bit number `0b 0000 0110`.
It represents the number 6.
It also has 6 zeros!

Or the binary, 16-bit number `0b 0000 0000 0000 1110`.
It represents the number 13.
It also has 13 zeros!

Are there other such 8-bit or 16-bit numbers?
For which bitwidths are there such numbers at all?
Are there some bitwidths for which several such numbers exist?
Is there an underlying pattern?

<!--
    And who took the cookie from the cookie jar?
    https://youtu.be/mj6l_5vDEAY?t=7)? ;)
-->

All these questions and more can be answered by simply running the program!

## Usage

Usage: `./selfcount.py {COMMAND} [ARGS]`

`./selfcount.py all`:
Prints the set of bitwidths (up to some hard-coded but easily configurable amount)
that have such a self-describing number.

`./selfcount.py about N`:
A short analysis of the bitwidth N is printed.

`./selfcount.py all_inv`:
For each bitwidth (up to some hard-coded but easily configurable amount)
prints how many self-describing numbers there are.

`./selfcount.py inv N`:
Prints the amount of self-descriptive numbers of N on the first line,
followed by the numbers themselves (in an unordered manner).

Running time and consumed memory is roughly logarithmic in N.
So this program has absolutely no problem to reason about bitwidths like 65535.

## Why would anyone care?

For some other project I considered adding a special "not a value" value
(i.e., another [billion-dollar mistake](https://en.wikipedia.org/wiki/Tony_Hoare#Apologies_and_retractions)).
I needed a simple, easily checkable property,
that couldn't "accidentally" be satisfied by an actual value.

I didn't end up using it though, don't worry.
I was just intrigued that the search space could be pared down so easily
by just a few inequalities, and then started wondering what the pattern looks like.

## Example results

```
$ ./selfcount.py all
{0, 2, 3, 5, 7, 8, 9, 10, 11, 12, 14, 16, 17, 19, 20, 22, 24, 25, 26, 27, 28, 29, 31,
33, 34, 35, 36, 38, 40, 41, 42, 43, 44, 45, 47, 49, 50, 52, 53, 55, 57, 58, 59, 60,
61, 62, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77, 79, 81, 82, 84, 85, 87,
89, 90, 91, 92, 93, 94, 96, 98, 99, 100, 101, 103, 105, 106, 107, 108, 109, 110, 112,
114, 115, 117, 118, 120, 122, 123, 124, 125, 126, 127}
$ ./selfcount.py about 0
v and its zeros: {0: 0}
self-maps: {0}
$ ./selfcount.py about 3
v and its zeros: {2: 2}
self-maps: {2}
$ ./selfcount.py about 24
v and its zeros: {20: 22, 21: 21, 22: 21, 23: 20}
self-maps: {21}
$ ./selfcount.py about 32
v and its zeros: {28: 29, 29: 28, 30: 28, 31: 27}
self-maps: set()
$ ./selfcount.py about 128
v and its zeros: {122: 123, 123: 122, 124: 123, 125: 122, 126: 122, 127: 121}
self-maps: set()
$ ./selfcount.py about 256
v and its zeros: {249: 250, 250: 250, 251: 249, 252: 250, 253: 249, 254: 249, 255: 248}
self-maps: {250}
$ 
```

## FAQ

### "`v and its zeros` doesn't consider enough numbers!  It must be a bug!"

The boundaries of the set considered for the `v and its zeros`
are given "immediately" by certain inequalities.
If a number is not even considered in this set,
then there is an "obvious" reason why it can't possibly work.

For example, there's no way a 12345-bit number has more than 12345 zero bits.
The other inequalities look similar.  For more details, see the source code, function `search`.

### "Are there other such 8-bit or 16-bit numbers?"

No, sadly:

```
$ ./selfcount.py about 8
v and its zeros: {6: 6, 7: 5}
self-maps: {6}
$ ./selfcount.py about 16
v and its zeros: {13: 13, 14: 13, 15: 12}
self-maps: {13}
```

### "Are there some bitwidths for which several such numbers exist?"

Yes!

```
$ ./selfcount.py about 64
v and its zeros: {59: 59, 60: 60, 61: 59, 62: 59, 63: 58}
self-maps: {59, 60}
```

I'm not sure how these bitwidths can be constructed in general.

### "For which bitwidths are there such numbers at all?  What's the pattern?"

I have no idea.

### "The amount of unique numbers is [A228085](https://oeis.org/A228085)!"

Nearly!  The sequence is defined as:

> a(n) = number of distinct k which satisfy n = k + bitcount(k)

Whereas "my" way of thinking about it could be described as:

> x(n) = number of distinct k which satisfy k = n - bitcount(k)

This ends up being identical.  This is quite intuitive,
as the amount of zeros and the amount of ones anti-correlate.

```
$ ./selfcount.py inv 129 | head -n1
3
$ python3 -c 'print(2**12+6)'
4102
$ ./selfcount.py inv $(python3 -c 'print(2**12+6)') | head -n1
4
$ ./selfcount.py inv $(python3 -c 'print(2**136+6)') | head -n1
5
$ ./selfcount.py inv $(python3 -c 'print(2**260+130)') | head -n1
6
$ ./selfcount.py inv $(python3 -c 'print(2**4233+130)') | head -n1
7
$ ./selfcount.py inv $(python -c 'print(2**8206+4103)') | head -n1
8
$ time ./selfcount.py inv $(python -c 'print(2**8206+4103)') | head -n1
8

real	0m0,293s
user	0m0,260s
sys	0m0,020s
```

So I can verify the results he got for 8 inverses, and quite quickly so.
For the higher results,
outputting the stream of numbers seems to be the limiting factor.

### The pattern

There's an obvious pattern to the numbers:
it's always `2^m+k+1`, where k is an earlier candidate: 5, 5, 129, 129, 4102, 4102.

The exponent can apparently be described by [some other black magic](https://oeis.org/A230303).

## Contributing

Pull requests and discussion very welcome, I'm curious about everything! :D
