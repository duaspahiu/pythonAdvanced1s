"""HAPI 4 (FINAL) - Pink Strike 3D: 3 armë, raunde me valë armiqsh, pikë dhe rifillim.

Kontrollet: W/A/S/D lëvizje, SHIFT vrapim, SPACE kërcim, maus shënjestër,
klik majtas = qëllo, R = ngarko (ose lojë e re kur humb), 1/2/3 = pistoletë/automatik/shotgun, ESC = dalje.
"""
import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title='Pink Strike 3D - Hapi 4 FINAL', borderless=False)
window.fps_counter.enabled = False   # fsheh panelin e zhvillimit
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.exit_button.visible = False
window.cog_button.enabled = False
Sky()


def box(x, z, w, d, h=4, col='#8a8a96', tex='white_cube'):
    return Entity(model='cube', position=(x, h / 2, z), scale=(w, h, d),
                  color=color.hex(col), texture=tex, texture_scale=(max(w, d) / 2, h / 2),
                  collider='box')


def house(x, z, w, d, door='s', gap=4, h=4, col='#b5654a'):
    t = 1
    door_z = z - d / 2 if door == 's' else z + d / 2
    solid_z = z + d / 2 if door == 's' else z - d / 2
    box(x, solid_z, w, t, h, col, 'brick')
    box(x - w / 2, z, t, d, h, col, 'brick')
    box(x + w / 2, z, t, d, h, col, 'brick')
    side = (w - gap) / 2
    box(x - (gap + side) / 2, door_z, side, t, h, col, 'brick')
    box(x + (gap + side) / 2, door_z, side, t, h, col, 'brick')


def build_map():
    # toka: bllok i trashë (sipërfaqja është në y=0), që lojtari të mos bjerë kurrë përtej saj
    Entity(model='cube', scale=(80, 4, 80), position=(0, -2, 0), texture='white_cube',
           texture_scale=(40, 40), color=color.hex('#5d8f55'), collider='box')
    box(0, 40, 80, 2, 6, '#555560')
    box(0, -40, 80, 2, 6, '#555560')
    box(40, 0, 2, 80, 6, '#555560')
    box(-40, 0, 2, 80, 6, '#555560')
    box(-18, -8, 14, 2)
    box(18, 6, 14, 2)
    box(0, 14, 2, 14)
    box(-28, 18, 2, 16)
    box(28, -16, 2, 16)
    for (x, z) in [(-8, -20), (8, -24), (-12, 2), (12, -4), (-24, -26), (24, 22), (0, -10)]:
        box(x, z, 2.5, 2.5, 2.5, '#9a7b4f')
    house(-24, 4, 12, 10, door='s')
    house(22, 28, 14, 10, door='s')


build_map()


# ---------- Objektivi (personazh që mund ta qëllosh) ----------
class Target(Entity):
    """Njeri i thjeshtë me jetë. Ka kolizion që raycast-i ta gjejë."""

    def __init__(self, position, shirt='#d94a4a'):
        super().__init__(position=position)
        self.hp = 100
        self.shirt = shirt
        self.collider = BoxCollider(self, center=Vec3(0, 1.05, 0), size=Vec3(1, 2.2, 1))
        Entity(parent=self, model='cube', color=color.hex('#2f3a5a'), scale=(.6, .8, .35), y=.4)       # këmbët
        self.body = Entity(parent=self, model='cube', color=color.hex(shirt), scale=(.8, .9, .45), y=1.25)
        Entity(parent=self, model='sphere', color=color.hex(random.choice(['#f1c9a5', '#c68e65', '#8d5a3c'])),
               scale=.5, y=1.9)                                                                          # koka
        Entity(parent=self, model='cube', color=color.hex('#2b2b30'), scale=(.12, .12, .6), position=(.35, 1.3, .4))
        self.bar_bg = Entity(parent=self, model='quad', color=color.hex('#222222'), scale=(1.04, .12),
                             y=2.55, billboard=True)
        self.bar = Entity(parent=self, model='quad', color=color.hex('#3cc850'), scale=(1, .08),
                          origin=(-.5, 0), x=-.5, y=2.55, z=-.01, billboard=True)

    def take_damage(self, dmg):
        self.hp -= dmg
        self.bar.scale_x = max(0, self.hp) / 100
        self.body.color = color.white
        invoke(self.unflash, delay=.07)
        if self.hp <= 0:
            self.die()

    def unflash(self):
        if self.hp > 0:
            self.body.color = color.hex(self.shirt)

    def die(self):
        destroy(self)


# ---------- Lojtari ----------
player = FirstPersonController(position=(0, 0, -35))
player.speed = 7
# Gravitacioni ndizet pas 1 sekonde: kuadrot e para (kur ngarkohet loja) kanë dt shumë të madh
# dhe do ta hidhnin lojtarin përmes tokës.
player.gravity = 0
invoke(setattr, player, 'gravity', 1, delay=1)

