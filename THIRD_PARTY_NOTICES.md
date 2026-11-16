# 第三方工具与来源

本工具库聚合并调用各上游工具，没有将其重新授权。每个工具与研究项目的许可、版权与依赖声明以原包内文件及上游为准。版本、下载 URL 和 SHA-256 见 `toolkit.json`。

# Third-party notices

## TH08 reconstruction: selected geometric predicates

本项目历史研究中的 `th08-rules.js`（此工具库不包含该游戏模块） adapts the ordinary-bullet, graze, and rotated-laser geometric
predicates from `src/Player.cpp` in N0zoM1z0/th08 and its TH08 Web fork.
This is a JavaScript adaptation of a small subset, not a complete port or a
claim of bit-exact / frame-exact original-game equivalence.

- https://github.com/N0zoM1z0/th08-web/tree/e3485ab9a9af3b5a90ce51841667bbdf5a867e5c
- https://github.com/N0zoM1z0/th08/tree/d3bfd9af15b96745da135245e13a345e570d9c00
- Function addresses: 0x44a230 (bullet collision), 0x44a470 (graze),
  0x44a6a0 (laser collision).
- History includes work from https://github.com/GensokyoClub/th08.

MIT License

Copyright (c) 2025 KSS
Copyright (c) 2026 N0zoM1z0

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Touhou Toolkit: archive inspection helper

`helpers/inspect_th08.py` adapts the PBGZ archive/decryption algorithm from
https://github.com/thpatch/thtk (thtk/thdat08.c and thtk/thcrypt.c).
The LZSS stream and plain-entry fallback were also checked against TH08 Web's
src/pbg/Lzss.cpp and src/Global.cpp, under the MIT license above.

Redistribution and use in source and binary forms, with
or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain this list
   of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce this
   list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.


## 工具来源

- Mesen Community Edition 2.2.1: https://github.com/nesdev-org/MesenCE
- mGBA 0.10.5: https://github.com/mgba-emu/mgba
- ndspy 4.2.0: https://github.com/RoadrunnerWMC/ndspy
- DeSmuME release_0_9_13: https://github.com/TASEmulators/desmume
- BizHawk 2.11.1: https://github.com/TASEmulators/BizHawk
- PCSX-Redux 31729.20261116.32.x64: https://github.com/pcsx-redux/pcsx-redux
- splat 0.50.1: https://github.com/ethteck/splat
- PCSX2 v2.8.2: https://github.com/PCSX2/pcsx2
- PPSSPP v1.20.4: https://github.com/hrydgard/ppsspp
- Dolphin 2609b: https://github.com/dolphin-emu/dolphin
- AssetRipper 2.0.0: https://github.com/AssetRipper/AssetRipper
- ILSpy／ILSpyCmd v11.2: https://github.com/icsharpcode/ILSpy
- Cpp2IL 2022.0.7: https://github.com/SamboyCoding/Cpp2IL
- FModel nov-2026: https://github.com/4sval/FModel
- CUE4Parse 1.2.2.202611: https://github.com/FabianFG/CUE4Parse
- GDRE Tools v2.7.4: https://github.com/GDRETools/gdsdecomp
- QuickBMS 0.12: https://aluigi.altervista.org/quickbms.htm
- Ghidra Ghidra_12.2_build: https://github.com/NationalSecurityAgency/ghidra
- x64dbg 2026.05.27: https://github.com/x64dbg/x64dbg
- Apktool v3.0.3: https://github.com/iBotPeaches/Apktool
- JADX v1.5.6: https://github.com/skylot/jadx
- Touhou Toolkit／thtk 12: https://github.com/thpatch/thtk
- TH08 Web e3485ab9a9af3b5a90ce51841667bbdf5a867e5c: https://github.com/N0zoM1z0/th08-web
- pret／pokeemerald 9103e529c2fbdd7add4a1ff3350c6c1f92112c42: https://github.com/pret/pokeemerald
- pret／pokeheartgold 4e9563397ab4e5c407271472935f9e270ac6a804: https://github.com/pret/pokeheartgold
- n64decomp／sm64 9921382a68bb0c865e5e45eb594d9c64db59b1af: https://github.com/n64decomp/sm64
- objdiff v3.8.3: https://github.com/encounter/objdiff

运行环境：CPython、Eclipse Temurin OpenJDK、Microsoft .NET、7-Zip，各自许可随运行环境保留。Python/NuGet 依赖的声明保留在其包目录。

不包含原始商业游戏文件、ROM 或 BIOS。
