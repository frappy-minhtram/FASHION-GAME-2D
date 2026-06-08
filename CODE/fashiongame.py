import pygame
import random
import math


pygame.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600




screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fashion Magic Battle")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32)
small_font = pygame.font.SysFont("arial", 24)


barbie_font = pygame.font.SysFont("comicsansms",13)
hint_font = pygame.font.SysFont("comicsansms", 24)


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    return image

def draw_text_wrapped(text, font, color, surface, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "




    lines.append(current_line)




    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * 25))




class Item:
    def __init__(
        self,
        image_path,
        image_size,
        icon_size,
        element,
        icon_pos,
        wear_pos,
        style_scores
    ):
        self.style_scores = style_scores




        self.image = load_image(
            image_path,
            image_size
        )




        self.icon = load_image(
            image_path,
            icon_size
        )




        self.element = element
       
        self.icon_rect = pygame.Rect(
            icon_pos[0],
            icon_pos[1],
            icon_size[0],
            icon_size[1]
        )
        self.wear_pos = wear_pos




class Boss:
    def __init__(
        self,
        image_path,
        element
    ):




        self.image = load_image(
            image_path,
            (247, 342)
        )




        self.element = element








class BaseState:




    def __init__(self, game):




        self.game = game




    def handle_event(self, event):
        pass
   
    def update(self):
        pass




    def draw(self):
        pass




class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)




        self.start_rect = pygame.Rect(
            325, 315, 240, 120
        )




    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                self.game.change_state(
                RollingState(self.game)
            )




    def draw(self):
        screen.blit(
            self.game.cover,
            (0,0)
        )




        screen.blit(
            self.game.start_button,
            self.start_rect.topleft
        )




class RollingState(BaseState):
   
    def __init__(self, game):
        super().__init__(game)




        pygame.mixer.music.load("assets/dice/rolling_music.mp3")
        pygame.mixer.music.play()
        self.show_next = False
        self.next_button = pygame.Rect(500, 480, 140, 70)
        self.next_img = load_image("assets/ui/next.png", (162.5, 115))




        self.start_time = pygame.time.get_ticks()




        self.phase = 0




        self.phase_time = self.start_time




        self.current_dice = random.choice(self.game.dice_list)
        self.dice_timer = 0




        self.game.current_boss = random.choice(self.game.boss_list)




        self.npc_map = {
            "FIRE": "assets/npc/npc1.png",
            "WATER": "assets/npc/npc1.png"
        }




        self.npc_img = None
        self.bubble = self.game.thought_bubble




        self.show_button = False
        self.battle_button = pygame.Rect(300, 450, 200, 110)




        self.hint_map = {
            "FIRE": {
                "text": "HAY MAC DO DO DE HA GUC BOSS !!",
                "items": [
                    self.game.hair_items[0],
                    self.game.shirt_items[1],
                    self.game.shoe_items[0]
                ]
            },
            "WATER": {
                "text": "HAY MAC DO Lanh DE HA GUC BOSS !!",
                "items": [
                    self.game.hair_items[2],
                    self.game.shirt_items[2],
                    self.game.shoe_items[1]
                ]
            }
        }




    def handle_event(self, event):




        if event.type == pygame.MOUSEBUTTONDOWN:




            if self.phase == 1 and self.show_next:
                if self.next_button.collidepoint(event.pos):
                    self.phase = 2
                    self.phase_time = pygame.time.get_ticks()




            elif self.phase == 2 and self.show_button:
                if self.battle_button.collidepoint(event.pos):
                    self.game.change_state(DressingState(self.game))




    def update(self):
        now = pygame.time.get_ticks()
        if self.phase == 0:
            if now - self.dice_timer > 120:
                self.current_dice = random.choice(self.game.dice_list)
                self.dice_timer = now




            if now - self.start_time > 2000:
                self.phase = 1
                self.phase_time = now




        elif self.phase == 1:
            if now - self.phase_time > 2000:
                self.show_next = True
                boss_type = self.game.current_boss.element
                self.npc_img = load_image(
                    self.npc_map[boss_type],
                    (290, 300)
                )


        elif self.phase == 2:
            if now - self.phase_time > 2000:
                self.show_button = True
        if self.phase == 2:
            self.show_button = True

    def draw(self):
        if self.phase == 0:
            screen.blit(self.game.rolling_bg, (0, 0))
            screen.blit(self.game.loading_img, (230, 90))
            screen.blit(self.current_dice, (300, 190))
            return


        if self.phase == 1:
            screen.blit(self.game.boss_bg, (0, 0))
            boss = self.game.current_boss
           
            screen.blit(self.game.thought_bubble, (420, 50))
            screen.blit(boss.image, (270, 150))


            text = "Xin chao, toi da nghe nhieu ve gu thoi trang cua ban. Hay cung thach dau theo                   style DE THUONG nao!!!"
            draw_text_wrapped(
                text,
                barbie_font,
                (255,105,180),
                screen,
                453,
                110,
                270
                )

            if self.show_next:
                screen.blit(self.next_img, self.next_button.topleft)
            return
        screen.blit(self.game.boss_bg, (0, 0))
       
        boss_type = self.game.current_boss.element
        hint = self.hint_map[boss_type]
       
        npc_x, npc_y = 40, 190
        screen.blit(self.npc_img, (npc_x, npc_y))




        bubble_x, bubble_y = npc_x + 210, npc_y - 150
        screen.blit(self.game.hint_bubble, (bubble_x, bubble_y))
        self.hint_font = pygame.font.SysFont("comicsansms", 22)




        title = hint_font.render("items hint",True,(255, 105, 180))
        screen.blit(title, title.get_rect(center=(bubble_x + 220, bubble_y + 70)))


        items = hint["items"]
        screen.blit(items[0].icon, (bubble_x + 60, bubble_y + 100))
        screen.blit(items[1].icon, (bubble_x + 155, bubble_y + 80))
        screen.blit(items[2].icon, (bubble_x + 300, bubble_y + 80))


        if self.show_button:
            screen.blit(self.game.menu_start_button, self.battle_button.topleft)
