# BizPilot · Olist 履约运营工作台

[打开公开工作台](https://bizpilot-olist.streamlit.app/)

本项目以 Olist 公开历史订单为案例，面向商家运营与物流团队。通过履约总览、调查助手和证据审计，判断延迟是否异常、定位优先核查环节，并生成运营核查工单草稿。

公开版按已验证 SQL 证据和规则生成建议。每轮提供查询参数、样本口径与完整 JSON。路线或承运商层面的原因需要承运记录核实。

数据来源：[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)。

本地运行：

`python -m pip install -r requirements.txt`，然后执行 `python -m streamlit run app.py`。
