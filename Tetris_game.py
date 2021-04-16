import tkinter as tk
import tkinter.messagebox
import numpy as np
import time

window = tk.Tk()
window.geometry('211x475+500+50')  # 12x20 grids, each 20x20
window.title('Tetris')

score = tk.IntVar()
label_title = tk.Label(window, text='score',font='bold')
label_title.pack(side='top')
label = tk.Label(window, height=1, width=10, textvar=score,borderwidth=2, relief='raised')
label.pack(side='top')

canvas = tk.Canvas(window, height=420, width=211)
canvas.pack()

def draw_cell_by_cr(r, c, color="#c3c3c3"):
    canvas.create_rectangle(1+21*(c-1), 1+21*(r-1), 21*c, 21*r, fill=color, outline='white')

# draw grey grids on canvas
for i in range(1,11):
    for j in range(1,21):
        draw_cell_by_cr(j,i)

"""
Define different kinds of tetris (8 types in total, each with different colors)
- each are assigned a number form 0 to 7, which is useful later for indication
"""
def draw_O(r,c,color='#0fc849'):
    if c+1 <= 10:
        draw_cell_by_cr(r,c,color)
        draw_cell_by_cr(r+1,c,color)
        draw_cell_by_cr(r,c+1,color)
        draw_cell_by_cr(r + 1, c + 1,color)
        rec = [(r,c),(r+1,c),(r,c+1),(r+1,c+1)]
        return 0,rec,r,c
    else:
        c -= 1
        draw_O(r,c)
        rec = [(r, c), (r + 1, c), (r, c + 1), (r + 1, c + 1)]
        return 0, rec, r, c

def draw_Z(r,c,color='yellow'):
    if c-1 >= 1 and c+1 <= 10:
        draw_cell_by_cr(r,c,color)
        draw_cell_by_cr(r+1, c, color)
        draw_cell_by_cr(r+1, c-1, color)
        draw_cell_by_cr(r, c+1, color)
        flash = [(r,c),(r+1,c),(r+1,c-1),(r,c+1)]
        return 1,flash,r,c
    else:
        if c >= 10:
            c -= 1
        else:  # c <= 1
            c += 1
        draw_Z(r, c)
        flash = [(r,c),(r+1,c),(r+1,c-1),(r,c+1)]
        return 1, flash, r, c

def draw_4I(r,c, color='purple'):
    if c-2>=1 and c+1<=10:
        draw_cell_by_cr(r, c, color)
        draw_cell_by_cr(r, c-1, color)
        draw_cell_by_cr(r, c+1, color)
        draw_cell_by_cr(r, c-2, color)
        four = [(r,c),(r,c-1),(r,c+1),(r,c-2)]
        return 2,four,r,c
    else:
        if c == 2:
            c += 1
        elif c == 1:
            c += 2
        else:  # c == 10
            c -= 1
        draw_4I(r, c)
        four = [(r,c),(r,c-1),(r,c+1),(r,c-2)]
        return 2, four, r, c

def draw_3I(r,c, color='blue'):
    if c-1>=1 and c+1 <= 10:
        draw_cell_by_cr(r, c, color)
        draw_cell_by_cr(r, c-1, color)
        draw_cell_by_cr(r, c+1, color)
        three = [(r,c), (r,c-1),(r, c+1)]
        return 3,three,r,c
    else:
        if c >= 10:
            c -= 1
        else:  # c <= 1
            c += 1
        draw_3I(r, c)
        three = [(r,c), (r,c-1),(r, c+1)]
        return 3, three, r, c

def draw_L(r,c, color='red'):
    if c+1<=10 and c-1>=1:
        draw_cell_by_cr(r, c, color)
        draw_cell_by_cr(r, c-1, color)
        draw_cell_by_cr(r, c+1, color)
        draw_cell_by_cr(r+1, c+1, color)
        L = [(r, c),(r, c-1),(r, c+1),(r+1, c+1)]
        return 4,L,r,c
    else:
        if c >= 10:
            c -= 1
        else:  # c <= 1
            c += 1
        draw_L(r, c)
        L = [(r, c),(r, c-1),(r, c+1),(r+1, c+1)]
        return 4, L, r, c

