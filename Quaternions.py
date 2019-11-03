'''The class of quaternions is defined.
The operations +, -, *, and / between quaternions are defined using operator overloading.
The class also contains a string representation of quaternions (as in 1+2i-3j+4k),
and methods to find the conjugate and the inverse of a quaternion.'''

import numbers

class Quaternion:
    # components is a sequence of 
    def __init__(self, components):
        self.comps = [float(comp) for comp in components]

    def __getitem__(self, index):
        return self.comps[index]
    
    # addPlus() takes care of the signs; for example, get 1+2i-3j-4k instead of 1+2i+-3j+-4k
    def __str__(self):
        return str(self[0]) + addPlus(self[1]) + 'i' \
                            + addPlus(self[2]) + 'j' + addPlus(self[3]) + 'k'
            
    def __abs__(self):
        return (sum([comp ** 2 for comp in self])) ** 0.5

    def __format__(self, fmt = ''):
        components = [format(c, fmt) for c in self]
        q = Quaternion(components)
        return str(q)

    def __bool__(self):
        return abs(self)

    def __neg__(self):
        return Quaternion([-comp for comp in self])
    
    def __add__(self, other):
        return Quaternion([a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        # Check first if the second quaternion is a number. This defines scalar product.
        # A scalar r can be seen as a quaternion r + 0i + 0j + 0k, so one could
        # define the scalar product using quaternion product with Quaternion(r,0,0,0).
        if isinstance(other, numbers.Real):
            return Quaternion([other * comp for comp in self])
        else:
            rcomp = self[0] * other[0] - self[1] * other[1] - \
                    self[2] * other[2] - self[3] * other[3]
            icomp = self[0] * other[1] + self[1] * other[0] + \
                    self[2] * other[3] - self[1] * other[2]
            jcomp = self[0] * other[2] - self[1] * other[3] + \
                    self[2] * other[0] + self[3] * other[1]
            kcomp = self[0] * other[3] + self[1] * other[2] - \
                    self[2] * other[1] + self[3] * other[0]
            return Quaternion([rcomp, icomp, jcomp, kcomp])

    # To allow scalar multiplication also from the left
    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other.inverse()

    def conjugate(self):
        return Quaternion([self[0], -self[1], -self[2], -self[3]])

    def inverse(self):
        return self.conjugate() * (1/(abs(self) ** 2))


def addPlus(number):
    return '+' + str(abs(number)) if number >= 0 else str(number)
