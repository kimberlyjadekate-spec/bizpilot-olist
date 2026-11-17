"""Public BizPilot Olist investigation."""

import html
from pathlib import Path
import sys
from tempfile import mkdtemp
from zipfile import ZipFile

import streamlit as st

st.set_page_config(
    page_title="BizPilot · Olist 履约调查",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource(show_spinner=False)
def unpack_source(archive_path):
    root = Path(mkdtemp(prefix="bizpilot-"))
    with ZipFile(archive_path) as archive:
        archive.extractall(root)
    sys.path.insert(0, str(root))
    return root


bundle = Path(__file__).with_name("bizpilot_source.zip")
source = unpack_source(bundle)

from bizpilot.seller_ui import public_seller_workspace


def e(value):
    return html.escape(str(value), quote=True)


def header(kicker,title,subtitle):
    st.markdown(f'<div class="hero"><div class="eyebrow">{e(kicker)}</div><h1>{e(title)}</h1><p>{e(subtitle)}</p></div>',unsafe_allow_html=True)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root{--navy:#102b40;--teal:#0b8395;--line:#dce8f0;--sub:#667f93}
html,body,[data-testid="stApp"]{font-family:'DM Sans','PingFang SC',-apple-system,sans-serif}
[data-testid="stAppViewContainer"]{background:linear-gradient(160deg,#f5faff,#edf5fb 64%,#f7fbff)}
[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1500px;padding-top:1rem;padding-bottom:3rem}
section[data-testid="stSidebar"]{background:linear-gradient(168deg,#0e2a40,#143552 70%,#102a41);border-right:0}
section[data-testid="stSidebar"] *{color:#e9f6fb}
section[data-testid="stSidebar"] small{color:#b7d8e4!important}
section[data-testid="stSidebar"] textarea,section[data-testid="stSidebar"] input{background:#284b64!important;color:white!important;border:1px solid #507288!important}
[data-testid="stMetric"]{background:#fff;border:1px solid var(--line);border-radius:16px;min-height:118px;padding:17px 19px;box-shadow:0 9px 24px #1747600a}
[data-testid="stMetricValue"]{color:#122f42;font-size:29px;font-weight:800}
[data-testid="stMetricLabel"]{font-size:12px;font-weight:700;color:#647c8f}
.stButton>button{border-radius:12px;min-height:44px;font-weight:750;transition:all .16s ease;border:1px solid #c7dbe7;box-shadow:0 3px 12px #0e3d580a}
section[data-testid="stSidebar"] .stButton>button{background:#203f56!important;color:#eefaff!important;border-color:#466c82!important}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:linear-gradient(115deg,#0d718a,#1196a4)!important;border-color:transparent!important}
.stButton>button:hover{border-color:#0d879b;color:#0b7085;transform:translateY(-1px)}
.stButton>button[kind="primary"],.stFormSubmitButton>button[kind="primary"]{background:linear-gradient(115deg,#0d718a,#1196a4);color:#fff;border:0;box-shadow:0 5px 16px #0b8f9c2a}
[data-testid="stDataFrame"]{border-radius:12px;overflow:hidden}
[data-testid="stTabs"] [data-baseweb="tab-list"]{gap:10px;flex-wrap:wrap}
[data-testid="stTabs"] [data-baseweb="tab"]{background:white;border:1px solid #d9e5ec;border-radius:12px;padding:10px 18px!important;font-weight:750}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"]{background:#116f89!important;color:white!important}
[data-testid="stTabs"] [data-baseweb="tab-highlight"],[data-testid="stTabs"] [data-baseweb="tab-border"]{display:none}
.logo{font-size:31px;font-weight:850;letter-spacing:-1.3px;color:#fff;margin-bottom:8px}.logo span{color:#62d8e5}
.topbar{display:flex;justify-content:space-between;align-items:center;margin:2px 0 18px}.topbar strong{font-size:21px;color:#163b50;letter-spacing:-.5px}.topbar span{font-size:11px;letter-spacing:1.4px;color:#557c90;font-weight:700}
.hero{position:relative;overflow:hidden;background:linear-gradient(112deg,#102e49 0%,#135775 62%,#087e92 100%);padding:36px 42px;border-radius:22px;margin:4px 0 22px;color:white;box-shadow:0 18px 38px #0d496223}
.hero:after{content:'';position:absolute;right:-75px;top:-70px;width:390px;height:390px;border-radius:47%;border:1px solid #8ae9f55c;box-shadow:0 0 0 45px #8ae9f509,0 0 0 90px #c3f8fe0b;transform:rotate(25deg)}
.hero .eyebrow{letter-spacing:2.7px;font-size:11px;font-weight:800;color:#99f1ff}
.hero h1{position:relative;z-index:1;font-size:35px;font-weight:850;letter-spacing:-1px;line-height:1.4;margin:11px 0 7px;color:white}
.hero p{position:relative;z-index:1;color:#def0f9;font-size:14px;line-height:1.8;max-width:960px}
.bp-card{border:1px solid #dbe8ef;border-radius:17px;background:#fff;padding:23px;margin:6px 0 15px;box-shadow:0 7px 23px #163c5009}
.bp-card h3{font-size:18px;color:#17394d;margin:3px 0 9px;font-weight:800}.bp-card p{font-size:13px;color:#627c8e;line-height:1.8;margin:0}
.eyebrow{color:#5e92a6;letter-spacing:1.8px;font-weight:850;font-size:10px;margin-bottom:9px}
.sectiontitle{margin:22px 0 13px;font-size:19px;font-weight:800;color:#173a50}
.chip{display:inline-block;padding:5px 11px;background:#e7f4f6;color:#147184;border-radius:22px;font-size:11px;font-weight:800;margin-right:7px}
.chip.warn{color:#ae654a;background:#fff0e5}
.flowbar{background:white;border:1px solid #dbeaf1;border-radius:17px;padding:16px 20px;line-height:2.8;color:#1b4b60;margin-bottom:20px;font-size:12px;font-weight:750;box-shadow:0 7px 24px #123b520a}
.feature-teal,.feature-blue,.feature-violet,.feature-green{border-radius:18px;padding:25px 28px 17px;color:white;min-height:155px;box-shadow:0 12px 24px #103e5019}
.feature-teal{background:linear-gradient(110deg,#02768d,#07aeb5)}.feature-blue{background:linear-gradient(110deg,#1761b0,#358ed2)}.feature-violet{background:linear-gradient(110deg,#5e55bf,#8e74c9)}.feature-green{background:linear-gradient(110deg,#087e7c,#18ada0)}
.feature-heading{font-size:25px;font-weight:800;margin-bottom:8px}.feature-sub{font-size:13px;line-height:1.7;color:#f4feff}
.incident{background:#fff;border:1px solid #d9e8ef;border-left:4px solid #e08a52;border-radius:13px;padding:18px 21px;margin:8px 0}
.incident strong{color:#1c3c50;font-size:16px}.incident small{display:block;color:#688195;margin-top:8px;line-height:1.6}
.foot{margin-top:28px;color:#8aa1ac;font-size:11px}
</style>""",unsafe_allow_html=True)

header('OLIST · SELLER INVESTIGATION', 'BizPilot · Olist 履约调查',
       '基于真实公开订单的五轮商家履约调查。')
public_seller_workspace(source / 'public_case' / 'olist_seller_verified.json')
