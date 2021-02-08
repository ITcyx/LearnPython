import pygame
import random
import traceback
import copy
import time


def get_food(rows, cols, snake_head, snake_body):
    # 生成食物

    while True:
        pos = (random.randint(0, cols - 1), random.randint(0, rows - 1))  # 随机生成食物
        
        if snake_head == pos:  # 判断是否生成在贪吃蛇头部
            continue
        for i in snake_body:  # 判断是否生成在贪吃蛇身体
            if i == pos:
                break
        if i == pos:
            continue
        else:
            break
    return pos


def draw_rect(pos, color, cell, window):
    # 绘制矩形

    cell = (20, 20)  # 设置矩形尺寸
    left = pos[0] * cell[0]  # 设置矩形左上角横坐标
    top = pos[1] * cell[1]  # 设置矩形左上角纵坐标
    pygame.draw.rect(window, color, (left, top, cell[0], cell[1]))  # 绘制矩形
    return


def final_display(window, background, score, score_img, score_rect, score_color, score_font, score_pos, game_time, game_time_img, game_time_rect, game_time_color, game_time_font, game_time_pos):
    # 展示最终画面（得分，游戏时长）
    
    window.blit(background, (0, 0))  # 显示游戏背景
    window.blit(score_img, score_rect)  # 显示游戏得分图标
    window.blit(game_time_img, game_time_rect)  # 显示游戏时长图标
    game_time_min = game_time // 60  # 计算游戏时长分钟数
    game_time_sec = game_time % 60  # 计算游戏时长秒数
    game_time_min_text = str(game_time_min)  # 将游戏时长分钟数转换成字符串
    if len(game_time_min_text) == 1:
        game_time_min_text = "0" + game_time_min_text  # 如果是单字符，前面加"0"
    game_time_sec_text = str(game_time_sec)  # 将游戏时长秒数转换成字符串
    if len(game_time_sec_text) == 1:
        game_time_sec_text = "0" + game_time_sec_text  # 如果是单字符，前面加"0"
    score_word = score_font.render(str(score), True, score_color)  # 设置score分数字体
    game_time_word = game_time_font.render(game_time_min_text + ":" + game_time_sec_text, True, game_time_color)  # 设置游戏时长分数字体
    window.blit(score_word, score_pos)  # 绘制分数文字
    window.blit(game_time_word, game_time_pos)  # 绘制游戏时长文字

    events = pygame.event.get()
    for event in events:
        pass  # 所有事件都不处理

    pygame.display.flip()  # 更新画面显示
    pygame.time.delay(3000)  # 程序延迟3000毫秒

    return


def help_display(window, background, wide, high, return_img, return_rect, help_color, help_font):
    clock = pygame.time.Clock()
    while True:
        window.blit(background, (0, 0))  # 显示游戏背景
        window.blit(return_img, return_rect)  # 显示返回图标
        help_text = "Hello! This is a Greedy Snake game."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 10))
        help_text = "When the game starts, you can use the keyboard to control the snake."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 70))
        help_text = "Use the 'w' or 'up' key to manipulate it to move up."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 130))
        help_text = "Use the 'a' or 'left' key to manipulate it to move left."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 190))
        help_text = "Use the 's' or 'down' key to manipulate it to move down."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 250))
        help_text = "Use the 'd' or 'right' key to manipulate it to move right."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 310))
        help_text = "Press 'space' key or click on the screen by left mouse button to pause the game."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 370))
        help_text = "Re-press 'space' key or re-click on the screen by left mouse button, to unpause the game."
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (10, 430))        
        help_text = "Designed by Andy"
        help_word = help_font.render(help_text, True, help_color)
        window.blit(help_word, (660, 480))
        events = pygame.event.get()
        for event in events:
            pass  # 所有事件都不处理
        if pygame.mouse.get_pressed()[0]:  # 如果用户按下鼠标左键
            pos = pygame.mouse.get_pos()  # 获取鼠标坐标
            if return_rect.left < pos[0] < return_rect.right and return_rect.top < pos[1] < return_rect.bottom:  # 用户点击返回图标
                break

        pygame.display.flip()  # 更新画面显示
        clock.tick(30)
    return