class DressingState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.music.load(
            "assets/sound/relax_music.mp3"
        )
       
        pygame.mixer.music.play(-1)
       
        self.next_img = load_image( "assets/ui/next2.png", (75, 75))

        self.next_rect = pygame.Rect(430, 490, 162, 115)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.game.hair_items:
                if item.icon_rect.collidepoint(
                    event.pos
                ):
                    self.game.current_hair = item

            for item in self.game.shirt_items:

                if item.icon_rect.collidepoint(
                    event.pos
                ):

                    self.game.current_shirt = item
            for item in self.game.shoe_items:

                if item.icon_rect.collidepoint(
                    event.pos
                ):

                    self.game.current_shoe = item
                   
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_rect.collidepoint(event.pos):
                self.game.change_state(
                    BattleState(self.game)
                    )

    def draw(self):

        screen.blit(self.game.current_background, (0,0))

        screen.blit(self.game.body,(150,40))
        
        screen.blit(self.game.current_shoe.image,self.game.current_shoe.wear_pos)

        screen.blit(self.game.current_shirt.image, self.game.current_shirt.wear_pos)

        screen.blit(elf.game.current_hair.image,self.game.current_hair.wear_pos)
     

        for item in self.game.hair_items:

            screen.blit(item.icon,item.icon_rect.topleft)
        

        for item in self.game.shirt_items:

            screen.blit(item.icon,item.icon_rect.topleft)

        for item in self.game.shoe_items:

            screen.blit(item.icon,item.icon_rect.topleft)

        screen.blit(self.next_img,self.next_rect.topleft)


