from __future__ import annotations

import html

import streamlit as st


st.set_page_config(
    page_title="ホテル開発 初期評価デモ",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="collapsed",
)


MOCK_RESULT = {
    "decision": "検討継続",
    "rank": "A",
    "score": 82,
    "pipeline_rank": "3 / 18",
    "planned_gfa": "5,400 ㎡",
    "rooms": "120 室",
    "adr": "35,000 円",
    "occupancy": "80.0%",
    "room_revenue": "12.3 億円",
    "total_revenue": "13.5 億円",
    "noi": "4.7 億円",
    "project_cost": "72.0 億円",
    "residual_land": "18.0 億円",
    "irr": "11.8%",
}


def inject_style() -> None:
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light;
            --navy: #102a43;
            --navy-2: #1b465f;
            --ink: #172b3a;
            --muted: #667785;
            --paper: #f5f2eb;
            --surface: #fffdf9;
            --line: #ddd7cc;
            --gold: #b78a4c;
            --gold-soft: #f2e7d5;
            --green: #176f55;
        }

        html, body, [class*="css"] {
            font-family: Inter, "Avenir Next", "Noto Sans JP", -apple-system,
                BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        [data-testid="stAppViewContainer"] {
            color: var(--ink);
            background:
                radial-gradient(circle at 92% 2%, rgba(183, 138, 76, 0.13), transparent 27rem),
                linear-gradient(180deg, #faf8f4 0%, var(--paper) 100%);
        }

        [data-testid="stHeader"] { height: 0; background: transparent; }
        [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer {
            visibility: hidden;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, [data-testid="stMarkdownContainer"] { color: var(--ink); }

        .hero {
            position: relative;
            overflow: hidden;
            min-height: 205px;
            padding: 2.5rem 2.7rem;
            margin-bottom: 1.3rem;
            border-radius: 28px;
            background: linear-gradient(128deg, var(--navy) 0%, var(--navy-2) 100%);
            box-shadow: 0 24px 70px rgba(16, 42, 67, 0.18);
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 360px;
            height: 360px;
            right: -80px;
            top: -190px;
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 50%;
            box-shadow: 0 0 0 70px rgba(255,255,255,0.035),
                        0 0 0 140px rgba(255,255,255,0.02);
        }

        .hero-mark {
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(245, 230, 205, 0.6);
            border-radius: 12px;
            color: #f5e6cd;
            font-family: Georgia, serif;
        }

        .hero-eyebrow {
            color: #d9bd8f;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }

        .hero h1 {
            position: relative;
            z-index: 1;
            margin: 0.55rem 0 0.45rem;
            color: white;
            font-size: clamp(2rem, 4.5vw, 3.4rem);
            font-weight: 650;
            letter-spacing: -0.05em;
        }

        .hero p {
            position: relative;
            z-index: 1;
            max-width: 650px;
            margin: 0;
            color: rgba(255,255,255,0.7);
            font-size: 0.92rem;
        }

        .section-title {
            margin: 2rem 0 0.85rem;
            color: var(--ink);
            font-size: 1.18rem;
            font-weight: 750;
            letter-spacing: -0.02em;
        }

        .section-title span {
            margin-right: 0.6rem;
            color: var(--gold);
            font-size: 0.7rem;
            letter-spacing: 0.15em;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border-color: var(--line) !important;
            border-radius: 20px !important;
            background: rgba(255,253,249,0.92);
            box-shadow: 0 10px 35px rgba(18,38,58,0.045);
        }

        [data-testid="stWidgetLabel"] p {
            color: #3d5363;
            font-size: 0.82rem;
            font-weight: 650;
        }

        [data-testid="stFileUploaderDropzone"] {
            border: 1px dashed #b8a98f;
            border-radius: 14px;
            background: #faf7f0;
        }

        [data-testid="stFileUploaderDropzone"] button,
        .stButton > button,
        .stFormSubmitButton > button {
            min-height: 44px;
            border: 1px solid var(--navy);
            border-radius: 12px;
            background: var(--navy);
            color: white;
            font-weight: 700;
        }

        [data-testid="stFileUploaderDropzone"] button *,
        .stButton > button *, .stFormSubmitButton > button * { color: white !important; }

        [data-testid="stFileUploaderDropzone"] button:hover,
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            border-color: var(--navy-2);
            background: var(--navy-2);
            color: white;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0,1fr));
            gap: 0.8rem;
            margin: 1rem 0 1.4rem;
        }

        .kpi-card {
            min-height: 122px;
            padding: 1.15rem;
            border: 1px solid var(--line);
            border-radius: 17px;
            background: var(--surface);
            box-shadow: 0 8px 26px rgba(18,38,58,0.035);
        }

        .kpi-label {
            color: var(--gold);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.12em;
        }

        .result-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            padding: 1.25rem 1.4rem;
            border: 1px solid var(--line);
            border-left: 5px solid var(--green);
            border-radius: 16px;
            background: var(--surface);
        }

        .result-overline {
            color: var(--muted);
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.15em;
        }

        .result-title {
            margin-top: 0.28rem;
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 750;
        }

        .rank-pill {
            min-width: 92px;
            padding: 0.55rem 0.8rem;
            border-radius: 999px;
            background: #dff2e9;
            color: var(--green);
            text-align: center;
            font-weight: 850;
        }

        .kpi-card { position: relative; }
        .kpi-card::before {
            content: "";
            position: absolute;
            left: 1.15rem;
            top: 0;
            width: 42px;
            height: 2px;
            background: var(--gold);
        }

        .kpi-label { color: var(--muted); letter-spacing: 0.07em; }
        .kpi-value {
            margin-top: 0.75rem;
            color: var(--ink);
            font-size: clamp(1.4rem, 2.4vw, 2rem);
            font-weight: 700;
            letter-spacing: -0.045em;
        }

        .mock-note {
            padding: 0.8rem 1rem;
            margin: 0.7rem 0 1rem;
            border-radius: 12px;
            background: var(--gold-soft);
            color: #745a34;
            font-size: 0.8rem;
            font-weight: 650;
        }

        .summary-line {
            padding: 0.9rem 1rem;
            border: 1px solid var(--line);
            border-radius: 13px;
            background: #faf7f0;
            color: var(--muted);
            font-size: 0.82rem;
        }

        .summary-line strong { color: var(--ink); }

        [data-testid="stDataFrame"] {
            overflow: hidden;
            border: 1px solid var(--line);
            border-radius: 14px;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.2rem;
            padding: 0.3rem;
            border-radius: 14px;
            background: #eae6dd;
        }

        .stTabs [data-baseweb="tab"] {
            height: 42px;
            padding: 0 1rem;
            border-radius: 10px;
        }

        .stTabs [aria-selected="true"] {
            background: var(--surface);
            color: var(--ink) !important;
            box-shadow: 0 3px 10px rgba(18,38,58,0.08);
        }

        .stTabs [data-baseweb="tab-highlight"] { display: none; }

        @media (max-width: 820px) {
            .block-container { padding: 1rem 1rem 3rem; }
            .hero { padding: 1.7rem; min-height: 220px; }
            .kpi-grid { grid-template-columns: repeat(2, minmax(0,1fr)); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_title(number: str, title: str) -> None:
    st.markdown(
        f'<div class="section-title"><span>{number}</span>{html.escape(title)}</div>',
        unsafe_allow_html=True,
    )


def render_value_table(rows: list[tuple[str, str]]) -> None:
    st.dataframe(
        [{"項目": item, "サンプル出力": value} for item, value in rows],
        hide_index=True,
        use_container_width=True,
    )


inject_style()

st.markdown(
    """
    <section class="hero">
        <div class="hero-mark">H</div>
        <div class="hero-eyebrow">Hotel Opportunity Screening</div>
        <h1>ホテル開発 初期評価デモ</h1>
    </section>
    """,
    unsafe_allow_html=True,
)

render_title("01", "案件情報を入力")

with st.form("screening_input"):
    with st.container(border=True):
        top_left, top_right = st.columns([1, 1], gap="large")
        with top_left:
            source_type = st.selectbox(
                "情報ソース",
                ["不動産仲介業者からの物件概要書", "LAND", "その他"],
            )
            uploaded = st.file_uploader("物件概要書（PDF・任意）", type=["pdf"])
            project_name = st.text_input("案件名", value="（仮称）中央区ホテル計画")
        with top_right:
            address = st.text_input("所在地", value="東京都中央区日本橋一丁目")
            land_area = st.number_input("土地面積（㎡）", min_value=0.0, value=1_050.0, step=10.0)
            asking_price = st.number_input("希望価格（億円）", min_value=0.0, value=15.0, step=0.5)

        detail_left, detail_right = st.columns([1, 1], gap="large")
        with detail_left:
            product_type = st.selectbox(
                "想定ホテルタイプ",
                ["未定", "都市型ホテル", "ライフスタイルホテル", "リゾートホテル"],
            )
        with detail_right:
            evaluation_purpose = st.selectbox(
                "評価目的",
                ["取得検討", "事業化検討", "案件比較・優先順位付け"],
            )

        submitted = st.form_submit_button(
            "デモ初期評価を作成",
            type="primary",
            use_container_width=True,
        )

if submitted:
    st.session_state["show_mock_result"] = True
    st.session_state["mock_snapshot"] = {
        "source_type": source_type,
        "project_name": project_name,
        "address": address,
        "land_area": land_area,
        "asking_price": asking_price,
        "product_type": product_type,
        "evaluation_purpose": evaluation_purpose,
        "filename": uploaded.name if uploaded else "未添付",
    }

if not st.session_state.get("show_mock_result"):
    st.stop()

snapshot = st.session_state.get("mock_snapshot", {})
safe_project = html.escape(str(snapshot.get("project_name", "デモ案件")))
safe_address = html.escape(str(snapshot.get("address", "")))

render_title("02", "初期評価サマリー")
st.markdown(
    f"""
    <div class="mock-note">この画面の評価値はデモ用の固定サンプルです。実際の判定ロジックや外部データ取得は行っていません。</div>
    <div class="result-head">
        <div>
            <div class="result-overline">INITIAL SCREENING</div>
            <div class="result-title">{safe_project}　—　{MOCK_RESULT['decision']}</div>
        </div>
        <div class="rank-pill">RANK {MOCK_RESULT['rank']}</div>
    </div>
    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-label">総合スコア</div><div class="kpi-value">{MOCK_RESULT['score']} / 100</div></div>
        <div class="kpi-card"><div class="kpi-label">想定客室数</div><div class="kpi-value">{MOCK_RESULT['rooms']}</div></div>
        <div class="kpi-card"><div class="kpi-label">安定化NOI</div><div class="kpi-value">{MOCK_RESULT['noi']}</div></div>
        <div class="kpi-card"><div class="kpi-label">候補案件内順位</div><div class="kpi-value">{MOCK_RESULT['pipeline_rank']}</div></div>
    </div>
    <div class="summary-line"><strong>{safe_address}</strong>　｜　入力土地面積 {snapshot.get('land_area', 0):,.0f} ㎡　｜　入力希望価格 {snapshot.get('asking_price', 0):,.1f} 億円</div>
    """,
    unsafe_allow_html=True,
)

tab_volume, tab_market, tab_cf, tab_priority = st.tabs(
    ["ボリューム", "ADR・稼働率", "CF", "優先順位"]
)

with tab_volume:
    volume_left, volume_right = st.columns([1, 1], gap="large")
    with volume_left:
        render_value_table([
            ("想定延床面積", MOCK_RESULT["planned_gfa"]),
            ("想定客室数", MOCK_RESULT["rooms"]),
            ("想定平均客室面積", "24 ㎡"),
            ("想定階数", "10 階"),
        ])
    with volume_right:
        render_value_table([
            ("客室・客室階", "68%"),
            ("ロビー・共用部", "10%"),
            ("料飲施設", "8%"),
            ("BOH・設備・動線", "14%"),
        ])

with tab_market:
    market_left, market_right = st.columns([1, 1], gap="large")
    with market_left:
        render_value_table([
            ("想定ADR", MOCK_RESULT["adr"]),
            ("安定稼働率", MOCK_RESULT["occupancy"]),
            ("想定RevPAR", "28,000 円"),
            ("市場ポジション", "アッパーミッドスケール"),
        ])
    with market_right:
        st.dataframe(
            [
                {"近隣ホテル": "Hotel A", "ADR": "32,000円", "稼働率": "78%"},
                {"近隣ホテル": "Hotel B", "ADR": "37,000円", "稼働率": "81%"},
                {"近隣ホテル": "Hotel C", "ADR": "34,000円", "稼働率": "79%"},
            ],
            hide_index=True,
            use_container_width=True,
        )

with tab_cf:
    cf_left, cf_middle, cf_right = st.columns(3, gap="large")
    with cf_left:
        render_value_table([
            ("年間客室売上", MOCK_RESULT["room_revenue"]),
            ("年間総売上", MOCK_RESULT["total_revenue"]),
            ("安定化NOI", MOCK_RESULT["noi"]),
        ])
    with cf_middle:
        render_value_table([
            ("想定総事業費", MOCK_RESULT["project_cost"]),
            ("残余土地価格", MOCK_RESULT["residual_land"]),
            ("入力希望価格", f"{snapshot.get('asking_price', 0):,.1f} 億円"),
        ])
    with cf_right:
        render_value_table([
            ("レバレッジ前IRR", MOCK_RESULT["irr"]),
            ("利益率", "15.2%"),
            ("初期評価", MOCK_RESULT["decision"]),
        ])

with tab_priority:
    priority_left, priority_right = st.columns([1, 1], gap="large")
    with priority_left:
        render_value_table([
            ("総合ランク", MOCK_RESULT["rank"]),
            ("総合スコア", f"{MOCK_RESULT['score']} / 100"),
            ("候補案件内順位", MOCK_RESULT["pipeline_rank"]),
            ("推奨アクション", "詳細検討へ進む"),
        ])
    with priority_right:
        st.dataframe(
            [
                {"順位": 1, "案件": "新宿案件", "スコア": 88, "ランク": "A"},
                {"順位": 2, "案件": "銀座案件", "スコア": 85, "ランク": "A"},
                {"順位": 3, "案件": safe_project, "スコア": 82, "ランク": "A"},
                {"順位": 4, "案件": "渋谷案件", "スコア": 76, "ランク": "B"},
            ],
            hide_index=True,
            use_container_width=True,
        )

render_title("03", "次の検討事項")
with st.container(border=True):
    next_left, next_right = st.columns(2, gap="large")
    with next_left:
        st.markdown(
            """
            **初期評価に含める項目**

            - CF・ADR・ボリューム・稼働率以外に必要な項目
            - 法令、商品企画、運営収支、取得条件の扱い
            """
        )
    with next_right:
        st.markdown(
            """
            **案件の優先順位付け**

            - 収益性、市場性、実現性の評価配分
            - 総合ランクと意思決定フローの定義
            """
        )
