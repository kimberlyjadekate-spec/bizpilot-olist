# BizPilot B.1 · 商家履约调查工作台

运行 `python -m pip install -r requirements.txt`，用 `python -m streamlit run app.py` 启动。

部署到 Streamlit Community Cloud 时，选择BizPilot 的 GitHub 仓库及 `app.py` 入口。推荐使用 Python 3.12。

「Olist 真实数据」默认打开 Seller Investigation Agent 的五轮已验证案例，可切换调查总览与逐轮证据，并下载原始 SQL 及参数。其余经营页面使用明确标注的合成数据。公开版只读取随包提供的案例，保留本地版的 Mac 启动器用于实时 Olist 导入与 Ollama 复核。

真实数据来源为 [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)。

应用源码和可复核案例位于 `bizpilot_source.zip`，解压即可审阅。
