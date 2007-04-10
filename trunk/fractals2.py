def build_palette(colors, numberOfColors, prop=None):
   palette = []

   if prop != None:
       prop.append(1 - sum(prop))

   for i in range(len(colors) - 1):
       colorFrom = colors[i]
       colorTo = colors[i + 1]

       if prop == None:
           width = numberOfColors / (len(colors) - 1)
       else:
           width = int(numberOfColors * prop[i])

       colorStep = tuple(
           [(colorTo[j] - colorFrom[j]) / float(width) for j in range(3)])

       for k in range(width):
           palette.append(tuple(
               [int(colorFrom[j] + k * colorStep[j]) for j in range(3)]))

   return palette
