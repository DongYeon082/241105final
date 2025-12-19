import math
from pathlib import Path
from urllib.parse import quote

import streamlit as st


st.set_page_config(page_title="무게 친구 저울", layout="centered")
st.title("무게 친구 저울 — 무엇이 더 무거울까?")
st.markdown("숫자를 조절해서 어떤 쪽이 더 무거운지 한 번 맞혀보자! 단위는 다음 수업에서 배워요.")


ASSETS_DIR = Path(__file__).parent / "assets"

ITEMS = {
    "사과": ASSETS_DIR / "apple.svg",
    "바나나": ASSETS_DIR / "banana.svg",
    "곰인형": ASSETS_DIR / "teddy.svg",
    "책": ASSETS_DIR / "book.svg",
}


def svg_data_uri(path: Path) -> str:
    svg_text = path.read_text(encoding="utf-8")
    return "data:image/svg+xml;utf8," + quote(svg_text)


def make_seesaw_svg(left_uri: str, right_uri: str, angle_deg: float) -> str:
    # Simple SVG: beam rotates around center (300,120)
    angle = float(angle_deg)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="300">
  <rect width="100%" height="100%" fill="#fbfbfd"/>
  <g transform="rotate({angle},300,120)">
    <!-- beam -->
    <rect x="120" y="110" width="360" height="8" rx="4" fill="#6b7280" />
    <!-- left pan support -->
    <line x1="180" y1="118" x2="180" y2="190" stroke="#6b7280" stroke-width="3" />
    <circle cx="180" cy="218" r="34" fill="#fff" stroke="#cbd5e1" />
    <!-- right pan support -->
    <line x1="420" y1="118" x2="420" y2="190" stroke="#6b7280" stroke-width="3" />
    <circle cx="420" cy="218" r="34" fill="#fff" stroke="#cbd5e1" />
    <!-- images on pans -->
    <image href="{left_uri}" x="146" y="184" width="68" height="68" preserveAspectRatio="xMidYMid meet" />
    <image href="{right_uri}" x="386" y="184" width="68" height="68" preserveAspectRatio="xMidYMid meet" />
  </g>
  <!-- pivot -->
  <circle cx="300" cy="124" r="10" fill="#111827" />
</svg>'''
    return svg


st.markdown("이 앱은 두 물건의 무게를 비교하여 양팔 저울로 시각화합니다.")


col1, col2 = st.columns(2)

with col1:
    st.subheader("왼쪽 물건")
    left_item = st.selectbox("선택", list(ITEMS.keys()), index=0, key="left_item")
    left_weight = st.slider("무게 (값 조절)", min_value=0, max_value=2000, value=150, step=10, key="left_w")

with col2:
    st.subheader("오른쪽 물건")
    right_item = st.selectbox("선택", list(ITEMS.keys()), index=1, key="right_item")
    right_weight = st.slider("무게 (값 조절)", min_value=0, max_value=2000, value=100, step=10, key="right_w")



# 단위를 학습하지 않은 학생들을 위해 단위 표시는 제거합니다.
# 여기서는 단위 없이 숫자(비교값)만 사용합니다.
lw_g = float(left_weight)
rw_g = float(right_weight)

st.write(f"왼쪽 값: {left_weight}, 오른쪽 값: {right_weight}  (단위 없음, 숫자 비교용)")

# compute tilt angle bounded to [-25, 25]
def compute_angle(lg: float, rg: float) -> float:
    if lg == 0 and rg == 0:
        return 0.0
    diff = rg - lg
    denom = (lg + rg) if (lg + rg) > 0 else 1.0
    angle = 25.0 * (diff / denom)
    return max(-25.0, min(25.0, angle))


angle = compute_angle(lw_g, rw_g)

left_uri = svg_data_uri(ITEMS[left_item])
right_uri = svg_data_uri(ITEMS[right_item])

svg = make_seesaw_svg(left_uri, right_uri, angle)

st.subheader("비교 시각화")
st.markdown(svg, unsafe_allow_html=True)

st.caption("단위를 g 또는 kg로 바꿔 동일한 단위(그램)로 비교합니다.")

st.subheader("학생 답안")
student_answer = st.radio("어떤 쪽이 더 무거울까요?", ("왼쪽", "오른쪽", "같음"), index=0)
if st.button("정답 확인"):
    if abs(lw_g - rw_g) < 1e-6:
        actual = "같음"
    elif lw_g > rw_g:
        actual = "왼쪽"
    else:
        actual = "오른쪽"

    st.info(f"정답: {actual}")
    if student_answer == actual:
        st.success("정답입니다! 잘했어요 🎉")
    else:
        st.error("아쉽지만 틀렸습니다. 한 번 더 생각해볼까요?")
