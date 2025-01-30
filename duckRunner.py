import pgzrun
from pgzhelper import *
import random
import math
import time


missile_sound = sounds.missile_sound

# Configuracao geral do jogo
WIDTH, HEIGHT = 800, 600
GROUND_Y = 400
GRAVITY = 1
JUMP_VELOCITY = -15
OBSTACLE_SPAWN_TIME = 50
OBSTACLE_SPEED = 8
PLANE_BASE_SPEED = 5
PLANE_FLOAT_RANGE = 10
BULLET_SPEED = 6
BULLET_SHOOT_TIME = random.randint(80, 150)
RUNNER_SPEED = 5 
SPEED_UP_THRESHOLD = 18 # pontuacao para objetivo de dobrar velocidade e mudar cor

# iniciar heroi
runner = Actor('run0', (100, GROUND_Y))
runner.images = ['run0', 'run1', 'run2', 'run3', 'run4']
jump_images = ['jmp0', 'jmp1', 'jmp2', 'jmp3']

# iniciar inimigo aviao
plane = Actor('fly1', (-100, random.randint(50, 200)))
plane.images = ['fly1', 'fly2']
plane_wave = random.uniform(0, math.pi * 2)
plane_speed = PLANE_BASE_SPEED + random.uniform(-1, 1)
plane_active = False
plane_timer = random.randint(200, 400)

# quantos de vida vamos ter
lives = 3
heart_image = Actor('heart', (WIDTH - 50, 50))  # Usando um ator para o coração

# variaveis de jogo
velocity_y = 0
obstacles = []
bullets = []
obstacles_timeout = 0
bullet_timer = 0
score = 0
game_over = False
is_jumping = False
invincible_time = 0 #depois que tomar o hit, quanto tempo vai ficar imune, tem uma funcao para isso

# spawn de coracoes
ground_hearts = []
heart_spawn_time = random.randint(200, 500)

# variaveis do menu
menu_active = True  #saber se estamos no menu do jogo ou nao
selected_option = 0  # 0 = Jogar, 1 = Mudar Som, 2 = Sair
last_navigation_time = 0 
navigation_delay = 0.2

# musica de fundo
bg_music_playing = False
music_muted = False

def spawn_obstacle():
    
    obstacle = Actor('cactus', (850, 390))
    obstacles.append(obstacle)

def shoot_bullet():
    
    bullet_x = plane.x + random.randint(-30, 30)
    bullet_y = plane.y + random.randint(5, 15)
    bullet = Actor('bullet2', (bullet_x, bullet_y))
    bullets.append(bullet)
    
    # tocar som quando o aviao atira
    missile_sound.play()

def spawn_heart():
   
    offset = random.randint(150, 300)  # distancia do coracao aparecer
    
    #garantir que o coracao nao vaze da tela e tambem nao va muito para baixo
    min_x = 150  
    max_x = WIDTH - 150  
    heart_x = runner.x + random.randint(-offset, offset)
    heart_x = max(min_x, min(max_x, heart_x))  

    heart_y = GROUND_Y  
    
    # Gera o coracao
    heart = Actor('heart', (heart_x, heart_y))
    ground_hearts.append(heart)

