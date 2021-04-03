from Crypto import Random
from Crypto.Util import number
import sys

#this code is from: https://asecuritysite.com/encryption/ped
#here, q appears to be p from the linked article (in which case, p here is q in article)


def generate(param):
    q = param[1]
    g = param[2]
    h = param[3]
    return q, g, h


class verifier:
    def setup(self, security):
        p = number.getPrime(2 * security, Random.new().read)
        #again, q appears to be p from the linked article
        q = 2 * p + 1

        g = number.getRandomRange(1, q - 1)
        s = number.getRandomRange(1, q - 1)
        print("Secret value:\t", s)
        h = pow(g, s, q)

        param = (p, q, g, h)
        print("p=", p)
        print("q=", q)
        print("g=", g)
        print("h=", h)

        return param

    def open(self, param, c, x, *r):
        result = "False"
        q, g, h = generate(param)

        sum = 0
        for i in r:
            sum += i

        res = (pow(g, x, q) * pow(h, sum, q)) % q

        if (c == res):
            result = "True"
        return result

    def add(self, param, *cm):
        addCM = 1
        for x in cm:
            addCM *= x
        addCM = addCM % param[1]
        return addCM


class prover:
    def commit(self, param, x):
        #again, q appears to be p from the linked article
        q, g, h = generate(param)

        r = number.getRandomRange(1, q - 1)
        c = (pow(g, x, q) * pow(h, r, q)) % q
        return c, r


security = 80
msg1 = 1
msg2 = 2

if (len(sys.argv) > 1):
    msg1 = int(sys.argv[1])

if (len(sys.argv) > 2):
    msg2 = int(sys.argv[2])

v = verifier()
p = prover()

param = v.setup(security)

c1, r1 = p.commit(param, msg1)
c2, r2 = p.commit(param, msg2)

addCM = v.add(param, c1, c2)

print("\nMsg1:", msg1)
print("Msg2:", msg2)

print("\nc1,r1:", c1, ",", r1)
print("c2,r2:", c2, ",", r2)
print("\nWe can now multiply c1 and c2, which is same as adding Msg1 and Msg2")
print("\nCommitment of adding (Msg1+Msg2):\t", addCM)

result1 = v.open(param, c1, msg1, r1)
result2 = v.open(param, c2, msg2, r2)

print("\nResult of verifying c1:\t\t", result1)
print("Result of verifying c2:\t\t", result2)

result = v.open(param, addCM, msg1 + msg2, r1, r2)

print("Result of verify Msg+Msg2:\t", result)