# Armët: dëmi, koha mes të shtënave, plumba në karikator, sa plumba në një të shtënë, shpërndarja, ngjyra, gjatësia
WEAPONS = [
    {'name': 'Pistoletë', 'damage': 22, 'cooldown': .28, 'mag': 12, 'pellets': 1, 'spread': .004, 'col': '#ff69b4', 'len': .4},
    {'name': 'Automatik', 'damage': 14, 'cooldown': .09, 'mag': 30, 'pellets': 1, 'spread': .02, 'col': '#ff69b4', 'len': .6},
    {'name': 'Shotgun', 'damage': 14, 'cooldown': .8, 'mag': 6, 'pellets': 7, 'spread': .08, 'col': '#c9a227', 'len': .75},
]
SPAWNS = [(-33, 0, 34), (-14, 0, 36), (6, 0, 36), (33, 0, 36), (-5, 0, 28)]

state = {'weapon': 1, 'ammo': [w['mag'] for w in WEAPONS], 'reloading': False, 'last_shot': 0.0,
         'hp': 100, 'over': False, 'kills': 0, 'round': 0, 'to_spawn': 0, 'between': False, 'gid': 0}
enemies = []

hp_bg = Entity(parent=camera.ui, model='quad', color=color.hex('#222222'), scale=(.4, .035), position=(-.65, -.44))
hp_fg = Entity(parent=camera.ui, model='quad', color=color.hex('#3cc850'), scale=(.4, .035), origin=(-.5, 0),
               position=(-.85, -.44), z=-.01)
hp_text = Text(text='', position=(-.85, -.385), scale=1.2, color=color.white)
damage_flash = Entity(parent=camera.ui, model='quad', scale=(3, 2), color=color.rgba(1, 0, 0, 0), z=1)
msg = Text(text='', origin=(0, 0), y=.2, scale=2.5, color=color.white)
ammo_text = Text(text='', position=(.5, -.42), scale=1.6, color=color.white)
info_text = Text(text='', position=(-.85, .47), scale=1.4, color=color.white)

# ---------- Arma në dorë ----------
gun = Entity(parent=camera, position=(.32, -.3, .6))
gun_body = Entity(parent=gun, model='cube', scale=(.12, .14, .6))
gun_barrel = Entity(parent=gun, model='cube', color=color.hex('#2b2b30'), scale=(.07, .07, .3), y=.03)
flash = Entity(parent=gun, model='quad', color=color.hex('#ffe066'), scale=.25, enabled=False)


def build_gun():
    """Përditëson pamjen e armës aktuale (ngjyra dhe gjatësia ndryshojnë). Pjesët krijohen vetëm një herë."""
    w = WEAPONS[state['weapon']]
    gun_body.color = color.hex(w['col'])
    gun_body.scale = (.12, .14, w['len'])
    gun_barrel.z = w['len'] / 2 + .1
    flash.z = w['len'] / 2 + .35


def set_weapon(i):
    if state['reloading'] or state['over'] or i == state['weapon']:
        return
    state['weapon'] = i
    build_gun()


def tracer(a, b):
    line = Entity(model=Mesh(vertices=[a, b], mode='line', thickness=2), color=color.yellow)
    destroy(line, delay=.06)


def banner(text, secs=2.0):
    msg.text = text
    token = state['gid'], text
    invoke(clear_banner, token, delay=secs)


def clear_banner(token):
    if msg.text == token[1] and token[0] == state['gid'] and not state['over']:
        msg.text = ''


def freeze_player(frozen):
    player.speed = 0 if frozen else 7
    player.mouse_sensitivity = Vec2(0, 0) if frozen else Vec2(40, 40)
    mouse.locked = not frozen


def damage_player(n):
    if state['over']:
        return
    state['hp'] -= n
    damage_flash.color = color.rgba(1, 0, 0, .4)
    damage_flash.animate_color(color.rgba(1, 0, 0, 0), duration=.35)
    if state['hp'] <= 0:
        state['hp'] = 0
        state['over'] = True
        freeze_player(True)
        msg.text = (f"LOJA PËRFUNDOI\nRaundi {state['round']}  -  Armiq të mundur: {state['kills']}"
                    f"\nShtyp R për lojë të re")