def draw_T(r,c, color='orange'):
    if c+1 <= 10 and c-1 >= 1:
        draw_cell_by_cr(r, c, color)
        draw_cell_by_cr(r+1, c, color)
        draw_cell_by_cr(r, c+1, color)
        draw_cell_by_cr(r, c-1, color)
        T = [(r, c),(r+1, c),(r, c+1),(r, c-1)]
        return 5,T,r,c
    else:
        if c >= 10:
            c -= 1
        else:  # c <= 1
            c += 1
        draw_T(r,c)
        T = [(r, c),(r+1, c),(r+1, c+1),(r+1, c-1)]
        return 5,T,r,c

def draw_reverse_L(r,c,color='#00a3ec'):
    if c+1<=10 and c-1>=1:
        draw_cell_by_cr(r, c, color)
        draw_cell_by_cr(r, c-1, color)
        draw_cell_by_cr(r, c+1, color)
        draw_cell_by_cr(r+1, c-1, color)
        L = [(r, c),(r, c-1),(r, c+1),(r+1, c-1)]
        return 6,L,r,c
    else:
        if c >= 10:
            c -= 1
        else:  # c <= 1
            c += 1
        draw_L(r, c)
        L = [(r, c),(r, c-1),(r, c+1),(r+1, c-1)]
        return 6, L, r, c

def draw_reverse_Z(r,c,color='#ff76a2'):
    if c-1 >= 1 and c+1 <= 10:
        draw_cell_by_cr(r,c,color)
        draw_cell_by_cr(r+1, c, color)
        draw_cell_by_cr(r, c-1, color)
        draw_cell_by_cr(r+1, c+1, color)
        flash = [(r,c),(r+1,c),(r,c-1),(r+1,c+1)]
        return 7,flash,r,c
    else:
        if c >= 10:
            c -= 1
        else:  # c <= 1
            c += 1
        draw_Z(r, c)
        flash = [(r,c),(r+1,c),(r,c-1),(r+1,c+1)]
        return 7, flash, r, c

# call corresponding function after indicating the corresponding tetris' types
def corresponding_function(r,c,color,type):
    if type == 0:
        a,b,c,d = draw_O(r, c, color)
    elif type == 1:
        a,b,c,d = draw_Z(r, c, color)
    elif type == 2:
        a,b,c,d = draw_4I(r, c, color)
    elif type == 3:
        a,b,c,d = draw_3I(r, c, color)
    elif type == 4:
        a,b,c,d = draw_L(r, c, color)
    elif type == 5:
        a,b,c,d = draw_T(r, c, color)
    elif type == 6:
        a,b,c,d = draw_reverse_L(r,c,color)
    else:
        a,b,c,d = draw_reverse_Z(r,c,color)
    return a,b,c,d

# initializing tetris (later we will input a random number r_num to call this function)
def random_create(r_num, beginning_col):
    block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
    a,b,r,c = corresponding_function(0, beginning_col, block_color[r_num], r_num)
    return a,b,r,c

# moving down blocks
def move_down():
    global type, block_list, status_board,c, r
    block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
    # cover the original tetris with gray cloth to make it disappear
    if if_next_step_land(block_list, status_board):
        for old_pairs in block_list:
            draw_cell_by_cr(old_pairs[0],old_pairs[1],'#c3c3c3')
        i = 0
        for pair in block_list:
            block_list[i] = (pair[0]+1, pair[1])  # update block_list
            draw_cell_by_cr(block_list[i][0], block_list[i][1],block_color[type])  # show the new image
            i += 1
        r += 1

def move_left(event):
    global type, block_list, status_board, c, skip
    block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
    check_left = []
    if if_next_step_land(block_list, status_board) or skip:  # make sure that we can go to the next place
        for pair in block_list:
            if (pair[0], pair[1] - 1) not in block_list:
                check_left.append(status_board[pair[0], pair[1] - 1])
        if set(check_left) == {999}:  # left side is empty
            c -= 1
            for old_pairs in block_list:
                draw_cell_by_cr(old_pairs[0], old_pairs[1], '#c3c3c3')  # cover the original image
            i = 0
            for pair in block_list:
                block_list[i] = (pair[0], pair[1]-1)  # update block_list
                draw_cell_by_cr(block_list[i][0], block_list[i][1], block_color[type])  # draw the new image
                i += 1
        else:
            pass  # don't make a respond if the tetris has landed
    else:
        pass

