import tkinter as tk
import random
import math

# ---------- Config globale (modifie si besoin) ----------
ROWS = 50
COLS = 50
CELL_SIZE = 22
BASE_INFECTION_DURATION = 6   # durée de référence (sera modulée par les paramètres)
MUTATION_INCREMENT = 0.002    # augmentation de mutation_rate chaque génération
MUTATION_EFFECT_SCALE = 0.05  # grandeur de la modification sur prop/mort quand muter
NEIGHBOR_DIRS = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),           (0, 1),
                 (1, -1),  (1, 0),  (1, 1)]

# ---------- Etats ----------
STATE_SUSCEPTIBLE = 0
STATE_INFECTED = 1
STATE_DEAD = 2

STATE_COLOR = {
    STATE_SUSCEPTIBLE: "white",
    STATE_INFECTED: "orange",
    STATE_DEAD: "black"
}

class Cell:
    def __init__(self, r, c, prop=None, mort=None, mut=None):
        self.r = r
        self.c = c
        # si None -> valeurs initiales aléatoires raisonnables
        self.propagation_rate = prop if prop is not None else random.uniform(0.08, 0.28)
        self.mortality_rate = mort if mort is not None else random.uniform(0.01, 0.12)
        self.mutation_rate = mut if mut is not None else random.uniform(0.0, 0.01)
        self.state = STATE_SUSCEPTIBLE
        self.infection_timer = 0  # si infectée, compte les ticks restants

    def copy_stats(self):
        # utilisé si on devait créer une nouvelle cellule identique (ici grille fixe)
        return (self.propagation_rate, self.mortality_rate, self.mutation_rate)