def game_start(window, background, wide, high, cell, eat_voice, dead_voice):
    # 游戏主逻辑函数

    # ---------- 地图尺寸 ----------
    cols = wide // cell[0]  # 设置列数
    rows = high // cell[1]  # 设置行数

    # ---------- 贪吃蛇初始化 ----------
    snake_head = (int(cols / 2), int(rows / 2))  # 贪吃蛇头部坐标
    snake_head_color = (0, 100, 0)  # 贪吃蛇头部颜色
    snake_body = [(snake_head[0] + 1, snake_head[1]), (snake_head[0] + 2, snake_head[1])]  # 贪吃蛇身体坐标
    snake_body_color = (144, 238, 144)  # 贪吃蛇身体颜色
    snake_direct = "left"  # 贪吃蛇移动方向 (left, right, up, down)

    # ---------- 食物初始化 ----------
    food_pos = get_food(rows, cols, snake_head, snake_body)
    food_color_cyan = (0, 255, 255)
    food_color_gold = (255, 215, 0)

    # ---------- 游戏基础数值初始化 ----------
    quit_flag = False  # 退出flag
    pause_flag = False  # 暂停flag 
    dead_flag = False  # 死亡flag
    pygame.mixer.music.play()  # 播放bgm
    clock = pygame.time.Clock()  # 创建游戏时钟对象
    fps = 5  # 设置游戏帧率
    fps_add_flag = False  # 设置帧率提高flag
    score = 0  # 设置游戏得分
    game_time = 0  # 设置游戏时长
    game_time_f = time.perf_counter()  # 设置游戏开始时间

    while not quit_flag:  # 判定quit_flag是否被置为false,若是进入后续的语句块进行循环
        
        # ---------- 外界输入事件处理 ----------
        events = pygame.event.get()  # 获取外界输入事件
        for event in events:  # 处理外界输入事件
            if event.type == pygame.QUIT:  # 处理退出事件
                pygame.mixer.music.stop()  # 停止播放bgm
                pygame.mixer.stop()  # 停止播放bgm
                quit_flag = True  # 将quit_flag置为True
            elif event.type == pygame.KEYDOWN:  # 处理按下键盘事件
                if event.key == pygame.K_SPACE:  # 判定是否为键盘space键
                    pause_flag = not pause_flag  # 暂停flag取反
                if not pause_flag:  # 判断是否暂停
                    if event.key == pygame.K_UP or event.key == pygame.K_w:  # 判定是否为键盘up键或者w键
                        if snake_direct == "left" or snake_direct == "right":
                            snake_direct = "up"  # 贪吃蛇移动方向改为向上
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:  # 判定是否为键盘down键或者s键
                        if snake_direct == "left" or snake_direct == "right":
                            snake_direct = "down"  # 贪吃蛇移动方向改为向下
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:  # 判定是否为键盘left键或者a键
                        if snake_direct == "up" or snake_direct == "down":
                            snake_direct = "left"  # 贪吃蛇移动方向改为向左
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # 判定是否为键盘right键或者d键
                        if snake_direct == "up" or snake_direct == "down":
                            snake_direct = "right"  # 贪吃蛇移动方向改为向右
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 处理按下鼠标事件
                if event.button == 1:  # 判断是否为鼠标左键
                    pause_flag = not pause_flag  # 暂停flag取反

        # ---------- 暂停事件处理 ----------
        if pause_flag:
            pygame.mixer.music.pause()  # 暂停播放bgm
            pygame.mixer.pause()  # 暂停所有声道播放
        else:
            pygame.mixer.music.unpause()  # 重新播放bgm
            pygame.mixer.unpause()  # 重新所有声道播放

        # ---------- 游戏主要事件处理 ----------
        if not pause_flag:

            if not pygame.mixer.music.get_busy():  # 判断bgm是否停止播放
                pygame.mixer.music.play()  # 播放bgm

            # ---------- 食物事件处理 ----------
            eat_flag = (snake_head == food_pos)  # 吃食物flag
            if eat_flag:
                eat_voice.play()  # 播放吃食物声音
                food_pos = get_food(rows, cols, snake_head, snake_body)  # 获取新的食物
                if score % 4 == 2:
                    score += 2
                    fps_add_flag = True
                else:
                    score += 1
            if not eat_flag:
                snake_body.pop()  # 删掉贪吃蛇身体最后一格

            # ---------- 贪吃蛇移动事件处理 ----------
            snake_body.insert(0, copy.deepcopy(snake_head))  # 贪吃蛇身体延伸到头部一格
            if snake_direct == "left":  # 向左移动
                snake_head = (snake_head[0] - 1, snake_head[1])  # 贪吃蛇头部向左移动一格
            elif snake_direct == "right":  # 向右移动
                snake_head = (snake_head[0] + 1, snake_head[1])  # 贪吃蛇头部向右移动一格
            elif snake_direct == "up":  # 向上移动
                snake_head = (snake_head[0], snake_head[1] - 1)  # 贪吃蛇头部向上移动一格
            else:  # 向下移动
                snake_head = (snake_head[0], snake_head[1] + 1)  # 贪吃蛇头部向下移动一格

            # ---------- 贪吃蛇死亡事件处理 ----------
            if snake_head[0] < 0 or snake_head[1] < 0 or snake_head[0] >= cols or snake_head[1] >= rows:  # 撞墙死亡
                dead_flag = True  # 将死亡flag置为True
            if snake_head in snake_body:  # 撞身体死亡
                dead_flag = True  # 将死亡flag置为True
            if dead_flag:
                dead_voice.play()  # 播放死亡音乐
                pygame.time.delay(int(dead_voice.get_length() * 1000))  # 等待死亡音乐播放完毕
                pygame.mixer.music.stop()  # 停止bgm播放
                pygame.mixer.stop()  # 停止所有声道播放
                quit_flag = True  # 将退出flag置为True

            # ---------- 游戏画面更新 ----------
            if not dead_flag:
                window.blit(background, (0, 0))  # 显示游戏背景
                for body in snake_body:  # 显示贪吃蛇身体
                    draw_rect(body, snake_body_color, cell, window)
                draw_rect(snake_head, snake_head_color, cell, window)  # 显示贪吃蛇头部
                if score % 4 == 2:
                    draw_rect(food_pos, food_color_gold, cell, window)  # 显示金色食物
                else:
                    draw_rect(food_pos, food_color_cyan, cell, window)  # 显示青色食物
                pygame.display.flip()  # 更新画面显示
            
            if fps_add_flag:
                fps += 5
                fps_add_flag = False
            clock.tick(fps)  # 设置帧率

    game_time = int(time.perf_counter() - game_time_f)
    return score, game_time


