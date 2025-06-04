import pygame
import sys
import random

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космонафт и астеройды")
clock = pygame.time.Clock()

# Загрузка изображений
player_image = pygame.transform.scale(pygame.image.load("ship.png"), (50, 50))
platform_image = pygame.Surface((100, 20))
platform_image.fill((100, 50, 0))
asteroid_image = pygame.transform.scale(pygame.image.load("asteroid.png"), (40, 40))
flag_size = (20, 30)
flag_image = pygame.transform.scale(pygame.image.load("flag_image.png"), flag_size)

sky_image = pygame.image.load("sky.jpg")  # Укажите правильный путь к вашему изображению sky.png
sky_image = pygame.transform.scale(sky_image, (WIDTH, HEIGHT))
# Шрифт для текста
font = pygame.font.SysFont(None, 48)

# Загрузка изображения фона
sky_background = pygame.image.load('sky_background.png')
# Можно масштабировать изображение под размер экрана, если нужно:
sky_background = pygame.transform.scale(sky_background, (WIDTH, HEIGHT))
# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 150
        self.x_speed = 0
        self.y_speed = 0
        self.on_ground = False

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_speed = -5
        elif keys[pygame.K_RIGHT]:
            self.x_speed = 5
        else:
            self.x_speed = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.y_speed = -15
            self.on_ground = False

        # Гравитация
        self.y_speed += 0.6

        # Обновление позиции
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Ограничения по границам экрана
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def handle_platform_collision(self, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.y_speed > 0 and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.y_speed = 0
                    self.on_ground = True

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_image
        self.rect = self.image.get_rect(topleft=(x, y))

# Класс астероида врага
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x_pos = random.randint(0, WIDTH - 40)
        y_pos = random.randint(-100, -40)
        self.image = asteroid_image
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.speed_y = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            # Возвращаем астероид наверх с новой позицией и скоростью
            self.rect.x = random.randint(0, WIDTH - 40)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(3, 6)

# Определение уровней: список словарей с позициями платформ и флагом.
levels_data = [
    # Уровень 1: базовый уровень.
    {
        "platforms": [
            (0, HEIGHT - 50),
            (150, HEIGHT - 150),
            (350, HEIGHT - 250),
            (550, HEIGHT - 350),
            (300, HEIGHT - 450),
            (50, HEIGHT - 370),
        ],
        "flag_pos": (WIDTH // 8 - flag_size[0] //2 , HEIGHT - 400)
    },
    # Уровень 2: другой набор платформ.
    {
        "platforms": [
            (0, HEIGHT -50),
            (200, HEIGHT -200),
            (400, HEIGHT -300),
            (600, HEIGHT -400),
            (350, HEIGHT -500),
        ],
        "flag_pos": (WIDTH //2 , HEIGHT -530)
    },
    # Уровень 3: финальный уровень.
    {
        "platforms": [
            (0, HEIGHT -50),
            (300, HEIGHT -150),
            (500, HEIGHT -250),
            (700, HEIGHT -350),
            (400 ,HEIGHT -450),
            (50 ,HEIGHT -450)
        ],
        "flag_pos": (WIDTH //8 , HEIGHT -480)
    }
]

current_level_index=0

def load_level(level_index):
    level_data=levels_data[level_index]
    platforms_group.empty()
    for pos in level_data["platforms"]:
        p=Platform(*pos)
        platforms_group.add(p)
    global flag_rect
    flag_x=level_data["flag_pos"][0]
    flag_y=level_data["flag_pos"][1]
    flag_rect=pygame.Rect(
       flag_x,
       flag_y,
       flag_size[0],
       flag_size[1]
   )

# Создаем группы спрайтов и игрока.
player_group=pygame.sprite.Group()
platforms_group=pygame.sprite.Group()
asteroids_group=pygame.sprite.Group()

player=Player()
player_group.add(player)

# Создаем астероиды.
for _ in range(5):
    asteroid=Asteroid()
    asteroids_group.add(asteroid)

load_level(current_level_index)

danger_zone_height=10

game_over=False
victory=False


def show_menu():
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Нажатие Enter стартует игру.
                    menu_active = False
                elif event.key == pygame.K_ESCAPE:  # Esc закрывает игру.
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))

        # Отрисовка фона
        screen.blit(sky_background, (0, 0))
        title_text = font.render("Космонафт и астеройды", True, (255, 255, 255))
        start_text = font.render("Нажмите Enter чтобы начать", True, (255, 255, 255))
        nastroyki_text = font.render("Настройки", True, (255, 255, 255))
        sparavka_text = font.render("Справка", True, (255, 255, 255))
        exit_text = font.render("Нажмите Esc чтобы выйти", True, (255, 255, 255))


        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT// 3))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(nastroyki_text, (WIDTH // 2 - exit_text.get_width() // 5, HEIGHT // 2 + 60))
        screen.blit(sparavka_text, (WIDTH // 2 - exit_text.get_width() // 6, HEIGHT // 2 + 120))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 180))

        pygame.display.flip()


# Перед запуском основной игры показываем меню.
show_menu()

while True:
    for event in pygame.event.get():
       if event.type==pygame.QUIT:
           pygame.quit()
           sys.exit()

    if not game_over and not victory:
       player.update()
       player.handle_platform_collision(platforms_group)
       asteroids_group.update()

       # Проверка касания с опасной зоной снизу.
       if player.rect.bottom>=HEIGHT-danger_zone_height:
           game_over=True

       # Столкновение с астероидами.
       if pygame.sprite.spritecollideany(player , asteroids_group):
           game_over=True

       # Проверка достижения флага для перехода к следующему уровню.
       if player.rect.colliderect(flag_rect):
           current_level_index+=1
           if current_level_index>=len(levels_data):
               victory=True
           else:
               load_level(current_level_index)
               # Перезапускаем игрок в стартовую позицию для нового уровня.
               player.rect.x=50
               player.rect.y=HEIGHT-150

   # Отрисовка сцены или сообщений о победе/проигрыше
    screen.fill((135 ,206 ,235))
    screen.blit(sky_image, (0, 0))
    if not game_over and not victory:
       platforms_group.draw(screen)
       asteroids_group.draw(screen)
       player_group.draw(screen)
       screen.blit(flag_image,(flag_rect.x ,flag_rect.y))
    elif victory:
        text_surface = font.render("Победа!", True, (0, 128, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)
    else:  
       text_surface = font.render("Вы проиграли", True, (255, 0, 0))
       text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
       screen.blit(text_surface, text_rect)

    pygame.display.flip()

    if game_over or victory:
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()


    clock.tick(60)
