# 参考图工作流

本参考只在用户提供图片、截图或链接时读取。用户可以在调用时附上一张图，并说明想保留哪些可迁移的视觉规律、想把新图改成什么；目标是让参考图帮助判断材料、光线或粗粒度版式，而不是把外部作品送入生成器后复刻出来。

## 先建立参考输入契约

在构思主隐喻前，为每张被使用的图建立以下**参考输入契约**。它只决定参考图的角色、权属、传输方式和允许提取项；没有明确说明时，采用安全默认值，不要静默猜测。

```yaml
reference:
  asset: "用户上传文件，或链接中已明确选定的单张图片"
  role: "style-only | composition-only | subject-photo"
  rights: "user-owned | authorized | external-inspiration | unknown"
  transport: "analyze-only | direct-conditioned"
  extract:
    - "允许保留的非识别性规律"
  requested_keep:
    - "用户想保留的、且属于 extract 的规律"
  requested_change:
    - "用户要求重新设计的主题、隐喻、版式、比例或配色"
  layout_rules:
    - "最多两个粗粒度空间规律；仅 composition-only 使用"
  prohibit:
    - "source-text"
    - "logo"
    - "watermark"
    - "likeness"
    - "exact-layout"
```

将用户的自然语言“保留/改变”要求映射到 `requested_keep` 和 `requested_change`：`requested_keep` 不是绕过 `prohibit` 的许可。它只能收录该角色允许提取的规律；来源文字、Logo、水印、对象、人物/产品外观和精确布局永远不能成为“保留”项。`requested_change` 要使新图服务于当前主题，而不是把来源图改色或改字。

然后独立完成当前作品的设计锁；主题与隐喻不能从参考图反推或替换。

```yaml
original_design_lock:
  topic: "当前用户主题"
  metaphor: "新的单一视觉隐喻"
  fingerprint:
    - "版式家族"
    - "工艺关系"
    - "标题角色"
    - "配色关系"
    - "图形几何"
```

生成前，将参考输入契约与设计锁合并为最终 `reference_contract`，并在交付中说明实际采用的 `role / rights / transport / extract / requested_keep / requested_change / prohibit`。这样即使参考图被允许参与生成，新的主题、隐喻和设计指纹也先于生成器输入确定。

图片、链接或截图没有角色说明时，默认：`role: style-only`、`rights: unknown`、`transport: analyze-only`。外部文章、作品集、社交帖子或多图链接必须先让用户选中具体图片；整组作品只能作为文字化的灵感来源，不能直接传入生成器。

## 路由

### style-only：风格规律参考

允许提炼：纸材、纤维密度、压纹深浅、侧光方向与软硬、色温和视觉密度。任何留白、阅读方向或文字/图形的空间关系都属于 `composition-only`。

- **默认 `analyze-only`**：外部、权属未知、带可识别主体、含品牌/签名/水印的图，只能先转成文字设计契约；生成时不传原图。
- **`direct-conditioned` 的条件**：用户明确声明该图自有或获授权；图的角色为 `style-only`；图中不得含人物、产品包装、地标、来源文字、Logo、签名或水印；每张成图只选择一张图片。生成请求必须列出 `requested_keep`、`requested_change` 与 `prohibit`。
- 使用 `direct-conditioned` 时，`requested_keep` 只能是纸材、纤维密度、压纹深浅、侧光方向与软硬、色温或视觉密度；`requested_change` 必须让主题、主隐喻、版式家族、标题角色、色彩关系、比例中的至少四项不同，且不重用参考图文字、Logo、构图或对象。

### composition-only：布局原则参考

允许提炼至多两个粗粒度规律，例如“主视觉在右三分之一”“左侧为无字留白”“阅读方向从上到下”“主视觉区与释放区约为 2:1”。

先用 3×3 网格或一句文字描述抽象这些规律，再以纯文字规格生成。**不直接传原图**。禁止保留精确坐标、形状轮廓、裁切方式、标题位置、配色关系或任何可识别构图。

### subject-photo：主体保真照片

人物、宠物、产品包装、客户素材、建筑地标或其他需要身份/外观保留的图片，不使用此 Skill 的图像生成分支。说明这是参考图转译或身份保持需求，应转交给能锁定主体不变量的流程。不得把 `subject-photo` 标为 `style-only` 来绕过这一边界。

## 生成器传图规则

- `analyze-only`：不传图片；只把 `extract`、允许的 `requested_keep`、`requested_change` 和 `layout_rules` 写入最终提示词。
- `direct-conditioned`：每张输入明确标注为“style reference, not an edit target”，并在提示词中重复 `requested_keep`、`requested_change` 和 `prohibit`。使用生成而非编辑；不能承诺保留参考图中的文字、主体、Logo 或布局。
- 每张成图最多一张 `direct-conditioned` 风格图。多张候选图中，只有用户明确指定且符合条件的一张可以传入；其他图只分析。没有指定主图时，全部保持 `analyze-only`。
- 用户的本地参考图在传入生成前先视觉检查；URL 内容先读取，再按契约决定是否能传图。不可访问、权属不明或未指定的图片保持 `analyze-only`。

## 验收门

生成后检查：

1. `role`、`rights` 与 `transport` 是否符合参考契约；
2. 成图是否泄漏来源文字、Logo、水印、人物/产品相似主体或可识别构图；
3. `style-only` 是否只保留获准的纸材/光线/密度规律；
4. `composition-only` 是否仅保留不超过两个粗粒度空间规则；
5. 用户明确的 `requested_keep` / `requested_change` 是否在合规范围内被执行；
6. 缩略图并排对照时，成图是否能被看作独立设计，而不是同一张海报的改色/改字版。

任何一项失败时，只针对泄漏的属性做一次修正。不要通过叠加更多元素、滤镜或更长的负面词来掩盖相似性。
