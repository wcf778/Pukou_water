# Pukou_water
第三方homeassistant插件，抓取浦口水务API

这个集成允许您在 Home Assistant 中监控南京浦口水务的水费和水表数据。它提供了当前和上个月的用水量、水费以及水价信息。

## 功能特点
- 显示当前月份用水量
- 显示当前月份水费
- 显示上个月用水量
- 显示上个月水费
- 显示当前水价
- 支持自定义更新间隔
- 支持能源仪表板集成

Prerequisition：

手机抓包程序抓取浦口水务WX API：

   - OpenID：
   - 户号：您的水表户号
   - JSLUID：



## 安装方法

### 方法 1: HACS（推荐）

1. 确保您已经安装了 [HACS](https://hacs.xyz/)
2. 在 HACS 中添加自定义仓库：
   - 仓库地址：`https://github.com/wcf778/Pukou_water`
   - 类别：集成
3. 在 HACS 中搜索 "Pukou water" 并安装

### 方法 2: 手动安装

1. 下载此仓库
2. 将 `nanjing_water` 文件夹复制到您的 Home Assistant 的 `custom_components` 目录
3. 重启 Home Assistant

## 配置

### 通过 UI 配置（推荐）

1. 在 Home Assistant 中，转到 **配置** > **集成**
2. 点击右下角的 **添加集成**
3. 搜索 "Nanjing Water"
4. 输入以下信息：
   - OpenID：从浦口水务微信公众号获取
   - 户号：您的水表户号
   - JSLUID：从浦口水务微信公众号获取
   - 更新间隔：数据更新间隔（小时），默认为 12 小时

### 通过 YAML 配置

```yaml
# configuration.yaml
nanjing_water:
  openid: "your_openid"
  account: "your_account_number"
  jsluid: "your_jsluid"
  update_interval: 12
```

## 传感器

安装后，以下传感器将被创建：

| 传感器名称 | 描述 | 单位 | 设备类型 |
|------------|------|------|----------|
| 当前用水量 | 当前月份用水量 | m³ | water |
| 当前水费 | 当前月份水费 | 元 | monetary |
| 上月用水量 | 上个月用水量 | m³ | water |
| 上月水费 | 上个月水费 | 元 | monetary |
| 水价 | 当前水价 | 元/m³ | monetary |

## 能源仪表板集成

此集成支持 Home Assistant 的能源仪表板。用水量传感器会自动显示在能源仪表板的水表部分。

## 故障排除

如果传感器显示为 "未知" 状态，请检查：

1. OpenID 和 JSLUID 是否有效
2. 户号是否正确
3. 网络连接是否正常
4. 查看 Home Assistant 日志以获取详细错误信息

## 日志

要启用详细日志记录，请在 `configuration.yaml` 中添加：

```yaml
logger:
  default: info
  logs:
    custom_components.nanjing_water: debug
```

## 贡献

欢迎提交问题和改进建议！

## 许可证

MIT License
