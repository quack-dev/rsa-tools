from RSA_includes import *
from primes import *

class RSA(object):
	def __init__(self, p = None, q = None, n = None, e = None, d = None, phi_n = None):
		self.p = p
		self.q = q
		self.e = e
		self.n = n
		self.d = d
		self.phi_n = phi_n
		self.calc_vars()
		self.check_valid()
	
	def check_valid(self):
		if self.phi_n != None and self.e != None:
			if self.phi_n % self.e == 0:
				print "phi_n is divisible by e"
				return False
			else:
				return True
		return True
	
	def count(self):
		return len([i for i in [self.find_q(), self.find_p(), self.find_e(), self.find_n(), self.find_d(), self.find_phi_n()] if i != None])
	
	
	################################
	#      auto variable calc      #
	################################
	def calc_vars(self):
		c_sum = self.count()
		p_sum = c_sum - 1
		while p_sum != c_sum:
			p_sum = c_sum
			c_sum = self.count()
	
	def find_q(self):
		if self.q == None:
			if self.n != None and self.p != None:
				if self.n % self.p != 0:
					print "n is not divisible by p"
					return None
				self.q = self.n / self.p
				return True
			elif self.phi_n != None and self.p != None:
				if self.phi_n % (self.p-1) != 0:
					print "phi_n is not divisible by (p-1)"
					return None
				self.q = (self.phi_n / (self.p - 1)) + 1
				return True
			else:
				return None
		else:
			return True
	
	def find_p(self):
		if self.p == None:
			if self.n != None and self.q != None:
				if self.n % self.q != 0:
					print "n is not divisible by q"
					return None
				self.p = self.n / self.q
				return True
			elif self.phi_n != None and self.q != None:
				if self.phi_n % (self.q-1) != 0:
					print "phi_n is not divisible by (q-1)"
					return None
				self.p = (self.phi_n / (self.q - 1)) + 1
				return True
			else:
				return None
		else:
			return True
	
	def find_n(self):
		if self.n == None:
			if self.q != None and self.p != None:
				self.n = self.p*self.q
				return True
			else:
				return None
		else:
			return True
	
	def find_phi_n(self):
		if self.phi_n == None:
			if self.q != None and self.p != None:
				self.phi_n = (self.p - 1) * (self.q - 1)
	
	def find_e(self):
		if self.e == None:
			if self.phi_n != None and self.d != None:
				self.e = multiplicative_inverse(self.d, self.phi_n)
				return True
			else:
				return None
		else:
			return True
	
	def find_d(self):
		if self.d == None:
			if self.phi_n != None and self.e != None:
				self.d = multiplicative_inverse(self.e, self.phi_n)
				if self.d != None:
					return True
				else:
					return None
			else:
				return None
		else:
			return True
	
	#############################
	#      encrypt/decrypt      #
	#############################
	def encrypt(self, m):
		if m > self.n:
			print "message to encrypt cannot be larger than N"
			return False
		return pow(m, self.e, self.n)
	
	def decrypt(self, c):
		if c > self.n:
			print "message to decrypt cannot be larger than N"
			return False
		return pow(c, self.d, self.n)
	
	#########################
	#      other stuff      #
	#########################
	def rep(s):
		return "p = %s\nq = %s\nn = %s\ne = %s\nphi_n = %s\nd = %s" % (s.p, s.q, s.n, s.e, s.phi_n, s.d)

if __name__ == "__main__":
	n_bits = 1024
	print "generating p..."
	p = random_prime(n_bits / 2)
	print "p = %s" % (p)
	print "generating q..."
	q = random_prime(n_bits / 2)
	print "q = %s" % (q)
	print "creating RSA object"
	r = RSA(p, q, None, 65537)
	print "capable of encrypting %s characters" % (int(math.floor(math.log(r.n, 2) / 8)))
	testchars = random._urandom(int(math.floor(math.log(r.n, 2) / 8)))
	Pt = unascii(testchars)
	Ct = r.encrypt(Pt)
	if ascii(r.decrypt(Ct)) == testchars:
		print "everything seems to be working"
	
	print "testing for vulnerabilities.."
	
	print "\nWiener..."
	
	if r.d < (1.0/3.0)*pow(r.n, .25):# and ((r.p > r.q and r.p < 2*r.q) or (r.q > r.p and r.q < 2*r.p)):
		print "appears to be vulnerable to Wiener attack"
		print "trying Wiener attack..."
		import Wiener_Attack
		w = Wiener_Attack.wiener_attack(RSA(None, None, r.n, r.e)) #only supplying n and e
		if w != False:
			print "successful factorization of N by Wiener attack --"
			print "p = %s\nq = %s" % (w.p, w.q)
		else:
			print "Wiener attack unsuccessful"
	else:
		print "not vulnerable to Wiener"
	
	#brute
	print "\nBrute force..."
	if n_bits < 36:
		print "warning: it'll take a reasonable computer somewhere around an hour to break this"
	elif n_bits < 330:
		print "warning: it'll take a reasonable computer with Msieve less than 4 hours to break this"
	elif n_bits < 768:
		print "warning: a hella computer could break this in two years"
	else:
		print "large enough to resist brute force attempts"
	
	#Fermat
	print "\nFermat factorization..."
	if r.p - r.q < 2*pow(r.n, .25):
		print "appears to be vulnerable"
		print "attempting"
		import Fermat_Factoring
		f = Fermat_Factoring.Fermat_(r)
		if f != False and f != None: #I forgot which value is returned on failure if any
			print "Fermat factorization successful:"
			print "p = %s, q = %s" % (f.p, f.q)
		else:
			print "Fermat factorization unsuccessful"
	else:
		print "not vulnerable to Fermat factorization"
	#Pollard
	
