from RSA import *

#derived from Chinese Remainder Theorem on wikipedia
def CRT(a_list, n_list):
	while len(a_list) > 1:
		a_list = [a_list[0] + (n_list[0]*((a_list[1] - a_list[0]) % n_list[1]) * multiplicative_inverse(n_list[0], n_list[1]))] + a_list[2:]
		n_list = [n_list[0]*n_list[1]] + n_list[2:]
	return a_list[0] % n_list[0], n_list[0]

def test_CRT(v = False):
	assert CRT([2, 3, 1], [3, 4, 5]) == (11, 60) #this is the example from the wikipedia page
	import random
	
	x = random.choice(range(1000, 5000))
	
	mods = []
	while len(mods) < 4:
		n = random_prime(8)
		if n not in mods:
			mods.append(n)
	
	a_list = [x%mods[i] for i in range(len(mods))]
	n_list = mods
	
	y, n = CRT(a_list, n_list)
	
	assert abs(x - y) % n == 0
	if x != y and v:
		print "%s != %s, but %s == %s + (%s*%s)" % (x, y, x, y, n, (x - y) / n)
	return True

if __name__ == "__main__":
	for i in range(1000):
		assert test_CRT(True)
	#~ print "yeah works p well"
