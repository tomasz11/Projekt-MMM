import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class Rlc_circut:
    def __init__(self, R, R2, C):
        self.R = R
        self.R2 = R2
        self.C = C
    
    def get_biegun(self):
        a = self.R * self.R2 * self.C
        b = self.R + self.R2
        return -b/a if a != 0 else 0

class Simulation(Rlc_circut):
    def model_ukladu(self, u_r, u_in_t, R, R2, C):
        return (R * u_in_t - (R2 + R) * u_r) / (R2 * R * C)

    def sim(self, R_val=None, R2_val=None, C_val=None):
       
        R = R_val if R_val is not None else self.R
        R2 = R2_val if R2_val is not None else self.R2
        C = C_val if C_val is not None else self.C
        
        T_max = 0.05 
        dt = 1e-4
        t = np.arange(0, T_max, dt)
        u_out = np.zeros(len(t))
        u_in_sig = 2 * np.sin(2 * np.pi * 100 * t)

        for i in range(len(t) - 1):
            y = u_out[i]
            u_t = u_in_sig[i] 
            # RK4
            k1 = self.model_ukladu(y, u_t, R, R2, C)
            k2 = self.model_ukladu(y + dt/2 * k1, u_t, R, R2, C)
            k3 = self.model_ukladu(y + dt/2 * k2, u_t, R, R2, C)
            k4 = self.model_ukladu(y + dt * k3, u_t, R, R2, C)
            u_out[i+1] = y + (dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)
            
        return t, u_out, u_in_sig

class InteractiveDisplay(Simulation):
    def __init__(self, R, R2, C):
        super().__init__(R, R2, C)
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        plt.subplots_adjust(bottom=0.3) # Miejsce na suwaki
        
        # Pierwsza symulacja
        self.t, self.u_out, self.u_in = self.sim()
        
        # Linie wykresu
        self.line_out, = self.ax.plot(self.t, self.u_out, label='Wyjście (u_out)', color='blue')
        self.line_in, = self.ax.plot(self.t, self.u_in, '--', label='Wejście (u_in)', color='red', alpha=0.5)
        
        self.ax.set_ylim(-2.5, 2.5)
        self.ax.grid(True, linestyle=':')
        self.ax.legend()
        self.title = self.ax.set_title(f"Biegun: {self.get_biegun():.2f}")

       
        ax_r = plt.axes([0.2, 0.15, 0.65, 0.03])
        ax_r2 = plt.axes([0.2, 0.10, 0.65, 0.03])
        ax_c = plt.axes([0.2, 0.05, 0.65, 0.03])

        self.slider_r = Slider(ax_r, 'R [Ω]', 100, 5000, valinit=R)
        self.slider_r2 = Slider(ax_r2, 'R2 [Ω]', 100, 5000, valinit=R2)
        self.slider_c = Slider(ax_c, 'C [μF]', 0.1, 10, valinit=C*1e6)

        # Reakcja na zmianę
        self.slider_r.on_changed(self.update)
        self.slider_r2.on_changed(self.update)
        self.slider_c.on_changed(self.update)

    def update(self, val):
    
        r_val = self.slider_r.val
        r2_val = self.slider_r2.val
        c_val = self.slider_c.val * 1e-6 # powrót do Faradów
        
        
        _, new_out, _ = self.sim(r_val, r2_val, c_val)
        
        
        self.line_out.set_ydata(new_out)
        
        
        self.R, self.R2, self.C = r_val, r2_val, c_val
        self.title.set_text(f"Biegun: {self.get_biegun():.2f}")
        
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


app = InteractiveDisplay(1000, 500, 1e-6)
app.show()
