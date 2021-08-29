# Boombastic

### Description :
> A pen and a paper, thats's all you need to watch the movie.    
> `nc 52.149.135.130 4872` 

### Files :  
*[boombastic.py]()*

### Solution : 
Giving a random ticket and by doing some maths we can recover the value of `y` :
```
y = (s^{2} + r) \times (s^{2} - r)^{-1}  \pmod{p}
```
And so the value of `secret` :


Then, we can get the ticket of the word "Boobmastic" and solve the challenge.

*Solver :*
```python

```

FLAG : **FwordCTF{N3v3r_x0r_w1thout_r4nd0m1s1ng_th3_k3y_0r_m4yb3_s3cur3_y0ur_c0d3}**
