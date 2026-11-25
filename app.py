import streamlit as st
import random
import pandas as pd

# 페이지 기본 설정
st.set_page_config(
    page_title="하현상 감성 주크박스 🎸",
    page_icon="🌙",
    layout="centered"
)

# --- 1. 서정적인 감성 테마 & 3D 입체 버튼 커스텀 CSS ---
st.markdown("""
<style>
    /* 전체 배경: 차분하고 따뜻한 린넨/아이보리 페이퍼 톤 */
    .stApp {
        background: linear-gradient(180deg, #F7F4EF 0%, #EFEAE1 100%);
        color: #2C2A29;
    }

    /* 타이틀 및 서브헤더 스타일링 */
    .main-title {
        text-align: center;
        color: #2C2A29;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .sub-title {
        text-align: center;
        color: #7A736B;
        font-size: 0.95rem;
        margin-bottom: 24px;
    }

    /* 질문 배너 박스 */
    .mood-banner {
        background-color: rgba(255, 255, 255, 0.78);
        border: 1px solid #DCD5C9;
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        color: #3E3A35;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(44, 42, 41, 0.04);
        margin-bottom: 18px;
    }

    /* 3D 입체 감성 버튼 스타일 */
    div.stButton > button {
        background-color: #FFFFFF;
        color: #3E3A35;
        border: 1.5px solid #C8BFA8;
        border-radius: 16px;
        padding: 12px 10px;
        font-size: 15px;
        font-weight: 600;
        box-shadow: 0px 5px 0px #C8BFA8, 0px 8px 15px rgba(44, 42, 41, 0.07);
        transition: all 0.12s ease-in-out;
        margin-bottom: 6px;
    }
    div.stButton > button:hover {
        background-color: #FAF6F0;
        color: #1F1D1B;
        border-color: #9E9279;
        transform: translateY(-2px);
        box-shadow: 0px 7px 0px #9E9279, 0px 10px 18px rgba(44, 42, 41, 0.1);
    }
    div.stButton > button:active {
        transform: translateY(3px);
        box-shadow: 0px 2px 0px #9E9279, 0px 3px 6px rgba(44, 42, 41, 0.08);
    }

    /* 앨범 커버 아트워크 카드 */
    .album-cover-card {
        width: 220px;
        height: 220px;
        margin: 0 auto 12px auto;
        border-radius: 14px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 18px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.18);
        position: relative;
        overflow: hidden;
    }
    .album-artist {
        font-size: 0.72rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        opacity: 0.85;
    }
    .album-title-art {
        font-size: 1.3rem;
        font-weight: 700;
        line-height: 1.3;
        word-break: keep-all;
    }
    .album-type-tag {
        font-size: 0.75rem;
        opacity: 0.8;
        align-self: flex-end;
    }

    /* 마무리 인사말 카드 */
    .closing-note {
        background-color: #3E3A35;
        color: #F7F4EF;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
        font-size: 1rem;
        font-weight: 500;
        letter-spacing: 0.3px;
        margin-top: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 기분별 이모티콘 & 감성 멘트 ---
mood_info = {
    "슬픔": {
        "emoji": "🌧️",
        "label": "😢 슬픔",
        "desc": "조용히 젖어 드는 밤공기처럼, 마음을 어루만져 줄 선율이에요."
    },
    "화나는": {
        "emoji": "🌊",
        "label": "😡 화나는",
        "desc": "거센 파도처럼 답답한 감정을 시원하게 털어내 줄 사운드예요."
    },
    "신나는": {
        "emoji": "✨",
        "label": "🥳 신나는",
        "desc": "햇살 부서지는 오후처럼 발걸음을 가볍게 만들어 줄 리듬이에요."
    },
    "행복함": {
        "emoji": "🌿",
        "label": "🥰 행복함",
        "desc": "포근한 온기와 다정한 시선이 머무는 순간에 어울리는 노래예요."
    },
    "우울함": {
        "emoji": "🌙",
        "label": "☁️ 우울함",
        "desc": "모두가 잠든 새벽, 조용히 곁에 앉아 위로를 건네는 목소리예요."
    }
}

# --- 3. 요청하신 기분별 하현상 음악 리스트 & 정확한 앨범 매칭 데이터베이스 ---
songs_by_mood = {
    "슬픔": [
        {
            "곡 제목": "집에 가는 길",
            "앨범명": "Time and Trace (정규 1집)",
            "cover_bg": "linear-gradient(135deg, #5C6B73 0%, #9DB4C0 100%)",
            "text_color": "#FAF9F5",
            "album_eng": "TIME AND TRACE",
            "release_type": "1st Full Album · 2023",
            "추천 이유 (분위기 및 감상)": "지친 하루 끝에 홀로 걸어가는 길 위의 쓸쓸함과 그리움을 담담하게 풀어내 가슴이 먹먹해지는 곡입니다."
        },
        {
            "곡 제목": "Pain",
            "앨범명": "With All My Heart (EP)",
            "cover_bg": "linear-gradient(135deg, #2B2D42 0%, #5C627D 100%)",
            "text_color": "#EDF2F4",
            "album_eng": "WITH ALL MY HEART",
            "release_type": "4th EP · 2024",
            "추천 이유 (분위기 및 감상)": "깊고 시린 감정의 아픔을 섬세하고 애절한 보컬로 그려내 조용히 눈물을 훔치게 만드는 트랙입니다."
        },
        {
            "곡 제목": "시간과 흔적",
            "앨범명": "Time and Trace (정규 1집)",
            "cover_bg": "linear-gradient(135deg, #6E7F6B 0%, #A9B8A4 100%)",
            "text_color": "#FAF9F5",
            "album_eng": "TIME AND TRACE",
            "release_type": "1st Full Album · 2023",
            "추천 이유 (분위기 및 감상)": "지나간 시간과 남겨진 흔적들을 되돌아보며 밀려오는 아련함과 벅찬 그리움을 담은 대표곡입니다."
        }
    ],
    "신나는": [
        {
            "곡 제목": "오디세이",
            "앨범명": "Elegy (EP)",
            "cover_bg": "linear-gradient(135deg, #2E5A88 0%, #6FA3D2 100%)",
            "text_color": "#FFFFFF",
            "album_eng": "ELEGY",
            "release_type": "5th EP · 2024",
            "추천 이유 (분위기 및 감상)": "미지의 세계로 모험을 떠나는 듯한 웅장하고 역동적인 사운드가 듣는 순간 가슴을 뛰게 만듭니다."
        },
        {
            "곡 제목": "소년의 방",
            "앨범명": "Time and Trace (정규 1집)",
            "cover_bg": "linear-gradient(135deg, #6E7F6B 0%, #A9B8A4 100%)",
            "text_color": "#FAF9F5",
            "album_eng": "TIME AND TRACE",
            "release_type": "1st Full Album · 2023",
            "추천 이유 (분위기 및 감상)": "경쾌한 밴드 사운드와 순수하고 자유로운 에너지가 기분 좋은 텐션과 설렘을 불어넣습니다."
        },
        {
            "곡 제목": "Tiny Dance",
            "앨범명": "With All My Heart (EP)",
            "cover_bg": "linear-gradient(135deg, #4F759B 0%, #8CB3D9 100%)",
            "text_color": "#FFFFFF",
            "album_eng": "WITH ALL MY HEART",
            "release_type": "4th EP · 2024",
            "추천 이유 (분위기 및 감상)": "가볍게 춤추듯 리드미컬하게 흘러가는 멜로디가 발걸음을 경쾌하게 만들어 주는 트랙입니다."
        }
    ],
    "행복함": [
        {
            "곡 제목": "New Boat",
            "앨범명": "Calibrate (EP)",
            "cover_bg": "linear-gradient(135deg, #3A6073 0%, #78A2B7 100%)",
            "text_color": "#F9FBFD",
            "album_eng": "CALIBRATE",
            "release_type": "2nd EP · 2021",
            "추천 이유 (분위기 및 감상)": "새로운 항해를 시작하는 설렘과 산뜻한 바람처럼 기분 좋은 기대감을 채워주는 밝은 곡입니다."
        },
        {
            "곡 제목": "눈꽃",
            "앨범명": "눈꽃 (싱글)",
            "cover_bg": "linear-gradient(135deg, #7B8FA1 0%, #CFD8DC 100%)",
            "text_color": "#263238",
            "album_eng": "SNOWFLAKE",
            "release_type": "Digital Single · 2023",
            "추천 이유 (분위기 및 감상)": "하얗게 내리는 눈꽃처럼 포근하고 로맨틱한 선율이 마음을 따뜻하고 행복하게 물들입니다."
        },
        {
            "곡 제목": "MAGIC",
            "앨범명": "MAGIC (싱글)",
            "cover_bg": "linear-gradient(135deg, #4E7A9E 0%, #9CC2DF 100%)",
            "text_color": "#FFFFFF",
            "album_eng": "MAGIC",
            "release_type": "Digital Single · 2022",
            "추천 이유 (분위기 및 감상)": "일상이 마법처럼 특별해지는 두근거림과 산뜻한 기타 리듬이 입가에 미소를 번지게 합니다."
        }
    ],
    "우울함": [
        {
            "곡 제목": "Dawn",
            "앨범명": "My Poor (EP)",
            "cover_bg": "linear-gradient(135deg, #1D222B 0%, #3A4252 100%)",
            "text_color": "#DCDFE6",
            "album_eng": "MY POOR",
            "release_type": "Debut EP · 2018",
            "추천 이유 (분위기 및 감상)": "모두가 잠든 고요한 새벽의 고독과 내면의 불안을 담아 새벽에 혼자 들으면 깊은 위로를 건네는 곡입니다."
        },
        {
            "곡 제목": "등대",
            "앨범명": "Calibrate (EP)",
            "cover_bg": "linear-gradient(135deg, #1F3A52 0%, #4A708B 100%)",
            "text_color": "#F4F7FA",
            "album_eng": "CALIBRATE",
            "release_type": "2nd EP · 2021",
            "추천 이유 (분위기 및 감상)": "어두운 밤바다에서 길을 잃고 헤맬 때, 묵묵히 빛을 비춰주며 버팀목이 되어주는 뭉클한 위로곡입니다."
        },
        {
            "곡 제목": "파랑골목",
            "앨범명": "Elegy (EP)",
            "cover_bg": "linear-gradient(135deg, #243B55 0%, #4B6CB7 100%)",
            "text_color": "#F0F4F8",
            "album_eng": "ELEGY",
            "release_type": "5th EP · 2024",
            "추천 이유 (분위기 및 감상)": "푸른 새벽빛이 내려앉은 골목길을 걷는 듯한 차분하고 서정적인 무드가 가라앉은 마음을 조용히 다독여 줍니다."
        }
    ],
    "화나는": [
        {
            "곡 제목": "송가",
            "앨범명": "Elegy (EP)",
            "cover_bg": "linear-gradient(135deg, #232526 0%, #414345 100%)",
            "text_color": "#E8E6E1",
            "album_eng": "ELEGY",
            "release_type": "5th EP · 2024",
            "추천 이유 (분위기 및 감상)": "웅장하게 고조되는 드라마틱한 사운드와 강렬한 에너지가 복잡하고 답답한 감정을 시원하게 환기해 줍니다."
        },
        {
            "곡 제목": "파도",
            "앨범명": "Time and Trace (정규 1집)",
            "cover_bg": "linear-gradient(135deg, #2C3E50 0%, #4CA1AF 100%)",
            "text_color": "#F4F7F8",
            "album_eng": "TIME AND TRACE",
            "release_type": "1st Full Album · 2023",
            "추천 이유 (분위기 및 감상)": "거칠게 몰아치다 부서지는 파도처럼 요동치는 감정을 깊은 울림으로 풀어내며 마음을 차분하게 가라앉혀 줍니다."
        },
        {
            "곡 제목": "Same Old Song",
            "앨범명": "Time and Trace (정규 1집)",
            "cover_bg": "linear-gradient(135deg, #3E3B39 0%, #736B65 100%)",
            "text_color": "#F7F4EF",
            "album_eng": "TIME AND TRACE",
            "release_type": "1st Full Album · 2023",
            "추천 이유 (분위기 및 감상)": "반복되는 지루하고 답답한 일상 속 날카로운 감정을 세련된 사운드로 날려버릴 수 있는 트랙입니다."
        }
    ]
}

# --- 4. 상태(Session State) 관리 ---
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

# --- 5. 웹앱 메인 UI ---
st.markdown("<div class='main-title'>🎸 하현상 감성 플레이리스트</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>당신의 오늘에 조용히 스며들 작은 선율 한 조각</div>", unsafe_allow_html=True)

# 접속 시 5가지 기분 목록과 함께 "오늘의 기분은 어떤가요?" 표시
st.markdown("<div class='mood-banner'>🌙 오늘의 기분은 어떤가요?</div>", unsafe_allow_html=True)

# 5가지 기분 선택 3D 입체 버튼
mood_options = ["슬픔", "화나는", "신나는", "행복함", "우울함"]
cols = st.columns(5)

for idx, mood in enumerate(mood_options):
    with cols[idx]:
        if st.button(mood_info[mood]["label"], key=f"btn_{mood}", use_container_width=True):
            st.session_state.selected_mood = mood

# --- 6. 기분 선택 시 앨범 커버 + 추천 테이블 출력 ---
if st.session_state.selected_mood:
    current_mood = st.session_state.selected_mood
    info = mood_info[current_mood]
    
    st.divider()
    st.markdown(f"### {info['emoji']} '{current_mood}' 기분일 때 추천하는 하현상 음악")
    st.caption(info["desc"])
    
    # random.sample로 해당 기분에 맞는 곡들 중 무작위 2곡 추천
    recommended_list = random.sample(songs_by_mood[current_mood], k=2)
    
    # 추천된 2곡의 앨범 표지 아트워크를 나란히 표시
    cover_cols = st.columns(2)
    for idx, song in enumerate(recommended_list):
        with cover_cols[idx]:
            st.markdown(f"""
            <div class="album-cover-card" style="background: {song['cover_bg']}; color: {song['text_color']};">
                <div class="album-artist">HA HYUN SANG</div>
                <div class="album-title-art">{song['album_eng']}<br><span style="font-size:0.9rem; font-weight:400;">- {song['곡 제목']} -</span></div>
                <div class="album-type-tag">{song['release_type']}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.write("")
    
    # 곡 제목과 앨범명이 드러나는 테이블(표) 형태로 출력
    table_data = [
        {
            "곡 제목": song["곡 제목"],
            "앨범명": song["앨범명"],
            "추천 이유 (분위기 및 감상)": song["추천 이유 (분위기 및 감상)"]
        }
        for song in recommended_list
    ]
    df = pd.DataFrame(table_data)
    st.table(df.set_index("곡 제목"))
    
    # 같은 기분으로 다시 뽑기 3D 버튼
    if st.button("🔄 다른 곡 랜덤 추천받기", use_container_width=True):
        st.rerun()
        
    # 마무리 인사 문구
    st.markdown("<div class='closing-note'>좋은 하루 보내세요 🌿</div>", unsafe_allow_html=True)
