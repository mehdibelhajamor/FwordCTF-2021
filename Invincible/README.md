# Invincible

### Description :
> Beat me in my game, if you can.  
> `nc 52.149.135.130 4874` 

### Files :  
*[invincible.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Invincible/invincible.py)*

### Solution : 
We notice that both *Add* and *Multiply* operations are independent of `b`. Also the EllipticCurve class doesn't check for the existance of a given point.  
Since we have control on a point we can go through the Invalid Curve Attack.

By modifying `b` we can get another curve that may have an order with a small factor.  
For exemple, `b = 3` generates a curve with order `115792089210356248762697446949407573529995394580452997270780266901612618829008` that had a small factor 3. So we can generate a point with order 3.  
Here's a [Sagemath](https://www.sagemath.org/) script :
```python
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
b = 3
E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]
P = G*ZZ(E.order()/3)
print(P)
```

***Solver :***
```python

```

FLAG : **FwordCTF{4ct_l1k3_a_V1P_4nd_b3c0m3_a_V1P}**
