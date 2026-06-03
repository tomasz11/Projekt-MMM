import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

r2_wartosc = 10.0
r_wartosc  = 50.0
c_wartosc  = 0.001

rodzaj_sygnalu = 'trojkatny'
amplituda = 10.0
czestotliwosc = 10.0

krok_dt = 0.0001
czas_symulacji = 0.5
czas = np.arange(0, czas_symulacji, krok_dt)

fig, axs = plt.subplots(3, 1, figsize=(10, 8))
plt.subplots_adjust(bottom=0.3, hspace=0.4)

ax_r2    = plt.axes([0.1, 0.20, 0.35, 0.03])
ax_r     = plt.axes([0.1, 0.15, 0.35, 0.03])
ax_c     = plt.axes([0.1, 0.10, 0.35, 0.03])
ax_amp   = plt.axes([0.55, 0.20, 0.35, 0.03])
ax_freq  = plt.axes([0.55, 0.15, 0.35, 0.03])
ax_radio = plt.axes([0.55, 0.02, 0.20, 0.10])

suwak_r2 = Slider(ax_r2, 'R2 [Ohm]', 1.0, 200.0, valinit=r2_wartosc)
suwak_r  = Slider(ax_r, 'R [Ohm]', 1.0, 200.0, valinit=r_wartosc)
suwak_c  = Slider(ax_c, 'C [mF]', 0.1, 10.0, valinit=c_wartosc * 1000)
suwak_amp  = Slider(ax_amp, 'Amp.', 1.0, 20.0, valinit=amplituda)
suwak_freq = Slider(ax_freq, 'Czes.', 1.0, 500.0, valinit=czestotliwosc)
przyciski = RadioButtons(ax_radio, ('trojkatny', 'prostokatny', 'harmoniczny'), active=0)

def aktualizuj(val):
    global r2_wartosc, r_wartosc, c_wartosc, amplituda, czestotliwosc, rodzaj_sygnalu
    
    r2_wartosc = suwak_r2.val
    r_wartosc = suwak_r.val
    c_wartosc = suwak_c.val / 1000.0
    amplituda = suwak_amp.val
    czestotliwosc = suwak_freq.val
    rodzaj_sygnalu = przyciski.value_selected
    
    u_wejscie = np.zeros(len(czas))
    
    if rodzaj_sygnalu == 'prostokatny':
        u_wejscie[(czas >= 0.05) & (czas <= 0.25)] = amplituda
        
    elif rodzaj_sygnalu == 'trojkatny':
        T = 1.0 / czestotliwosc
        for i in range(len(czas)):
            t_w_okresie = czas[i] % T
            if t_w_okresie < T / 2:
                u_wejscie[i] = -amplituda + (4 * amplituda / T) * t_w_okresie
            else:
                u_wejscie[i] = 3 * amplituda - (4 * amplituda / T) * t_w_okresie
        
    elif rodzaj_sygnalu == 'harmoniczny':
        u_wejscie = amplituda * np.sin(2 * np.pi * czestotliwosc * czas)
        
    u_c = np.zeros(len(czas))
    for k in range(0, len(czas) - 1):
        prad_wej = (u_wejscie[k] - u_c[k]) / r2_wartosc
        prad_wyj = u_c[k] / r_wartosc
        du_c = (prad_wej - prad_wyj) / c_wartosc
        u_c[k+1] = u_c[k] + du_c * krok_dt
        
    f_bode = np.logspace(-1, 4, 1000)
    w = 2 * np.pi * f_bode
    
    k = r_wartosc / (r_wartosc + r2_wartosc)
    T_stala = (r_wartosc * r2_wartosc * c_wartosc) / (r_wartosc + r2_wartosc)
    
    bode_amplituda = 20 * np.log10(k / np.sqrt(1 + (w * T_stala)**2))
    bode_faza = -np.arctan(w * T_stala) * 180 / np.pi
    
    for ax in axs:
        ax.clear()
        
    axs[0].plot(czas, u_wejscie, 'r-', label='Wejscie u(t)')
    axs[0].plot(czas, u_c, 'b-', label='Wyjscie y(t)')
    axs[0].set_title('Odpowiedz czasowa układu')
    axs[0].set_ylabel('Napiecie [V]')
    axs[0].grid(True)
    axs[0].legend()
    
    axs[1].semilogx(f_bode, bode_amplituda, 'g-')
    axs[1].set_title('Charakterystyka amplituda-czestotliwosc (Bode)')
    axs[1].set_ylabel('Amplituda [dB]')
    axs[1].grid(True, which="both")
    
    axs[2].semilogx(f_bode, bode_faza, 'm-')
    axs[2].set_title('Charakterystyka faza-czestotliwosc (Bode)')
    axs[2].set_xlabel('Czestotliwosc [Hz]')
    axs[2].set_ylabel('Faza [deg]')
    axs[2].grid(True, which="both")
    
    fig.canvas.draw_idle()

suwak_r2.on_changed(aktualizuj)
suwak_r.on_changed(aktualizuj)
suwak_c.on_changed(aktualizuj)
suwak_amp.on_changed(aktualizuj)
suwak_freq.on_changed(aktualizuj)
przyciski.on_clicked(aktualizuj)

aktualizuj(None)
plt.show()