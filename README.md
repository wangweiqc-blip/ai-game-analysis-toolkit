# AI 游戏解析工具库

让 AI 在本地选择并调用游戏解析工具：提取玩法、追踪指定功能、还原局部代码，再运行核对并制作原型。

这是面向 AI 的工具库。使用者提供游戏文件路径与研究目标，AI 负责选择工具、读取参数、编写必要脚本并执行。

## 下载完整本地库

完整 Windows x64 运行包见 [Releases](https://github.com/wangweiqc-blip/ai-game-analysis-toolkit/releases/latest)。仓库代码不包含可执行程序，直接下载 GitHub 的 Source code 不能替代完整运行包。

下载同一版本的全部 `GameAnalysisToolkit-win-x64.7z.*` 分卷到同一目录，用 7-Zip 打开 `.001` 并解压。建议解压到 `F:/`，得到 `F:/GameAnalysisToolkit`。压缩包包含工具、Python、Java、.NET、NuGet 与 Python 依赖，以及本地研究源码；解压后日常调用无需重复安装下载。

`SHA256SUMS.txt` 与 `release-manifest.json` 提供各分卷的大小和校验值。展开后约需 4 GB，解压期间还需容纳下载的分卷。包内保留原工具自带的许可与说明，原始下载包的重复备份不再打入运行包。

## 给 AI 的入口

在 Codex 中可使用随包的 `skills/local-game-analysis`；其他能读取文件并执行命令的 AI 先读解压目录的 `AGENTS.md`。

示例任务：

> 先读 F:/GameAnalysisToolkit/AGENTS.md。用本地工具分析【游戏路径】，研究【目标功能】，并在【项目路径】实现一个可运行原型。

```powershell
& 'F:/GameAnalysisToolkit/toolkit.cmd' route NDS
& 'F:/GameAnalysisToolkit/toolkit.cmd' catalog NDS
& 'F:/GameAnalysisToolkit/toolkit.cmd' info ndspy
& 'F:/GameAnalysisToolkit/toolkit.cmd' check ndspy
& 'F:/GameAnalysisToolkit/toolkit.cmd' run ndspy -- 'F:/游戏副本/game.nds'
```

如果安装到别处，将示例中的根路径替换成实际解压目录；执行器内部路径由自身位置解析。返回格式与自动化能力说明见 [AI 调用约定](docs/AI_USAGE.md)。

## 覆盖范围

23 项工具与 4 份主要研究源码，包含 FC/SFC/GB/GBA/NDS/N64/MD、PS1/PS2/PSP、GameCube/Wii、Unity、Unreal、Godot、Android、东方与通用二进制分析。别名和运行环境合计 39 个可查询条目。

工具包括 Mesen CE、mGBA、ndspy、DeSmuME、BizHawk、PCSX-Redux、splat、PCSX2、PPSSPP、Dolphin、AssetRipper、ILSpy、Cpp2IL、FModel、CUE4Parse、GDRE、QuickBMS、Ghidra、x64dbg、Apktool、JADX、thtk、objdiff。研究源码包括 TH08 Web、pokeemerald、pokeheartgold、sm64。

`toolkit.json` 锁定实际安装版本、来源、命令和测试记录；`ai-config.json` 标注各工具能否直接调用、是否需要脚本或开发库接入。已安装不等于所有平台都已配置全自动解析。

## 已验证范围

已检查本地文件与运行环境，验证机器查询接口、部分启动/帮助命令、合成 NDS 文件读取、合成资源包解包、本地样例 DLL 反编译与 Ghidra 样例导入。证据见 [logs](logs)。这些测试不代表任意游戏都兼容；AI 需对实际输入和目标功能运行核对。

不随包提供商业游戏、ROM、BIOS 或用户的原始游戏资源。第三方工具和研究源码分别遵循自身许可与使用条件，来源见 [第三方说明](THIRD_PARTY_NOTICES.md)。
