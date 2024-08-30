import re

class validators:
  @staticmethod
  def match_code_or_null(element, patterns, null_values):
    #pattern = re.compile(r"\d\d-\d\d\d")
    if str(element) in null_values: return True;
    if any(re.match(pattern, str(element)) for pattern in patterns): return True;
    #if pattern.match(str(element)): return True;
    return False;

  @staticmethod
  def match_date(element, patterns):
    element = str(element);
    if any(re.match(pattern, element) for pattern in patterns): return True;
    #if pattern.match(str(element)): return True;
    return False;

  @staticmethod
  def match_date_or_null(element, patterns, null_values):
    if element in null_values: return True;
    #pattern = re.compile(r"\d\d-\d\d\d")
    element = str(element);
    if any(re.match(pattern, element) for pattern in patterns): return True;
    #if pattern.match(str(element)): return True;
    return False;

  @staticmethod
  def in_int_interval(element, lower_bound, upper_bound):
    if not isinstance(element, int): return False;
    if lower_bound <= element <= upper_bound: return True;
    return False;

  @staticmethod
  def in_int_interval_or_null(element, lower_bound, upper_bound, null_values):
    if (element in null_values): return True;
    element = str(element);
    if not element.strip().isdigit(): return False;
    if lower_bound <= int(element) <= upper_bound: return True;
    #print("'" + element + "'");
    return False;

  @staticmethod
  def in_category_or_null(element, allowed_values, null_values):
    if element in null_values: return True;
    element = str(element);
    if element in allowed_values: return True;
    return False;

  @staticmethod
  def in_int_category(element, allowed_values):
    if element in allowed_values: return True;
    return False;

  @staticmethod
  def in_int_category_or_null(element, allowed_values, null_values):
    if element in null_values: return True;
    if not isinstance(element, int):
      if not isinstance(element, str) or not element.isdigit(): return False;
      #if not element.isdigit(): return False;
      element = int(element);
    if element in allowed_values: return True;
    return False;

  @staticmethod
  def in_category(element, allowed_values):
    element = str(element);
    if element in allowed_values: return True;
    return False;

  @staticmethod
  #def valid_string(element, null_values):
  def valid_string(element):
    #if element in null_values: return True;
    if not isinstance(element, str): return False;
    return True;

  def valid_string_or_null(element):
    if element in null_values: return True;
    if not isinstance(element, str): return False;
    return True;

  @staticmethod
  def valid_float(element):
    if not isinstance(element, float): return False;
    return True;

  @staticmethod
  def valid_float_or_null(element, null_values):
    if element in null_values: return True;
    if not isinstance(element, float): return False;
    return True;