class BattleState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.attr_keys = ["cute", "sexy", "elegant", "modern", "active"]
        self.player_hp = self.player_target_hp = 1000
        self.boss_hp = self.boss_target_hp = 1000
        self.current_round = 0
        self.timer = 0
        self.result_time = 0
        self.player_scores = self.get_total_scores()
        self.boss_scores = {key: random.randint(150, 250) for key in self.attr_keys}
        self.result = ""
        self.start_time = pygame.time.get_ticks()




        self.round_names = ["CUTE","ELEGANT","ACTIVE","MODERN","SEXY"]
        pygame.mixer.music.load("assets/battle/battle_music.mp3")
        pygame.mixer.music.play(-1)




    def get_total_scores(self):
        scores = {}
        items = [self.game.current_hair, self.game.current_shirt, self.game.current_shoe]
        for key in self.attr_keys:
            scores[key] = sum(item.style_scores.get(key, 70) for item in items)
        return scores




    def update(self):
       
        if self.player_hp > self.player_target_hp: self.player_hp -= 2
        if self.boss_hp > self.boss_target_hp: self.boss_hp -= 2




        self.timer += 1
        if self.timer > 120:
            if self.current_round < 5:
                self.battle_round()
                self.current_round += 1
                self.timer = 0
            else:
                self.check_final()




    def battle_round(self):
        key = self.attr_keys[self.current_round]
        diff = self.player_scores[key] - self.boss_scores[key]
        if diff > 0: self.boss_target_hp = max(0, self.boss_target_hp - diff * 2)
        else: self.player_target_hp = max(0, self.player_target_hp - abs(diff) * 2)
       
        if self.boss_target_hp <= 0: self.check_final()
        elif self.player_target_hp <= 0: self.check_final()




    def check_final(self):
        if self.result == "":




            if self.boss_target_hp < self.player_target_hp:
                self.result = "WIN"
            else:
                self.result = "LOSE"




            self.game.final_result = self.result




            self.game.change_state(
                FinalState(self.game)
            )




    def draw(self):




        screen.blit(self.game.battle_bg, (0, 0))




        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time




        if elapsed < 1000:
            text = "GAME START !!"

        else:
            round_index = (elapsed - 1000) // 2000




            if round_index < len(self.round_names):
                text = f"ROUND {round_index + 1} : {self.round_names[round_index]}"
            else:
                text = ""


        if text != "":


            pygame.draw.rect(
                screen,
                (255, 230, 240),
                (250, 15, 300, 60),
                border_radius=15
            )




            pygame.draw.rect(
                screen,
                (255, 105, 180),
                (250, 15, 300, 60),
                3,
                border_radius=15
            )




            title = font.render(
                text,
                True,
                (255, 105, 180)
            )




            screen.blit(
                title,
                title.get_rect(center=(400, 45))
            )




        off = (-140, -20)




        screen.blit(
            self.game.body,
            (150 + off[0], 40 + off[1])
        )




        screen.blit(
            self.game.current_shirt.image,
            (
                self.game.current_shirt.wear_pos[0] + off[0],
                self.game.current_shirt.wear_pos[1] + off[1]
            )
        )




        screen.blit(
            self.game.current_shoe.image,
            (
                self.game.current_shoe.wear_pos[0] + off[0],
                self.game.current_shoe.wear_pos[1] + off[1]
            )
        )




        screen.blit(
            self.game.current_hair.image,
            (
                self.game.current_hair.wear_pos[0] + off[0],
                self.game.current_hair.wear_pos[1] + off[1]
            )
        )




        screen.blit(
            pygame.transform.scale(
                self.game.current_boss.image,
                (255, 459)
            ),
            (470, 100)
        )




        self.draw_health_bar(385, 120, self.player_hp)
        self.draw_health_bar(435, 120, self.boss_hp)
    def draw_health_bar(self, x, y, hp):
        pygame.draw.rect(screen, WHITE, (x, y, 30, 300), 2, border_radius=15)
        fill_h = (hp / 1000) * 300
        if fill_h > 0:
            pygame.draw.rect(screen, (255, 105, 180), (x, y + (300 - fill_h), 30, fill_h), border_radius=15)




    def handle_event(self, event):
        if self.result != "" and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.game.change_state(MenuState(self.game))