def main():

    pygame.init()  # pygame初始化

    # ---------- 窗口设置 ----------
    wide = 960  # 窗口的宽
    high = 540  # 窗口的高
    size = (wide, high)  # 窗口尺寸
    window = pygame.display.set_mode(size)  # 设置窗口尺寸
    pygame.display.set_caption("x Greedy Snake")  # 设置窗口标题
    icon = pygame.image.load("GreedySnake.ico")  # 加载窗口图标
    pygame.display.set_icon(icon)  # 设置窗口图标

    # ---------- 游戏图片设置 ----------
    background = pygame.image.load("background.jpg").convert()  # 设置背景图片
    start_img = pygame.image.load("start.png").convert()  # 加载开始图标
    start_img.set_colorkey((0, 0, 0))  # 将开始图标黑色透明化
    start_rect = start_img.get_rect()  # 将开始图标转换为矩形
    start_rect.left = (wide - start_rect.width) // 2  # 设置开始图标左上角横坐标
    start_rect.top = 300  # 设置开始图标左上角纵坐标
    quit_img = pygame.image.load("quit.png").convert()  # 加载退出图标
    quit_img.set_colorkey((0, 0, 0))  # 将退出图标黑色透明化
    quit_rect = quit_img.get_rect()  # 将退出图标转换为矩形
    quit_rect.left = (wide - quit_rect.width) // 2  # 设置退出图标左上角横坐标
    quit_rect.top = 420  # 设置退出图标左上角纵坐标
    help_img = pygame.image.load("help.png").convert()  # 加载帮助图标
    help_img.set_colorkey((0, 0, 0))  # 将帮助图标黑色透明化
    help_rect = help_img.get_rect()  # 将帮助图标转换为矩形
    help_rect.left = 80  # 设置帮助图标左上角横坐标
    help_rect.top = 420  # 设置帮助图标左上角纵坐标
    return_img = pygame.image.load("return.png").convert()  # 加载返回图标
    return_img.set_colorkey((0, 0, 0))  # 将返回图标黑色透明化
    return_rect = return_img.get_rect()  # 将返回图标转换为矩形
    return_rect.left = 860  # 设置返回图标左上角横坐标
    return_rect.top = 20  # 设置返回图标左上角纵坐标
    score_img = pygame.image.load("score.png").convert()  # 加载得分图标
    score_img.set_colorkey((0, 0, 0))  # 将得分图标黑色透明化
    score_rect = score_img.get_rect()  # 将得分图标转换为矩形
    score_rect.left = wide // 2 - score_rect.width  # 设置得分图标左上角横坐标
    score_rect.top = 100  # 设置得分图标左上角纵坐标
    game_time_img = pygame.image.load("time.png").convert()  # 加载游戏时长图标
    game_time_img.set_colorkey((0, 0, 0))  # 将游戏时长图标黑色透明化
    game_time_rect = game_time_img.get_rect()  # 将游戏时长图标转换为矩形
    game_time_rect.left = wide // 2 - game_time_rect.width  # 设置游戏时长图标左上角横坐标
    game_time_rect.top = 340  # 设置游戏时长图标左上角纵坐标

    # ---------- 游戏字体设置 ----------
    title_color = (128, 255, 128)  # 设置标题rgb颜色
    title_font = pygame.font.Font("font.ttf", 64)  # 设置标题字体
    title = title_font.render("x Greedy Snake", True, title_color)  # 设置标题
    help_color = (128, 255, 128)  # 设置帮助rgb颜色
    help_font = pygame.font.Font("font.ttf", 32)  # 设置帮助字体
    score_color = (128, 255, 128)  # 设置游戏得分rgb颜色
    score_font = pygame.font.Font("font.ttf", 128)  # 设置游戏得分字体
    game_time_color = (128, 255, 128)  # 设置游戏时长
    game_time_font = pygame.font.Font("font.ttf", 128)  # 设置游戏时长字体

    # ---------- 游戏音效设置 ----------
    pygame.mixer.music.load("bgm.mp3")  # 加载bgm音效
    pygame.mixer.music.set_volume(0.2)  # 设置bgm播放音量
    eat_voice = pygame.mixer.Sound("eat.mp3")  # 加载吃食物音效
    eat_voice.set_volume(0.8)  # 设置吃食物音效音量
    dead_voice = pygame.mixer.Sound("dead.mp3")  # 加载死亡音效
    dead_voice.set_volume(0.8)  # 设置死亡音效音量

    clock = pygame.time.Clock()  # 创建游戏时钟对象

    quit_flag = False  # 退出逻辑判定flag
    while not quit_flag:
        events = pygame.event.get()  # 获取用户事件
        for event in events:  # 获取退出事件
            if event.type == pygame.QUIT:
                quit_flag = True

        # ---------- 游戏入口界面显示 ----------
        window.blit(background, (0, 0))  # 显示游戏背景
        window.blit(title, (308, 32))  # 显示游戏标题
        window.blit(start_img, start_rect)  # 显示游戏开始图标
        window.blit(quit_img, quit_rect)  # 显示游戏退出图标
        window.blit(help_img, help_rect)  # 显示游戏帮助图标

        # ---------- 检测用户鼠标操作 ----------
        if pygame.mouse.get_pressed()[0]:  # 如果用户按下鼠标左键
            pos = pygame.mouse.get_pos()  # 获取鼠标坐标
            if start_rect.left < pos[0] < start_rect.right and start_rect.top < pos[1] < start_rect.bottom:  # 用户点击开始图标
                score, game_time = game_start(window, background, wide, high, (20, 20), eat_voice, dead_voice)  # 开始运行游戏主逻辑函数
                final_display(window, background, score, score_img, score_rect, score_color, score_font, (wide // 2 , 80),game_time, game_time_img, game_time_rect, game_time_color, game_time_font, (wide // 2 , 320))  # 展示最终画面（得分，游戏时长）
            elif quit_rect.left < pos[0] < quit_rect.right and quit_rect.top < pos[1] < quit_rect.bottom:  # 用户点击退出图标
                quit_flag = True
                pygame.quit()  # 退出游戏函数
            elif help_rect.left < pos[0] < help_rect.right and help_rect.top < pos[1] < help_rect.bottom:  # 用户点击帮助图标
                help_display(window, background, wide, high, return_img, return_rect, help_color, help_font)  # 开始帮助显示函数

        # ---------- 画面显示 ----------
        if not quit_flag:
            pygame.display.flip()  # 更新画面显示
            clock.tick(30)  # 设置帧率
    
    return


if __name__ == "__main__":
    main()