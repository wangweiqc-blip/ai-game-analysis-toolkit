# AI 调用约定

默认操作方式是 AI 通过命令行执行。`index.html` 和图形启动菜单只是备用浏览入口，不是分析任务的前置步骤。

## 发现与选择

| 命令 | 返回内容 |
|---|---|
| `toolkit.cmd route NDS` | JSON：平台候选路线、工具 ID、下一步；不自动识别文件格式 |
| `toolkit.cmd catalog NDS` | JSON：匹配工具的版本、能力、文件状态、验证级别 |
| `toolkit.cmd info ndspy` | JSON：单个工具的完整记录、绝对路径、调用参数数组、输入条件 |
| `toolkit.cmd check ndspy` | JSON：入口文件及已知运行环境是否存在；不启动程序 |
| `toolkit.cmd check` | JSON：检查全部条目；日常只检查选中的工具即可 |
| `toolkit.cmd run ID -- 参数` | 执行已有工具，原样转交其输出和退出码 |

无参数时等同于 `catalog`；日常优先带平台或关键词，以减少上下文占用。`list`、`doctor` 继续保留为人工可读的兼容入口。

`info` 的 `invoke_argv` 是传给子进程的参数数组前缀，追加工具参数即可；它经过统一执行器配置本地 Python、Java、.NET 与 NuGet 缓存。`resolved_command` 仅展示真实底层命令，直接执行时可能缺少这些环境配置。

目录路径以查询结果为准，所有输入和输出参数使用绝对路径。批处理入口不支持包含 `& | < > ^ % !` 或换行的参数；遇到这种路径时，将输入复制到任务目录的普通路径中使用。

查询命令的 stdout 是 UTF-8 JSON。`check` 返回码 0 表示所查文件齐全，1 表示缺文件；`info/check` 不认识工具 ID 时输出 JSON 错误并返回 2。查询无匹配项时返回空数组。`run` 的输出格式由上游工具决定，不统一保证为 JSON；由 AI 捕获 stdout、stderr、退出码，并按任务设置超时。工具未提供命令入口时返回 2。

## 读取能力状态再执行

| `automation.readiness` | AI 下一步 |
|---|---|
| `invocable` | 查本地帮助，准备所需输入和输出路径，直接调用 |
| `adapter_required` | 工具已安装，AI 需先接脚本或公开调试接口，并验证一次最小调用 |
| `code_required` | 读取本地开发库文档和模板，由 AI 编写调用程序 |
| `gui_only_in_this_bundle` | 先看 `preferred_tool`；没有合适替代时再按任务接调试或 UI 操作流程 |
| `reference_only` | 先读源码、核对版本，需要运行时再准备该项目依赖 |

`invocable` 只表示已有可调用入口，不表示所有输入都兼容。`availability.files_present` 只覆盖文件和已知运行环境，不能证明插件、BIOS、游戏专用数据都齐备。

`verification.test` 区分已做的实际测试。例如 `process-startup` 只是启动，`cli-help-or-version` 只是帮助/版本命令，`synthetic-*` 是人工样例；任何一个都不能替代目标游戏验证。GUI 启动测试中的 `stopped_after_timeout: true` 表示检查后主动结束进程。

## 最小可调用例子

```powershell
# 路线与能力查询
& 'F:/GameAnalysisToolkit/toolkit.cmd' route NDS
& 'F:/GameAnalysisToolkit/toolkit.cmd' info ndspy

# 库内样例：读取文件表并输出 JSON，不修改输入
& 'F:/GameAnalysisToolkit/toolkit.cmd' run ndspy -- 'F:/GameAnalysisToolkit/work/smoke-samples/test.nds'

# 查看代码反编译器参数
& 'F:/GameAnalysisToolkit/toolkit.cmd' run ilspycmd -- --help

# 自己编写的脚本使用库内 Python，复用 ndspy 等已安装依赖
& 'F:/GameAnalysisToolkit/toolkit.cmd' run python -- 'F:/GameAnalysisToolkit/work/任务/analyze.py'
```

执行器只设置子进程环境，不更改全局 PATH。会创建 `work/工具ID/` 作为默认工作目录；任务日志和导出文件另行指定到 `work/任务名/`。F 盘写入被沙盒拦截时，使用当前环境提供的权限申请途径；不要误判工具缺失或另装一份。

## 接入具体游戏

先识别用户给的文件和版本，再按目标选路线。实际使用中由 AI 补上目标格式的参数或脚本，不向用户转交工具选型工作。仅在缺少游戏路径、目标不明确或关键输入确实缺失时询问。

平台与入口映射在 `ai-config.json`；实际安装版本和验证记录在 `toolkit.json`。按 `info` 返回的 `local_docs` 逐项读取相关本地材料，其他研究源码位置见 `local_folder`。TH08 先读 `docs/TH08_RESEARCH.md`，避免重复碰到已记录的汉化版 DAT 兼容问题。

每个分析任务保留输入版本/哈希、所用命令与脚本、输出文件及观察证据。面向用户交付目标功能的结论和原型产物，而不是只返回一张工具清单。
