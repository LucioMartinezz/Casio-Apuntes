import casioplot
print(dir(casioplot))
try:
  import matplotl
  print("matplotl: si")
except ImportError:
  print("matplotl: no")
print("Ahora apreta AC/ON")
try:
  while 1:pass
except KeyboardInterrupt:
  print("AC atrapado: OK")
print("Fin de la prueba")