class FinalState(BaseState):




    def __init__(self, game):
        super().__init__(game)




        self.start_time = pygame.time.get_ticks()




        self.alpha = 0




        self.result_scale = 0.3
        self.result_done = False




        self.show_button = False
        self.button_alpha = 0




        self.menu_img = pygame.transform.scale(
            self.game.back_menu_btn,
            (195, 138)
        )




        self.menu_rect = self.menu_img.get_rect(
            center=(WIDTH // 2, 450)
        )




        self.sparkles = [
            [
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(0.5, 1.5)
            ]
            for _ in range(25)
        ]




    def handle_event(self, event):




        if self.show_button and event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(event.pos):
                self.game.change_state(MenuState(self.game))




    def update(self):




        now = pygame.time.get_ticks()
        elapsed = now - self.start_time




        if self.alpha < 255:
            self.alpha += 5




        if self.result_scale < 1:
            self.result_scale += 0.03




        if elapsed > 2000:
            self.show_button = True




        if self.show_button and self.button_alpha < 255:
            self.button_alpha += 5




        for s in self.sparkles:
            s[1] -= s[2]
            if s[1] < 0:
                s[0] = random.randint(0, WIDTH)
                s[1] = HEIGHT




    def draw(self):




        bg = self.game.result_bg.copy()
        bg.set_alpha(self.alpha)
        screen.blit(bg, (0, 0))




        if self.game.final_result == "WIN":
            img = self.game.win_screen
        else:
            img = self.game.game_over_screen




        w = int(img.get_width() * self.result_scale)
        h = int(img.get_height() * self.result_scale)




        img_scaled = pygame.transform.smoothscale(img, (w, h))




        if self.game.final_result == "WIN":
            img = self.game.win_screen
            rect = img_scaled.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 60)
                )
        else:
            img = self.game.game_over_screen
            rect = img_scaled.get_rect(
                center=(WIDTH // 2 - 20, HEIGHT // 2 - 60)
                )




        screen.blit(img_scaled, rect)




        for s in self.sparkles:
            x, y, size = s
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(x), int(y)),
                int(size)
            )




        if self.show_button:




            btn = self.menu_img.copy()
            btn.set_alpha(self.button_alpha)




            bounce = math.sin(pygame.time.get_ticks() * 0.005) * 5




            btn_rect = btn.get_rect(
                center=(WIDTH // 2, 460 + bounce)
            )




            screen.blit(btn, btn_rect)




class Game:
   
    def __init__(self):




        self.loading_img = load_image("assets/dice/loading.png", (325,100))
        self.result_bg = load_image("assets/result/result_bg.png",(800,600))
        self.win_screen = load_image(
            "assets/result/win.png",
            (650,180)
        )




        self.game_over_screen = load_image(
            "assets/result/game_over.png",
            (650,210)
        )




        self.back_menu_btn = load_image("assets/ui/back_to_menu.png",(273,195))




        self.body = load_image(
            "assets/body/body.png",
            (393.75,577.5)
        )
        self.cover = load_image(
            "assets/cover1/bg1.png",
            (800,600)
        )




        self.rolling_bg = load_image(
            "assets/dice/bg2.png",
            (800,600)
        )
       
        self.boss_bg = load_image(
            "assets/dice/bg3.png",
            (800,600)
        )
        self.current_background = load_image("assets/background/dressing_bg.png",(800,600))




        self.battle_bg = load_image("assets/battle/battle_bg.png",(800,600))








        self.dice1 = load_image(
            "assets/dice/dice1.png",
            (200,200)
        )




        self.dice2 = load_image(
            "assets/dice/dice2.png",
            (200,200)
        )




        self.dice3 = load_image(
            "assets/dice/dice3.png",
            (200,200)
        )




        self.dice_list = [self.dice1,self.dice2,self.dice3]








        self.fire_boss = Boss("assets/boss/fire_boss.png","FIRE")
        self.water_boss = Boss("assets/boss/water_boss.png","WATER")




        self.thought_bubble = load_image("assets/ui/bubble.png",(320,180))
        self.hint_bubble = load_image("assets/ui/bubble.png",(450,300))
        self.boss_list = [self.fire_boss,self.water_boss]




        self.current_boss = self.fire_boss
        self.start_button = load_image("assets/ui/start.png",(162.5,115))
        self.menu_start_button = load_image("assets/ui/start.png",(195,138))
        pygame.mixer.music.load("assets/sound/relax_music.mp3")




        self.hair_items = [
    Item(
        "assets/hair/hair.png",
        (92,120),
        (64.4,84),
        "fire",
        (580,25),
        (300,59),
        {
            "cute":120,
            "sexy":30,
            "elegant":60,
            "modern":40,
            "active":50
        }
    ),




    Item(
        "assets/hair/hair2.png",
        (115,200),
        (80.5,140),
        "water",
        (670,25),
        (290,60),
        {
            "cute":50,
            "sexy":120,
            "elegant":90,
            "modern":60,
            "active":70
        }
    ),




    Item(
        "assets/hair/hair3.png",
        (105,145),
        (73.5,101.5),
        "wind",
        (575,150),
        (298,56),
        {
            "cute":60,
            "sexy":70,
            "elegant":80,
            "modern":120,
            "active":100
        }
    )
]




        self.shirt_items = [




            Item(
                "assets/shirt/shirt1.png",
                (376,520),
                (160,230),
                "water",
                (520,238),
                (158,103),
                {
                    "cute":110,
                    "sexy":20,
                    "elegant":50,
                    "modern":40,
                    "active":60
                }
            ),




            Item(
                "assets/shirt/shirt2.png",
                (336,495),
                (140,190),
                "fire",
                (660,230),
                (180,75),
                {
                    "cute":40,
                    "sexy":120,
                    "elegant":80,
                    "modern":90,
                    "active":70
                }
            ),




            Item(
                "assets/shirt/shirt3.png",
                (245,340.2),
                (122,170),
                "wind",
                (550,420),
                (226,111.5),
                {
                    "cute":60,
                    "sexy":50,
                    "elegant":90,
                    "modern":120,
                    "active":110
                }
            )
        ]




        self.shoe_items = [
            Item(
                "assets/shoes/shoe1.png",
                (108,126),
                (97.2,113.4),
                "water",
                (665,450),
                (290,474),
                {
                    "cute":110,
                    "sexy":20,
                    "elegant":40,
                    "modern":50,
                    "active":70
                }
            ),




            Item(
                "assets/shoes/shoe2.png",
                (108,126),
                (97.2,113.4),
                "fire",
                (665,130),
                (292,474),
                {
                    "cute":30,
                    "sexy":100,
                    "elegant":70,
                    "modern":90,
                    "active":110
                }
            )
        ]




        self.current_hair = self.hair_items[0]
        self.current_shirt = self.shirt_items[0]
        self.current_shoe = self.shoe_items[0]




        self.state = MenuState(self)




    def change_state(self, new_state):
        self.state = new_state
    def run(self):
       
        running = True




        while running:
           
            for event in pygame.event.get():




                if event.type == pygame.QUIT:
                    running = False




                self.state.handle_event(event)
               
            self.state.update()
            self.state.draw()




            pygame.display.update()
           
            clock.tick(60)
        pygame.quit()
game = Game()
game.run()









import pygame
import random
import math




pygame.init()
pygame.mixer.init()




WIDTH = 800
HEIGHT = 600




screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fashion Magic Battle")




clock = pygame.time.Clock()




font = pygame.font.SysFont("arial", 32)
small_font = pygame.font.SysFont("arial", 24)




barbie_font = pygame.font.SysFont("comicsansms",13)
hint_font = pygame.font.SysFont("comicsansms", 24)




WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)




