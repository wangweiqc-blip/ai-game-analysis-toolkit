# AI 本地游戏解析工具库

这套工具供 AI 直接调用。用户只需提供游戏文件和目标功能；由 AI 选工具、查参数、写脚本、执行并核对结果。不要让用户打开目录页、选择软件或复制命令。

入口：本目录 `toolkit.cmd`。默认输出 JSON；先按平台缩小范围，避免读入整套清单。

```powershell
& 'F:/GameAnalysisToolkit/toolkit.cmd' route NDS
& 'F:/GameAnalysisToolkit/toolkit.cmd' info ndspy
& 'F:/GameAnalysisToolkit/toolkit.cmd' check ndspy
& 'F:/GameAnalysisToolkit/toolkit.cmd' run ndspy -- 'F:/任务/game.nds'
```

- `route 平台` 给出候选工具及接入次序；`catalog 关键词` 返回机器可读的能力清单；`info ID` 给出绝对路径、输入要求、自动化状态和实际验证记录。完整调用约定见 `docs/AI_USAGE.md`。
- 按 `automation.readiness` 决策：`invocable` 可直接传参；`adapter_required` 需要 AI 接脚本或接口；`code_required` 需要写库调用代码；`gui_only_in_this_bundle` 尚无配置好的自动化入口；`reference_only` 是源码研究。优先选 `preferred_tool`，但继续核对其能力状态。
- `check` 只检查文件与已知运行环境。帮助命令、启动检查、样例解析、目标游戏实测是不同证据；查看 `verification.test`，不能只看 `passed`。
- 先核对游戏版本、引擎和目标，使用本地资料及最小工具组合。只有缺工具、输入不兼容或用户要求更新时才补查官方来源，不重复下载已可用的工具。
- 原始输入保留原样，输出使用 `work/任务名/` 或用户指定目录的绝对路径。执行器默认工作目录是 `work/工具ID/`，不会自动替你区分任务输出。
- 研究源码与输入版本未必一致。先读相关 README，再决定是否构建；游戏、BIOS 和各项目专用编译链不保证齐全。
- 将命令、日志、输入版本及证据位置随任务保留。最终报告已确认规则、未确认项和可复用产物，不能把移植版运行结果当作原版验证。
