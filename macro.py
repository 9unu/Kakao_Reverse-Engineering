from pywinauto import application
import time
import pyautogui
import time
from win32api import GetSystemMetrics
pyautogui.FAILSAFE = False
import pyperclip
from kakao_text_preprocessing import *
# 상위 폴더 내 함수 가져오기 위함 

def kakao_macro(path, user_name):
    # 윈도우 창 크기 계산
    win_height=GetSystemMetrics(1)
    win_width=GetSystemMetrics(0)
    """
    카톡앱 열기
    """
    app = application.Application(backend='uia') 
    app.start("C:\Program Files (x86)\Kakao\KakaoTalk\KakaoTalk.exe")
    """
    메모장 앱 열기
    """
    app = application.Application(backend='uia')
    try:
        app.connect(title_re=u".*메모장.*")
    except:
        app.start("notepad.exe")
        time.sleep(2)
        app.connect(title_re=u".*메모장.*")#

    dlg = app.window(title_re=u".*메모장.*")

    # # 메모장 창 옮기기
    dlg.set_focus()
    #마우스로 창 왼쪽 상단과 오른쪽 하단을 잡고 드래그해서 600,600사이즈로 맞춰버리기
    memo=pyautogui.getActiveWindow()
    left_corner=[memo.left+3, memo.top]
    right_corner=[memo.right-3, memo.bottom-1]
    # 우측 하단
    pyautogui.moveTo(right_corner[0], right_corner[1])
    pyautogui.dragTo(win_width, win_height//2)
    # # 왼쪽 상단
    pyautogui.moveTo(left_corner[0], left_corner[1])
    pyautogui.dragTo(win_width-200, 200)

    """카톡 기본창 크기 조정"""
    kakao_win=pyautogui.getWindowsWithTitle('카카오톡')
    kakao_win_list=[]
    for win in kakao_win:
        kakao_win_list.append(win)
    print(kakao_win_list)
    kakao_win=kakao_win_list[0]
    kakao_win.activate()
    left_corner=[kakao_win.left+3, kakao_win.top]
    right_corner=[kakao_win.right-3, kakao_win.bottom-1]
    # 화면 중앙으로 이동
    pyautogui.moveTo((left_corner[0]+right_corner[0])//2, kakao_win.top+10)
    pyautogui.dragTo(win_width//2, 100)
    left_corner=[kakao_win.left+3, kakao_win.top]
    right_corner=[kakao_win.right-3, kakao_win.bottom-1]
    # 왼쪽 상단
    pyautogui.moveTo(left_corner[0], left_corner[1])
    pyautogui.dragTo(100, 100)
    # 우측 하단
    pyautogui.moveTo(right_corner[0], right_corner[1])
    pyautogui.dragTo(100+10, 100+800)

    kakao_win=pyautogui.getActiveWindow()

    """나와의 채팅방 열기"""
    # 606*801 크기 창 기준, 가로 기준 중간, 세로로부터 117픽셀 떨어져있음
    profile = [(kakao_win.left+kakao_win.right)//2, kakao_win.top+130]
    # 나와의 채팅방 열림
    pyautogui.doubleClick(profile[0], profile[1])

    #마우스로 창 왼쪽 상단과 오른쪽 하단을 잡고 드래그해서 600,600사이즈로 맞춰버리기
    me=pyautogui.getActiveWindow()
    # 화면 중앙으로 이동
    left_corner=[me.left+3, me.top]
    right_corner=[me.right-3, me.bottom-1]
    pyautogui.moveTo((left_corner[0]+right_corner[0])//2, me.top+10)
    pyautogui.dragTo(win_width//2, 100)
    left_corner=[me.left+3, me.top]
    right_corner=[me.right-3, me.bottom-1]
    # 왼쪽 상단
    pyautogui.moveTo(left_corner[0], left_corner[1])
    pyautogui.dragTo(100, 100)
    # 우측 하단
    pyautogui.moveTo(right_corner[0], right_corner[1])
    pyautogui.dragTo(100+10, 100+800)

    # 강제 픽스된 창 객체
    me=pyautogui.getActiveWindow()

    # ai 버튼을 클릭 및 위치 확인
    #창 왼쪽 기준 오른쪽으로 183픽셀 떨어져있고
    #창 맨밑 기준 26띄워져있음
    pyautogui.moveTo(me.left+me.width//2, me.bottom-26)
    # 버튼 위치 저장해놓기
    ai_button=[me.left+183, me.bottom-26]
    formal_button=[me.right+120+30 ,me.bottom-120]
    gentle_button=[me.right+60,me.bottom-120]
    origin_button=[gentle_button[0], gentle_button[1]-(formal_button[0]-gentle_button[0])//1.7]
    input_box=[ai_button[0], ai_button[1]-50]
    start = time.time()
    """ 이제 변환 시작"""
    """원본 텍스트 파일을 txt_to_csv()함수로 df로 변환"""
    print("<<<데이터프레임 생성 시작>>>")
    data=txt_file_multiprocess(path, result_file)
    # a=0       """데이터가 너무 길 경우 3000개 씩 잘라서 수동으로 재시작해야함"
    # data=data.iloc[a:a+3000]
    print(data.head())
    print("데이터 수:", len(data))
    # 각 행 순회하면서 텍스트를 한번씩 변환해서 집어넣음
    def memo_focus():
        dlg.set_focus()
    def copy_paste_to_memo():
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','c')
        memo_focus()
        pyautogui.hotkey('ctrl', 'v')
    def add_enter():
        pyperclip.copy('\n')
        pyautogui.hotkey('ctrl', 'v')
    def input_text(text):
        pyperclip.copy(f"{text}")
        pyautogui.hotkey('ctrl', 'v')
    def input_text_to_memo(text):
        pyperclip.copy(f"{text}")
        memo_focus()
        pyautogui.hotkey('ctrl', 'v')
    def click_button(button):
        # pyautogui.moveTo(button, duration=0.15)
        pyautogui.click(button)
    def input_clear():
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')

    """파일 이름 = 첫줄"""
    memo_focus()
    input_text_to_memo(result_file)   ###########################사용자 이름 넣어주기
    add_enter()
    """ai 처음부터 잘 세팅"""
    click_button(input_box)
    input_text("some")
    # ai 돌려놓기
    click_button(ai_button)
    click_button(origin_button)
    # 남아있는거 지우기
    click_button(input_box)

    # 행을 150개씩 잘라서 수행
    n=len(data)
    n_list=[]
    for i in range(n):
        if(i*150>n):
            n_list.append(n)
            break
        n_list.append(i*150)

    style_dict={"formal":formal_button, "gentle":gentle_button}

    for i in range(len(n_list)-1):
        data_sample=data.iloc[n_list[i]:n_list[i+1]]


        """원본 메모장에 입력"""
        for index, row in data_sample.iterrows():
            target=row['text']
            memo_focus()
            input_text_to_memo("[user]")
            input_text_to_memo(target)
            add_enter()

        
        for key, value in style_dict.items():
            click_button(input_box)
            input_text("some")
            click_button(ai_button)
            time.sleep(1)
            click_button(value)
            time.sleep(1)
            for _, row in data_sample.iterrows():
                """formal"""
                target=row['text']
                input_text_to_memo(f"[{key}]")
                # 입력창 클릭 -> 원본 입력
                click_button(input_box)
                input_clear()
                input_text(target)
                click_button(ai_button)
                time.sleep(0.75)
                click_button(input_box)
                copy_paste_to_memo()
                add_enter()
        print("현재까지 범위:", n_list[i],"~", n_list[i+1])
    end = time.time()
    print(f"{end - start:.5f} sec") #"""매크로 시간 측정"""
    
    """쓰여진 TXT파일 저장"""

    dlg['파일'].select()
    dlg['다른 이름으로 저장'].select()
    # 인코딩 콤보박스 선택
    encoding_combo = dlg.child_window(title="인코딩:", control_type="ComboBox")
    encoding_combo.select("UTF-8")

    # 파일 형식 콤보박스 선택
    file_type_combo = dlg.child_window(title="파일 형식:", auto_id="FileTypeControlHost", control_type="ComboBox")
    file_type_combo.select("텍스트 문서(*.txt)")

    # 저장 버튼 클릭
    save_button = dlg.child_window(title="저장(S)", auto_id="1", control_type="Button")
    save_button.click()

    #메모장 닫기(현재 활성화된 창)
    memo=pyautogui.getActiveWindow()
    memo.close()



if __name__ == "__main__":
    result_file=input("결과 txt파일 이름:")
    kakao_macro("텍스트 파일 경로", result_file)
    