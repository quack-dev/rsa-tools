#useful functions

def ascii(num):
	h = hex(num).replace("0x", "").replace("L", "")
	if len(h) % 2 != 0:
		h = "0" + h
	return h.decode("hex")

def unascii(strn):
	return int(strn.encode("hex"), 16)

def gcd(a, b):
	while b != 0:
		a, b = b, a % b
	return a

def multiplicative_inverse(e, phi):
	original_e = e
	d = 0
	x1 = 0
	x2 = 1
	y1 = 1
	temp_phi = phi
	
	while e > 0:
		temp1 = temp_phi/e
		temp2 = temp_phi - temp1 * e
		temp_phi = e
		e = temp2
		
		x = x2- temp1* x1
		y = d - temp1 * y1
		
		x2 = x1
		x1 = x
		d = y1
		y1 = y
	
	if temp_phi == 1:
		return d + phi
