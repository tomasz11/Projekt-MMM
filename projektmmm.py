import numpy as np
import matplotlib.pyplot as plt

def model_ukladu(t, u_r, u_in_t, R, R2, C):
    return (R * u_in_t - (R2 + R) * u_r) / (R2 * R * C)
def bieguny(R,R2,C):
    a = R * R2 * C
    b = R + R2
    biegun = -b/a
    print(biegun)
    return biegun

R = 1000.0
R2 = 500.0
C = 1e-6
dt = 1e-5  
T_max = 0.01 


t = np.arange(0, T_max, dt)
u_out = np.zeros(len(t))
u_in = np.ones(len(t)) 
u_in2 = 2 * np.sin(2 * np.pi * 100 * t)
#Tu najdokladniejsza metoda rk4 , dzieki czemu uzyskujemy (chyba) najlepsze przyblizenie, o wiele lepsze niz w przypadku metody eulera
for i in range(len(t) - 1):
    curr_t = t[i]
    y = u_out[i]
    u_t = u_in2[i] 
    
 
    k1 = model_ukladu(curr_t, y, u_t, R, R2, C)
    
    k2 = model_ukladu(curr_t + dt/2, 
                      y + dt/2 * k1, u_t, R, R2, C)
    
    k3 = model_ukladu(curr_t + dt/2,y + dt/2 * k2, u_t, R, R2, C)
    
    k4 = model_ukladu(curr_t + dt,  y + dt * k3,u_t, R, R2, C)
    
    u_out[i+1] = y + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)


bieguny(R,R2,C)
plt.figure(figsize=(10, 5))
plt.plot(t, u_out, label='Napięcie na R (Wyjście)')
plt.plot(t, u_in2, '--', label='Napięcie wejściowe (Skok)')
plt.grid(True)
plt.legend()
plt.title("Symulacja układu metodą Rungego-Kutty 4. rzędu")
plt.show()

R=1000
R2=500
C=1e-6

