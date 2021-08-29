# Invincible

### Description :
> Beat me in my game, if you can.  
> `nc 52.149.135.130 4874` 

### Files :  
*[invincible.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Invincible/invincible.py)*

### Solution : 
We notice that both *Add* and *Multiply* operations are independent of `b`. Also the EllipticCurve class doesn't check for the existance of a given point.  
Since we have control on a point we can go through the Invalid Curve Attack.

By modifying `b` we can generates another curve that may have an order with a small factor.  
For exemple, `b = 3` generates a curve with order `115792089210356248762697446949407573529995394580452997270780266901612618829008` that had a small factor 3.  
So we can generate a point with order 3.  
Here's a [Sagemath](https://www.sagemath.org/) script :
```python
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
b = 3
E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]
T = G*ZZ(E.order()/3)
print(T)
```
We get this point `T = (89995002874197087156160429731648695860910221822426040658975619972952380673767, 101442345749797973087567911870369208228023400114057003174595439233607451145078)`  
It can only generates 3 point :
```
(0 : 1 : 0)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 101442345749797973087567911870369208228023400114057003174595439233607451145078 : 1)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 14349743460558275675129535079038365302062743301233311020938192075259646708873 : 1)
(0 : 1 : 0)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 101442345749797973087567911870369208228023400114057003174595439233607451145078 : 1)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 14349743460558275675129535079038365302062743301233311020938192075259646708873 : 1)
(0 : 1 : 0)
```
Choosing this point T, The first seed will always be either `0` or `89995002874197087156160429731648695860910221822426040658975619972952380673767`.  
And if we know the first seed, we can know all next seeds and so we can compute all 100 key to decrypt all 100 ciphertexts and win the game. 

***Solver :***
```python

```

FLAG : **FwordCTF{4ct_l1k3_a_V1P_4nd_b3c0m3_a_V1P}**
