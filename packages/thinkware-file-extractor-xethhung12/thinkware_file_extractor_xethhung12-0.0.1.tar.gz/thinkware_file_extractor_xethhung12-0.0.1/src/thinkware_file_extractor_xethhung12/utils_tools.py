import sys

width_for_4k="3840"
width_for_2k="2560"

def get_scale(val) -> str:
  if val == width_for_4k:
    return "940"
  elif val == width_for_2k:
    return "740"
  else:
    return "UNKNOWN"

def  get_x(val) -> str:
  if val == width_for_4k:
    return "420"
  elif val == width_for_2k:
    return "350"
  else:
    return "UNKNOWN"

def get_y(val) -> str:
  if val == width_for_4k:
    return "1500"
  elif val == width_for_2k:
    return "980"
  else:
    return "UNKNOWN"

# if __name__ == "__main__":
#   if sys.argv[1] == "scale":
#     print(get_scale())
#   elif sys.argv[1] == "x":
#     print(get_x())
#   elif sys.argv[1] == "y":
#     print(get_y())
#   else:
#     sys.exit(1)
