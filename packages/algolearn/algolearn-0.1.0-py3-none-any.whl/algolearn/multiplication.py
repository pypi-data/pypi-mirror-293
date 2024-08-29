class Multiplication:
  """
  Instantiate a multiplication operation.
  Numbers will be multiplied by the given multiplier.

  :param multiplier:
  :type multiplier: int
  """
  def __init__(self, multiplier: int):
    self.multiplier = multiplier
  
  def multiply(self, number: int) -> int:
    """
    Multiply a given number by a given multiplier.
  
    :param number: The number to multiply.
    :type number:

    :return: The result of the multiplication
    :rtype: int
    """
    return number * self.multiplier

multiplication = Multiplication(2)

print(multiplication.multiply(5))
