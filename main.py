import os
import sqlite3
import random
import math
from datetime import datetime

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.utils import platform
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.properties import NumericProperty

if platform == 'android':
    try:
        from jnius import autoclass
        ToneGenerator = autoclass('android.media.ToneGenerator')
        AudioManager = autoclass('android.media.AudioManager')
        tone_gen = ToneGenerator(AudioManager.STREAM_MUSIC, 85)
    except Exception:
        tone_gen = None
else:
    tone_gen = None

THEMES = {
    "Shiv Ratri": {
        "bg": (0.04, 0.02, 0.10),
        "gold": (0.78, 0.58, 0.16),
        "accent": (0.55, 0.18, 0.75),
        "counter": (0.00, 0.95, 0.80),
        "text": (0.95, 0.90, 0.80),
        "petals": [(0.78,0.58,0.16,1),(0.55,0.18,0.75,1),(1.00,0.42,0.21,1)],
    },
    "Sunrise Saffron": {
        "bg": (0.10, 0.04, 0.00),
        "gold": (1.00, 0.75, 0.10),
        "accent": (0.95, 0.35, 0.00),
        "counter": (1.00, 0.85, 0.20),
        "text": (1.00, 0.95, 0.85),
        "petals": [(1.00,0.75,0.10,1),(0.95,0.35,0.00,1),(1.00,0.55,0.00,1)],
    },
    "Ocean Blue": {
        "bg": (0.00, 0.04, 0.14),
        "gold": (0.20, 0.80, 1.00),
        "accent": (0.00, 0.55, 0.85),
        "counter": (0.10, 0.95, 0.90),
        "text": (0.85, 0.95, 1.00),
        "petals": [(0.20,0.80,1.00,1),(0.00,0.55,0.85,1),(0.10,0.90,0.85,1)],
    },
    "Forest Green": {
        "bg": (0.02, 0.08, 0.02),
        "gold": (0.55, 0.90, 0.20),
        "accent": (0.20, 0.70, 0.20),
        "counter": (0.55, 1.00, 0.45),
        "text": (0.88, 0.98, 0.85),
        "petals": [(0.55,0.90,0.20,1),(0.20,0.70,0.20,1),(0.80,1.00,0.10,1)],
    },
    "Rose Gold": {
        "bg": (0.12, 0.04, 0.06),
        "gold": (0.95, 0.70, 0.55),
        "accent": (0.85, 0.35, 0.50),
        "counter": (1.00, 0.80, 0.70),
        "text": (1.00, 0.92, 0.90),
        "petals": [(0.95,0.70,0.55,1),(0.85,0.35,0.50,1),(1.00,0.60,0.40,1)],
    },
}
THEME_NAMES = list(THEMES.keys())

MANTRAS = [
    {"name": "Sambh Sadashiv",  "display": "Sambh Sadashiv",  "flash": "Sambh Sadashiv"},
    {"name": "Om Namah Shivay", "display": "Om Namah Shivay", "flash": "Om Namah Shivay"},
    {"name": "Hare Krishna",    "display": "Hare Krishna",     "flash": "Hare Krishna"},
    {"name": "Jai Shri Ram",    "display": "Jai Shri Ram",     "flash": "Jai Shri Ram"},
    {"name": "Om Namo Narayan", "display": "Om Namo Narayan",  "flash": "Narayan"},
    {"name": "Ganpati Bappa",   "display": "Ganpati Bappa",    "flash": "Ganpati Bappa"},
    {"name": "Jai Mata Di",     "display": "Jai Mata Di",      "flash": "Mata Rani"},
    {"name": "Om",              "display": "Om",               "flash": "Om"},
]

def get_db_path():
    if platform == 'android':
        from android.storage import app_storage_path
        return os.path.join(app_storage_path(), "jaap_v2.db")
    return "jaap_v2.db"

DB = get_db_path()

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS records (
        date TEXT, mantra TEXT, count INTEGER, last_updated TEXT,
        PRIMARY KEY(date, mantra))''')
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY, value TEXT)''')
    conn.commit()
    conn.close()

def get_count(mantra_name):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT count FROM records WHERE date=? AND mantra=?", (today, mantra_name))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

