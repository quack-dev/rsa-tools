from RSA import *

def isqrt(n):
		x = n
		y = (x + n // x) // 2
		while y < x:
			x = y
			y = (x + n // x) // 2
		return x

def Fermat_(r):
	n = r.n
	if n == None:
		return False
	a = isqrt(n)
	b2 = a*a - n
	b = isqrt(n)
	count = 0
	while b*b != b2:
		a = a + 1
		b2 = a*a - n
		b = isqrt(b2)
		count += 1
	p=a+b
	q=a-b
	assert n == p * q
	
	return RSA(p, q, p*q, r.e, r.d, r.phi_n)

def test_fermat():
	p = 0
	q = 0
	for i in range(2000, 3000):
		if is_prime(i):
			if q == 0:
				q = i
			else:
				if p == 0:
					p = i
				else:
					break
	n = p*q
	R = Fermat_(RSA(None, None, n))
	if sorted([R.p, R.q]) == sorted([p, q]):
		return True
	else:
		return False

if __name__ == "__main__":
	assert test_fermat()