def update():
    global velocity_y, obstacles_timeout, score, game_over, is_jumping
    global plane_wave, bullet_timer, plane_speed, plane_active, plane_timer, BULLET_SHOOT_TIME
    global lives, invincible_time, heart_spawn_time, menu_active, selected_option, last_navigation_time
    global navigation_delay, bg_music_playing, PLANE_BASE_SPEED, RUNNER_SPEED, OBSTACLE_SPEED 
    global music_muted, last_sound_toggle_time 

    current_time = time.time()

    if menu_active:
        # Navegacao no menu
        if current_time - last_navigation_time > navigation_delay:  # Delay de navegacao
            if keyboard.up:
                selected_option = (selected_option - 1) % 3
                last_navigation_time = current_time
            if keyboard.down:
                selected_option = (selected_option + 1) % 3
                last_navigation_time = current_time
        
            if keyboard.space or keyboard.RETURN:
                if selected_option == 0:  # Jogar
                    menu_active = False  # Comeca o jogo
                    if not bg_music_playing and not music_muted:
                        music.play('game_music')  # Toca a musica de fundo
                        bg_music_playing = True
                elif selected_option == 1:  # Mudar Som
                    # Verifica se passou tempo suficiente para alternar o estado do som
                    if current_time - last_sound_toggle_time > 0.5:  # Cooldown de 0.5 segundos
                        music_muted = not music_muted
                        if music_muted:
                            mudar_som_text = "Som Desligado"
                            music.stop()  # Para a musica se estiver no modo mudoo
                        else:
                            mudar_som_text = "Som Ligado"
                            music.play('game_music')  # Recomeça a musica se o som for ativado
                        last_sound_toggle_time = current_time  # Atualiza o tempo do ultimo toggle
                elif selected_option == 2:  # sair
                    exit()  # fecha o jogo
    else:
        if game_over:
            music.stop()  # para a musica no final do jogo
            return
        
        # Aumentar a velocidade quanto pegar 18 pontos
        if score >= SPEED_UP_THRESHOLD:
            OBSTACLE_SPEED = 16
            PLANE_BASE_SPEED = 10
            RUNNER_SPEED = 10
        
        # Aumentar taxa de tiros quando a pontuacao atingir o limite
        if score >= SPEED_UP_THRESHOLD:
            BULLET_SHOOT_TIME = random.randint(50, 100)
        
        # movimentar boneco para os lados
        if keyboard.left:
            runner.x -= RUNNER_SPEED
        if keyboard.right:
            runner.x += RUNNER_SPEED

        # Limitar movimento do boneco na tela
        runner.x = max(50, min(WIDTH - 50, runner.x))

        # Animacao de correr
        if not is_jumping:
            runner.next_image()
        else:
            runner.image = jump_images[0]

        # aviao so aparece depois de um tempo
        if not plane_active:
            plane_active = True
            plane.x = -100  #comeca a voar na mesma hora que comeca o jogo
            plane.y = random.randint(50, 200)
            plane_wave = random.uniform(0, math.pi * 2)
            plane_speed = PLANE_BASE_SPEED + random.uniform(-1, 1)
        
        if plane_active:
            plane.x += plane_speed
            plane_wave += 0.1
            plane.y = 100 + math.sin(plane_wave) * PLANE_FLOAT_RANGE
            
            if plane.x > WIDTH + 100:
                plane_active = False  # O aviao desaparece mais rapido quando sai da tela
                plane_timer = random.randint(200, 400)
            
            bullet_timer += 1
            if bullet_timer > BULLET_SHOOT_TIME:
                shoot_bullet()
                bullet_timer = 0
                BULLET_SHOOT_TIME = random.randint(80, 150)

        # movimento doos tiros
        for bullet in bullets[:]:
            bullet.y += BULLET_SPEED
            if bullet.y > HEIGHT:
                bullets.remove(bullet)
        
        # Gerenciamento dos cactus
        obstacles_timeout += 1
        if obstacles_timeout > OBSTACLE_SPAWN_TIME:
            spawn_obstacle()
            obstacles_timeout = 0
        
        for obstacle in obstacles[:]:
            obstacle.x -= OBSTACLE_SPEED
            if obstacle.x < -50:
                obstacles.remove(obstacle)
                score += 1
        
        # pulo do boneco
        if keyboard.up and runner.y == GROUND_Y and not is_jumping:
            velocity_y = JUMP_VELOCITY
            is_jumping = True
            runner.images = jump_images
        
        if is_jumping:
            runner.y += velocity_y
            velocity_y += GRAVITY
            if runner.y >= GROUND_Y:
                runner.y = GROUND_Y
                velocity_y = 0
                is_jumping = False
                runner.images = ['run0', 'run1', 'run2', 'run3', 'run4']
        
        # se nao tiver imune ele verifica a colisao
        if invincible_time == 0:
            if runner.collidelist(obstacles) != -1 or runner.collidelist(bullets) != -1:
                lives -= 1
                invincible_time = 40
                if lives <= 0:
                    game_over = True
        
        # Atualizando o tempo de imunidade
        if invincible_time > 0:
            invincible_time -= 1

        # verifica colisao com coracoes para ganhar vida
        for heart in ground_hearts[:]:
            if runner.collidepoint(heart.x, heart.y):
                ground_hearts.remove(heart)
                lives = min(lives + 1, 3)  # maximo de vida e 3

        # so vai ter coracao gerado se tiver 2 vidas ou menos, no caso, menor que tres
        if lives < 3:
            heart_spawn_time -= 1
            if heart_spawn_time <= 0:
                spawn_heart()
                heart_spawn_time = random.randint(200, 500)

# controle do cooldown do som para evitar spam no menu principal
last_sound_toggle_time = 0



def draw():
    
    screen.draw.filled_rect(Rect(0, 0, WIDTH, 400), (163, 232, 254))  # ceu
    screen.draw.filled_rect(Rect(0, 400, WIDTH, 200), (88, 242, 152))  # chao

    # Se o score atingir 18, o fundo fica preto
    if score >= SPEED_UP_THRESHOLD:
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (0, 0, 0))  # fundo preto

    if menu_active:
        
        jogar_text = "JOGAR"
        mudar_som_text = "Som ON/OFF"
        sair_text = "SAIR"
        screen.draw.text(jogar_text, center=(WIDTH // 2, HEIGHT // 2 - 60), color='Yellow', fontsize=60)
        screen.draw.text(mudar_som_text, center=(WIDTH // 2, HEIGHT // 2), color='blue', fontsize=60)
        screen.draw.text(sair_text, center=(WIDTH // 2, HEIGHT // 2 + 60), color='red', fontsize=60)

        # risco para destacar onde ta selecionado
        if selected_option == 0:
            screen.draw.rect(Rect((WIDTH // 2 - 80, HEIGHT // 2 - 40), (160, 2)), color="purple")
        elif selected_option == 1:
            screen.draw.rect(Rect((WIDTH // 2 - 80, HEIGHT // 2 + 20), (160, 2)), color="purple")
        elif selected_option == 2:
            screen.draw.rect(Rect((WIDTH // 2 - 80, HEIGHT // 2 + 78), (160, 2)), color="purple")
    else:
        # Jogo
        if game_over:
            screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2), color=(255, 0, 0), fontsize=80)
        else:
            runner.draw()
            plane.draw()
            for obstacle in obstacles:
                obstacle.draw()
            for bullet in bullets:
                bullet.draw()
            for heart in ground_hearts:
                heart.draw()
            
            # Vidas no canto direito
            for i in range(lives):
                heart_image.x = WIDTH - 50 - i * 50  # ajustar posicao
                heart_image.draw()

            # pontuacao
            screen.draw.text(f"Score: {score}", (10, 10), color="white", fontsize=40)


pgzrun.go()