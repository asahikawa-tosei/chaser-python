import math
import random
import CHaser # 同じディレクトリに CHaser.py がある前提

# 定数
UP = 1
DOWN = 7
LEFT = 3
RIGHT = 5
UPLEFT = 0
UPRIGHT = 2
DOWNLEFT = 6
DOWNRIGHT =8

# アイテム
BLANK = 0
ENEMY = 1
BLOCK = 2
ITEM = 3

# アクション
WALK = 0
PUT = 1
LOOK = 2
SEARCH = 3

# ポート
COOL = 2009
HOT = 2010

# rotation: 回転方向
COUNTER_CLOCKWISE = 0   # 反時計回り
CLOCKWISE = 1           # 時計回り


# モード
SAFE = 0        # 安全
ITEMS = 20      # 周囲にアイテムがある場合。
WAIT = 70       # 待ったほうが良い
WARN = 80       # 斜めに敵がいる
EMERGENCY = 90  # 周囲に敵がいる場合
RANDOM = 100    # ７回に１回はランダムに動く

# 大まかな進む方角 course
#          NORTH
#            ^
#            |
# WEST <= course => EAST
#            |
#            v
#          SOUTH
NORTH = 0   # NORTH:ブロック（壁）にぶつかるまで、上に移動する。
WEST  = 1   # WEST:ブロック（壁）にぶつかるまで、左に移動する。
SOUTH = 2   # SOUTH:ブロック（壁）にぶつかるまで、下に移動する。
EAST  = 3   # EAST:ブロック（壁）にぶつかるまで、右に移動する。


