def decor(func1):

  def inner():
    s = func1()
    return s.upper()

  return inner

def decor1(func2):

  def wrapper():
    s = func2()
    return s.split()

  return wrapper


def decor2(func3):

  def wrapper1():
    s = func3()
    return s.lower()

  return wrapper1


@decor1
@decor
@decor2
def print_s():
  return "hello world!"


print(print_s())