class VirusLife:
    def __init__(self, master):
        self.master = master
        self.rows = ROWS
        self.cols = COLS
        self.grid = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.buttons = [[None]*self.cols for _ in range(self.rows)]
        self.running = False
        self.generation = 0
        self.initial_clicked = False
        self.speed_ms = 250

        self.build_ui()
        self.update_stats_labels()

    def build_ui(self):
        top = tk.Frame(self.master)
        top.pack(side="top", padx=6, pady=6)

        grid_frame = tk.Frame(top)
        grid_frame.grid(row=0, column=0, rowspan=6)

        for r in range(self.rows):
            for c in range(self.cols):
                b = tk.Button(grid_frame, width=2, height=1,
                              command=lambda rr=r, cc=c: self.on_cell_click(rr, cc))
                b.grid(row=r, column=c, padx=0, pady=0)
                self.buttons[r][c] = b
                self.refresh_cell_visual(r, c)

        # Controls
        controls = tk.Frame(top)
        controls.grid(row=0, column=1, sticky="nw", padx=10)

        self.start_btn = tk.Button(controls, text="Start", command=self.start)
        self.start_btn.pack(fill="x")
        tk.Button(controls, text="Pause", command=self.pause).pack(fill="x", pady=(4,0))
        tk.Button(controls, text="Step", command=self.step).pack(fill="x", pady=(4,0))
        tk.Button(controls, text="Reset", command=self.reset).pack(fill="x", pady=(4,0))

        tk.Label(controls, text="Vitesse (ms):").pack(anchor="w", pady=(8,0))
        self.speed_scale = tk.Scale(controls, from_=50, to=1000, orient="horizontal",
                                    command=self.on_speed_change)
        self.speed_scale.set(self.speed_ms)
        self.speed_scale.pack(fill="x")

        # Stats
        stats = tk.Frame(top)
        stats.grid(row=1, column=1, sticky="nw", padx=10, pady=(8,0))
        self.gen_label = tk.Label(stats, text="Gen: 0")
        self.gen_label.pack(anchor="w")
        self.infected_label = tk.Label(stats, text="Infectés: 0")
        self.infected_label.pack(anchor="w")
        self.dead_label = tk.Label(stats, text="Morts: 0")
        self.dead_label.pack(anchor="w")

        # Instructions
        instr = tk.Label(top, text="Clique une seule case pour initier l'infection.\n(Seule la première est prise en compte.)",
                         fg="blue", justify="left")
        instr.grid(row=2, column=1, sticky="nw", padx=10, pady=(8,0))

        # Paramètres affichés (pour debug/ajustement rapide)
        params = tk.Frame(top)
        params.grid(row=3, column=1, sticky="nw", padx=10, pady=(8,0))
        tk.Label(params, text=f"Mutation incr/gén: {MUTATION_INCREMENT}").pack(anchor="w")
        tk.Label(params, text=f"Effet mutation: ±{MUTATION_EFFECT_SCALE*100:.1f}%").pack(anchor="w")

    def on_speed_change(self, val):
        try:
            self.speed_ms = int(val)
        except:
            pass

    def on_cell_click(self, r, c):
        if self.initial_clicked:
            return  # on n'active qu'une cellule initiale
        cell = self.grid[r][c]
        cell.state = STATE_INFECTED
        cell.infection_timer = self.compute_infection_duration(cell)
        self.initial_clicked = True
        self.refresh_cell_visual(r, c)
        self.update_stats_labels()

    def compute_infection_duration(self, cell):
        # durée modulée par propagation et mortalité
        # plus propagation est élevée -> infection se propage plus vite donc souvent plus courte chez l'hôte
        # plus mortalité est élevée -> durée moyenne plus courte (décès rapide)
        prop = max(0.0, min(1.0, cell.propagation_rate))
        mort = max(0.0, min(1.0, cell.mortality_rate))
        # formule heuristique — tu peux l'ajuster
        dur = BASE_INFECTION_DURATION * (1.0 - 0.6 * prop) * (1.0 - 0.7 * mort)
        dur = max(1, int(round(dur + random.uniform(-1, 1))))
        return dur

    def step(self):
        # une génération
        self.generation += 1

        # 1) MUTATION : chaque cellule voit sa mutation_rate augmenter
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                cell.mutation_rate = min(0.95, cell.mutation_rate + MUTATION_INCREMENT)
                # avec prob = mutation_rate appliquer une petite mutation sur prop/mort
                if random.random() < cell.mutation_rate:
                    # mutation additive relative
                    delta_prop = random.uniform(-MUTATION_EFFECT_SCALE, MUTATION_EFFECT_SCALE) * cell.propagation_rate
                    delta_mort = random.uniform(-MUTATION_EFFECT_SCALE, MUTATION_EFFECT_SCALE) * cell.mortality_rate
                    cell.propagation_rate = max(0.0, min(0.99, cell.propagation_rate + delta_prop))
                    cell.mortality_rate = max(0.0, min(0.99, cell.mortality_rate + delta_mort))

        # 2) Calcul des infections à appliquer (on lit l'état initial de la génération pour décider)
        new_infections = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.state != STATE_SUSCEPTIBLE:
                    continue
                # compter voisins infectés
                infected_neighbors = 0
                for dr, dc in NEIGHBOR_DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc].state == STATE_INFECTED:
                            infected_neighbors += 1
                if infected_neighbors == 0:
                    continue
                # probabilité effective : plus il y a d'infectés, plus la prob augmente.
                # On utilise la formule de prob complémentaire : 1 - (1 - p)^{k}
                p = cell.propagation_rate
                effective_p = 1.0 - (1.0 - p) ** infected_neighbors
                # chance additionnelle : si proportion d'infectés dans la grille est élevée, amplification légère
                total_infected = sum(1 for rr in range(self.rows) for cc in range(self.cols)
                                     if self.grid[rr][cc].state == STATE_INFECTED)
                frac_infected = total_infected / (self.rows * self.cols)
                # amplification factor : 1 + frac_infected*0.5 (si beaucoup d'infectés, propagation encore plus rapide)
                effective_p = 1.0 - (1.0 - min(0.99, p * (1 + 0.5 * frac_infected))) ** infected_neighbors
                if random.random() < effective_p:
                    new_infections.append((r, c))

        # appliquer nouvelles infections (avec durée calculée)
        for (r, c) in new_infections:
            cell = self.grid[r][c]
            if cell.state == STATE_SUSCEPTIBLE:
                cell.state = STATE_INFECTED
                cell.infection_timer = self.compute_infection_duration(cell)

        # 3) Avancer le timer des infectés -> récupération ou mort
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.state == STATE_INFECTED:
                    cell.infection_timer -= 1
                    if cell.infection_timer <= 0:
                        # tirage pour la mort
                        if random.random() < cell.mortality_rate:
                            cell.state = STATE_DEAD
                        else:
                            cell.state = STATE_SUSCEPTIBLE  # revient susceptible (pas d'immunité durable)
                        cell.infection_timer = 0

        # rafraichir visuel et stats
        self.refresh_all_cells()
        self.update_stats_labels()

    def refresh_cell_visual(self, r, c):
        btn = self.buttons[r][c]
        cell = self.grid[r][c]
        btn.config(bg=STATE_COLOR[cell.state])
        if cell.state == STATE_INFECTED:
            # montre aussi l'infection_timer en petit texte
            btn.config(text=str(cell.infection_timer) if cell.infection_timer>0 else "")
        else:
            btn.config(text="")

    def refresh_all_cells(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.refresh_cell_visual(r, c)

    def update_stats_labels(self):
        infected = sum(1 for r in range(self.rows) for c in range(self.cols)
                       if self.grid[r][c].state == STATE_INFECTED)
        dead = sum(1 for r in range(self.rows) for c in range(self.cols)
                   if self.grid[r][c].state == STATE_DEAD)
        self.gen_label.config(text=f"Gen: {self.generation}")
        self.infected_label.config(text=f"Infectés: {infected}")
        self.dead_label.config(text=f"Morts: {dead}")

    def run_loop(self):
        if self.running:
            self.step()
            self.master.after(self.speed_ms, self.run_loop)

    def start(self):
        if not self.initial_clicked:
            # empêche démarrage sans cellule initiale
            tk.messagebox.showinfo("Info", "Clique une case pour initier l'infection avant de démarrer.")
            return
        if not self.running:
            self.running = True
            self.run_loop()

    def pause(self):
        self.running = False

    def reset(self):
        self.running = False
        self.generation = 0
        self.initial_clicked = False
        # recréer grille (on conserve pas les stats précédentes)
        self.grid = [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        self.refresh_all_cells()
        self.update_stats_labels()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Virus-Life — Jeu de la vie modifié")
    app = VirusLife(root)
    root.mainloop()
