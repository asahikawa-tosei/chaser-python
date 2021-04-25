import math
import random
import CHaser # 同じディレクトリに CHaser.py がある前提

# 定数を使ったプログラム例
UP = 1
DOWN = 7
LEFT = 3
RIGHT = 5
UPLEFT = 0
UPRIGHT = 2
DOWNLEFT = 6
DOWNRIGHT =8

BLANK = 0
ENEMY = 1
BLOCK = 2
ITEM = 3

WALK = 0
PUT = 1
LOOK = 2
SEARCH = 3

def main():
    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス
    # 変数
    direction = UP  # 方向   UP|DOWN|LEFT|RIGHT
    mode = WALK     # モード WALK|PUT|LOOK|SEARCH

    while True:
        # ゲット・レディ
        value = client.get_ready()

        # 分析
        if value[UP] == ENEMY :
            direction = UP
            mode = PUT
        elif value[LEFT] == ENEMY:
            direction = LEFT
            mode = PUT
        elif value[DOWN] == ENEMY:
            direction = DOWN
            mode = PUT
        elif value[DOWN] == ENEMY:
            direction = RIGHT
            mode = PUT
        elif value[UP] == ITEM:
            direction = UP
            mode = WALK
        elif value[LEFT] == ITEM:
            direction = LEFT
            mode = WALK
        elif value[DOWN] == ITEM:
            direction = DOWN
            mode = WALK
        elif value[RIGHT] == ITEM:
            direction = RIGHT
            mode = WALK
        elif value[UP] == BLANK :
            direction = UP
            mode = WALK
        elif value[LEFT] == BLANK:
            direction = LEFT
            mode = WALK
        elif value[DOWN] == BLANK:
            direction = DOWN
            mode = WALK
        elif value[RIGHT] == BLANK:
            direction = RIGHT
            mode = WALK
        else:
            direction = RIGHT
            mode = SEARCH

        # 行動
        if mode == WALK:
            if direction == UP:
                client.walk_up()
            elif direction == LEFT:
                client.walk_left()
            elif direction == DOWN:
                client.walk_down()
            else:
                client.walk_right()
        elif mode == PUT:
            if direction == UP:
                client.put_up()
            elif direction == LEFT:
                client.put_left()
            elif direction == DOWN:
                client.put_down()
            else:
                client.put_right()
        else:
            client.search_right()

        



if __name__ == "__main__":
    main()
