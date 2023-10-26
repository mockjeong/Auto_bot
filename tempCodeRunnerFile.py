
# driver.window_handles    # 창 개수 확인
# driver.window_handles[0] # 메인창
# driver.window_handles[1] # 첫 번째 팝업 창
# driver.switch_to.window(driver.window_handles[1]) # 첫 번째 팝업 창으로 제어권 옮기기
# driver.close()                                    # 첫 번째 팝업 창 닫기
# driver.switch_to.window(driver.window_handles[0]) # 홈 화면 으로 제어권 옮기기
# time.sleep(1)