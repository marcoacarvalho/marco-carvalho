from sys import stdout

for y in range(-16, 17):
 stdout.write('\n')

 for x in range(0, 86):
   i = j = k = r = 0

   while j**2 + i**2 < 11 and k < 112:
     j = r**2 - i **2 -2 + x / 25.0
     i = 2 * r * i + y / 10.0

     r = j
     k += 1

   stdout.write(" .: ;!/>)|&IH%*#"[k & 15])
