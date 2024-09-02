import sys

waypoints = sys.argv[1]

# directives r<N> right N
#            l<N> left N
#            u<N> up N
#            d<N> down N
# ',' seperates directives, ',,' marks a waypoint (except for the last)
# no spaces

res = [ [0,0] ]

for p in waypoints.split(",,"):
    dlist = p.split(",")
    nx = res[-1][0]
    ny = res[-1][1]
    for d in dlist:
        di = d[0].upper()
        v = float(d[1:])
        if di == "U":
            ny += v
        if di == "D":
            ny -= v
        if di == "L":
            nx -= v
        if di == "R":
            nx += v
    res += [ [nx, ny] ]

res += [ [0,0] ]

print(res)