def load_image(path, size):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, size)
    return image




def draw_text_wrapped(text, font, color, surface, x, y, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""




    for word in words:
        test_line = current_line + word + " "




        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "




    lines.append(current_line)




    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (x, y + i * 25))




class Item:
    def __init__(
        self,
        image_path,
        image_size,
        icon_size,
        element,
        icon_pos,
        wear_pos,
        style_scores
    ):
        self.style_scores = style_scores




        self.image = load_image(
            image_path,
            image_size
        )




        self.icon = load_image(
            image_path,
            icon_size
        )




        self.element = element
       
        self.icon_rect = pygame.Rect(
            icon_pos[0],
            icon_pos[1],
            icon_size[0],
            icon_size[1]
        )
        self.wear_pos = wear_pos




class Boss:
    def __init__(
        self,
        image_path,
        element
    ):




        self.image = load_image(
            image_path,
            (247, 342)
        )




        self.element = element








class BaseState:




    def __init__(self, game):




        self.game = game




    def handle_event(self, event):
        pass
   
    def update(self):
        pass




    def draw(self):
        pass




class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)




        self.start_rect = pygame.Rect(
            325, 315, 240, 120
        )




    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_rect.collidepoint(event.pos):
                self.game.change_state(
                RollingState(self.game)
            )




    def draw(self):
        screen.blit(
            self.game.cover,
            (0,0)
        )




        screen.blit(
            self.game.start_button,
            self.start_rect.topleft
        )




class RollingState(BaseState):
   
    def __init__(self, game):
        super().__init__(game)




        pygame.mixer.music.load("assets/dice/rolling_music.mp3")
        pygame.mixer.music.play()
        self.show_next = False
        self.next_button = pygame.Rect(500, 480, 140, 70)
        self.next_img = load_image("assets/ui/next.png", (162.5, 115))




        self.start_time = pygame.time.get_ticks()




        self.phase = 0




        self.phase_time = self.start_time




        self.current_dice = random.choice(self.game.dice_list)
        self.dice_timer = 0




        self.game.current_boss = random.choice(self.game.boss_list)




        self.npc_map = {
            "FIRE": "assets/npc/npc1.png",
            "WATER": "assets/npc/npc1.png"
        }




        self.npc_img = None
        self.bubble = self.game.thought_bubble




        self.show_button = False
        self.battle_button = pygame.Rect(300, 450, 200, 110)




        self.hint_map = {
            "FIRE": {
                "text": "HAY MAC DO DO DE HA GUC BOSS !!",
                "items": [
                    self.game.hair_items[0],
                    self.game.shirt_items[1],
                    self.game.shoe_items[0]
                ]
            },
            "WATER": {
                "text": "HAY MAC DO Lanh DE HA GUC BOSS !!",
                "items": [
                    self.game.hair_items[2],
                    self.game.shirt_items[2],
                    self.game.shoe_items[1]
                ]
            }
        }




    def handle_event(self, event):




        if event.type == pygame.MOUSEBUTTONDOWN:




            if self.phase == 1 and self.show_next:
                if self.next_button.collidepoint(event.pos):
                    self.phase = 2
                    self.phase_time = pygame.time.get_ticks()




            elif self.phase == 2 and self.show_button:
                if self.battle_button.collidepoint(event.pos):
                    self.game.change_state(DressingState(self.game))




    def update(self):
        now = pygame.time.get_ticks()
        if self.phase == 0:
            if now - self.dice_timer > 120:
                self.current_dice = random.choice(self.game.dice_list)
                self.dice_timer = now




            if now - self.start_time > 2000:
                self.phase = 1
                self.phase_time = now




        elif self.phase == 1:
            if now - self.phase_time > 2000:
                self.show_next = True
                boss_type = self.game.current_boss.element
                self.npc_img = load_image(
                    self.npc_map[boss_type],
                    (290, 300)
                )




        elif self.phase == 2:
            if now - self.phase_time > 2000:
                self.show_button = True
        if self.phase == 2:
            self.show_button = True




    def draw(self):
        if self.phase == 0:
            screen.blit(self.game.rolling_bg, (0, 0))
            screen.blit(self.game.loading_img, (230, 90))
            screen.blit(self.current_dice, (300, 190))
            return




        if self.phase == 1:
            screen.blit(self.game.boss_bg, (0, 0))
            boss = self.game.current_boss
           
            screen.blit(self.game.thought_bubble, (420, 50))
            screen.blit(boss.image, (270, 150))




            text = "Xin chao, toi da nghe nhieu ve gu thoi trang cua ban. Hay cung thach dau theo                   style DE THUONG nao!!!"
            draw_text_wrapped(
                text,
                barbie_font,
                (255,105,180),
                screen,
                453,
                110,
                270
                )




            if self.show_next:
                screen.blit(self.next_img, self.next_button.topleft)
            return
        screen.blit(self.game.boss_bg, (0, 0))
       
        boss_type = self.game.current_boss.element
        hint = self.hint_map[boss_type]
       
        npc_x, npc_y = 40, 190
        screen.blit(self.npc_img, (npc_x, npc_y))




        bubble_x, bubble_y = npc_x + 210, npc_y - 150
        screen.blit(self.game.hint_bubble, (bubble_x, bubble_y))
        self.hint_font = pygame.font.SysFont("comicsansms", 22)




        title = hint_font.render(
            "items hint",
            True,
            (255, 105, 180)
        )
        screen.blit(title, title.get_rect(center=(bubble_x + 220, bubble_y + 70)))




        items = hint["items"]
        screen.blit(items[0].icon, (bubble_x + 60, bubble_y + 100))
        screen.blit(items[1].icon, (bubble_x + 155, bubble_y + 80))
        screen.blit(items[2].icon, (bubble_x + 300, bubble_y + 80))




        if self.show_button:
            screen.blit(self.game.menu_start_button, self.battle_button.topleft)