# ---------- Armiqtë ----------
class Enemy(Target):
    def __init__(self, position, speed=3.5):
        super().__init__(position, shirt=random.choice(['#d94a4a', '#c97a2a', '#8a3fb0', '#b03f5f']))
        self.speed = speed
        self.shoot_t = random.uniform(.8, 1.6)
        self.side = random.choice([-1, 1])
        enemies.append(self)

    def die(self):
        if self in enemies:
            enemies.remove(self)
        state['kills'] += 1
        destroy(self)

    def try_move(self, d):
        probe = raycast(self.world_position + Vec3(0, 1, 0), d, distance=1.0, ignore=[self, player])
        if not probe.hit:
            self.position += d * self.speed * time.dt
            return True
        return False

    def update(self):
        if state['over']:
            return
        flat = Vec3(player.x - self.x, 0, player.z - self.z)
        dist = flat.length()
        if dist < .1:
            return
        dirn = flat.normalized()
        self.look_at_2d(player.position, 'y')

        chest = self.world_position + Vec3(0, 1.5, 0)
        target = player.world_position + Vec3(0, 1.2, 0)
        to_t = target - chest
        los = not raycast(chest, to_t.normalized(), distance=to_t.length(), ignore=[self, player]).hit

        if los and dist < 30:
            self.shoot_t -= time.dt
            if self.shoot_t <= 0:
                self.shoot_t = random.uniform(.8, 1.5)
                tracer(chest + self.forward * .7, target)
                if random.random() < .45:
                    damage_player(random.randint(6, 11) + state['round'] // 3)

        if dist > (9 if los else 1.5):
            if not self.try_move(dirn):
                if not self.try_move(self.right * self.side):
                    self.side *= -1
        elif los:
            if not self.try_move(self.right * self.side):
                self.side *= -1


# ---------- Raundet ----------
def spawn_enemy(gid):
    if gid != state['gid'] or state['over']:
        return
    Enemy(random.choice(SPAWNS), speed=3 + .25 * state['round'])
    state['to_spawn'] -= 1


def start_round(n, gid):
    if gid != state['gid'] or state['over']:
        return
    state['round'] = n
    state['between'] = False
    state['to_spawn'] = min(2 + n * 2, 14)
    banner(f'RAUNDI {n}', 2.0)
    for i in range(state['to_spawn']):
        invoke(spawn_enemy, gid, delay=1.5 + i * .9)


def new_game():
    state['gid'] += 1
    for e in list(enemies):
        destroy(e)
    enemies.clear()
    state.update(weapon=1, ammo=[w['mag'] for w in WEAPONS], hp=100, over=False, reloading=False,
                 kills=0, round=0, to_spawn=0, between=False)
    player.position = (0, .1, -35)
    player.rotation_y = 0
    player.camera_pivot.rotation_x = 0
    freeze_player(False)
    msg.text = ''
    build_gun()
    start_round(1, state['gid'])


# ---------- Qitja ----------
def shoot():
    i = state['weapon']
    w = WEAPONS[i]
    if state['over'] or state['reloading'] or time.time() - state['last_shot'] < w['cooldown']:
        return
    if state['ammo'][i] <= 0:
        reload()
        return
    state['last_shot'] = time.time()
    state['ammo'][i] -= 1
    flash.enabled = True
    invoke(setattr, flash, 'enabled', False, delay=.04)
    gun.z = .5
    gun.animate_z(.6, duration=.08)
    player.camera_pivot.rotation_x -= .2 + w['pellets'] * .1        # rikthimi i armës lart
    hit_enemy = False
    for _ in range(w['pellets']):
        s = w['spread']
        d = (camera.forward + camera.right * random.uniform(-s, s) + camera.up * random.uniform(-s, s)).normalized()
        hit = raycast(camera.world_position, d, distance=200, ignore=[player])
        if hit.hit:
            mark = Entity(model='sphere', scale=.12, color=color.yellow, position=hit.world_point)
            destroy(mark, delay=.4)
            if hasattr(hit.entity, 'take_damage'):
                hit.entity.take_damage(w['damage'])
                hit_enemy = True
    if hit_enemy:
        player.cursor.color = color.red
        invoke(setattr, player.cursor, 'color', color.pink, delay=.1)


def reload():
    i = state['weapon']
    if state['reloading'] or state['ammo'][i] == WEAPONS[i]['mag']:
        return
    state['reloading'] = True
    invoke(finish_reload, i, state['gid'], delay=1.3)


def finish_reload(i, gid):
    if gid != state['gid']:
        return
    state['ammo'][i] = WEAPONS[i]['mag']
    state['reloading'] = False


def input(key):
    if key == 'escape':
        application.quit()
    if key == 'r':
        if state['over']:
            new_game()
        else:
            reload()
    if key in ('1', '2', '3'):
        set_weapon(int(key) - 1)


def update():
    if not state['over']:
        player.speed = 11 if held_keys['left shift'] else 7
        if held_keys['left mouse']:
            shoot()
        # fundi i raundit
        if state['round'] > 0 and not state['between'] and state['to_spawn'] == 0 and not enemies:
            state['between'] = True
            state['hp'] = min(100, state['hp'] + 25)
            state['ammo'] = [w['mag'] for w in WEAPONS]
            banner(f"Raundi {state['round']} u fitua!  +25 jetë, armët u mbushën", 3.0)
            invoke(start_round, state['round'] + 1, state['gid'], delay=3.5)
    w = WEAPONS[state['weapon']]
    ammo_text.text = ('Po ngarkon...' if state['reloading']
                      else f"{w['name']}  {state['ammo'][state['weapon']]} / {w['mag']}")
    hp_fg.scale_x = .4 * state['hp'] / 100
    hp_text.text = f"Jeta {state['hp']}"
    info_text.text = f"Raundi {state['round']}   Armiq të mundur: {state['kills']}   Mbeten: {len(enemies) + state['to_spawn']}"


new_game()

if __name__ == '__main__':
    app.run()