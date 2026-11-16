---
name: local-game-analysis
description: 让 AI 直接调用 F 盘本地游戏解析工具库。用于解析游戏文件、提取玩法、追踪指定功能或还原代码；按平台查询机器可读的工具能力，优先复用已安装工具和本地研究，避免重复查找下载。
---

工具库位于 `F:/GameAnalysisToolkit`，供 AI 使用。用户只需给游戏路径和目标功能；由 AI 选工具、查参数、编写必要的脚本、执行并验证，不要求用户打开目录网页或手动操作工具菜单。

先读根目录 `AGENTS.md`，再按平台查询候选路线，只加载所需条目：

```powershell
& 'F:/GameAnalysisToolkit/toolkit.cmd' route NDS
& 'F:/GameAnalysisToolkit/toolkit.cmd' info ndspy
& 'F:/GameAnalysisToolkit/toolkit.cmd' check ndspy
& 'F:/GameAnalysisToolkit/toolkit.cmd' run ndspy -- 'F:/游戏副本/game.nds'
```

不知道工具 ID 时用 `catalog 关键词`。这些查询返回 UTF-8 JSON；`info` 给出版本、输入要求、绝对路径、`invoke_argv` 以及验证记录。具体返回约定和运行环境见 `docs/AI_USAGE.md`，无需先读整份安装清单。

按 `automation.readiness` 判断下一步：

- `invocable`：可传参调用，先查该版本的帮助。
- `adapter_required`：AI 需先接脚本或调试接口，做最小验证。
- `code_required`：AI 需用本地开发库写调用程序。
- `gui_only_in_this_bundle`：优先查 `preferred_tool`；尚未配置无人值守解析。
- `reference_only`：研究源码，先核对游戏版本，不能当成已构建工具。

优先调用命令行入口，例如 `ilspycmd`、`ghidra-headless`、`objdiff-cli`；需要脚本时使用工具库 `python` 或 `dotnet` 入口复用依赖。输入输出使用绝对路径，产物放在 `work/任务名/` 或用户指定目录，原始游戏保持原样。执行权限限制与工具缺失分开处理；F 盘写入需要时使用受支持的权限申请途径，不重新下载。

先核对输入版本，再选最小工具组合。查看 `verification.test`，不要将帮助、启动或合成样例通过当成目标游戏验证。TH08 复用 `docs/TH08_RESEARCH.md` 与补充解析器；其他研究项目按 `info` 的 `local_folder` 定位并核对版本。

只有本地缺少适配工具、输入不兼容或用户要求更新时才补查官方研究与下载。完成任务时交付规则或代码证据、运行核对结果及产物位置；仍未确认的部分单列。游戏文件、主机 BIOS 和各项目专用编译链不保证随库齐备。
