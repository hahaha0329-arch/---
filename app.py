import streamlit as st
import random
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 하현상 플레이리스트 🎸",
    page_icon="🧸",
    layout="centered"
)

# --- 1. 귀여운 테마 & 3D 입체 버튼 커스텀 CSS ---
st.markdown("""
<style>
    /* 전체 배경을 포근한 파스텔 크림톤으로 변경 */
    .stApp {
        background-color: #FFFDF9;
    }
    
    /* 3D 입체 버튼 스타일 (기분 선택 버튼 & 다시 뽑기 버튼) */
    div.stButton > button {
        background-color: #FFE4E1;
        color: #5C4B51;
        border: 2px solid #FFB6C1;
        border-radius: 20px;
        padding: 12px 16px;
        font-size: 16px;
        font-weight: bold;
        /* 입체감을 주는 하단 그림자 */
        box-shadow: 0px 6px 0px #FFB6C1, 0px 8px 15px rgba(0, 0, 0, 0.08);
        transition: all 0.1s ease-in-out;
        margin-bottom: 8px;
    }
    
    /* 버튼에 마우스를 올렸을 때 살짝 떠오르는 효과 */
    div.stButton > button:hover {
        background-color: #FFD1DC;
        color: #3E2F35;
        border-color: #FF9AA2;
        transform: translateY(-2px);
        box-shadow: 0px 8px 0px #FF9AA2, 0px 10px 18px rgba(0, 0, 0, 0.1);
    }
    
    /* 버튼을 클릭했을 때 꾹 눌리는 입체 효과 */
    div.stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0px 2px 0px #FF9AA2, 0px 3px 6px rgba(0, 0, 0, 0.1);
    }

    /* 추천 결과 박스 및 표 디자인 다듬기 */
    .mood-banner {
        background-color: #FFF0F5;
        border: 2px dashed #FFB6C1;
        border-radius: 18px;
        padding: 15px;
        text-align: center;
        color: #5C4B51;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 기분별 이모티콘 & 감성 일러스트 이미지 URL 매핑 ---
mood_info = {
    "슬픔": {
        "emoji": "😢💧",
        "label": "😢 슬픔",
        "image": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=800&q=80",
        "caption": "빗소리처럼 촉촉하게 마음을 적셔줄 하현상의 발라드예요 ☔"
    },
    "화나는": {
        "emoji": "😡🔥",
        "label": "😡 화나는",
        "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "caption": "거센 파도처럼 답답한 속을 시원하게 날려버릴 록 사운드예요 🌊"
    },
    "신나는": {
        "emoji": "🥳🎶",
        "label": "🥳 신나는",
        "image": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=800&q=80",
        "caption": "반짝이는 불꽃처럼 기분 좋은 텐션을 올려줄 청량한 곡이에요 ✨"
    },
    "행복함": {
        "emoji": "🥰🍀",
        "label": "🥰 행복함",
        "image": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=800&q=80",
        "caption": "따스한 햇살과 꽃향기처럼 포근한 설렘을 담은 노래예요 🌸"
    },
    "우울함": {
        "emoji": "☁️🌙",
        "label": "☁️ 우울함",
        "image": "https://images.unsplash.com/photo-1507400492013-162706c8c05e?auto=format&fit=crop&w=800&q=80",
        "caption": "고요한 밤하늘의 달빛처럼 조용히 곁을 지켜줄 위로곡이에요 🧸"
    }
}

# --- 3. 100% 실제 하현상 정식 발매 앨범 & 수록곡 데이터베이스 ---
songs_by_mood = {
    "슬픔": [
        {
            "곡 제목": "바람이 되어 🌬️",
            "앨범명": "미스터 션샤인 OST Part.11",
            "추천 이유 (분위기 및 리스너 반응)": "닿을 수 없는 그리움을 노래한 애절한 가사와 서정적인 현악 선율로 '듣자마자 눈물이 난다', '가슴이 먹먹해진다'는 반응이 많은 대표 발라드입니다."
        },
        {
            "곡 제목": "Nostalgia 🍂",
            "앨범명": "Nostalgia (싱글)",
            "추천 이유 (분위기 및 리스너 반응)": "지나간 찬란한 시절에 대한 상실감과 그리움을 담아 '과거가 떠올라 마음이 시리다'는 평이 많은 서정적인 곡입니다."
        },
        {
            "곡 제목": "불꽃놀이 🎆",
            "앨범명": "불꽃놀이 (싱글)",
            "추천 이유 (분위기 및 리스너 반응)": "아름답게 흩어져 사라지는 순간의 공허함과 아련함을 담아 '후반부 보컬이 터질 때 울컥한다'는 감상이 주를 이룹니다."
        }
    ],
    "화나는": [
        {
            "곡 제목": "3108 ⚡",
            "앨범명": "3108 (싱글)",
            "추천 이유 (분위기 및 리스너 반응)": "답답한 현실을 깨부수고 앞으로 질주하는 강렬한 비트 덕분에 '스트레스가 풀린다', '속이 뻥 뚫린다'는 반응이 많습니다."
        },
        {
            "곡 제목": "등대 🚨",
            "앨범명": "Calibrate (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "거센 파도와 어둠을 뚫고 나아가는 폭발적인 록 사운드와 시원한 고음이 답답한 마음을 환기해 주는 카타르시스를 선사합니다."
        },
        {
            "곡 제목": "죽은 새 🎸",
            "앨범명": "Calibrate (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "날 선 기타 사운드와 억눌린 감정을 토해내는 강렬한 보컬이 복잡한 분노와 답답함을 대변해 줍니다."
        }
    ],
    "신나는": [
        {
            "곡 제목": "Magic ✨",
            "앨범명": "Magic (싱글)",
            "추천 이유 (분위기 및 리스너 반응)": "경쾌하게 통통 튀는 기타 리듬과 설레는 분위기로 '발걸음이 가벼워진다', '기분이 확 업된다'는 반응이 대표적입니다."
        },
        {
            "곡 제목": "By My Side 🏃‍♂️",
            "앨범명": "The Edge (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "청량하고 속도감 있는 밴드 사운드로 '드라이브할 때 듣기 최고다', '페스티벌에서 뛰어놀고 싶은 곡'으로 꼽힙니다."
        },
        {
            "곡 제목": "소년의 방 🎈",
            "앨범명": "Time and Trace (정규 1집)",
            "추천 이유 (분위기 및 리스너 반응)": "경쾌한 밴드 사운드와 순수하고 자유로운 에너지가 기분 좋은 텐션과 설렘을 불어넣습니다."
        }
    ],
    "행복함": [
        {
            "곡 제목": "A Book of Love 📖",
            "앨범명": "The Edge (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "사랑하는 사람과의 매일을 동화책처럼 그려낸 포근한 곡으로 '듣는 내내 미소가 지어진다', '마음이 따뜻해진다'는 평이 많습니다."
        },
        {
            "곡 제목": "Close 🤍",
            "앨범명": "The Edge (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "다정하게 속삭이는 보컬과 부드러운 어쿠스틱 선율이 사랑스럽고 충만한 기분을 더해줍니다."
        },
        {
            "곡 제목": "고양이 🐱",
            "앨범명": "Time and Trace (정규 1집)",
            "추천 이유 (분위기 및 리스너 반응)": "따스한 햇살 아래 여유를 즐기는 나른하고 평화로운 분위기로, 기분 좋은 일상의 소소한 행복감을 더해줍니다."
        }
    ],
    "우울함": [
        {
            "곡 제목": "Dawn 🌅",
            "앨범명": "My Poor (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "모두가 잠든 고요한 새벽의 고독과 내면의 불안을 담아 '새벽에 혼자 들으면 큰 위로가 된다'는 반응이 많습니다."
        },
        {
            "곡 제목": "Where Are You Now 🧭",
            "앨범명": "My Poor (EP)",
            "추천 이유 (분위기 및 리스너 반응)": "방향을 잃고 멈춰 선 듯한 무력감을 담담히 읊조려, 가라앉은 마음을 억지로 끌어올리지 않고 조용히 다독여 줍니다."
        },
        {
            "곡 제목": "심야영화 🎬",
            "앨범명": "심야영화 (싱글)",
            "추천 이유 (분위기 및 리스너 반응)": "불 꺼진 극장에 혼자 남은 듯한 공허함과 쓸쓸함을 잔잔하게 풀어내 센치하고 우울한 밤에 깊이 스며듭니다."
        }
    ]
}

# --- 4. 상태(Session State) 초기화 ---
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

# --- 5. 웹앱 메인 UI ---
st.markdown("<h1 style='text-align: center; color: #5C4B51;'>🧸 오늘의 하현상 주크박스 🎸</h1>", unsafe_allow_html=True)

# 상단 귀여운 감성 배너 이미지
st.image(
    "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=900&q=80",
    use_container_width=True
)

st.markdown("<div class='mood-banner'>💌 오늘의 기분은 어떤가요? 아래 3D 버튼을 꾹 눌러보세요! 💌</div>", unsafe_allow_html=True)

# 5가지 기분 선택 3D 입체 버튼 가로 배치
mood_options = ["슬픔", "화나는", "신나는", "행복함", "우울함"]
cols = st.columns(5)

for idx, mood in enumerate(mood_options):
    with cols[idx]:
        if st.button(mood_info[mood]["label"], key=f"btn_{mood}", use_container_width=True):
            st.session_state.selected_mood = mood

# --- 6. 기분 선택 시 추천 결과 및 맞춤 이미지·표 출력 ---
if st.session_state.selected_mood:
    current_mood = st.session_state.selected_mood
    info = mood_info[current_mood]
    
    st.divider()
    st.subheader(f"{info['emoji']} '{current_mood}' 기분일 때 딱 맞는 하현상 음악")
    
    # 기분에 어울리는 감성 이미지와 설명 표시
    st.image(info["image"], caption=info["caption"], use_container_width=True)
    
    # random.sample로 해당 기분에 맞는 곡 2개 랜덤 추천
    recommended_list = random.sample(songs_by_mood[current_mood], k=2)
    df = pd.DataFrame(recommended_list)
    
    # 테이블(표) 형태로 출력
    st.table(df.set_index("곡 제목"))
    
    # 다른 곡 다시 뽑기 입체 버튼
    if st.button("🎲 같은 기분으로 다른 노래 또 뽑기!", use_container_width=True):
        st.rerun()
        
    st.divider()
    # 마무리 인사 문구
    st.success("🌷 오늘도 하현상 노래와 함께 좋은 하루 보내세요! 🌷")
