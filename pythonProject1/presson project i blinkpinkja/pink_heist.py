import math
import random
import sys

import pygame

pygame.init()

# ---------- Cilësimet ----------
WIDTH, HEIGHT = 1000, 700
FPS = 60

PLAYER_SPEED = 230
BOT_SPEED = 115
RADIUS = 16
BULLET_SPEED = 900

FREEZE_TIME = 3.0       # sekonda përgatitje në fillim të raundit
ROUND_TIME = 90.0       # kohëzgjatja e raundit
ROUND_END_TIME = 3.0
WIN_SCORE = 5           # sa raunde duhen për të fituar ndeshjen

# Armët: dëmi, koha mes plumbave, plumba në karikator, sa plumba ne një të shtënë, shpërndarja (gradë)
WEAPONS = [
    {"name": "Pistoletë", "damage": 20, "cooldown": 0.30, "mag": 12, "pellets": 1, "spread": 2},
    {"name": "Automatik", "damage": 22, "cooldown": 0.10, "mag": 30, "pellets": 1, "spread": 5},
    {"name": "Shotgun",   "damage": 12, "cooldown": 0.85, "mag": 6,  "pellets": 7, "spread": 11},
]
RELOAD_TIME = 1.4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pink Strike - Lojë 2D me ekipe")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
small_font = pygame.font.SysFont("arial", 18)
big_font = pygame.font.SysFont("arial", 54, bold=True)

WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
YELLOW = (255, 230, 90)
BLUE = (70, 130, 230)
RED = (225, 70, 70)

# ---------- Harta ----------
WALLS = [pygame.Rect(*r) for r in [
    # kornizat
    (0, 0, WIDTH, 20), (0, HEIGHT - 20, WIDTH, 20), (0, 0, 20, HEIGHT), (WIDTH - 20, 0, 20, HEIGHT),
    # muret e brendshme
    (200, 150, 160, 30), (200, 150, 30, 150),
    (640, 520, 160, 30), (770, 370, 30, 180),
    (420, 230, 160, 40), (420, 430, 160, 40),
    (150, 420, 30, 150), (820, 130, 30, 150),
    (300, 330, 60, 60), (640, 330, 60, 60),
]]

WAYPOINTS = [(100, 100), (500, 80), (900, 300), (500, 350), (300, 600),
             (700, 620), (100, 350), (900, 600), (500, 600), (500, 150)]

SPAWN_A = [(80, 640), (80, 590), (130, 640)]    # ekipi yt (poshtë majtas)
SPAWN_B = [(920, 60), (920, 110), (870, 60)]    # ekipi kundër (lart djathtas)


def resolve_walls(pos, r=RADIUS):
    """Largon rrethin nga muret që të mos kalojë brenda tyre."""
    for _ in range(2):
        for w in WALLS:
            cx = max(w.left, min(pos.x, w.right))
            cy = max(w.top, min(pos.y, w.bottom))
            d = pygame.Vector2(pos.x - cx, pos.y - cy)
            dist = d.length()
            if dist < r:
                if dist == 0:
                    pos.x = w.left - r
                else:
                    pos += d.normalize() * (r - dist)


def has_los(a, b):
    """A ka vijë shikimi te B (pa mur në mes)?"""
    for w in WALLS:
        if w.clipline(int(a.x), int(a.y), int(b.x), int(b.y)):
            return False
    return True


