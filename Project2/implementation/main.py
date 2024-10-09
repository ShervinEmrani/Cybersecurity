import random
import sys

PRIMENO = 89
generator = 3


secretVal = 5

X = pow(generator, secretVal) % PRIMENO
y = 3
Y = pow(generator, y) % PRIMENO

print("Alice (the Prover) generates these values:")
print("secretVal(secret)= ", secretVal)
print("PRIMENO= ", PRIMENO)
print("X= ", X)

print("\nAlice generates a random value (y):")
print("y=", y)

print("\nAlice computes Y = generator^y \ (mod PRIMENO) and passes to Bob:")

print("Y=", Y)

print("\nBob generates a random value (c) and\ passes to Alice:")

c = 6
print("c=", c)
print("\nAlice calculates z = y.secretVal^c \ (mod PRIMENO) and send to Bob (the Verifier):")

z = (y + c * secretVal)

print("z=", z)

print("\nBob now computes val=generator^z (mod PRIMENO)\ and (Y X^c (mod PRIMENO)) and determines if they are the same\primeNo")

val1 = pow(generator, z) % PRIMENO
val2 = (Y * (X**c)) % PRIMENO

print("val1= ", val1, end=' ')
print(" val2= ", val2)

if (val1 == val2):
	print("Alice has proven that she knows x")
else:
	print("Failure to prove")
