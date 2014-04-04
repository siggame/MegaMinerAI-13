from seastar import *

print "Small List Test"

x = xytuples_to_clist([(3,4),(5,6)])

print "Created Ctype:"
print x

print "Reverse (known length)"
y = list(clist_to_xytuples(x, 4))

print y

print "Small List Test (-1 Terminate)"

x = xytuples_to_clist([(3,4),(5,6),(-1,0)])
y = list(clist_to_xytuples(x))

print y

ss = Seastar(20,20)

print ss.get_path([(0,0)],[(19,19)])
