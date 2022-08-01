"""
강화 학습이 적용된 화면을 비교해 보는 파일입니다.

실행하면 나오는 창은 각각 '낮은 틱레이트', '높은 틱레이트', '낮은 틱레이트에 예측 적용'입니다.
"""

# 라이브러리 불러오기
import math
import tkinter as tk

'''
공통 함수 선언 부분
'''

# 키 입력 반응 함수 (움직임)
def key_down(event) :
    origin_dot[0] = origin_dot[0] + r*math.cos(math.radians(angle))
    origin_dot[1] = origin_dot[1] + r*math.sin(math.radians(angle))

# 클릭 반응 함수 (방향 재설정)
def click(event) :
    global angle
    rad = math.atan2(origin_dot[1]-event.y, origin_dot[0]-event.x)
    PI = math.pi
    angle = 180 + rad*180/PI

'''
각 창의 무한 반복 설정 (위치 갱신 및 틱레이트 설정)
'''

# 무한 반복 함수 (첫 번째 창)
def main_proc1():
    sketchbook1.delete('all')
    sketchbook1.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
    client1.after(100, main_proc1) # 100밀리초(0.1초)마다 함수 다시 호출 -> 틱레이트 10

loop_num = 0

# 무한 반복 함수 (두 번째 창)
def main_proc2and3():
    global loop_num

    sketchbook2.delete('all')
    sketchbook2.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
    
    if loop_num % 5 == 0 : # 함수가 5번 반복될 때마다 세 번째 창을 갱신함. -> 0.1초마다 호출(틱레이트 10)
        sketchbook3.delete('all')
        sketchbook3.create_oval(origin_dot[0], origin_dot[1], origin_dot[0]+30, origin_dot[1]+30, fill = "white" )
    
    loop_num += 1
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