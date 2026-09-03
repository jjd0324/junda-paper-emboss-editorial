# 提示词蓝图

实际生成时，先完成设计判断，再将下列字段写成一份自然、连贯的图像生成规格。不要把每个可选项逐字罗列给模型。

```text
Use case: ads-marketing
Asset type: {用途，例如：文章头图 / 3:4 社交媒体封面 / 书封概念图}
Primary request: Create one original minimal paper-emboss editorial visual about “{主题}”.
Reference contract: {none，或引用已解析的 role / rights / transport / allowed extraction / prohibit 内容。若有未标注参考，写 style-only + analyze-only。}
Reference intent: {仅列出允许的 requested_keep；列出 requested_change 中必须重新设计的主题/隐喻/版式/比例/配色；若无参考则写 none。}

Semantic core: express {情绪、关系、动作或状态} through one restrained visual metaphor: {主隐喻}.
Canvas: {比例}.
Composition: {选定的版式家族；标题、隐喻和留白之间的关系}.
Typography hierarchy: {直接文字模式：a dominant headline “{标题}”; {副标题或留空说明}; sparse micro-index information only. 严格文字模式：reserve a headline-safe area and an optional small index area; render no readable text on the art layer}. The lettering is part of the composition, not a label placed on top.
Paper and relief: real uncoated {纸色} paper with fine visible fibers. Use {工艺主次关系}; shallow edge impressions, restrained highlights and extremely soft shadows from one approximately 45-degree side light.
Color palette: {1–2 种主色与可选小强调色}.
Mood: quiet, intelligent, contemporary editorial design; like an independent magazine or art-book cover.
Constraints: one main metaphor only; generous negative space; no busy illustration, no complex background, no glossy plastic, no exaggerated 3D extrusion, no metallic engraving, no hard drop shadows, no watermark, no invented logos, no source-image text, no source logo, no recognizable source layout.
Text (verbatim): “{需要让模型直接生成的最短文字；严格文字模式时填 NO TEXT ON ART LAYER}”.
```

## 文字的两种处理

- 文案短、且用户明确接受近似：将标题以引号写入 `Text (verbatim)`，并在验收时核对拼写、层级和是否多出字符。
- 文案严格或较长：不让模型画可读文字。将 `Text (verbatim)` 设为 `NO TEXT ON ART LAYER`，并按 [严格文字模式](strict-text-mode.md) 做精确覆盖层。

## 变化规则

每个新版本记录并随交付列出离散的“版式家族、工艺主次关系、主隐喻、主色关系、标题的构图角色”五项设计指纹，并至少改变其中两项。细微位置或色差不算变化；只改变背景颜色不算新设计。
