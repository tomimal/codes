'''The class of quaternions is defined.
The operations +, -, *, and / between quaternions are defined using operator overloading.
The class also contains a string representation of quaternions (as in 1+2i-3j+4k),
and methods to find the conjugate and the inverse of a quaternion.
It also contains a method (isReal) to check whether a quaternion has
real numbers as its components.'''

import numbers

class Quaternion:
    # rcomp, icomp, jcomp, and kcomp are the components of a quaternion. They are numbers.
    def __init__(self, rcomp, icomp, jcomp, kcomp):
        self.__rcomp = rcomp
        self.__icomp = icomp
        self.__jcomp = jcomp
        self.__kcomp = kcomp

    # Return the components of a quaternion using index operator
    def __getitem__(self, index):
        if index == 0:
            return self.__rcomp
        if index == 1:
            return self.__icomp
        if index == 2:
            return self.__jcomp
        if index == 3:
            return self.__kcomp

    # Return a string representation
    # addPlus() takes care of the signs; for example, get 1+2i-3j-4k instead of 1+2i+-3j+-4k
    def __str__(self):
        return str(self.__rcomp) + addPlus(self.__icomp) + 'i' \
                                 + addPlus(self.__jcomp) + 'j' + addPlus(self.__kcomp) + 'k' 

    # Define +, -, *, and / between quaternions
    def __add__(self, secondQuaternion):
        rcomp = self.__rcomp + secondQuaternion[0]
        icomp = self.__icomp + secondQuaternion[1]
        jcomp = self.__jcomp + secondQuaternion[2]
        kcomp = self.__kcomp + secondQuaternion[3]
        return Quaternion(rcomp, icomp, jcomp, kcomp)

    def __sub__(self, secondQuaternion):
        rcomp = self.__rcomp - secondQuaternion[0]
        icomp = self.__icomp - secondQuaternion[1]
        jcomp = self.__jcomp - secondQuaternion[2]
        kcomp = self.__kcomp - secondQuaternion[3]
        return Quaternion(rcomp, icomp, jcomp, kcomp)

    def __mul__(self, secondQuaternion):
        # Check first if the second quaternion is a number. This defines the scalar product.
        # A scalar r can be seen as a quaternion r + 0i + 0j + 0k, so one could
        # define the scalar product using quaternion product with Quaternion(r,0,0,0).
        # A direct definition reduces the number of calculations from 16 to 4.
        if isinstance(secondQuaternion, numbers.Real):
            return Quaternion(self.__rcomp * secondQuaternion, self.__icomp * secondQuaternion,
                              self.__jcomp * secondQuaternion, self.__kcomp * secondQuaternion)
        else:
            rcomp = self.__rcomp * secondQuaternion[0] - \
                    self.__icomp * secondQuaternion[1] - \
                    self.__jcomp * secondQuaternion[2] - \
                    self.__kcomp * secondQuaternion[3]
            icomp = self.__rcomp * secondQuaternion[1] + \
                    self.__icomp * secondQuaternion[0] + \
                    self.__jcomp * secondQuaternion[3] - \
                    self.__kcomp * secondQuaternion[2]
            jcomp = self.__rcomp * secondQuaternion[2] - \
                    self.__icomp * secondQuaternion[3] + \
                    self.__jcomp * secondQuaternion[0] + \
                    self.__kcomp * secondQuaternion[1]
            kcomp = self.__rcomp * secondQuaternion[3] + \
                    self.__icomp * secondQuaternion[2] - \
                    self.__jcomp * secondQuaternion[1] + \
                    self.__kcomp * secondQuaternion[0]
            return Quaternion(rcomp, icomp, jcomp, kcomp)

    # Division uses the inverse of a quaternion. This is defined below.
    def __truediv__(self, secondQuaternion):
        return self * secondQuaternion.inverse()

    # Define the length, the conjugate, and the inverse of a quaternion
    def norm(self):
        return (self.__rcomp ** 2 + self.__icomp ** 2 +
                self.__jcomp ** 2 + self.__kcomp ** 2) ** 0.5

    def conjugate(self):
        return Quaternion(self.__rcomp, -self.__icomp, -self.__jcomp, -self.__kcomp)

    def inverse(self):
        return self.conjugate() * (1/(self.norm() ** 2))

    # Check whether the components of a quaternion are real numbers
    def isReal(self):
        return isinstance(self.__rcomp, numbers.Real) and \
               isinstance(self.__icomp, numbers.Real) and \
               isinstance(self.__jcomp, numbers.Real) and \
               isinstance(self.__kcomp, numbers.Real)

def addPlus(number):
    return '+' + str(number) if number >= 0 else str(number)
