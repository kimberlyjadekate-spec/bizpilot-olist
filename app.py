"""Public BizPilot workbench for the Olist fulfillment case."""

from pathlib import Path
import sys
from tempfile import mkdtemp
from zipfile import ZipFile

import streamlit as st

st.set_page_config(
    page_title="BizPilot · Olist 履约运营",
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

from bizpilot.seller_overview import render_case_overview, show_sql
from bizpilot.seller_ui import _public_case, _round_view

case_path = source / "public_case" / "olist_seller_verified.json"
case = _public_case(case_path)
rounds = {row["round"]: row for row in case["rounds"]}
st.markdown(
    """<style>
    [data-testid="stAppViewContainer"]{background:#f3f7fa}
    [data-testid="stHeader"]{background:transparent}
    .block-container{max-width:1160px;padding-top:1rem}
    .biz-hero{padding:28px 32px;border-radius:18px;background:#102b40;color:#eef9fd}
    .biz-hero h1{color:white;padding:4px 0;font-size:clamp(1.7rem,4vw,2.4rem)}
    .biz-hero p{margin:0;color:#c3e3ed}
    .biz-brand{font-size:.85rem;color:#a1e6ed;font-weight:700}
    [data-testid="stMetric"]{background:#fff;border-radius:12px}
    </style>
    <div class="biz-hero"><div class="biz-brand">BizPilot · Olist 公开数据案例</div>
    <h1>商家履约运营工作台</h1>
    <p>发现异常、定位履约环节、生成运营核查工单。</p></div>""",
    unsafe_allow_html=True,
)
st.caption(f"商家 {case['seller_id']} · Olist 历史订单 · 只读案例")
overview, decision, audit = st.tabs(["履约总览", "调查助手", "证据审计"])


def evidence(number, key):
    return rounds[number]["evidence"][key]


def select_row(number, key, field, value):
    return next(row for row in evidence(number, key)["rows"] if row[field] == value)


with overview:
    render_case_overview(case)

with decision:
    st.subheader("这家商家应该先查什么？")
    question = st.radio(
        "选择运营问题",
        ["是否需要上调核查优先级？", "应该从哪个履约环节查起？", "如何处理低评分信号？"],
    )
    st.caption("助手按案例中的 SQL 结果和判断规则组织建议。工单由运营人员审核。")

    if question == "是否需要上调核查优先级？":
        peer = select_row(3, "peer", "metric", "late_rate")
        gap = 100 * (peer["target_mean"] - peer["peer_mean"])
        finding = (
            f"目标延迟率 {peer['target_mean']:.2%}，标准化同行 {peer['peer_mean']:.2%}，"
            f"差 {gap:+.2f} 个百分点。匹配覆盖 {peer['matched_orders']:,}/{peer['target_orders']:,} 笔。"
        )
        verdict = rounds[3]["judgments"]["seller"]
        action = "由商家运营复核延迟订单清单，与物流运营确认交接后异常是否集中。"
        followup = "记录可归类的延迟订单比例，持续跟踪同口径延迟率与同行差。"
        refs = [(3, "peer"), (3, "strata"), (1, "risk")]
    elif question == "应该从哪个履约环节查起？":
        pre = select_row(3, "peer", "metric", "pre_days")
        post = select_row(3, "peer", "metric", "transit_days")
        finding = (
            f"与严格匹配同行相比，批准至交接均值差 {pre['target_mean']-pre['peer_mean']:+.2f} 天，"
            f"交接至签收均值差 {post['target_mean']-post['peer_mean']:+.2f} 天。"
        )
        verdict = rounds[3]["judgments"]["stage"]
        action = "由物流运营按收货州查看延迟订单，关联交接扫描、运输轨迹和签收异常记录。"
        followup = "记录轨迹覆盖率与异常环节，按路线检查交接后 P50、P90 和承诺逾期率。"
        refs = [(2, "timeline"), (3, "peer"), (2, "focus")]
    else:
        samples = {row["transit_group"]: row for row in evidence(5, "counter")["rows"] if row["late"] == 0}
        long = samples["long_7plus"]
        short = samples["short_under_7"]
        shared = select_row(5, "contrast", "scope", "post_delivery")
        finding = (
            f"按时交付中，长配送低评分率 {long['low_rate']:.2%}，短配送 {short['low_rate']:.2%}。"
            f"仅签收后评价的同行共同分层覆盖 {shared['coverage']:.2%}。"
        )
        verdict = "优先核查承诺逾期与评价时点"
        action = "由客户体验团队按签收前后复核差评，结合承诺到货日和实际签收日抽查。"
        followup = "分别跟踪按时与逾期订单的签收后低评分率和样本量。"
        refs = [(4, "review"), (5, "counter"), (5, "contrast")]

    st.markdown(f"### {verdict}")
    st.write(finding)
    st.markdown("**下一步核查**")
    st.write(action)
    st.markdown("**跟踪指标**")
    st.write(followup)
    st.caption("建议来自历史样本。具体线路、承运商及异常签收原因需用承运记录核实。")

    source_items = [evidence(number, key) for number, key in refs]
    with st.expander("查看关联证据与 SQL"):
        for item in source_items:
            st.markdown(f"**{item['title']} · {item['id']}**")
            st.dataframe(item["rows"], hide_index=True)
            show_sql(item)
    ticket = "\n\n".join([
        f"# Olist 履约核查工单草稿\n商家 {case['seller_id']}",
        f"## {question}\n{verdict}", f"## 证据\n{finding}",
        f"## 核查动作\n{action}", f"## 跟踪指标\n{followup}",
        "## 证据编号\n" + "、".join(item["id"] for item in source_items),
    ])
    st.download_button("下载运营核查工单草稿", ticket, "olist-fulfillment-review.md", "text/markdown")

with audit:
    st.subheader("查看五轮调查的计算口径")
    selected = st.selectbox(
        "调查轮次", list(rounds), format_func=lambda number: f"R{number:02} · {rounds[number]['title']}"
    )
    _round_view(rounds[selected])
    st.download_button(
        "导出全部证据与 SQL", case_path.read_bytes(), "olist_seller_verified.json", "application/json"
    )
    st.caption("数据来源：[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)")
