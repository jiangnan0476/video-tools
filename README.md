# video-tools（本地工具，不改上游 story-studio）

依赖：python3 + Pillow，ffmpeg，字体 /usr/share/fonts/opentype/noto/NotoSansCJK-*.ttc。

| 脚本 | 作用 |
|---|---|
| `subs.py script.json timeline.json out.ass` | 1080×1920 ASS；按标点切分，短句只与同句下一短句合并（不跨 。！？），按实测字宽断行（安全宽 900px，最多 2 行/条），时长按字数分配 |
| `loudnorm2.py in out` | 两遍 loudnorm（测量→linear=true），默认 I=-14 TP=-1.5；视频则拷贝画面只重编音频；打印成品实测值，超出 ±0.5 退出码 1 |
| `check_shots.py storyboard.json` | 分镜类型轮换检查（规则见 STORYBOARD.md） |
| `cards.py spec.json` / `from cards import card` | 信息卡/数字卡，三种主题，超宽自动缩字号，侵入字幕区告警 |

推荐流水线：
1. 写 storyboard.json → `check_shots.py`；数字卡 `cards.py`，其余按 STORYBOARD.md 模板出图
2. 配音分段 → 拼接得 voice.wav 与 timeline.json（[[id,start,end],...]）
3. render.py 出无字幕 render/final.mp4
4. `subs.py` → subs.ass；`ffmpeg -i render/final.mp4 -vf "ass=subs.ass:fontsdir=/usr/share/fonts/opentype/noto" -c:a copy burned.mp4`
5. `loudnorm2.py burned.mp4 final.mp4`（在最终成品上做，避免编码后偏差）

## 风格包
`styles/<name>/`：可切换风格包（文案指南、画风模板、封面脚本、选题库）。当前：`styles/huaxia`（华夏辉煌历史）。
本仓库不含任何人声样本或私人文件，可公开。