# ---------- Personazhet ----------
def make_panther_sprite():
    s = pygame.Surface((56, 48), pygame.SRCALPHA)
    pink, dark, light = (255, 105, 180), (200, 60, 130), (255, 170, 215)
    pygame.draw.lines(s, dark, False, [(14, 24), (6, 32), (2, 24), (4, 16)], 6)
    pygame.draw.ellipse(s, pink, (12, 8, 24, 32))
    pygame.draw.ellipse(s, dark, (12, 8, 24, 32), 2)
    pygame.draw.line(s, pink, (26, 12), (40, 21), 5)
    pygame.draw.line(s, pink, (26, 36), (40, 27), 5)
    pygame.draw.line(s, (60, 60, 65), (34, 24), (54, 24), 5)
    pygame.draw.circle(s, pink, (22, 14), 5)
    pygame.draw.circle(s, pink, (22, 34), 5)
    pygame.draw.circle(s, dark, (22, 14), 2)
    pygame.draw.circle(s, dark, (22, 34), 2)
    pygame.draw.circle(s, pink, (28, 24), 10)
    pygame.draw.circle(s, dark, (28, 24), 10, 2)
    pygame.draw.ellipse(s, light, (30, 19, 12, 10))
    pygame.draw.circle(s, BLACK, (41, 24), 2)
    for y in (19, 29):
        pygame.draw.circle(s, WHITE, (33, y), 3)
        pygame.draw.circle(s, BLACK, (34, y), 1)
    return s


def make_person_sprite(shirt, skin, hair):
    s = pygame.Surface((56, 48), pygame.SRCALPHA)
    pygame.draw.line(s, shirt, (24, 11), (38, 19), 5)
    pygame.draw.line(s, shirt, (24, 37), (38, 29), 5)
    pygame.draw.line(s, (60, 60, 65), (36, 24), (54, 24), 5)   # arma
    pygame.draw.circle(s, skin, (39, 19), 3)
    pygame.draw.circle(s, skin, (39, 29), 3)
    pygame.draw.ellipse(s, shirt, (14, 8, 18, 32))
    pygame.draw.ellipse(s, BLACK, (14, 8, 18, 32), 2)
    pygame.draw.circle(s, skin, (24, 24), 8)
    pygame.draw.circle(s, hair, (22, 24), 7)
    pygame.draw.circle(s, skin, (32, 24), 2)
    return s


PANTHER = make_panther_sprite()
TEAM_A_BOTS = [make_person_sprite((50, 90, 200), (240, 200, 160), (50, 30, 20)),
               make_person_sprite((40, 110, 170), (200, 150, 110), (20, 20, 20))]
TEAM_B_BOTS = [make_person_sprite((200, 60, 60), (225, 180, 140), (90, 50, 30)),
               make_person_sprite((170, 90, 40), (120, 80, 55), (10, 10, 10)),
               make_person_sprite((120, 40, 40), (245, 215, 180), (200, 150, 60))]


def draw_sprite(sprite, pos, look_dir):
    angle = -math.degrees(math.atan2(look_dir.y, look_dir.x))
    rotated = pygame.transform.rotate(sprite, angle)
    screen.blit(rotated, rotated.get_rect(center=(int(pos.x), int(pos.y))))


# ---------- Luftëtarët ----------
class Fighter:
    def __init__(self, team, sprite, is_player=False):
        self.team = team            # 0 = ekipi yt, 1 = armiqtë
        self.sprite = sprite
        self.is_player = is_player
        self.weapon = 1             # automatiku si fillim
        self.pos = pygame.Vector2(0, 0)

    def reset(self, spawn):
        self.pos = pygame.Vector2(spawn)
        self.health = 100
        self.alive = True
        center = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.aim = (center - self.pos).normalize()
        self.shoot_timer = 0.0
        self.reload_timer = 0.0
        self.ammo = [w["mag"] for w in WEAPONS]
        # të dhëna për inteligjencën e bot-eve
        self.react = 0.0
        self.goal = None
        self.goal_timer = 0.0
        self.strafe_dir = 1
        self.strafe_timer = 0.0
        self.last_pos = self.pos.copy()
        self.stuck_timer = 0.0


