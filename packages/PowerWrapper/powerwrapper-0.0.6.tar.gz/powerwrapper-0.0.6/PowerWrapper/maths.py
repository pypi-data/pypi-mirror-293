import statistics
import math

# Main maths class
class maths():
        def getMean(self, meanVal):
            return statistics.mean(meanVal)
        
        def getMedian(self, medianVal):
            return statistics.median(medianVal)
        
        def getMode(self, modeVal):
            return statistics.mode(modeVal)

        def squareRoot(self, squarerootValue):
             return math.sqrt(squarerootValue)
                
        def getMod(self, valOne, valTwo):
             return math.fmod(valOne, valTwo)
