import random
import math
import time

def is_prime(num):
	if num == 2:
		return True
	if num < 2 or num % 2 == 0:
		return False
	for n in xrange(3, int(num**0.5)+2, 2):
		if num % n == 0:
			return False
	return True

def probable_prime(n, k): #k is accuracy
	if n == 2:
		return True
	if n == 3:
		return True
	if n < 3:
		return False
	if n%2 == 0:
		return False
	#find r and d such that 2**r * d == n-1 and d is odd
	nm1 = n - 1
	d = 0
	for power in range(int(math.floor(math.log(n, 2))))[::-1]:
		if nm1 % 2**power == 0:
			if (nm1 / 2**power) % 2 != 0:
				d = nm1 / 2**power
				r = power
				break
	if d == 0:
		print "something fucked up on %s" % (n)
		return False
	
	for ignore_me in range(k):
		a = random.randint(2, n-1) #[2, n-2] range
		x = pow(a,d, n)
		if x == 1 or x == nm1:
			continue
		for ignore_me_too in xrange(r - 1):
			x = pow(x, 2, n)
			if x == 1:
				return False
			if x == nm1:
				continue
		return False
	return True

def random_prime(bits, k = 16):
	upperbound = 2**bits - 1
	lowerbound = 2**(bits - 1) - 1
	while True:
		if bits < 32:
			test = random.choice(xrange(lowerbound, upperbound))
		else:
			eight_bits_needed = int(math.ceil(bits / 8))
			test = random._urandom(eight_bits_needed)
			test = int(test.encode("hex"), 16) % 2**bits
		if bits <= 16: #there seems to be a failure on primes of the form 2**n + 1, the largest of which known is 2**16 + 1 (65537)
			if is_prime(test):
				return test
		else:
			if probable_prime(test, k):
				return test

if __name__ == "__main__":
	print is_prime(715638145381343)
	exit()
	def brute_Factor(n): #assumes two prime factors
		if n <= 3:
			return False
		for d in xrange(3, int(n**.5)+2, 2):
			if n%d==0: return d, n/d
		return False
	import time
	for bits in range(8, 33):
		n = random_prime(bits) * random_prime(bits)
		start_time = time.time()
		p, q = brute_Factor(n)
		print "%s bits took %s seconds" % (bits, time.time() - start_time)
"""
sameple output of main:
8 bits took 0.0 seconds
9 bits took 0.0 seconds
10 bits took 0.0 seconds
11 bits took 0.0 seconds
12 bits took 0.0 seconds
13 bits took 0.0 seconds
14 bits took 0.0 seconds
15 bits took 0.0 seconds
16 bits took 0.0 seconds
17 bits took 0.0159997940063 seconds
18 bits took 0.0160000324249 seconds
19 bits took 0.0310001373291 seconds
20 bits took 0.0629999637604 seconds
21 bits took 0.18700003624 seconds
22 bits took 0.40700006485 seconds
23 bits took 0.625 seconds
24 bits took 1.04699993134 seconds
25 bits took 2.08299994469 seconds
26 bits took 4.68499994278 seconds
27 bits took 9.41900014877 seconds
28 bits took 21.1079998016 seconds
29 bits took 49.873000145 seconds
30 bits took 70.1129999161 seconds
31 bits took 141.301000118 seconds
32 bits took 37.6480000019 seconds
"""
