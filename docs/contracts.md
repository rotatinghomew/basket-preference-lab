# 资料与接口约定

## 领域记录
一个 household 有多次 visit，chosen 是按 products 顺序的整数件数。price_lower/upper 由称重精度给出，为共同可解释价格的允许区间，并非随机重采样区间。opportunities 记录当次真实库存、预算、袋容积和整篮优惠。POST /quote 传 visit、basket，返回可实现性、折扣后 payable_yuan 与机会版本，预算充足不代表满足库存与容积。POST /detail 传 visit 返回机会集合规则。整篮优惠有金额触发点，不能把每件价格均摊后假设线性预算；跨次比较使用同一 household。



## 冻结来源
GET /manifest 返回 release、digest、row_count、metadata。digest 对完整领域资料按 JSON 键排序、紧凑分隔和 UTF-8 计算 SHA-256。
GET /records 及后续 cursor 请求、POST /quote、POST /detail 都要求 If-Match 等于清单 release，否则返回 412。
游标仅用于所属版本，客户端不能自行猜测页数。source 进程在启动时固定加载 data/release.json。
业务请求成功返回 release、request、result；业务值非法返回 422，游标不合法返回 400，未知地址返回 404。
仅有资料概览与领域核价，不含方案选型、统计推断或预测能力。

## 已有消费接口
GET /health 返回 status=ok；GET /overview 返回 release、digest 与描述性 overview。
POST /quotes 的 JSON 为 release 和 request，结果转发来源方回执。
POST /reports 接受 release、source_digest、kind、result、receipts，返回内容寻址 id；相同内容重复保存得到同一 id。
GET /reports/{id} 返回 id 与原 payload，重启后仍可读，不重算来源资料；不存在时 404。
这些接口的字段和返回类型保持兼容，新增业务可以扩展而不改变旧档案内容。
数据数值保留原始精度；只有领域服务中已标注的金额按对应货币规则处理。