class Game:
    def __init__(self):
        self.score = [0, 0]
        self.round_no = 0
        self.fighters = [Fighter(0, PANTHER, is_player=True)]
        self.fighters += [Fighter(0, s) for s in TEAM_A_BOTS]
        self.fighters += [Fighter(1, s) for s in TEAM_B_BOTS]
        self.player = self.fighters[0]
        self.bullets = []
        self.phase = "freeze"
        self.timer = 0.0
        self.round_time = 0.0
        self.message = ""
        self.new_round()

    def new_round(self):
        self.round_no += 1
        self.phase = "freeze"
        self.timer = FREEZE_TIME
        self.round_time = 0.0
        self.bullets = []
        a = [f for f in self.fighters if f.team == 0]
        b = [f for f in self.fighters if f.team == 1]
        for f, sp in zip(a, SPAWN_A):
            f.reset(sp)
        for f, sp in zip(b, SPAWN_B):
            f.reset(sp)

    def start_reload(self, f):
        if f.reload_timer <= 0 and f.ammo[f.weapon] < WEAPONS[f.weapon]["mag"]:
            f.reload_timer = RELOAD_TIME

    def player_fire(self):
        p = self.player
        w = WEAPONS[p.weapon]
        if p.reload_timer > 0 or p.shoot_timer > 0:
            return
        if p.ammo[p.weapon] <= 0:
            self.start_reload(p)
            return
        p.ammo[p.weapon] -= 1
        p.shoot_timer = w["cooldown"]
        for _ in range(w["pellets"]):
            d = p.aim.rotate(random.uniform(-w["spread"], w["spread"]))
            self.bullets.append([p.pos + p.aim * 26, d, p.team, w["damage"]])

    def update_bot(self, b, dt):
        enemies = [f for f in self.fighters if f.alive and f.team != b.team]
        if not enemies:
            return
        b.shoot_timer -= dt
        target, best = None, 1e9
        for e in enemies:
            d = b.pos.distance_to(e.pos)
            if d < 650 and d < best and has_los(b.pos, e.pos):
                best, target = d, e
        move = pygame.Vector2(0, 0)
        if target:
            b.aim = (target.pos - b.pos).normalize()
            b.react += dt
            if best > 320:
                move = pygame.Vector2(b.aim)
            elif best < 160:
                move = -b.aim
            else:
                b.strafe_timer -= dt
                if b.strafe_timer <= 0:
                    b.strafe_dir = random.choice([-1, 1])
                    b.strafe_timer = random.uniform(0.5, 1.5)
                move = b.aim.rotate(90 * b.strafe_dir)
            if b.react > 0.4 and b.shoot_timer <= 0:
                d = b.aim.rotate(random.uniform(-7, 7))
                self.bullets.append([b.pos + b.aim * 26, d, b.team, 14])
                b.shoot_timer = random.uniform(0.3, 0.55)
        else:
            b.react = 0.0
            b.goal_timer -= dt
            if b.goal is None or b.goal_timer <= 0 or b.pos.distance_to(b.goal) < 30:
                if random.random() < 0.6:
                    e = random.choice(enemies)
                    b.goal = e.pos + pygame.Vector2(random.randint(-80, 80), random.randint(-80, 80))
                else:
                    b.goal = pygame.Vector2(random.choice(WAYPOINTS))
                b.goal_timer = random.uniform(2, 4)
            to_g = b.goal - b.pos
            if to_g.length() > 0:
                move = to_g.normalize()
                b.aim = pygame.Vector2(move)
        # nëse ngec te një mur, zgjedh një pikë tjetër
        b.stuck_timer += dt
        if b.stuck_timer > 0.6:
            if b.pos.distance_to(b.last_pos) < 12 and not target:
                b.goal = pygame.Vector2(random.choice(WAYPOINTS))
                b.goal_timer = 3
            b.last_pos = b.pos.copy()
            b.stuck_timer = 0
        if move.length() > 0:
            b.pos += move.normalize() * BOT_SPEED * dt
            resolve_walls(b.pos)

    def step(self, dt, move, mouse, firing):
        p = self.player
        # shënjestra e lojtarit përditësohet gjithmonë
        if p.alive:
            d = mouse - p.pos
            if d.length() > 0:
                p.aim = d.normalize()

        self.timer -= dt
        if self.phase == "freeze":
            if self.timer <= 0:
                self.phase = "live"
            return
        if self.phase == "round_end":
            if self.timer <= 0:
                if max(self.score) >= WIN_SCORE:
                    self.phase = "match_over"
                else:
                    self.new_round()
            return
        if self.phase == "match_over":
            return

        # ----- faza "live" -----
        self.round_time += dt
        if p.alive:
            if move.length() > 0:
                p.pos += move.normalize() * PLAYER_SPEED * dt
                resolve_walls(p.pos)
            p.shoot_timer -= dt
            if p.reload_timer > 0:
                p.reload_timer -= dt
                if p.reload_timer <= 0:
                    p.ammo[p.weapon] = WEAPONS[p.weapon]["mag"]
            if firing:
                self.player_fire()

        for f in self.fighters:
            if f.alive and not f.is_player:
                self.update_bot(f, dt)

        # plumbat
        alive_bullets = []
        for bl in self.bullets:
            bl[0] += bl[1] * BULLET_SPEED * dt
            if not (0 <= bl[0].x <= WIDTH and 0 <= bl[0].y <= HEIGHT):
                continue
            if any(w.collidepoint(bl[0].x, bl[0].y) for w in WALLS):
                continue
            hit = False
            for f in self.fighters:
                if f.alive and f.team != bl[2] and bl[0].distance_to(f.pos) < RADIUS + 3:
                    f.health -= bl[3]
                    if f.health <= 0:
                        f.alive = False
                    hit = True
                    break
            if not hit:
                alive_bullets.append(bl)
        self.bullets = alive_bullets

        # fundi i raundit
        a_alive = any(f.alive for f in self.fighters if f.team == 0)
        b_alive = any(f.alive for f in self.fighters if f.team == 1)
        winner = None
        if not b_alive:
            winner = 0
        elif not a_alive:
            winner = 1
        elif self.round_time >= ROUND_TIME:
            winner = -1
        if winner is not None:
            self.phase = "round_end"
            self.timer = ROUND_END_TIME
            if winner == 0:
                self.score[0] += 1
                self.message = "Ekipi yt fiton raundin!"
            elif winner == 1:
                self.score[1] += 1
                self.message = "Armiqtë fitojnë raundin"
            else:
                self.message = "Koha mbaroi - raund i barabartë"
            if max(self.score) >= WIN_SCORE:
                self.message = "FITOVE NDESHJEN!" if self.score[0] > self.score[1] else "HUMBE NDESHJEN"


