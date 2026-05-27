import streamlit as st
import random
import time

# 1. 페이지 설정
st.set_page_config(page_title="🔥 GD: MULTI-VERSE MANIA", page_icon="⚡", layout="centered")

st.title("🔥 GD: MULTI-VERSE MANIA (Streamlit Ed.)")
st.markdown("속도 화살표와 변칙적인 블록들이 가득한 스테이지에 도전하세요! 🏆")

# 2. 게임 설정 사이드바 / 슬라이더
st.sidebar.header("🛠️ 게임 설정")
difficulty = st.sidebar.radio("난이도 선택", ["EASY", "NORMAL", "HARDCORE"], index=2)
practice_mode = st.sidebar.toggle("연습 모드 (Practice Mode)", value=False)

# 메인 화면 슬라이더: 도전할 스테이지 길이(세션 수)
stage_length = st.slider("스테이지 길이 설정 (돌파해야 할 장애물 개수)", 5, 30, 10)

# 최고 기록 관리를 위한 Session State 초기화
if "high_score" not in st.session_state:
    st.session_state.high_score = 0

# 3. 게임 실행 로직 함수
def run_geometry_dash(length, diff, practice):
    score = 0
    current_mode = "CUBE"
    is_mini = False
    
    # 난이도별 기본 생존 확률 설정
    base_survival = 0.85 if diff == "EASY" else (0.75 if diff == "NORMAL" else 0.60)
    
    # 거대 속도 화살표 변수 (1x ~ 4x)
    speed_multiplier = 1
    
    st.markdown("### 🏃‍♂️ 스테이지 진입 중...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 장애물 연속 돌파 시뮬레이션 시작
    for i in range(1, length + 1):
        time.sleep(0.3) # 시뮬레이션 맛을 살리기 위한 잠깐의 대기
        progress_bar.progress(i / length)
        
        # 무작위 이벤트 및 장애물 유형 결정
        event_rand = random.random()
        
        # [이벤트 1] 모드 변경 포탈 등장 (크기 극대화되어 무조건 통과)
        if event_rand < 0.25:
            current_mode = random.choice(["CUBE", "SHIP", "BALL", "WAVE"])
            st.toast(f"🔮 포탈 통과! [{current_mode}] 모드로 강제 변경!", icon="🔮")
            
        # [이벤트 2] 크기 변환 포탈 등장 (무조건 통과)
        elif event_rand < 0.40:
            is_mini = not is_mini
            size_str = "MINI" if is_mini else "NORMAL"
            st.toast(f"✨ 크기 변환! 이제 [{size_str}] 상태입니다.", icon="✨")
            
        # [이벤트 3] 거대 배속 화살표 등장 (크기가 화면 전체라 무조건 속도 업)
        elif event_rand < 0.55:
            speed_multiplier = random.choice([2, 3, 4])
            st.toast(f"⚡ 거대 배속 화살표 통과! 현재 속도: {speed_multiplier}x", icon="⚡")

        # 속도가 빨라질수록, 미니 상태일수록, 난이도가 높을수록 생존 확률 하락
        penalty = (speed_multiplier - 1) * 0.1
        if is_mini: penalty += 0.05
        
        survival_chance = base_survival - penalty
        if survival_chance < 0.2: survival_chance = 0.2 # 최소 확률 보장
        
        # 장애물 돌파 판정
        if random.random() < survival_chance:
            score += 1
            status_text.write(f"🧱 **장애물 {i}번** 돌파 성공! (모드: {current_mode} | 속도: {speed_multiplier}x)")
        else:
            # 연습 모드라면 파괴되지 않고 부활
            if practice:
                st.warning(f"⚠️ 장애물 {i}번에서 충돌! 하지만 연습 모드라 체크포인트에서 부활합니다.")
                score += 1
            else:
                # 일반 모드라면 즉시 게임 오버
                return False, score
                
    return True, score

# 4. 도전 시작 버튼 클릭 시
if st.button("🏁 스테이지 도전 시작!"):
    success, final_score = run_geometry_dash(stage_length, difficulty, practice_mode)
    
    st.markdown("---")
    if success:
        st.balloons()
        st.success(f"🎉 대성공! 스테이지를 완벽하게 클리어했습니다! (최종 스코어: {final_score})")
    else:
        st.error(f"💥 크래시 발생! 장애물에 부딪혀 플레이어가 파괴되었습니다.")
        
        # 연습 모드가 아닐 때만 최고 기록 갱신 및 출력
        if not practice_mode:
            if final_score > st.session_state.high_score:
                st.session_state.high_score = final_score
                st.toast("🥇 최고 기록 경신!", icon="🏆")
            
            # 요청하신 예시 포맷 적용 (최고기록:X)
            st.info(f"📊 현재 기록: {final_score}  |  **(최고기록:{st.session_state.high_score})**")
        else:
            st.caption("ℹ️ 연습 모드 중 획득한 점수는 최고 기록에 반영되지 않습니다.")

else:
    st.caption("⬆️ 사이드바에서 난이도를 고르고 도전 시작 버튼을 눌러보세요!")

st.markdown("---")
st.caption("Made with Streamlit · 한 번 가보자고! 🍀")
