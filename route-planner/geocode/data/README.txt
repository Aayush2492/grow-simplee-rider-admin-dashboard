- Mock Test Case Challange 2:
- Given the file with 216 address the initial addresss , cluster and create routes . (bangalore dispatch address.xlsx)
- Number of riders [ 216/20 , 216/30] ~ [7,10] , for this exercise we can take take any number  riders in this range , lets say 8 ,( in final test case we will have 2000 initial addresses , so estimate riders there in a similar fashion)
- Create the initial routes for the dispatch tour , assign each tour to one rider
- Output the route in  formats mentioned in earlier conversations ,
- Lets say initial routes are created , each will have a fixed distance to cover before return to dispatch hub , if all the riders start at same time , say 9am,
  each rider will have covered same distance in an ideal scenario (same average speed)  in any time interval , so after  1 hour , these dynamic points are added,
  this should output a file with rerouted tour and routes .
- In the final 2000 order test case we will have a few dynamic points addition after every hour , twice , i.e, at end of 1st hour and end of 2nd hour, that's how the relative position of each rider for dynamic routing will be determined.
- There is no extra effort required to build a separate visualisation for the evaluation ,
  after each hour the estimated positions of rider in each tour is to be known .



