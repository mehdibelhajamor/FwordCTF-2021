# Transfer

### Description :
> My friend got access to the National Bank Money Transfer. He tried to transfer money to his account as much as he wants BUT it's limited.  
> Could you break it ?  
> `nc 52.149.135.130 4870` 

### Files :  
*[transfer.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Transfer/transfer.py)*  
*[ed25519.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Transfer/ed25519.py)*

### Solution : 
[Ed25519](https://en.wikipedia.org/wiki/EdDSA) is still compromised if two different messages are signed using the same value for `r`. This is obviously impossible in theory, since it is deterministic. But what if an error occurs during the computation of `Hint(R, pk, m)` and produces a `S'` instead ?  
That can cause a Fault Attack where you can possibly recover the value `a` by computing :

![CodeCogsEqn (2)](https://user-images.githubusercontent.com/62826765/131237348-8b95980d-1677-4616-97f9-349a85e0a901.gif)

with `h = Hint(R, pk, m)` and `h' = Hint(R', pk, m)`





***Solver :***
```python

```

FLAG : **FwordCTF{4lw47ys_ch3ck_1f_a_p01nt_1s_0n_th3_curv3_0r_g3t_tr1ck3d}**
