## Findings  
  
- The addresses are assumed to be accurate, can be considered points.
- Around 10% of points can be added dynamically (pickups).
- Suppose we have `m` drivers and `n` shipments,
- `m` is in the range of `n/30` to `n/20`
- `m` is a whole number
- `80*80*100` cms and `60*60*100` are the dimensions of the bags.  
- Object will be of max `l*b*h = 40*40*20` cms and min `3*3*3` cms.  


## Objectives

- Design a route to traverse `N` nodes using `M` trucks such that
  at any point in time, the total volume of $i^{\text{th}}$ truck
  $v_i$ is less than or equal to the volume of the bag $V_b$.
- Say that the time required to reach node $i$ is $t_i$, then we
  want to maximize the number of $i$ such that $t_i \leq T_i$ where  
  $T_i$ is the time limit for the driver to reach the destination.

