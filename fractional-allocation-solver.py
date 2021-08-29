import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# adds up all the values in in configuration from [ dimension, len(configuration) )
def sum(dimension, configuration):
    total = 0.0
    for d in range(dimension, len(configuration)):
        total += configuration[d]
    return total

def iterateFixedQuantity(totalQuantity, interval, numDimensions):
    configuration = [totalQuantity]
    for d in range(1, numDimensions):
        configuration.append(0.0)
    
    yield configuration

    while (totalQuantity - configuration[len(configuration)-1]) > interval: # while last square hasn't taken up the entire area
        for d in range(1, len(configuration)):
            if totalQuantity - sum(d, configuration) > interval: # if this square is able to grow at the expense of its subordinate squares
                configuration[d] += interval # then grow it
                break
            else:
                configuration[d] = 0.0 # otherwise reset it and try the higher-order square
        configuration[0] = totalQuantity - sum(1, configuration)

        yield configuration

def getLinear(m,b):
  def linear(x):
    return m*x+b
  return linear

def getExponential(a, b, c, d):
  def exponential(x):
    return 1/(a*(x-b)**c) + d
  return exponential

class Use:
  def __init__(self, name, h, m, b) -> None:
    self.name = name
    self.h = h
    self.price = getLinear(m, b)
  def getRevenue(self, quantity) -> float:
    return self.h * quantity * self.price(quantity * self.h)

with open('sample-data') as f:
  # Read the file and parse as JSON object
  text = f.read()
  jsonData = json.loads(text)

  # Read some global information
  priceUnit = jsonData['priceUnit']
  quantityUnit = jsonData['quantityUnit']
  totalQuantity = jsonData['totalQuantity']


  # Read descriptions of all the uses for the resource

  usesData = jsonData['uses']

  uses = [ ]
  for use in usesData:
    uses.append(
      Use(use['name'],use['h'],use['m'],use['b'])
    )

  if len(uses) < 3:
    print('This program does not currently support the allocation of fewer than 3 resources')
    exit()


  # Loop through all permissible combinations

  maxConfig, maxRevenue = None, None

  for configuration in iterateFixedQuantity(totalQuantity, totalQuantity/100.0, len(uses)):
    revenue = 0.0
    for useIdx in range(len(configuration)):
      # 'uses' and 'configuration' are parallel arrays
      revenue += uses[useIdx].getRevenue(configuration[useIdx])
    if maxRevenue is None or maxRevenue < revenue:
      maxConfig = configuration.copy()
      maxRevenue = revenue


  # Output the final configuration

  for useIdx in range(len(uses)):
    print(f'Quantity for {uses[useIdx].name}:\t{maxConfig[useIdx]:.2f}')
  print(f'Total Revenue: {maxRevenue:.2f}')
