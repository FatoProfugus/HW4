from sympy import isprime
from math import gcd

def gen_public_key(generator, private_key, prime):
	public_key = pow(generator, private_key, prime)
	return public_key

def shared_private_key(public_key, private_key, prime):
	shared_private_key = pow(public_key, private_key, prime)
	return shared_private_key


def gen_ephemeral_key(generator, private_key, prime):
	ephemeral_key = pow(generator, private_key, prime)
	return ephemeral_key

def elgamal_encryption(plaintext, masking_key, prime):
	ciphertext = (plaintext*masking_key)%prime
	return ciphertext

def elgamal_decryption(ciphertext, masking_key, prime):
	inverse = pow(masking_key, -1, prime)
	plaintext = (ciphertext*inverse)%prime
	return plaintext

def prime_answers(n):
    print('It is '+str(isprime(n))+' that n is a prime.')
    
    q = n//2
    n_is_safe = isprime(q)
    if n_is_safe:
    	print('n is a safe prime.')
    	print('The Sophie Germain prime used to create n is '+str(q)+'.')
    else:
    	print('n is not a safe prime.')
    
    period_2 = []
    period_q = []
    period_full = []
    start = pow(10,20)+1
    end = pow(10,20)+1000
    for i in range(start, end):
    	if len(period_2) > 0 and len(period_q) > 0 and len(period_full) > 0:
    		break
    	if pow(i, 2, n) == 1:
    		period_2.append(i)
    		continue
    	if pow(i, q, n) == 1:
    		period_q.append(i)
    		continue
    	if pow(i, n-1, n) == 1:
    		period_full.append(i)
    		continue
    if len(period_2) > 0:
    	print('The smallest g with period 2 is '+str(period_2[0])+'.')
    else:
    	print('There is no g in the defined range with period 2.')
    if len(period_q) > 0:
    	print('The smallest g with period q is '+str(period_q[0])+'.')
    else:
    	print('There is no g in the defined range with period q.')
    if len(period_full) > 0:
    	print('The smallest g with full period is '+str(period_full[0])+'.')
    else:
    	print('There is no g in the defined range with full period.')

    return period_full[0]

def main():
	n = 2649376219191757686333291073027588009793925231566294290337286424331787812414080960960191670815548639
	# prints answers to Qs7-11 & returns generator for future use
	generator = prime_answers(n)

	alice_private_key = 847103968584668876211685654320008118123427186620312004872780981364332116943060841529842231006541702
	bob_private_key = 446593010317615872511323696615805232046956121634004055696443978134375265180448081001217084488791222

	alice_public_key = gen_public_key(generator, alice_private_key, n)
	bob_public_key = gen_public_key(generator, bob_private_key, n)
	print('Alice\'s public key is '+str(alice_public_key)+'.')
	print('Bob\'s public key is '+str(bob_public_key)+'.')

	agreed_private_key = shared_private_key(alice_public_key, bob_private_key, n)
	sanity_check = shared_private_key(bob_public_key, alice_private_key, n)
	if sanity_check != agreed_private_key:
		print('Error: something is wrong with shared_private_key()')
		return
	print('The agreed key is '+str(agreed_private_key)+'.')

	plaintext = 123456789012345678901234567890
	ephemeral_key = 446593010317615872511323696615805232046956121634004055696443978134375265180448081001217084488791222
	masking_key = pow(ephemeral_key, alice_private_key, n)
	ciphertext = elgamal_encryption(plaintext, masking_key, n)
	decrypted_message = elgamal_decryption(ciphertext, masking_key, n)
	print('Elgamal ciphertext is '+str(ciphertext)+'.')
	print('plaintext == decrypted_message is '+str(plaintext == decrypted_message)+'.')
	ephemeral_inverse = pow(ephemeral_key, -1, n)
	print('The inverse of the ephemeral key is '+str(ephemeral_inverse)+'.')

	z = 373835199237255951027858818817526711465008640656023977712641048809225685925891061359604637083333261
	inverse_z = pow(z, -1, n)
	coprime_res = gcd(z, n-1)
	if coprime_res == 1:
		print('Yes, gcd(z, n-1) = 1.')
	else:
		print('No, gcd(z, n-1) = '+str(coprime_res)+'.')

	m = plaintext
	r = pow(generator, z, n)
	s = ((m-bob_private_key*r)*inverse_z)%(n-1)
	print('m = '+str(m)+'.')
	print('r = '+str(r)+'.')
	print('s = '+str(s)+'.')
	print('Xa^r mod p is '+str(pow(bob_public_key, r, n))+'.')
	print('r^s mod p is '+str(pow(r, s, n))+'.')
	print('g^m mod p is '+str(pow(generator, m, n))+'.')
	t = (pow(bob_public_key, r, n)*pow(r, s, n))%n
	if t == pow(generator, m, n):
		print('Yes, it is a valid signature.')
	else:
		print('No, the signature is invalid.')

	return


if __name__ == '__main__':
    main()