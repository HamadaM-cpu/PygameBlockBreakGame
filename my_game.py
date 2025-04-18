import pygame
import sys
import time
import random

# 初期化
pygame.init()

# 画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('カラフルブロック崩し')

# 色の定義
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

# フォント設定
font = pygame.font.Font(None, 36)

# パドルの設定
paddle_width = 120
paddle_height = 10
paddle_speed = 10
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height - 30, paddle_width, paddle_height)

# ボールの設定
ball_radius = 10
ball_speed_x = 5
ball_speed_y = -5
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)

# ブロックの設定
block_width = 60
block_height = 20
block_rows = 6
block_cols = 13

# ステージの初期設定
def create_blocks():
    blocks = []
    for row in range(block_rows):
        block_row = []
        for col in range(block_cols):
            block_x = col * (block_width + 10) + 35
            block_y = row * (block_height + 10) + 50
            block = pygame.Rect(block_x, block_y, block_width, block_height)
            # ランダムで色を決定
            block_color = random.choice([green, yellow, red, blue])
            block_row.append({"rect": block, "color": block_color})
        blocks.append(block_row)
    return blocks

blocks = create_blocks()

# スコア
score = 0
level = 1  # ステージ
game_won = False

# スタート画面の表示
def display_start_screen():
    screen.fill(black)
    start_text = font.render("Press Enter to Start", True, white)
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2))
    pygame.display.flip()

    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting_for_start = False

# カウントダウンの表示
def countdown():
    for i in range(3, 0, -1):
        screen.fill(black)
        countdown_text = font.render(f'Starting in {i}', True, white)
        screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

# ゲームループ
running = True
game_over = False

# スタート画面を表示
display_start_screen()

# カウントダウンを表示
countdown()

# ゲーム開始
while running:
    if game_over:
        if game_won:
            level += 1  # ステージを進める
            blocks = create_blocks()  # 新しいブロックを作成
            countdown()  # 次のステージに進むカウントダウン
        else:
            break  # ゲームオーバーで終了
    
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # パドルの操作
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.right += paddle_speed
    
    # ボールの移動
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    # 壁との衝突判定
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y
    if ball.bottom >= screen_height:
        game_over = True  # ボールが下に落ちたらゲームオーバー
        
    # パドルとの衝突判定
    if ball.colliderect(paddle):
        ball_speed_y = -ball_speed_y
        
    # ブロックとの衝突判定
    for row in blocks:
        for block in row:
            if ball.colliderect(block["rect"]):
                ball_speed_y = -ball_speed_y
                row.remove(block)  # ブロックを消す
                score += 100
                break

    # 画面の描画
    screen.fill(black)
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.ellipse(screen, white, ball)
    for row in blocks:
        for block in row:
            # ここでは色を変更せず、最初に決定された色を使用
            pygame.draw.rect(screen, block["color"], block["rect"])

    # スコアの表示
    score_text = font.render(f'Score: {score}', True, white)
    level_text = font.render(f'Level: {level}', True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (screen_width - level_text.get_width() - 10, 10))
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    
    # ブロックが全て消えたらゲームクリア
    if not any(blocks):
        score += 1000
        game_over = True
        game_won = True

pygame.quit()
