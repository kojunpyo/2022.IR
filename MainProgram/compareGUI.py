"""
실행하면 나오는 창은 각각 '낮은 틱레이트', '높은 틱레이트', '낮은 틱레이트에 예측 적용'입니다.
"""

# 라이브러리 불러오기
import math
import tkinter as tk
import time

'''
공통 함수 선언
'''

# 현재 시간 저장
start = time.time()

# 키 입력 반응 함수 (오브젝트 움직임, 오차에 따라 예측값 갱신)
def key_down(event) :
    global start, compare, plus

    # 프레임마다 예측값만큼 오브젝트가 움직이도록 함
    compare[1] = [origin_dot[0] + (loop_num+1)*plus*math.cos(math.radians(angle)), origin_dot[1] + (loop_num+1)*plus*math.sin(math.radians(angle))]

    # 서버 처리 시점과 맞추기 위해 조건 설정
    if time.time() > start + 0.1 :

        # 실제값과 예측값 순서쌍 비교 (두 번째 창과 세 번째 창)
        print(compare)

        # 대소관계에 맞춰 예측값 갱신
        if compare[0][0] > compare [1][0] :
            plus *= 0.95
        elif compare[0][0] < compare [1][0] :
            plus *= 1.05
        start = time.time()

    # 세 번째 창을 프레임마다 갱신 (서버값은 아님)
    sketchbook3.delete('all')
    sketchbook3.create_oval(compare[1][0], compare[1][1], compare[1][0]+30, compare[1][1]+30, fill = "white" )

    # 서버값 갱신
    origin_dot[0] = origin_dot[0] + r*math.cos(math.radians(angle))
    origin_dot[1] = origin_dot[1] + r*math.sin(math.radians(angle))

# 클릭 반응 함수 (방향 재설정)
def click(event) :
    global angle
    rad = math.atan2(origin_dot[1]-event.y, origin_dot[0]-event.x)
    PI = math.pi
    angle = 180 + rad*180/PI

'''
무한 반복 함수 선언
'''

# 무한 반복 함수 (첫 번째 창)
def main_proc1():
    sketchbook1.delete('all')
    sketchbook1.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
    client1.after(100, main_proc1) # 100밀리초(0.1초)마다 함수 다시 호출 -> 틱레이트 10

# 두 번째 창의 갱신 반복 횟수 저장 (목적은 line 47에서 확인)
loop_num = 0

# 예측값 (프레임마다 더할 값)
plus = 20.0

# 예측 좌표값과 실제 좌표값 비교를 위한 순서쌍 선언
compare = [[0, 0], [0, 0]]

# 무한 반복 함수 (두 번째 창과 세 번째 창)
def main_proc2and3():
    global loop_num, compare

    sketchbook2.delete('all')
    sketchbook2.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
    
    compare[0][0], compare[0][1] = origin_dot[0], origin_dot[1]

    if loop_num % 5 == 0 : # 두 번째 창이 5번 갱신될 때마다 세 번째 창을 갱신함. -> 0.1초마다 호출(틱레이트 10)
        sketchbook3.delete('all')
        sketchbook3.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
        loop_num = 0

    loop_num += 1 # 갱신 반복 횟수에 1 추가
    client2.after(20, main_proc2and3) # 20밀리초(0.02초)마다 함수 다시 호출 -> 틱레이트 50

'''
첫 번째 창 (보정 안 된 느린 창) -> 낮은 틱레이트를 가지며 보정이 안 된 케이스로서 가져옴
'''

# 첫 번째 창 세팅
client1 = tk.Tk() # client1 GUI 생성
client1.title("틱레이트: 10") # 창 이름 설정
client1.geometry("450x600+50+50") # 화면 크기: 450x600, 화면 위치: x=50, y=50
client1.configure(bg='white') # 배경을 하얀색으로 설정
client1.resizable(False, False) # 실행 중에 화면 크기를 바꿀 수 없도록 함
client1.bind("<KeyPress>", key_down) # 아무 키나 누르면 key_down 함수 호출
client1.bind("<Button-1>", click) # 마우스 클릭하면 click 함수 호출

r = 8 # 이동 거리 (고정적)
angle = 0.5 # 이동 방향 (가변적)
origin_dot = [200, 300] # 원래 위치의 좌표

moved_dot = [r*math.cos(math.radians(angle)), r*math.sin(math.radians(angle))] # 이동 후 좌표

# 정의역
sketchbook1 = tk.Canvas(client1, width = 800, height = 600 , bg= 'white')
sketchbook1.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
sketchbook1.pack()

# 조작 설명 라벨
fixed_label = tk.Label(sketchbook1)
fixed_label.place(x=25, y=36)
fixed_label.config(font=('Helvatical bold', 15), bg='white')
fixed_label['text'] = 'Press any key to move, \nand click any position to change your direction'

main_proc1()

'''
두 번째 창 (보정 안 된 빠른 창) -> 세 번째 창과 비교당할 대상
'''

# 두 번째 창 세팅
client2 = tk.Toplevel(client1) # client2 GUI 생성
client2.title("틱레이트: 50")
client2.geometry("450x600+550+50") # 화면 크기: 450x600, 화면 위치: x=550, y=50
client2.configure(bg='white')
client2.resizable(False, False)
client2.bind("<KeyPress>", key_down)
client2.bind("<Button-1>", click)

r = 8 # 이동 거리 (고정적)
angle = 0.5 # 이동 방향 (가변적)
origin_dot = [200, 300] # 원래 위치의 좌표

moved_dot = [r*math.cos(math.radians(angle)), r*math.sin(math.radians(angle))] # 이동 후 좌표

# 정의역
sketchbook2 = tk.Canvas(client2, width = 800, height = 600 , bg= 'white')
sketchbook2.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
sketchbook2.pack()

# 조작 설명 라벨
fixed_label = tk.Label(sketchbook2)
fixed_label.place(x=25, y=36)
fixed_label.config(font=('Helvatical bold', 15), bg='white')
fixed_label['text'] = 'Press any key to move, \nand click any position to change your direction'

'''
세 번째 창 (보정되어 빠른 창) -> 두 번째 창을 통해 정확도 측정
'''

# 세 번째 창 세팅
client3 = tk.Toplevel(client1) # client3 GUI 생성
client3.title("틱레이트: 10 (예측 적용)")
client3.geometry("450x600+1050+50") # 화면 크기: 450x600, 화면 위치: x=1050, y=50
client3.configure(bg='white')
client3.resizable(False, False)
client3.bind("<KeyPress>", key_down)
client3.bind("<Button-1>", click)

r = 8 # 이동 거리 (고정적)
angle = 0.5 # 이동 방향 (가변적)
origin_dot = [200, 300] # 원래 위치의 좌표

moved_dot = [r*math.cos(math.radians(angle)), r*math.sin(math.radians(angle))] # 이동 후 좌표

# 정의역
sketchbook3 = tk.Canvas(client3, width = 800, height = 600 , bg= 'white')
sketchbook3.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
sketchbook3.pack()

# 조작 설명 라벨
fixed_label = tk.Label(sketchbook3)
fixed_label.place(x=25, y=36)
fixed_label.config(font=('Helvatical bold', 15), bg='white')
fixed_label['text'] = 'Press any key to move, \nand click any position to change your direction'

main_proc2and3()

client1.mainloop()