def move_right(event):
    global type, block_list, status_board, c, skip
    block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
    check_right = []
    if if_next_step_land(block_list, status_board) or skip:
        for pair in block_list:
            if (pair[0], pair[1] + 1) not in block_list:
                check_right.append(status_board[pair[0], pair[1] + 1])
        if set(check_right) == {999}:
            c += 1
            for old_pairs in block_list:
                draw_cell_by_cr(old_pairs[0], old_pairs[1], '#c3c3c3')  # cover the original one
            i = 0
            for pair in block_list:
                block_list[i] = (pair[0], pair[1] + 1)  # update block_list
                draw_cell_by_cr(block_list[i][0], block_list[i][1], block_color[type])  # draw the new image
                i += 1
        else:
            pass
    else:
        pass

"""
Rotating blocks clock-wise
- create an empty_board to simulate the general rotation first and then come back to
  status_board to make real change base on the actual condition
"""
def rotate(event):  # rotation of tetris
    global type, block_list, status_board, r, c
    block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
    empty_board = np.zeros((23, 13))  # larger than status_board to make sure that index later will not be out of range
    empty_board[:,:] = 999
    after_list = []
    check_list = []
    for item in block_list:
        empty_board[item[0],item[1]] = type  # record current condition before rotation
    copy_board = empty_board.copy()
    if type == 0:  # rec
        pass
    elif type == 2:  # 4line
        if r <= 19 and c <= 9:
            empty_board[r, c-1] = copy_board[r-1, c]
            empty_board[r, c-2] = copy_board[r-2, c]
            empty_board[r+1, c] = copy_board[r, c-1]
            empty_board[r+2, c] = copy_board[r, c-2]
            empty_board[r-1, c] = copy_board[r, c+1]
            empty_board[r-2, c] = copy_board[r, c+2]
            empty_board[r, c+1] = copy_board[r+1, c]
            empty_board[r, c+2] = copy_board[r+2, c]
            for s_row in range(r-2, r+3):
                for s_col in range(c-2, c+3):
                    if empty_board[s_row,s_col] != 999:
                        check_list.append(status_board[s_row, s_col])
                        after_list.append((s_row,s_col))
            if set(check_list) == {999}:     # 准备旋转去的位置是空的
                for item in block_list:
                    draw_cell_by_cr(item[0], item[1],'#c3c3c3')          # 清空原来
                block_list = after_list    # 更新block_list到旋转后
                for item in block_list:
                    draw_cell_by_cr(item[0], item[1],block_color[type])  # 画出后来
            else:
                pass
        else:
            pass
    else:  # blocks other than rec and 4line
        empty_board[r-1,c] = copy_board[r,c-1]
        empty_board[r, c+1] = copy_board[r-1, c]
        empty_board[r+1, c] = copy_board[r, c+1]
        empty_board[r, c-1] = copy_board[r+1, c]
        empty_board[r-1, c+1] = copy_board[r-1, c-1]
        empty_board[r+1, c+1] = copy_board[r-1, c+1]
        empty_board[r+1, c-1] = copy_board[r+1, c+1]
        empty_board[r-1, c-1] = copy_board[r+1, c-1]
        for s_row in range(r-1, r+2):
            for s_col in range(c-1, c+2):
                if empty_board[s_row,s_col] != 999:
                    check_list.append(status_board[s_row, s_col])
                    after_list.append((s_row,s_col))
        if set(check_list) == {999}:     # 准备旋转去的位置是空的
            for item in block_list:
                draw_cell_by_cr(item[0], item[1],'#c3c3c3')          # 清空原来
            block_list = after_list    # 更新block_list到旋转后
            for item in block_list:
                draw_cell_by_cr(item[0], item[1],block_color[type])  # 画出后来
        else:
            pass

def to_the_bottom(event):  # when player hit certain button, go to the button directly
    global block_list, status_board, type, skip
    block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
    skip = False
    for pair in block_list:
        draw_cell_by_cr(pair[0], pair[1], '#c3c3c3')
    dis_list = []
    for pair in block_list:
        for r in range(1,22):
            row, col = pair
            if status_board[r, col] != 999 and (r-1 >= row):
                dis_list.append(r-1 - row)
    row_diff = min(dis_list)
    for i in range(len(block_list)):
        block_list[i] = (block_list[i][0]+row_diff, block_list[i][1])  # update block_list
    for pair in block_list:
        draw_cell_by_cr(pair[0], pair[1], block_color[type])           # show the new picture

def acceleration(event):  # accelerate tetris to make them drop faster
    move_down()


