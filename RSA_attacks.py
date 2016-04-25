from RSA import * #should also includes primes and RSA_includes

import math

class attack(object):
	def __init__(self, name, func, testfunc = None, inputs = 1):
		self.name = name
		self.func = func
		self.testfunc = testfunc
		self.inputs = inputs
	def run(self, *r):
		try:
			return self.func(*r)
		except:
			print "Error raised on run of %n" % self.name
			return False
	def test(self):
		try:
			if self.testfunc == None:
				return None
			return self.testfunc()
		except:
			print "Error raised on test of %n" % self.name
			return False

#################### successful if:
#      Fermat      # p and q are too close together
#################### abs(p-q) < 2n**(1/4)
from Fermat_Factoring import *
	
Fermat = attack("Fermat factorization", Fermat_, test_fermat)

#################### successful if:
#      Wiener      # p is between q and 2q (which is quite typical) and d < (n**(1/4))/3
#################### recognizable because e is usually near the same order of magnitude as n
from Wiener_Attack import *
Wiener = attack("Wiener", wiener_attack, test_wiener)

##################################### successful if:
#      Pollard's p-1 factoring      # p-1 or q-1 only have small prime factors
#####################################
def Pollard_(r):
	def factor(n,b):
		""" Factor using Pollard's p-1 method """

		a = 2;
		for j in range(2,b):
			a = a**j % n
		
		d = gcd(a-1,n);
		#~ print "d:",d,"a-1:",a-1
		if 1 < d < n: return d;
		else: return -1;
	
	def factor(n,b):
		""" Factor using Pollard's p-1 method """

		a = 2;
		for j in range(2,b):
			a = a**j % n
		
		d = gcd(a-1,n);
		#~ print "d:",d,"a-1:",a-1
		if 1 < d < n: return d;
		else: return -1;
	
	n = r.n
	s = 2
	d = -1

	while s < n and d == -1:
		s +=1
		d = factor(n,s)
	
	if d == -1:
		return False
	else:
		return RSA(d, n/d, n, r.e, r.d, r.phi_n)

def test_Pollard():
	r = Pollard_(RSA(None, None, 65537*2011))#13493
	if sorted([r.p, r.q]) == sorted([65537, 2011]):
		return True
	else:
		return False
Pollard = attack("Pollard's p-1", Pollard_, test_Pollard)


################### successful if n < 256 bits
#      Brute      # note: install YAFU to increase this to 300+ bits for a 30 minute timeframe
################### note 2: which is faster, YAFU or Msieve?
def brute_Factor(r, time = 3600): #assumes that r.n only has two factors
	n = r.n
	if time > math.log(:
		return False
	if n <= 3:
		return False
	time_est = 4.685 * (2**(bits - 26))
	if test_est > time:
		ans = raw_input("time estimated to brute force is %s, continue anyway?\n(y/n)" % time_est)
		if ans == "n":
			return False
	for d in xrange(3, int(n**.5)+2, 2):
		if n%d==0: return RSA(d, n/d, n, r.e, r.d, r.phi_n)
	return False
def test_brute():
	r = brute_Factor(RSA(None, None, 17*19))
	if sorted([r.p, r.q]) == sorted([17, 19]):
		return True
	else:
		return False
Brute = attack("Brute factor", brute_Factor, test_brute)

#################
#      CRT      #
#################
class RSA_Ct(RSA):
	def __init__(self, Ct, *args):
		RSA.__init__(self, *args)
		self.Ct = Ct

import ChineseRemainderTheorem as _CRT
def CRT_(*rs):
	a_list = [r.Ct for r in rs]
	n_list = [r.n for r in rs]
	output, mod = _CRT.CRT(a_list, n_list)
	
	return int(math.ceil(output ** (1.0/rs[0].e)))

def test_CRT():
	assert _CRT.test_CRT()
	import random
	Pt = random.choice(range(1000, 2000))
	
	primes_used = []
	for i in range(3 * 2): #a p and a q for three congruencies
		p = random_prime(11)
		if not p in primes_used:
			primes_used.append(p)
	n1 = primes_used[0] * primes_used[1]
	n2 = primes_used[2] * primes_used[3]
	n3 = primes_used[4] * primes_used[5]
	
	r1 = RSA(None, None, n1, 3)
	r2 = RSA(None, None, n2, 3)
	r3 = RSA(None, None, n3, 3)
	r1 = RSA_Ct(r1.encrypt(Pt), None, None, n1, 3)
	r2 = RSA_Ct(r2.encrypt(Pt), None, None, n2, 3)
	r3 = RSA_Ct(r3.encrypt(Pt), None, None, n3, 3)
	return CRT_(r1, r2, r3) == Pt

CRT = attack("Chinese Remainder Theorem", CRT_, test_CRT, "many")

attacks = [Fermat, Wiener, Pollard, Brute, CRT]

def test_attacks():
	for a in attacks:
		#~ print a.name
		test = a.test()
		if test == None:
			print "%s does not have a test func" % (a.name)
		else:
			if not test:
				print "%s test returned %s" % (a.name, test)

def centerequals(s, w = 79):
	workable = w - len(s)
	out = "="*(workable/2) + s + "="*(workable/2)
	while len(out) < w:
		out += "="
	return out

def break_RSA(*args):
	if len(args) == 1:
		r = args[0]
	for a in attacks: #maybe will want to multithread this for things that take awhile, like bruting
		if len(args) == a.inputs or (a.inputs == "many" and len(args) > 1):
			try:
				output = a.run(*args)
			except: #should definitely put some debugging here
				break
			if type(output) == type(RSA()): #if it returned an RSA object
				r_ = output
				if r_ != False:
					if r_.count() > r.count():
						print centerequals(a.name)
						print r_.rep()
			else: #if it returned something else. This is for attacks that derive Pt without deriving p, q, or d
				print output

def main():
	test_attacks()
	#~ r1 = RSA(None, None, 90581, 17993) #vulnerable to Wiener & Fermat & Pollard & Brute
	                                   #~ #e value only required for Wiener
	#~ break_RSA(r1)
	

if __name__ == "__main__":
	main()