class DressingState(BaseState):




    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.music.load(
            "assets/sound/relax_music.mp3"
        )
       
        pygame.mixer.music.play(-1)
       
        self.next_img = load_image( "assets/ui/next2.png", (75, 75))




        self.next_rect = pygame.Rect(430, 490, 162, 115)




    def handle_event(self, event):




        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in self.game.hair_items:
                if item.icon_rect.collidepoint(
                    event.pos
                ):




                    self.game.current_hair = item




            for item in self.game.shirt_items:




                if item.icon_rect.collidepoint(
                    event.pos
                ):




                    self.game.current_shirt = item
            for item in self.game.shoe_items:




                if item.icon_rect.collidepoint(
                    event.pos
                ):




                    self.game.current_shoe = item
                   
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.next_rect.collidepoint(event.pos):
                self.game.change_state(
                    BattleState(self.game)
                    )




    def draw(self):




        screen.blit(
            self.game.current_background,
            (0,0)
        )




        screen.blit(
            self.game.body,
            (150,40)
        )




        screen.blit(
            self.game.current_shoe.image,
            self.game.current_shoe.wear_pos
        )




        screen.blit(
            self.game.current_shirt.image,
            self.game.current_shirt.wear_pos
        )




        screen.blit(
            self.game.current_hair.image,
            self.game.current_hair.wear_pos
        )




        for item in self.game.hair_items:




            screen.blit(
                item.icon,
                item.icon_rect.topleft
            )




        for item in self.game.shirt_items:




            screen.blit(
                item.icon,
                item.icon_rect.topleft
            )




        for item in self.game.shoe_items:




            screen.blit(
                item.icon,
                item.icon_rect.topleft
            )




        screen.blit(
            self.next_img,
            self.next_rect.topleft)