def main():
    # インスタンス生成
    client = CHaser.Client() # サーバーと通信するためのインスタンス

    # 変数の宣言
    value = [] # フィールド情報を保存するリスト
    counter_all = 0 # 全体のカウンタ
    
    # 変数のデフォルト設定
    mode        = SAFE
    course      = SOUTH     # 大まかな進む方向
    direction   = UP        # 方向 UP|DOWN|LEFT|RIGHT
    action      = WALK      # 行動 WALK|PUT|LOOK|SEARCH
    rotation    = COUNTER_CLOCKWISE     # デフォルトでCOOLと想定。反時計回り
    if int(client.port) != COOL:        # HOTの場合、最初は、時計回りとする
        rotation = CLOCKWISE


    # メインループ
    while True:
        # ゲット・レディ
        value = client.get_ready()

        # モードの確認
        if (value[UP] == ENEMY) or (value[LEFT] == ENEMY) or (value[DOWN] == ENEMY) or (value[RIGHT] == ENEMY):
            mode = EMERGENCY
        elif (value[UP] == ITEM) or (value[LEFT] == ITEM) or (value[DOWN] == ITEM) or (value[RIGHT] == ITEM):
            mode = ITEMS
        elif counter_all % 7 == 0:
            mode = RANDOM
        else:
            mode = SAFE

        # モード毎での分析
        if mode == EMERGENCY:
            '''敵がいる場合の下準備'''
            if value[UP] == ENEMY :
                direction = UP
                action = PUT
            elif value[LEFT] == ENEMY:
                direction = LEFT
                action = PUT
            elif value[DOWN] == ENEMY:
                direction = DOWN
                action = PUT
            elif value[RIGHT] == ENEMY:
                direction = RIGHT
                action = PUT
        elif mode == ITEMS:
            '''アイテムがある場合の下準備'''
            if value[UP] == ITEM:
                direction = UP
                action = WALK
            elif value[LEFT] == ITEM:
                direction = LEFT
                action = WALK
            elif value[DOWN] == ITEM:
                direction = DOWN
                action = WALK
            elif value[RIGHT] == ITEM:
                direction = RIGHT
                action = WALK
        elif mode == RANDOM:
            '''７回に１回はランダムに動く'''
            d = random.choice((UP,LEFT,DOWN,RIGHT))
            if (d == UP) and (value[UP] != BLOCK) and (value[UP] != ENEMY):
                direction = UP
                action = WALK
            elif (d == LEFT) and (value[LEFT] != BLOCK) and (value[LEFT] != ENEMY):
                direction = LEFT
                action = WALK
            elif (d == DOWN) and (value[DOWN] != BLOCK) and (value[DOWN] != ENEMY):
                direction = DOWN
                action = WALK
            elif (d == RIGHT) and (value[RIGHT] != BLOCK) and (value[RIGHT] != ENEMY):
                direction = RIGHT
                action = WALK
            else:
                direction = d
                action = SEARCH
        else:   # (mode == SAFE)
            '''安全性な場合、方向性を確認し、そちらに進む（下準備）'''   
            if rotation == COUNTER_CLOCKWISE:
                '''回転方向がCOUNTER_CLOCKWISEの場合、反時計回りに回る傾向とする'''
                if course == SOUTH:
                    '''南方角: ブロック（壁）にぶつかるまで、下に移動する。'''
                    if value[DOWN] != BLOCK:
                        action = WALK
                        direction = DOWN
                        course = SOUTH
                    else:
                        action = LOOK
                        direction = RIGHT
                        course = EAST
                elif course == EAST:
                    ''''東方角: ブロック（壁）にぶつかるまで、右に移動する。'''
                    if value[RIGHT] != BLOCK:
                        action = WALK
                        direction = RIGHT
                        course = EAST
                    else:
                        action = LOOK
                        direction = UP
                        course = NORTH
                elif course == NORTH:
                    ''''北方角: ブロック（壁）にぶつかるまで、上に移動する。'''
                    if value[UP] != BLOCK:
                        action = WALK
                        direction = UP
                        course = NORTH
                    else:
                        action = LOOK
                        direction = LEFT
                        course = WEST
                elif course == WEST:
                    ''''西方角: ブロック（壁）にぶつかるまで、左に移動する。'''
                    if value[LEFT] != BLOCK:
                        action = WALK
                        direction = LEFT
                        course = WEST
                    else:
                        action = LOOK
                        direction = DOWN
                        course = SOUTH
                else:
                    ''''その他の場合: '''
                    action = LOOK
                    direction = RIGHT
            else:
                '''rotationがCLOCKWISEの場合、時計回りに回る傾向とする'''
                if course == SOUTH:
                    '''南方角: ブロック（壁）にぶつかるまで、下に移動する。'''
                    if value[DOWN] != BLOCK:
                        action = WALK
                        direction = DOWN
                        course = SOUTH
                    else:
                        action = LOOK
                        direction = LEFT
                        course = WEST
                elif course == EAST:
                    ''''東方角: ブロック（壁）にぶつかるまで、右に移動する。'''
                    if value[RIGHT] != BLOCK:
                        action = WALK
                        direction = RIGHT
                        course = EAST
                    else:
                        action = LOOK
                        direction = DOWN
                        course = SOUTH
                elif course == NORTH:
                    ''''北方角: ブロック（壁）にぶつかるまで、上に移動する。'''
                    if value[UP] != BLOCK:
                        action = WALK
                        direction = UP
                        course = NORTH
                    else:
                        action = LOOK
                        direction = RIGHT
                        course = EAST
                elif course == WEST:
                    ''''西方角: ブロック（壁）にぶつかるまで、左に移動する。'''
                    if value[LEFT] != BLOCK:
                        action = WALK
                        direction = LEFT
                        course = WEST
                    else:
                        action = LOOK
                        direction = UP
                        course = NORTH
                else:
                    ''''その他の場合: '''
                    action = LOOK
                    direction = LEFT


        # 行動
        if action == WALK:
            if direction == UP:
                client.walk_up()
            elif direction == LEFT:
                client.walk_left()
            elif direction == DOWN:
                client.walk_down()
            else:
                client.walk_right()
        elif action == PUT:
            if direction == UP:
                client.put_up()
            elif direction == LEFT:
                client.put_left()
            elif direction == DOWN:
                client.put_down()
            else:
                client.put_right()
        elif action == LOOK:
            if direction == UP:
                client.look_up()
            elif direction == LEFT:
                client.look_left()
            elif direction == DOWN:
                client.look_down()
            else:
                client.look_right()
        else:
            client.search_right()

        # 全体のカウンタをインクリメントする
        counter_all += 1
        if counter_all % 40 == 0:   # 40ターン経過後（後半、回転方向を入れ替える）
            if rotation == COUNTER_CLOCKWISE:
                rotation = CLOCKWISE
            else:
                rotation = COUNTER_CLOCKWISE 


"""
python sample.py のようにこのファイルを直接実行すると，
__name__ は "__main__" となる．これを利用して main() を実行する．
"""
if __name__ == "__main__":
    main()
