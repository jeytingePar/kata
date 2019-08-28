import json
import requests
import geopy.distance

def main():  
 goodInput = False
 while not goodInput:
  latitude = input("Enter latitude ")
  latitude = ConvertCoordinates(latitude, True)
  longitude = input("Enter longitude ")
  longitude = ConvertCoordinates(longitude, False)
  goodInput = HandleInputs(latitude, longitude)

 response = requests.get('https://opensky-network.org/api/states/all',verify=False)
 data = response.json()
 planes = data["states"]
 closestPlane=None
 closestDistance = 99999999
 for x in planes:
  currentDistance = GetMilesBetweenCoordinates(x[6],x[5],latitude,longitude)
  if currentDistance < closestDistance:
   closestDistance = currentDistance
   closestPlane=x

 print ("The closest plane is ",closestDistance," miles away")
 print ("Name ",closestPlane[1],"\nLatitude ",closestPlane[5],"\nLongitude",closestPlane[6],"\nAltitude",closestPlane[7]," meters","\nCountry of origin ",closestPlane[2])


def GetMilesBetweenCoordinates(fromLat,fromLong,toLat,toLong):
 coordsFrom = (fromLat, fromLong)
 coordsTo = (toLat,toLong) 
 return geopy.distance.geodesic(coordsFrom, coordsTo).miles

def ConvertCoordinates(coordinate, isLatitude):
  coordinate = coordinate.replace(" ", "")
  dirs = ["N", "n", "S","s", "E", "e", "W", "w"]
  if (coordinate.endswith(tuple(dirs))):
   direction = coordinate[-1:].lower()   
   coordinate = coordinate[:-1]    
   coordinate = int(coordinate)
   if (isLatitude == True):
    if (direction == "s"):
     coordinate = coordinate * -1
   else:
    if (direction == "w"):
     coordinate = coordinate * -1
  coordinate = int(coordinate)
  return coordinate  

def HandleInputs(latitude, longitude):  
 if latitude < -90 or latitude > 90:
  print ("latitude must be between -90 and 90")
  return False 
 if longitude < -180 or longitude > 180:
  print ("longitude must be between 180 and -180")
  return False
 return True

if __name__ == "__main__":
 main()