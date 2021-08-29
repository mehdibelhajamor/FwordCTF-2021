# Invincible

### Description :
> Beat me in my game, if you can.  
> `nc 52.149.135.130 4874` 

### Files :  
*[invincible.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Invincible/invincible.py)*

### Solution : 
Giving a random ticket and by doing some maths we can recover the value of `y` :

![CodeCogsEqn (1)](https://user-images.githubusercontent.com/62826765/131235239-0cf2e8cb-10c5-4845-927b-dcfff79ce604.gif)

And so the value of `secret` :

![CodeCogsEqn](https://user-images.githubusercontent.com/62826765/131235230-dcbee216-d720-45ff-b647-8d5f09f6c7d6.gif)

Then, we can generate a ticket for the word "Boobmastic" and solve the challenge.

***Solver :***
```python

```

FLAG : **FwordCTF{4ct_l1k3_a_V1P_4nd_b3c0m3_a_V1P}**
