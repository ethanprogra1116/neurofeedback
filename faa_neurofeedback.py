"""
FAA Neurofeedback - Visualización en tiempo real vía LSL
---------------------------------------------------------
Recibe el valor FAA desde OpenViBE por LSL y muestra
un gradiente proporcional: negro (negativo) → blanco (positivo).

Requisito:
    pip install pylsl

Teclas:
    ESC  - cerrar
    +/-  - ajustar umbral (rango esperado del FAA)
"""

import threading
import tkinter as tk

from pylsl import StreamInlet, resolve_byprop

# ── Configuración ─────────────────────────────────────────────────────────────
FAA_RANGE = 5.0  # Umbral ±: ajusta si la pantalla se queda muy oscura/clara
UPDATE_MS = 50  # Refresco de pantalla en ms
# ──────────────────────────────────────────────────────────────────────────────

latest_faa = [None]  # compartido entre hilo LSL y hilo GUI
lsl_status = ["Buscando stream LSL..."]


def lsl_thread():
    """Hilo que recibe muestras LSL continuamente."""
    from pylsl import resolve_streams

    lsl_status[0] = "Buscando stream LSL..."
    # Espera cualquier stream disponible (sin filtrar por tipo)
    streams = []
    while not streams:
        streams = resolve_streams(wait_time=1.0)
    inlet = StreamInlet(streams[0])
    info = streams[0]
    lsl_status[0] = ""
    while True:
        sample, _ = inlet.pull_sample()
        latest_faa[0] = sample[0]  # primer canal = FAA


def faa_to_gray(faa, faa_range):
    t = (faa + faa_range) / (2 * faa_range)
    t = max(0.0, min(1.0, t))
    return int(t * 255)


def gray_to_hex(g):
    return f"#{g:02x}{g:02x}{g:02x}"


class NeurofeedbackApp:
    def __init__(self):
        self.faa_range = FAA_RANGE

        self.root = tk.Tk()
        self.root.title("FAA Neurofeedback")
        self.root.geometry("900x600")
        self.root.configure(bg="#808080")

        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#808080")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.lbl_faa = tk.Label(
            self.root,
            text="FAA: --",
            font=("Helvetica", 28, "bold"),
            bg="#808080",
            fg="#ffffff",
        )
        self.lbl_faa.place(relx=0.5, rely=0.88, anchor="center")

        self.lbl_range = tk.Label(
            self.root,
            text=f"Umbral ±{self.faa_range:.2f}",
            font=("Helvetica", 14),
            bg="#808080",
            fg="#aaaaaa",
        )
        self.lbl_range.place(relx=0.5, rely=0.94, anchor="center")

        self.lbl_status = tk.Label(
            self.root,
            text=lsl_status[0],
            font=("Helvetica", 12),
            bg="#808080",
            fg="#ff6666",
        )
        self.lbl_status.place(relx=0.5, rely=0.97, anchor="center")

        self._draw_scale_bar()

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<plus>", lambda e: self._adjust_range(+0.1))
        self.root.bind("<minus>", lambda e: self._adjust_range(-0.1))
        self.root.bind("<KP_Add>", lambda e: self._adjust_range(+0.1))
        self.root.bind("<KP_Subtract>", lambda e: self._adjust_range(-0.1))

        # Hilo LSL en background
        t = threading.Thread(target=lsl_thread, daemon=True)
        t.start()

        self._update()
        self.root.mainloop()

    def _draw_scale_bar(self):
        bar_w, bar_h = 30, 400
        bar_x, bar_y = 30, 100
        self.canvas.delete("scalebar")
        for i in range(bar_h):
            g = int((1 - i / bar_h) * 255)
            self.canvas.create_line(
                bar_x,
                bar_y + i,
                bar_x + bar_w,
                bar_y + i,
                fill=gray_to_hex(g),
                tags="scalebar",
            )
        self.canvas.create_text(
            bar_x + bar_w // 2,
            bar_y - 15,
            text="+",
            fill="white",
            font=("Helvetica", 14, "bold"),
            tags="scalebar",
        )
        self.canvas.create_text(
            bar_x + bar_w // 2,
            bar_y + bar_h + 15,
            text="-",
            fill="white",
            font=("Helvetica", 14, "bold"),
            tags="scalebar",
        )
        faa = latest_faa[0]
        if faa is not None:
            g_cur = faa_to_gray(faa, self.faa_range)
            ind_y = bar_y + bar_h - int((g_cur / 255) * bar_h)
            self.canvas.create_line(
                bar_x - 8,
                ind_y,
                bar_x + bar_w + 8,
                ind_y,
                fill="#00ff88",
                width=2,
                tags="scalebar",
            )

    def _adjust_range(self, delta: float):
        self.faa_range = max(0.1, self.faa_range + delta)
        self.lbl_range.config(text=f"Umbral ±{self.faa_range:.2f}")

    def _update(self):
        faa = latest_faa[0]

        self.lbl_status.config(text=lsl_status[0])

        if faa is not None:
            gray = faa_to_gray(faa, self.faa_range)
            color = gray_to_hex(gray)
            text_fg = "#000000" if gray > 140 else "#ffffff"

            self.canvas.configure(bg=color)
            self.root.configure(bg=color)
            self.lbl_faa.configure(text=f"FAA: {faa:+.4f}", bg=color, fg=text_fg)
            self.lbl_range.configure(bg=color, fg=text_fg)
            self.lbl_status.configure(bg=color)
            self._draw_scale_bar()

        self.root.after(UPDATE_MS, self._update)


if __name__ == "__main__":
    NeurofeedbackApp()
