# CS61C-fa20-proj4

This is my complete solution for CS61C-fa20-proj4 when I'm learning CS61C fa20 version by myself.
However, I can't access dumbpy module, which is on hive machine and can't access by those
without remote machine account.
But during the process of building this project, I realized that the dumbpy module is only a version
of numc without any optimization, just for speed up comparison, that's why it's called dumbpy.
So I rewrite the full tests to test the correctness of my base version of numc, then copy it to 
create dumbpy module. 
After that, I optimize the code to speed up, and compare the speedup version of numc with my base
version, which is also my dumbpy version.
The base version is with little optimization, because when I iterate through matrix to compute 
multiplication, I used the knowledge of cache, so maybe you may find your code is slower than my 
dumbpy version

# numc

Here's what I did in project 4:
-