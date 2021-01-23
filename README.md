# JIT-Cloud-shield
从零开始设计并构建“金科云盾”网站防护系统。自行构建web网站（敏感请求包括：注册、登录、详情、支付等），使用Nginx实现反向代理，负载均衡，并统一日志格式。模拟慢连接、DDOS、撞库、爆破等恶意攻击并统一数据格式，Logstash过滤收集有效日志，日志分类归档检索ES。日志量比较大，HDFS保存三天，快速响应，具有很好的 HA。针对各模块采取相应的分析算法，其中尤其关注敏感请求，IP 信誉库、ip+cookie等结合。分析不同种类的攻击数据的特征，提取特征字段。完成深度学习平台的搭建，并导入相关恶意访问识别算法LSTM，完成对于样本数据的模型训练以及功能测试，能够查看到训练的过程以及测试的结果。通过脚本，每半分钟“巡逻”一次，让模型对数据实时地进行识别预测，得到识别结果并用Kibana可视化展示。针对实时的识别结果立即给于封杀IP、形成黑名单。在给出防御措施后，需及时存储相关防御日志，要求详细可溯源，并通过邮件等方式通知相关安全人员。可进行视化的展示、Zabbix性能监控、调试等工作。整个系统通过脚本串联，从检测到攻击到更新黑名单、封杀、收到邮件的响应时间在4秒左右。