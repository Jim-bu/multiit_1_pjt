import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from openpyxl import Workbook
import os

def crawl_youtube_comments(url):
    # Chrome 웹 드라이버 실행
    driver = webdriver.Chrome()
    # 유튜브 댓글 페이지 열기
    driver.get(url)
    # 페이지가 로드될 때까지 잠시 대기
    time.sleep(6)
    
    # 스크롤을 내려 더 많은 댓글을 로드
    body = driver.find_element(By.TAG_NAME, 'body')
    while True:
        # 현재 댓글 수
        current_comments = len(driver.find_elements(By.CSS_SELECTOR, "#content-text"))
        # 페이지 스크롤 다운
        body.send_keys(Keys.END)
        time.sleep(4)  # 스크롤 후 페이지가 로드될 때까지 대기
        # 새로 로드된 댓글 수
        new_comments = len(driver.find_elements(By.CSS_SELECTOR, "#content-text"))
        # 댓글이 더 이상 로드되지 않으면 종료
        if new_comments == current_comments:
            break
        st.write(f"댓글 수: {new_comments}")
        
    # 댓글 요소들 찾기
    comment_elements = driver.find_elements(By.CSS_SELECTOR, "#content-text")
    comments = []
    # 댓글 텍스트 추출
    for comment in comment_elements:
        comments.append(comment.text)
        # 답글 찾기
        parent_element = comment.find_element(By.XPATH, "..")
        replies = parent_element.find_elements(By.XPATH, ".//yt-formatted-string[@id='content-text']")
        for reply in replies:
            comments.append("답글: " + reply.text)
    # 크롬 드라이버 종료
    driver.quit()
    return comments

def save_to_excel(comments, filename):
    # 엑셀 워크북 생성
    wb = Workbook()
    ws = wb.active
    ws.append(["댓글"])
    # 댓글을 엑셀에 쓰기
    for comment in comments:
        ws.append([comment])
    # 파일 경로 지정
    save_path = os.path.join(r"C:\Users\Hong\snsmarketing", filename)
    # 엑셀 파일 저장
    wb.save(save_path)
    st.success("댓글이 성공적으로 저장되었습니다.")
    return os.path.abspath(save_path)

# Streamlit 인터페이스
st.title("유튜브 댓글 크롤러")
youtube_url = st.text_input("유튜브 동영상 URL을 입력하세요:")
file_name = st.text_input("저장할 파일명을 입력하세요:") + '.xlsx'

if st.button("크롤링 시작"):
    if youtube_url and file_name:
        st.write("크롤링 중... 잠시만 기다려 주세요.")
        comments = crawl_youtube_comments(youtube_url)
        st.write("댓글 저장 중...")
        file_path = save_to_excel(comments, file_name)
        st.success(f"작업이 완료되었습니다! 파일이 저장된 위치: {file_path}")
    else:
        st.error("URL과 파일명을 모두 입력해 주세요.")