# ---------- Vizatimi ----------
def draw_text_center(text, f, color, y):
    t = f.render(text, True, color)
    screen.blit(t, t.get_rect(center=(WIDTH // 2, y)))


def draw(g, mouse):
    screen.fill((52, 58, 52))
    for x in range(0, WIDTH, 50):
        pygame.draw.line(screen, (46, 52, 46), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 50):
        pygame.draw.line(screen, (46, 52, 46), (0, y), (WIDTH, y))
    # zonat e fillimit
    zone = pygame.Surface((220, 160), pygame.SRCALPHA)
    zone.fill((70, 130, 230, 45))
    screen.blit(zone, (20, HEIGHT - 180))
    zone.fill((225, 70, 70, 45))
    screen.blit(zone, (WIDTH - 240, 20))

    for w in WALLS:
        pygame.draw.rect(screen, (95, 95, 108), w)
        pygame.draw.rect(screen, (40, 40, 48), w, 2)

    for f in g.fighters:
        if not f.alive:
            pygame.draw.circle(screen, (110, 110, 110), f.pos, 12)
            pygame.draw.line(screen, BLACK, f.pos + (-7, -7), f.pos + (7, 7), 3)
            pygame.draw.line(screen, BLACK, f.pos + (-7, 7), f.pos + (7, -7), 3)

    for bl in g.bullets:
        pygame.draw.circle(screen, YELLOW, bl[0], 3)

    for f in g.fighters:
        if f.alive:
            draw_sprite(f.sprite, f.pos, f.aim)
            # shirit i vogël jete mbi kokë
            col = BLUE if f.team == 0 else RED
            pygame.draw.rect(screen, BLACK, (f.pos.x - 15, f.pos.y - 28, 30, 5))
            pygame.draw.rect(screen, col, (f.pos.x - 14, f.pos.y - 27, 28 * f.health / 100, 3))

    # maunsi (shënjestra)
    pygame.draw.circle(screen, WHITE, mouse, 9, 1)
    pygame.draw.line(screen, WHITE, mouse + (-14, 0), mouse + (-4, 0))
    pygame.draw.line(screen, WHITE, mouse + (4, 0), mouse + (14, 0))
    pygame.draw.line(screen, WHITE, mouse + (0, -14), mouse + (0, -4))
    pygame.draw.line(screen, WHITE, mouse + (0, 4), mouse + (0, 14))

    # HUD sipër
    pygame.draw.rect(screen, (20, 20, 25), (WIDTH // 2 - 110, 22, 220, 34), border_radius=8)
    draw_text_center(f"Ti {g.score[0]}  :  {g.score[1]} Armiqtë", font, WHITE, 39)
    left = max(0, ROUND_TIME - g.round_time)
    draw_text_center(f"Raundi {g.round_no}   Koha {int(left)}s", small_font, WHITE, 70)

    # HUD poshtë
    p = g.player
    pygame.draw.rect(screen, BLACK, (30, 28, 204, 24))
    pygame.draw.rect(screen, (60, 200, 80), (32, 30, 200 * max(0, p.health) / 100, 20))
    screen.blit(small_font.render(f"Jeta {max(0, p.health)}", True, WHITE), (38, 30))
    w = WEAPONS[p.weapon]
    ammo_txt = "Po ngarkon..." if p.reload_timer > 0 else f"{p.ammo[p.weapon]} / {w['mag']}"
    screen.blit(font.render(f"{w['name']}   {ammo_txt}", True, WHITE), (WIDTH - 300, HEIGHT - 62))
    screen.blit(small_font.render("1 Pistoletë  2 Automatik  3 Shotgun  R Ngarko", True, WHITE),
                (WIDTH - 400, HEIGHT - 36))

    if not p.alive and g.phase == "live":
        draw_text_center("Ke vdekur - prit raundin tjetër", font, WHITE, HEIGHT // 2 - 220)
    if g.phase == "freeze":
        draw_text_center(f"Raundi {g.round_no} fillon pas {int(g.timer) + 1}...", big_font, WHITE, HEIGHT // 2 - 220)
    if g.phase in ("round_end", "match_over"):
        draw_text_center(g.message, big_font, WHITE, HEIGHT // 2 - 220)
        if g.phase == "match_over":
            draw_text_center("Shtyp R për ndeshje të re", font, WHITE, HEIGHT // 2 - 170)


def main():
    pygame.mouse.set_visible(False)
    g = Game()
    while True:
        dt = min(clock.tick(FPS) / 1000, 0.05)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    if g.phase == "match_over":
                        g = Game()
                    elif g.player.alive:
                        g.start_reload(g.player)
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3) and g.player.alive:
                    g.player.weapon = event.key - pygame.K_1
                    g.player.reload_timer = 0.0

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1
        mouse = pygame.Vector2(pygame.mouse.get_pos())
        firing = pygame.mouse.get_pressed()[0]

        g.step(dt, move, mouse, firing)
        draw(g, mouse)
        pygame.display.flip()


if __name__ == "__main__":
    main()