def save_count(mantra_name, count):
    today = datetime.now().strftime("%Y-%m-%d")
    now_t = datetime.now().strftime("%H:%M:%S")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''INSERT INTO records VALUES(?,?,?,?)
        ON CONFLICT(date,mantra) DO UPDATE SET count=?,last_updated=?''',
        (today, mantra_name, count, now_t, count, now_t))
    conn.commit()
    conn.close()

def get_lifetime(mantra_name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT SUM(count) FROM records WHERE mantra=?", (mantra_name,))
    r = c.fetchone()[0]
    conn.close()
    return r or 0

def get_setting(key, default=""):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT value FROM settings WHERE key=?", (key,))
    r = c.fetchone()
    conn.close()
    return r[0] if r else default

def save_setting(key, value):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=?",
              (key, value, value))
    conn.commit()
    conn.close()

def reset_mantra(mantra_name):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM records WHERE mantra=?", (mantra_name,))
    conn.commit()
    conn.close()


class ParticleWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.particles = []

    def burst(self, petals):
        cx = self.width / 2
        cy = self.height / 2
        for _ in range(35):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            self.particles.append({
                'x': cx, 'y': cy,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.uniform(8, 18),
                'life': random.uniform(0.7, 1.3),
                'max_life': 1.2,
                'color': random.choice(petals),
            })
        Clock.unschedule(self._step)
        Clock.schedule_interval(self._step, 1 / 40)

    def _step(self, dt):
        self.canvas.clear()
        alive = []
        with self.canvas:
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] -= 0.2
                p['life'] -= dt
                if p['life'] > 0:
                    a = p['life'] / p['max_life']
                    r, g, b, _ = p['color']
                    Color(r, g, b, a)
                    s = p['size'] * a
                    Ellipse(pos=(p['x'] - s/2, p['y'] - s/2), size=(s, s * 1.5))
                    alive.append(p)
        self.particles = alive
        if not self.particles:
            Clock.unschedule(self._step)
            self.canvas.clear()


class MandalaWidget(Widget):
    angle = NumericProperty(0)

    def __init__(self, theme, **kw):
        super().__init__(**kw)
        self.theme = theme
        self.bind(pos=self._draw, size=self._draw, angle=self._draw)
        Clock.schedule_interval(self._spin, 1/30)

    def set_theme(self, theme):
        self.theme = theme
        self._draw()

    def _spin(self, dt):
        self.angle = (self.angle + 0.5) % 360
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        if self.width <= 0:
            return
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        r = min(self.width, self.height) / 2 * 0.85
        t = self.theme
        a = self.angle

        with self.canvas:
            # Outer ring
            Color(*t["gold"], 0.7)
            Line(circle=(cx, cy, r), width=dp(2))

            # Rotating petals
            cols = t["petals"]
            pr = r * 0.28
            for layer in range(2):
                ao = a if layer == 0 else -a * 1.3
                for i in range(12):
                    theta = math.radians(i * 30 + ao)
                    dist = r * 0.62
                    px = cx + math.cos(theta) * dist
                    py = cy + math.sin(theta) * dist
                    col = cols[i % len(cols)]
                    Color(*col[:3], 0.7 - layer * 0.2)
                    Ellipse(pos=(px - pr*0.4, py - pr*0.85), size=(pr*0.8, pr*1.7))

            # Inner star
            Color(*t["gold"], 0.9)
            pts = []
            for i in range(8):
                a1 = math.radians(i * 45 + a * 0.5)
                a2 = math.radians(i * 45 + 22.5 + a * 0.5)
                pts += [cx + math.cos(a1)*r*0.38, cy + math.sin(a1)*r*0.38,
                        cx + math.cos(a2)*r*0.22, cy + math.sin(a2)*r*0.22]
            pts += [pts[0], pts[1]]
            Line(points=pts, width=dp(1.5))

            # Center circle
            cr = r * 0.26
            Color(*t["accent"], 0.9)
            Ellipse(pos=(cx-cr, cy-cr), size=(cr*2, cr*2))
            Color(*t["gold"], 0.6)
            Line(circle=(cx, cy, cr), width=dp(1.5))


class MalaRingWidget(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self._beads = 0
        self._theme = list(THEMES.values())[0]
        self.bind(size=self._draw, pos=self._draw)

    def update(self, beads, theme):
        self._beads = beads
        self._theme = theme
        self._draw()

    def _draw(self, *_):
        self.canvas.clear()
        if self.width <= 0:
            return
        with self.canvas:
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2
            ring_r = min(self.width / 2 - dp(6), self.height / 2 - dp(4))
            bead_r = dp(4)
            for i in range(108):
                ang = math.radians(i * 360 / 108 - 90)
                bx = cx + math.cos(ang) * ring_r
                by = cy + math.sin(ang) * ring_r
                if i < self._beads:
                    Color(*self._theme["gold"], 1.0)
                    Ellipse(pos=(bx-bead_r, by-bead_r), size=(bead_r*2, bead_r*2))
                else:
                    Color(*self._theme["text"], 0.18)
                    Ellipse(pos=(bx-bead_r*0.7, by-bead_r*0.7), size=(bead_r*1.4, bead_r*1.4))


class JaapApp(App):
    def build(self):
        init_db()
        Window.clearcolor = (0.04, 0.02, 0.10, 1)

        saved_theme = get_setting("theme", THEME_NAMES[0])
        saved_mantra = get_setting("mantra", MANTRAS[0]["name"])
        self.theme = THEMES.get(saved_theme, THEMES[THEME_NAMES[0]])
        self.theme_name = saved_theme if saved_theme in THEMES else THEME_NAMES[0]
        self.current_mantra = next((m for m in MANTRAS if m["name"] == saved_mantra), MANTRAS[0])
        self.count = get_count(self.current_mantra["name"])
        self._flash_ev = None

        root = FloatLayout()

        # Background
        self.bg = Widget(size_hint=(1, 1))
        self._draw_bg()
        root.add_widget(self.bg)

        # Particles
        self.particles = ParticleWidget(size_hint=(1, 1))
        root.add_widget(self.particles)

        # Main layout
        main = BoxLayout(
            orientation='vertical',
            padding=[dp(14), dp(8), dp(14), dp(8)],
            spacing=dp(4),
            size_hint=(1, 1)
        )

        # Top bar
        top = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(40), spacing=dp(6))
        self.clock_lbl = Label(
            text="", font_size=sp(12),
            color=(*self.theme["gold"], 1),
            size_hint=(0.55, 1), halign='left', valign='middle')
        self.clock_lbl.bind(size=self.clock_lbl.setter('text_size'))

        btn_theme  = self._mk_btn("Theme",  self._show_theme_picker)
        btn_mantra = self._mk_btn("Mantra", self._show_mantra_picker)
        btn_stats  = self._mk_btn("Stats",  self._show_stats)

        top.add_widget(self.clock_lbl)
        top.add_widget(btn_theme)
        top.add_widget(btn_mantra)
        top.add_widget(btn_stats)
        main.add_widget(top)

        # Mantra name
        self.mantra_lbl = Label(
            text=self.current_mantra["display"],
            font_size=sp(18), bold=True,
            color=(*self.theme["gold"], 1),
            size_hint=(1, None), height=dp(30),
            halign='center', valign='middle')
        self.mantra_lbl.bind(size=self.mantra_lbl.setter('text_size'))
        main.add_widget(self.mantra_lbl)

        # Mala progress text
        self.mala_txt = Label(
            text="0 / 108 beads",
            font_size=sp(11),
            color=(*self.theme["text"], 0.7),
            size_hint=(1, None), height=dp(18),
            halign='center', valign='middle')
        self.mala_txt.bind(size=self.mala_txt.setter('text_size'))
        main.add_widget(self.mala_txt)

        # Mala ring
        self.mala_ring = MalaRingWidget(size_hint=(1, None), height=dp(40))
        main.add_widget(self.mala_ring)

        # Mandala + OM
        mandala_wrap = FloatLayout(size_hint=(1, 1))
        self.mandala = MandalaWidget(
            theme=self.theme,
            size_hint=(0.75, 0.95),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        mandala_wrap.add_widget(self.mandala)

        self.om_lbl = Label(
            text="OM",
            font_size=sp(32), bold=True,
            color=(*self.theme["gold"], 0.95),
            size_hint=(0.35, 0.35),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center', valign='middle')
        self.om_lbl.bind(size=self.om_lbl.setter('text_size'))
        mandala_wrap.add_widget(self.om_lbl)
        main.add_widget(mandala_wrap)

        # Flash label
        self.flash_lbl = Label(
            text="",
            font_size=sp(18), bold=True,
            color=(*self.theme["accent"], 1),
            size_hint=(1, None), height=dp(28),
            halign='center', valign='middle')
        self.flash_lbl.bind(size=self.flash_lbl.setter('text_size'))
        main.add_widget(self.flash_lbl)

        # Count
        self.count_lbl = Label(
            text=str(self.count),
            font_size=sp(62), bold=True,
            color=(*self.theme["counter"], 1),
            size_hint=(1, None), height=dp(80),
            halign='center', valign='middle')
        self.count_lbl.bind(size=self.count_lbl.setter('text_size'))
        main.add_widget(self.count_lbl)

        # Stats row
        stats_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(24), spacing=dp(8))
        self.mala_count_lbl = Label(
            text="Mala: 0", font_size=sp(13),
            color=(*self.theme["gold"], 1),
            size_hint=(0.5, 1), halign='center', valign='middle')
        self.mala_count_lbl.bind(size=self.mala_count_lbl.setter('text_size'))
        self.life_lbl = Label(
            text="Total: 0", font_size=sp(13),
            color=(*self.theme["gold"], 1),
            size_hint=(0.5, 1), halign='center', valign='middle')
        self.life_lbl.bind(size=self.life_lbl.setter('text_size'))
        stats_row.add_widget(self.mala_count_lbl)
        stats_row.add_widget(self.life_lbl)
        main.add_widget(stats_row)

        # Tap button
        self.tap_btn = Button(
            text="TAP TO JAAP",
            font_size=sp(18), bold=True,
            background_color=(*self.theme["accent"], 1),
            background_normal='',
            size_hint=(1, None), height=dp(58))
        self.tap_btn.bind(on_press=self._on_tap)
        main.add_widget(self.tap_btn)

        # Reset button
        reset_btn = Button(
            text="Reset Today",
            font_size=sp(13),
            background_color=(0.7, 0.1, 0.1, 1),
            background_normal='',
            size_hint=(0.45, None), height=dp(36),
            pos_hint={'center_x': 0.5})
        reset_btn.bind(on_press=self._confirm_reset)
        main.add_widget(reset_btn)

        root.add_widget(main)
        self.root_layout = root

        self._refresh_ui()
        Clock.schedule_interval(self._tick, 1)
        self.bg.bind(size=lambda *_: self._draw_bg())

        return root

    def _mk_btn(self, text, cb):
        b = Button(
            text=text, font_size=sp(12),
            background_color=(0.2, 0.1, 0.35, 1),
            background_normal='',
            size_hint=(None, 1), width=dp(52))
        b.bind(on_press=cb)
        return b

    def _draw_bg(self, *_):
        self.bg.canvas.clear()
        with self.bg.canvas:
            Color(*self.theme["bg"], 1)
            Rectangle(pos=self.bg.pos, size=self.bg.size)

    def _tick(self, dt):
        now = datetime.now()
        self.clock_lbl.text = now.strftime("%I:%M %p  %d %b")

    def _refresh_ui(self):
        c = self.count
        mala = c // 108
        bead = c % 108
        life = get_lifetime(self.current_mantra["name"])
        self.count_lbl.text = str(c)
        self.mala_count_lbl.text = f"Mala: {mala}"
        self.life_lbl.text = f"Total: {life:,}"
        self.mala_txt.text = f"{bead} / 108 beads"
        self.mala_ring.update(bead, self.theme)
        self.mantra_lbl.text = self.current_mantra["display"]

    def _on_tap(self, *_):
        self.count += 1
        save_count(self.current_mantra["name"], self.count)
        self._refresh_ui()

        self.flash_lbl.text = self.current_mantra["flash"]
        if self._flash_ev:
            Clock.unschedule(self._flash_ev)
        self._flash_ev = Clock.schedule_once(lambda dt: setattr(self.flash_lbl, 'text', ''), 0.8)

        self.particles.burst(self.theme["petals"])

        if platform == 'android' and tone_gen:
            try:
                tone_gen.startTone(ToneGenerator.TONE_PROP_BEEP, 80)
            except Exception:
                pass

    def _confirm_reset(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(14), spacing=dp(10))
        lbl = Label(
            text=f"Reset all count for\n'{self.current_mantra['name']}'?",
            halign='center', font_size=sp(14))
        btns = BoxLayout(spacing=dp(10), size_hint=(1, None), height=dp(44))
        yes = Button(text="Yes, Reset", background_color=(0.8, 0.1, 0.1, 1), background_normal='')
        no  = Button(text="Cancel",     background_color=(0.1, 0.5, 0.1, 1), background_normal='')
        btns.add_widget(yes)
        btns.add_widget(no)
        content.add_widget(lbl)
        content.add_widget(btns)
        pop = Popup(title="Reset?", content=content, size_hint=(0.82, 0.30), auto_dismiss=True)
        def do_reset(*_):
            reset_mantra(self.current_mantra["name"])
            self.count = 0
            self._refresh_ui()
            pop.dismiss()
        yes.bind(on_press=do_reset)
        no.bind(on_press=pop.dismiss)
        pop.open()

    def _show_theme_picker(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        content.add_widget(Label(text="Choose Theme", font_size=sp(15),
                                  size_hint=(1, None), height=dp(34)))
        grid = GridLayout(cols=1, spacing=dp(6), size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        pop = Popup(title="Theme", content=content, size_hint=(0.88, 0.70), auto_dismiss=True)
        for name in THEME_NAMES:
            th = THEMES[name]
            btn = Button(
                text=name, font_size=sp(14), bold=True,
                background_color=(*th["accent"], 1),
                background_normal='',
                size_hint=(1, None), height=dp(46))
            def _pick(_, n=name):
                self.theme = THEMES[n]
                self.theme_name = n
                save_setting("theme", n)
                self._apply_theme()
                pop.dismiss()
            btn.bind(on_press=_pick)
            grid.add_widget(btn)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        pop.open()

    def _show_mantra_picker(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(8))
        content.add_widget(Label(text="Choose Mantra", font_size=sp(15),
                                  size_hint=(1, None), height=dp(34)))
        grid = GridLayout(cols=1, spacing=dp(6), size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        pop = Popup(title="Mantra", content=content, size_hint=(0.88, 0.78), auto_dismiss=True)
        for m in MANTRAS:
            btn = Button(
                text=m["display"], font_size=sp(15), bold=True,
                background_color=(*self.theme["accent"], 1),
                background_normal='',
                size_hint=(1, None), height=dp(48))
            def _pick(_, mantra=m):
                self.current_mantra = mantra
                self.count = get_count(mantra["name"])
                save_setting("mantra", mantra["name"])
                self._refresh_ui()
                pop.dismiss()
            btn.bind(on_press=_pick)
            grid.add_widget(btn)
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        pop.open()

    def _show_stats(self, *_):
        content = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(6))
        content.add_widget(Label(text="All Mantra Counts", font_size=sp(15),
                                  size_hint=(1, None), height=dp(34)))
        grid = GridLayout(cols=2, spacing=dp(4), size_hint=(1, None))
        grid.bind(minimum_height=grid.setter('height'))
        for m in MANTRAS:
            life = get_lifetime(m["name"])
            grid.add_widget(Label(text=m["display"], font_size=sp(12),
                                   size_hint=(1, None), height=dp(34)))
            grid.add_widget(Label(text=f"{life:,}", font_size=sp(12), bold=True,
                                   color=(*self.theme["counter"], 1),
                                   size_hint=(1, None), height=dp(34)))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        content.add_widget(scroll)
        Popup(title="Stats", content=content, size_hint=(0.88, 0.70), auto_dismiss=True).open()

    def _apply_theme(self):
        t = self.theme
        self._draw_bg()
        self.mandala.set_theme(t)
        self.clock_lbl.color    = (*t["gold"], 1)
        self.mantra_lbl.color   = (*t["gold"], 1)
        self.count_lbl.color    = (*t["counter"], 1)
        self.mala_count_lbl.color = (*t["gold"], 1)
        self.life_lbl.color     = (*t["gold"], 1)
        self.flash_lbl.color    = (*t["accent"], 1)
        self.mala_txt.color     = (*t["text"], 0.7)
        self.om_lbl.color       = (*t["gold"], 0.95)
        self.tap_btn.background_color = (*t["accent"], 1)
        self.mala_ring.update(self.count % 108, t)


if __name__ == '__main__':
    JaapApp().run()
