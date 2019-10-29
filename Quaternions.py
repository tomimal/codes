'''The class of quaternions is defined.
The operations +, -, *, and / between quaternions are defined using operator overloading.
The class also contains a string representation of quaternions (as in 1+2i-3j+4k),
and methods to find the conjugate and the inverse of a quaternion.'''

import numbers

class Quaternion:
    # rcomp, icomp, jcomp, and kcomp are the components of a quaternion.
    def __init__(self, rcomp, icomp, jcomp, kcomp):
        self.rcomp = float(rcomp)
        self.icomp = float(icomp)
        self.jcomp = float(jcomp)
        self.kcomp = float(kcomp)
        self.qlist = [self.rcomp, self.icomp, self.jcomp, self.kcomp]

    def __getitem__(self, index):
        return self.qlist[index]
    
    # addPlus() takes care of the signs; for example, get 1+2i-3j-4k instead of 1+2i+-3j+-4k
    def __str__(self):
        return str(self.rcomp) + addPlus(self.icomp) + 'i' \
                               + addPlus(self.jcomp) + 'j' + addPlus(self.kcomp) + 'k'

    def __iter__(self):
        return (i for i in self.qlist)

    def __abs__(self):
        return (self.rcomp ** 2 + self.icomp ** 2 +
                self.jcomp ** 2 + self.kcomp ** 2) ** 0.5

    def __format__(self, fmt = ''):
        components = (format(c, fmt) for c in self)
        q = Quaternion(*components)
        return str(q)

    def __bool__(self):
        return abs(self)
    
    def __add__(self, secondQuaternion):
        rcomp = self.rcomp + secondQuaternion[0]
        icomp = self.icomp + secondQuaternion[1]
        jcomp = self.jcomp + secondQuaternion[2]
        kcomp = self.kcomp + secondQuaternion[3]
        return Quaternion(rcomp, icomp, jcomp, kcomp)

    def __sub__(self, secondQuaternion):
        rcomp = self.rcomp - secondQuaternion[0]
        icomp = self.icomp - secondQuaternion[1]
        jcomp = self.jcomp - secondQuaternion[2]
        kcomp = self.kcomp - secondQuaternion[3]
        return Quaternion(rcomp, icomp, jcomp, kcomp)

    def __mul__(self, secondQuaternion):
        # Check first if the second quaternion is a number. This defines the scalar product.
        # A scalar r can be seen as a quaternion r + 0i + 0j + 0k, so one could
        # define the scalar product using quaternion product with Quaternion(r,0,0,0).
        # A direct definition reduces the number of calculations from 16 to 4.
        if isinstance(secondQuaternion, numbers.Real):
            return Quaternion(self.rcomp * secondQuaternion, self.icomp * secondQuaternion,
                              self.jcomp * secondQuaternion, self.kcomp * secondQuaternion)
        else:
            rcomp = self.rcomp * secondQuaternion[0] - \
                    self.icomp * secondQuaternion[1] - \
                    self.jcomp * secondQuaternion[2] - \
                    self.kcomp * secondQuaternion[3]
            icomp = self.rcomp * secondQuaternion[1] + \
                    self.icomp * secondQuaternion[0] + \
                    self.jcomp * secondQuaternion[3] - \
                    self.kcomp * secondQuaternion[2]
            jcomp = self.rcomp * secondQuaternion[2] - \
                    self.icomp * secondQuaternion[3] + \
                    self.jcomp * secondQuaternion[0] + \
                    self.kcomp * secondQuaternion[1]
            kcomp = self.rcomp * secondQuaternion[3] + \
                    self.icomp * secondQuaternion[2] - \
                    self.jcomp * secondQuaternion[1] + \
                    self.kcomp * secondQuaternion[0]
            return Quaternion(rcomp, icomp, jcomp, kcomp)

    # To allow scalar multiplication also from the left
    def __rmul__(self, secondQuaternion):
        return self.mul__(secondQuaternion)

    def __truediv__(self, secondQuaternion):
        return self * secondQuaternion.inverse()

    def conjugate(self):
        return Quaternion(self.rcomp, -self.icomp, -self.jcomp, -self.kcomp)

    def inverse(self):
        return self.conjugate() * (1/(abs(self) ** 2))


def addPlus(number):
    return '+' + str(number) if number >= 0 else str(number)