class BattleState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.attr_keys = ["cute", "sexy", "elegant", "modern", "active"]
        self.player_hp = self.player_target_hp = 1000
        self.boss_hp = self.boss_target_hp = 1000
        self.current_round = 0
        self.timer = 0
        self.result_time = 0
        self.player_scores = self.get_total_scores()
        self.boss_scores = {key: random.randint(150, 250) for key in self.attr_keys}
        self.result = ""
        self.start_time = pygame.time.get_ticks()




        self.round_names = ["CUTE","ELEGANT","ACTIVE","MODERN","SEXY"]
        pygame.mixer.music.load("assets/battle/battle_music.mp3")
        pygame.mixer.music.play(-1)




    def get_total_scores(self):
        scores = {}
        items = [self.game.current_hair, self.game.current_shirt, self.game.current_shoe]
        for key in self.attr_keys:
            scores[key] = sum(item.style_scores.get(key, 70) for item in items)
        return scores




    def update(self):
       
        if self.player_hp > self.player_target_hp: self.player_hp -= 2
        if self.boss_hp > self.boss_target_hp: self.boss_hp -= 2




        self.timer += 1
        if self.timer > 120:
            if self.current_round < 5:
                self.battle_round()
                self.current_round += 1
                self.timer = 0
            else:
                self.check_final()




    def battle_round(self):
        key = self.attr_keys[self.current_round]
        diff = self.player_scores[key] - self.boss_scores[key]
        if diff > 0: self.boss_target_hp = max(0, self.boss_target_hp - diff * 2)
        else: self.player_target_hp = max(0, self.player_target_hp - abs(diff) * 2)
       
        if self.boss_target_hp <= 0: self.check_final()
        elif self.player_target_hp <= 0: self.check_final()




    def check_final(self):
        if self.result == "":




            if self.boss_target_hp < self.player_target_hp:
                self.result = "WIN"
            else:
                self.result = "LOSE"




            self.game.final_result = self.result




            self.game.change_state(
                FinalState(self.game)
            )




    def draw(self):




        screen.blit(self.game.battle_bg, (0, 0))




        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time




        if elapsed < 1000:
            text = "GAME START !!"




        else:
            round_index = (elapsed - 1000) // 2000




            if round_index < len(self.round_names):
                text = f"ROUND {round_index + 1} : {self.round_names[round_index]}"
            else:
                text = ""




        if text != "":




            pygame.draw.rect(
                screen,
                (255, 230, 240),
                (250, 15, 300, 60),
                border_radius=15
            )




            pygame.draw.rect(
                screen,
                (255, 105, 180),
                (250, 15, 300, 60),
                3,
                border_radius=15
            )




            title = font.render(
                text,
                True,
                (255, 105, 180)
            )




            screen.blit(
                title,
                title.get_rect(center=(400, 45))
            )




        off = (-140, -20)




        screen.blit(
            self.game.body,
            (150 + off[0], 40 + off[1])
        )




        screen.blit(
            self.game.current_shirt.image,
            (
                self.game.current_shirt.wear_pos[0] + off[0],
                self.game.current_shirt.wear_pos[1] + off[1]
            )
        )




        screen.blit(
            self.game.current_shoe.image,
            (
                self.game.current_shoe.wear_pos[0] + off[0],
                self.game.current_shoe.wear_pos[1] + off[1]
            )
        )




        screen.blit(
            self.game.current_hair.image,
            (
                self.game.current_hair.wear_pos[0] + off[0],
                self.game.current_hair.wear_pos[1] + off[1]
            )
        )




        screen.blit(
            pygame.transform.scale(
                self.game.current_boss.image,
                (255, 459)
            ),
            (470, 100)
        )




        self.draw_health_bar(385, 120, self.player_hp)
        self.draw_health_bar(435, 120, self.boss_hp)
    def draw_health_bar(self, x, y, hp):
        pygame.draw.rect(screen, WHITE, (x, y, 30, 300), 2, border_radius=15)
        fill_h = (hp / 1000) * 300
        if fill_h > 0:
            pygame.draw.rect(screen, (255, 105, 180), (x, y + (300 - fill_h), 30, fill_h), border_radius=15)




    def handle_event(self, event):
        if self.result != "" and (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
            self.game.change_state(MenuState(self.game))
class FinalState(BaseState):




    def __init__(self, game):
        super().__init__(game)




        self.start_time = pygame.time.get_ticks()




        self.alpha = 0




        self.result_scale = 0.3
        self.result_done = False




        self.show_button = False
        self.button_alpha = 0




        self.menu_img = pygame.transform.scale(
            self.game.back_menu_btn,
            (195, 138)
        )




        self.menu_rect = self.menu_img.get_rect(
            center=(WIDTH // 2, 450)
        )




        self.sparkles = [
            [
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(0.5, 1.5)
            ]
            for _ in range(25)
        ]




    def handle_event(self, event):




        if self.show_button and event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_rect.collidepoint(event.pos):
                self.game.change_state(MenuState(self.game))




    def update(self):




        now = pygame.time.get_ticks()
        elapsed = now - self.start_time




        if self.alpha < 255:
            self.alpha += 5




        if self.result_scale < 1:
            self.result_scale += 0.03




        if elapsed > 2000:
            self.show_button = True
          
        if self.show_button and self.button_alpha < 255:
            self.button_alpha += 5




        for s in self.sparkles:
            s[1] -= s[2]
            if s[1] < 0:
                s[0] = random.randint(0, WIDTH)
                s[1] = HEIGHT




    def draw(self):




        bg = self.game.result_bg.copy()
        bg.set_alpha(self.alpha)
        screen.blit(bg, (0, 0))




        if self.game.final_result == "WIN":
            img = self.game.win_screen
        else:
            img = self.game.game_over_screen




        w = int(img.get_width() * self.result_scale)
        h = int(img.get_height() * self.result_scale)




        img_scaled = pygame.transform.smoothscale(img, (w, h))




        if self.game.final_result == "WIN":
            img = self.game.win_screen
            rect = img_scaled.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 60)
                )
        else:
            img = self.game.game_over_screen
            rect = img_scaled.get_rect(
                center=(WIDTH // 2 - 20, HEIGHT // 2 - 60)
                )




        screen.blit(img_scaled, rect)




        for s in self.sparkles:
            x, y, size = s
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (int(x), int(y)),
                int(size)
            )




        if self.show_button:




            btn = self.menu_img.copy()
            btn.set_alpha(self.button_alpha)




            bounce = math.sin(pygame.time.get_ticks() * 0.005) * 5




            btn_rect = btn.get_rect(
                center=(WIDTH // 2, 460 + bounce)
            )




            screen.blit(btn, btn_rect)




class Game:
   
    def __init__(self):




        self.loading_img = load_image("assets/dice/loading.png", (325,100))
        self.result_bg = load_image("assets/result/result_bg.png",(800,600))
        self.win_screen = load_image(
            "assets/result/win.png",
            (650,180)
        )




        self.game_over_screen = load_image(
            "assets/result/game_over.png",
            (650,210)
        )




        self.back_menu_btn = load_image("assets/ui/back_to_menu.png",(273,195))




        self.body = load_image(
            "assets/body/body.png",
            (393.75,577.5)
        )
        self.cover = load_image(
            "assets/cover1/bg1.png",
            (800,600)
        )




        self.rolling_bg = load_image(
            "assets/dice/bg2.png",
            (800,600)
        )
       
        self.boss_bg = load_image(
            "assets/dice/bg3.png",
            (800,600)
        )
        self.current_background = load_image("assets/background/dressing_bg.png",(800,600))




        self.battle_bg = load_image("assets/battle/battle_bg.png",(800,600))








        self.dice1 = load_image(
            "assets/dice/dice1.png",
            (200,200)
        )




        self.dice2 = load_image(
            "assets/dice/dice2.png",
            (200,200)
        )




        self.dice3 = load_image(
            "assets/dice/dice3.png",
            (200,200)
        )




        self.dice_list = [self.dice1,self.dice2,self.dice3]








        self.fire_boss = Boss("assets/boss/fire_boss.png","FIRE")
        self.water_boss = Boss("assets/boss/water_boss.png","WATER")




        self.thought_bubble = load_image("assets/ui/bubble.png",(320,180))
        self.hint_bubble = load_image("assets/ui/bubble.png",(450,300))
        self.boss_list = [self.fire_boss,self.water_boss]




        self.current_boss = self.fire_boss
        self.start_button = load_image("assets/ui/start.png",(162.5,115))
        self.menu_start_button = load_image("assets/ui/start.png",(195,138))
        pygame.mixer.music.load("assets/sound/relax_music.mp3")




        self.hair_items = [
    Item(
        "assets/hair/hair.png",
        (92,120),
        (64.4,84),
        "fire",
        (580,25),
        (300,59),
        {
            "cute":120,
            "sexy":30,
            "elegant":60,
            "modern":40,
            "active":50
        }
    ),




    Item(
        "assets/hair/hair2.png",
        (115,200),
        (80.5,140),
        "water",
        (670,25),
        (290,60),
        {
            "cute":50,
            "sexy":120,
            "elegant":90,
            "modern":60,
            "active":70
        }
    ),




    Item(
        "assets/hair/hair3.png",
        (105,145),
        (73.5,101.5),
        "wind",
        (575,150),
        (298,56),
        {
            "cute":60,
            "sexy":70,
            "elegant":80,
            "modern":120,
            "active":100
        }
    )
]




        self.shirt_items = [




            Item(
                "assets/shirt/shirt1.png",
                (376,520),
                (160,230),
                "water",
                (520,238),
                (158,103),
                {
                    "cute":110,
                    "sexy":20,
                    "elegant":50,
                    "modern":40,
                    "active":60
                }
            ),




            Item(
                "assets/shirt/shirt2.png",
                (336,495),
                (140,190),
                "fire",
                (660,230),
                (180,75),
                {
                    "cute":40,
                    "sexy":120,
                    "elegant":80,
                    "modern":90,
                    "active":70
                }
            ),




            Item(
                "assets/shirt/shirt3.png",
                (245,340.2),
                (122,170),
                "wind",
                (550,420),
                (226,111.5),
                {
                    "cute":60,
                    "sexy":50,
                    "elegant":90,
                    "modern":120,
                    "active":110
                }
            )
        ]




        self.shoe_items = [
            Item(
                "assets/shoes/shoe1.png",
                (108,126),
                (97.2,113.4),
                "water",
                (665,450),
                (290,474),
                {
                    "cute":110,
                    "sexy":20,
                    "elegant":40,
                    "modern":50,
                    "active":70
                }
            ),




            Item(
                "assets/shoes/shoe2.png",
                (108,126),
                (97.2,113.4),
                "fire",
                (665,130),
                (292,474),
                {
                    "cute":30,
                    "sexy":100,
                    "elegant":70,
                    "modern":90,
                    "active":110
                }
            )
        ]




        self.current_hair = self.hair_items[0]
        self.current_shirt = self.shirt_items[0]
        self.current_shoe = self.shoe_items[0]




        self.state = MenuState(self)




    def change_state(self, new_state):
        self.state = new_state
    def run(self):
       
        running = True




        while running:
           
            for event in pygame.event.get():




                if event.type == pygame.QUIT:
                    running = False

                self.state.handle_event(event)
               
            self.state.update()
            self.state.draw()




            pygame.display.update()
           
            clock.tick(60)
        pygame.quit()
game = Game()
game.run()