# Use array to simulate the game interface
# every movement of the blocks is recorded in "status_board", it is used to check the condition of any position with it
# the way to visualize things is draw_cell_by_cr, we can easily draw the picture with status_board
status_board = np.zeros((22, 12))
status_board[:,:] = 999  # 999 means unoccupied
status_board[21,:] = 1   # 1 does not mean the flash tetris, just to indicate the bottom of the game interface
status_board[2:,0] = 1   # left side of the game interface, blocks are stopped
status_board[2:,11] = 1  # right side, blocks are stopped

def save_status(block_list, status_board,type):
    for coordinate in block_list:
        status_board[coordinate[0],coordinate[1]] = type  # 999 means empty, 1~7 shows corresponding tetris

"""
Check whether the next step is ok to go to
- Check all the blocks in the next step to see if they are all empty
- used when the tetris is about to move down, move right or move left
"""
def if_next_step_land(block_list, status_board):
    checklist = []
    for pair in block_list:
        checklist.append(status_board[pair[0]+1, pair[1]])
    if set(checklist) == {999}:  # blocks in the next steps are all empty, good to step forward
        return True
    else:                        # can't move another step
        return False

"""
Increase score and remove blocks when the player clear lines
- 10 points for clearing one line; 30 for two; 60 for three; 100 for four
"""
def score_and_clear(status_board):
    count = 0
    rownumber = []
    for i in range(1, 21):
        if 999 not in status_board[i]:
            count += 1
            rownumber.append(i)
    if count == 1:
        score.set(score.get() + 10)
    elif count == 2:
        score.set(score.get() + 30)
    elif count == 3:
        score.set(score.get() + 60)
    elif count == 4:
        score.set(score.get() + 100)
    # cancellation
    if len(rownumber) > 0:
        for i in rownumber:
            status_board[i, 1:11] = 777  # 777 here is just a notation that I use to show that this line has gone
            for j in range(1, 11):
                draw_cell_by_cr(i, j, '#c3c3c3')
        # move (mostly) everything downward
        empty_count = 1
        for row in range(max(rownumber) - 1, 0, -1):
            if set(status_board[row, 1:11]) != {777}:
                status_board[row + empty_count, 1:11] = status_board[row, 1:11]
            else:
                empty_count += 1
                row += 1
        status_board[1:len(rownumber) + 1, 1:11] = status_board[0, 1:11]  # update status_board
        global FPS
        time.sleep(FPS*10**(-3)/2)  # wait a few milliseconds to show the change
        # draw the new image
        block_color = {0: '#0fc849', 1: 'yellow', 2: 'purple', 3: 'blue', 4: 'red', 5: 'orange', 6: '#00a3ec', 7: '#ff76a2'}
        for row in range(max(rownumber), 2 + len(rownumber), -1):
            for col in range(1, 11):
                if status_board[row, col] != 999:
                    draw_cell_by_cr(row, col, block_color[status_board[row, col]])
                else:
                    draw_cell_by_cr(row, col, '#c3c3c3')


if __name__ == "__main__":
    run = True
    block_list = []
    FPS = 300  # milliseconds
    acce = False
    skip = True
    def game_loop():
        global run,r, type, c, block_list, status_board, acce, FPS, skip
        if run == True:  # to determine if we need to drop down a new tetris at the top
            r_num = np.random.randint(0,8)  # random from 0 to 7 (8 kinds of tetris)
            beginning_col = 6
            type, block_list, r, c = random_create(r_num, beginning_col)  # r = 1
            run = False
            skip = True
        else:
            pass

        if if_next_step_land(block_list, status_board):     # execute only if the blocks have not landed
            window.update()
            move_down()          # moving downward automatically
            FPS = 300
            window.after(FPS, game_loop)
        else:
            save_status(block_list, status_board,type)  # update status_board
            score_and_clear(status_board)               # update status_board again
            # print(status_board)                       # use this for debugging
            if set(status_board[1]) == {999}:           # game-over check: check if there is any block in the first row
                run = True
                game_loop()
            else:
                run = False
                tkinter.messagebox.showinfo(message='Game over, your score is '+ str(score.get()))

    # buttons on the keyboard
    window.focus_set()
    window.bind('<KeyPress-Up>', rotate)
    window.bind('<KeyPress-Left>', move_left)
    window.bind('<KeyPress-Right>', move_right)
    window.bind('<KeyPress-Down>', acceleration)
    window.bind('<space>', to_the_bottom)


    game_loop()
    window.mainloop()
