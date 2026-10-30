# 分镜规则 / 提示模板

## 镜头类型（storyboard.json 每镜必填 `type`）
| type | 含义 | 典型用途 |
|---|---|---|
| portrait | 人物近景/半身，表情可读 | 开场钩子、人物登场、内心抉择 |
| wide | 全景/大场面（宫殿、城门、军阵） | 交代时代与局势 |
| object | 物件特写（玉玺、诏书、兵器、账单） | 关键道具、转折信物 |
| action | 动作/冲突瞬间 | 高潮（刺杀、对峙） |
| detail | 环境细节（烛火、台阶、旗帜） | 节奏缓冲、情绪 |
| card | 信息卡/数字卡（cards.py 生成） | 数字、步骤、公式、时间线 |

## 硬性规则（check_shots.py 自动检查）
1. 相邻两镜类型不同。
2. 全片至少 3 种类型；任一类型不超过 40%（≥5 镜时）。
3. 任意连续 3 镜内信息卡不超过 1 张。
4. 第 1 镜要有钩子，不能是 detail（安静细节镜）。

## 软规则（人工）
- 同一人物连续出现时换景别或角度（正面近景 → 背影全景）。
- 画面下方 1250–1540px 为字幕区，构图主体放中上部；提示词写明 “subject in upper two-thirds, empty lower area”。
- 历史题材不出现可读文字/现代物件；数字只放在 card。
- 每镜一个视觉焦点，与该段文案的核心名词对应。

## 图片提示模板（historical-realism）
```
Vertical 9:16 cinematic historical realism, {朝代} China, {type 对应景别: close-up portrait | wide establishing shot | macro close-up of object | dynamic action moment | atmospheric detail},
{画面内容：谁/什么，在哪，在做什么}, {光线：candlelight / overcast dawn / fire glow},
authentic {朝代} costume and architecture, muted desaturated palette, film grain,
subject in upper two-thirds, empty lower area for subtitles, no text, no watermark, no modern objects.
```

## storyboard.json 示例
```json
[{"id":"S1","type":"portrait","text":"…","prompt":"…"},
 {"id":"S2","type":"wide","text":"…","prompt":"…"}]
```
