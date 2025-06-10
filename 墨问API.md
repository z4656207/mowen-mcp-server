# 1. 概述

## 域名

`open.mowen.cn`

## 会员专属

:::tip[]
目前只为`墨问 Pro 会员`提供 API 接入的能力，`Pro 会员`过期后，`API-KEY` 也会一起失效。
:::

## 关于 `API-KEY`

### 获取

:::highlight green 📌
API-KEY 是调用`墨问 OpenAPI`的私密凭证，**墨问不会明文保存任何用户的私密凭证**，所以获取了之后用户需要**自行保存好**。
:::

### 遗失

:::highlight red 💡
一旦遗失，**墨问无法再次提供之前的 API-KEY**，只能再次**重新生成**。一旦重新生成新的 API-KEY，**旧有的 API-KEY 即时失效**。所以更换 API-KEY 时，开发者应做好自己业务的适配。
:::

### 使用

将获取到的`API-KEY`放置于 API 请求的 Authorization Header 中，形如 `Authorization: Bearer ${API-KEY}` 


![CleanShot 2025-05-19 at 15.41.42@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/525243/image-preview)
    

# 2. NoteAtom 的结构说明

## NoteAtom 结构

<DataSchema id="167993166" />

## 说明

`NoteAtom` 是笔记的原子结构。一个 `NoteAtom` 节点，可以包含其他的`NoteAtom` 节点，以一个树状的结构来描述一篇笔记。 

`NoteAtom` 可以包含如下属性：


| 属性 | 类型 | 说明 |
| --- | --- | --- |
|  type | string | 表示当前 `atom` 节点的类型，可能包含 `doc(一篇笔记)` `paragraph(笔记中的段落)` `text(段落中的文本)` 等类型。⚠️ 根节点的 type 必须是 `doc` |
| text | string | 节点的文本内容 |
| marks| []NoteAtom | 由多个`atom`节点组成，通常用来修饰 text 文本的样式，如`高亮` `加粗` `链接` |
| attrs| map\<string\>string| 节点的属性 |
| content | []NoteAtom | 当前节点的子节点，由多个`atom`节点组成。譬如一个`doc` 节点包含多个 `paragraph` 节点， `paragraph` 又可以包含多个 `text` 节点 |


## 举例

```
{
   "type": "doc",
   "content": [
      {
         "content": [
            {
               "text": "这是一条 API 创建的笔记",
               "type": "text"
            }
         ],
         "type": "paragraph"
      },
      {
         "type": "paragraph"
      },
      {
         "content": [
            {
               "text": "第一段，普通文本段落",
               "type": "text"
            }
         ],
         "type": "paragraph"
      },
      {
         "type": "paragraph"
      },
      {
         "content": [
            {
               "text": "第二段，富文本段落 ",
               "type": "text"
            },
            {
               "marks": [
                  {
                     "type": "bold"
                  }
               ],
               "text": "加粗",
               "type": "text"
            },
            {
               "text": " ",
               "type": "text"
            },
            {
               "marks": [
                  {
                     "type": "highlight"
                  }
               ],
               "text": "高亮",
               "type": "text"
            },
            {
               "text": " ",
               "type": "text"
            },
            {
               "marks": [
                  {
                     "attrs": {
                        "href": "https://baidu.com"
                     },
                     "type": "link"
                  }
               ],
               "text": "链接",
               "type": "text"
            }
         ],
         "type": "paragraph"
      },
      {
         "type": "paragraph"
      },
      {
         "attrs": {
            "align": "center",
            "alt": "第二段与第三段之间插入一张图",
            "uuid": "iLg8nJvIhexM-VxBHjXYZ-TMP"
         },
         "type": "image"
      },
      {
         "type": "paragraph"
      },
      {
         "content": [
            {
               "text": "第三段，富文本段落 ",
               "type": "text"
            },
            {
               "marks": [
                  {
                     "attrs": {
                        "href": "https://bing.com"
                     },
                     "type": "link"
                  },
                  {
                     "type": "highlight"
                  },
                  {
                     "type": "bold"
                  }
               ],
               "text": "加粗并高亮的链接",
               "type": "text"
            }
         ],
         "type": "paragraph"
      },
      {
         "type": "paragraph"
      },
      {
         "attrs": {
            "audio-uuid": "iLg8nJvIhexM-VxBHjXYZ-TMP",
            "show-note": "00:00 这里是音频 ShowNote\n02:00 开头\n04:00 结尾"
         },
         "type": "audio"
      },
      {
         "type": "paragraph"
      },
      {
         "content": [
            {
               "text": "第四段，引用文本段落",
               "type": "text"
            }
         ],
         "type": "quote"
      },
      {
         "type": "paragraph"
      },
      {
         "content": [
            {
               "text": "第五段，引用文本段落也可以有富文本 ",
               "type": "text"
            },
            {
               "marks": [
                  {
                     "attrs": {
                        "href": "https://bing.com"
                     },
                     "type": "link"
                  },
                  {
                     "type": "highlight"
                  },
                  {
                     "type": "bold"
                  }
               ],
               "text": "加粗并高亮的链接",
               "type": "text"
            }
         ],
         "type": "quote"
      },
      {
         "type": "paragraph"
      },
      {
         "attrs": {
            "uuid": "pnYaQHZpippbfleHTrVa-"
         },
         "type": "note"
      },
      {
         "attrs": {
            "uuid": "ew6POhwnucrXmWNRTuXYZ-TMP"
         },
         "type": "pdf"
      }
   ]
}
```


![image.png](https://api.apifox.com/api/v1/projects/6381454/resources/533263/image-preview)

# 3. 错误码

## 错误码结构说明

错误码由`code` `reason` `message` `meta` 四部分组成:

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| code | int | 目前和 http 状态码保持一致，后续有必要的话，可能会变更为具体的 errcode |
| reason | string | 表示错误原因 |
| message | string | 表示更详细的错误信息，用来做原因分析与问题排查 |
| meta | map\<string\>string | 在一些场景中，用来表示附加信息 |


```
{
    "code": 404,
    "reason": "NOT_FOUND",
    "message": "biz [NoteUsecase.preEdit]: note not found. note_id=XXX",
    "metadata": {}
}
```


:::highlight orange 📌
API 对接开发时，建议使用 `reason` 字段来做错误适配
:::

## 常见的错误列表

| Reason | HTTP 状态码 |说明 |
| --- | --- | --- |
| LOGIN| 400 | 需要登录，在 OpenAPI 的场景中，通常是缺少 API-KEY 或者 无法正确解析出请求者身份 |
| PARAMS | 400 |参数错误，详细信息需要参考 message |
| PERM | 403 | 权限错误，譬如尝试编辑了不属于自己的笔记 |
| NOT_FOUND | 404 | 资源未找到，可以是用户未找到，也可以是笔记未找到，详细信息需要参考 message |
| RATELIMIT | 429 | 请求被限频 |
| RISKY | 403 | 有风险的请求 |
| BLOCKED | 403 | 账户或请求被封禁 |
| Quota | 403 | 配额不足 |

# 4. ChangeLog

# [v0.1.4]
> 2025.06.10

## New
* 【API】[获取上传授权信息](https://mowen.apifox.cn/304801589e0.md)
    * 用于本地上传时，获取授权信息
* 【API】[文件投递示例](https://mowen.apifox.cn/306385915e0.md)
    * 用于本地上传时，投递文件到文件服务器的联调测试
* 【API】[基于 URL 上传文件](https://mowen.apifox.cn/304984752e0.md)
    * 用于使用 URL 通过网络远程上传文件
* 【MCP】 服务增加 Tool: UploadViaURL 

## Changed
* 【API】[笔记创建](https://mowen.apifox.cn/295621359e0.md)
    * 新增笔记节点类型 `image`，支持在笔记中插入图片
    * 新增笔记节点类型 `audio`，支持在笔记中插入音频
    * 新增笔记节点类型 `pdf`，支持在笔记中插入 pdf 文档
* 【API】[笔记编辑](https://mowen.apifox.cn/296486093e0.md)
    * 新增笔记节点类型 `image`，支持在笔记中插入图片
    * 新增笔记节点类型 `audio`，支持在笔记中插入音频
    * 新增笔记节点类型 `pdf`，支持在笔记中插入 pdf 文档
* 【DOC】[2. NoteAtom 的结构说明](https://mowen.apifox.cn/6682171m0.md)
    * 丰富了 NoteAtom 的示例说明，增加了 `图片` `音频` `pdf`的部分

## Fixed
* 【MCP】创建笔记设定自动公开时，有概率无法自动公开

# [v0.1.3]
> 2025.06.04

## Changed
* [API-笔记创建](https://mowen.apifox.cn/295621359e0.md)
    * 新增笔记节点类型 `quote`，支持在创建笔记时，添加引用
    * 新增笔记节点类型 `note`，支持在创建笔记时，添加内链笔记
* [API-笔记编辑](https://mowen.apifox.cn/296486093e0.md)
    * 新增笔记节点类型 `quote`，支持在编辑笔记时，添加引用
    * 新增笔记节点类型 `note`，支持在创编辑记时，添加内链笔记   
* [2. NoteAtom 的结构说明](https://mowen.apifox.cn/6682171m0.md)
    * 丰富了 NoteAtom 的示例说明，增加了 `引用` `内链笔记`的部分

# [v0.1.2]
> 2025.05.26

## Changed
* [API-笔记创建](https://mowen.apifox.cn/295621359e0.md)
    * 新增参数 `settings.tags`，支持在创建笔记时，设置标签

## Others
* 支持 CORS

# [v0.1.1]
> 2025-05-20
## New

* [API-笔记设置](https://mowen.apifox.cn/298137640e0.md) 
    * 用于设置笔记私密状态

## Changed

* [API-笔记创建](https://mowen.apifox.cn/295621359e0.md)
    * 新增参数 `settings.auto_publish（自动发表）`，支持在创建笔记后的自动公开发表（风控后）

---
# [v0.1.0]
> 2025.05-19
## New

* [API-笔记创建](https://mowen.apifox.cn/295621359e0.md)
    * 用于创建笔记，文本支持加粗、高亮、链接

* [API-笔记编辑](https://mowen.apifox.cn/296486093e0.md)
    * 用于编辑笔记

* [API-APIKey重置](https://mowen.apifox.cn/297614056e0.md)
    * 用于重置 API KEY

# APIKey 重置

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/open/api/v1/auth/key/reset:
    post:
      summary: APIKey 重置
      deprecated: false
      description: |-
        :::tip[限频：1]
        每个用户/每个API/每秒钟内请求 1 次，超出频率的请求会被拦截掉。
        :::

        :::tip[配额：100 次/天]
        调用成功才计为 1 次
        :::
      operationId: OpenApi_KeyReset
      tags:
        - 授权
        - OpenApi
      parameters:
        - name: Authorization
          in: header
          description: ''
          example: Bearer {{API-KEY}}
          schema:
            type: string
            default: Bearer {{API-KEY}}
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/KeyResetRequest'
            examples: {}
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/KeyResetReply'
          headers: {}
          x-apifox-name: 成功
        '500':
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 授权
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6381454/apis/api-297614056-run
components:
  schemas:
    KeyResetRequest:
      type: object
      properties: {}
      x-apifox-orders: []
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    KeyResetReply:
      type: object
      properties:
        apiKey:
          type: string
          description: API-KEY
      x-apifox-orders:
        - apiKey
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    Status:
      type: object
      properties:
        code:
          type: integer
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          format: int32
        message:
          type: string
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
        details:
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
      x-apifox-orders:
        - code
        - message
        - details
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    GoogleProtobufAny:
      type: object
      properties:
        '@type':
          type: string
          description: The type of the serialized message.
      additionalProperties: true
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      x-apifox-orders:
        - '@type'
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers: []
security: []

```


# 笔记创建

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/open/api/v1/note/create:
    post:
      summary: 笔记创建
      deprecated: false
      description: |-
        :::tip[限频：1]
        每个用户/每个API/每秒钟内请求 1 次，超出频率的请求会被拦截掉。
        :::

        :::tip[配额：100 次/天]
        调用成功才计为 1 次，**即：每天可以基于 API 创建 100 篇**
        :::
      operationId: OpenApi_NoteCreate
      tags:
        - 笔记
        - OpenAPI
        - 笔记
      parameters:
        - name: Authorization
          in: header
          description: ''
          example: Bearer {{API-KEY}}
          schema:
            type: string
            default: Bearer {{API-KEY}}
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NoteCreateRequest'
            examples: {}
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NoteCreateReply'
          headers: {}
          x-apifox-name: 成功
        '500':
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 笔记
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6381454/apis/api-295621359-run
components:
  schemas:
    NoteCreateRequest:
      type: object
      properties:
        body:
          allOf:
            - &ref_0
              $ref: '#/components/schemas/NoteAtom'
          description: 笔记内容
        settings:
          allOf:
            - $ref: '#/components/schemas/NoteCreateRequest_Settings'
          description: 笔记设置
      x-apifox-orders:
        - body
        - settings
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteCreateRequest_Settings:
      type: object
      properties:
        autoPublish:
          type: boolean
          description: 自动发布
        tags:
          type: array
          items:
            type: string
          description: |-
            标签
             标签列表 <= 10 个
             标签名长度 <= 30 个字符
      x-apifox-orders:
        - autoPublish
        - tags
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteAtom:
      type: object
      properties:
        type:
          type: string
          description: |-
            节点类型： 必填
             * 根节点(顶层节点必须是根节点)： `doc`
             * 段落(block)： `paragraph`
             * 文本(inline)： `text`
             * 高亮(marks)： `highlight`
             * 链接(marks)： `link`
             * 加粗(marks)： `bold`
             * 引用(block)： `quote`
             * 内链笔记(block)： `note`
             * 图片(block)： `image`
             * 音频(block)： `audio`
             * PDF(block)： `pdf`
        text:
          type: string
          description: |-
            节点文本： 非必填
             通常用在 `text` 类型的节点中
        content:
          type: array
          items: *ref_0
          description: |-
            节点内容： 非必填
             通常用在 `block` 类型的节点中
        marks:
          type: array
          items: *ref_0
          description: |-
            节点标记： 非必填
             通常用在 `inline` 类型的节点中，用于描述样式
        attrs:
          type: object
          additionalProperties:
            type: string
          description: |-
            节点属性： 非必填
             与各种节点配合使用，用于描述属性信息
             * href: 链接地址，用于 `marks.link` 类型的节点
             * align: 对齐方式，用于 `image` 类型的节点，可选值：`left`、`center`、`right`
             * uuid: 
                  * 作为 `内链笔记的笔记 ID`，用于 `note` 类型的节点
                  * 作为 `图片文件 ID`，用于 `image` 类型的节点
                  * 作为 `PDF 文件 ID`，用于 `pdf` 类型的节点
             * alt:
                  * 作为图片描述，用于 `image` 类型的节点
             * show-note:
                  * 作为音频的 ShowNote，用于 `audio` 类型的节点
          x-apifox-orders: []
          properties: {}
          x-apifox-ignore-properties: []
      description: 笔记-原子节点信息
      x-apifox-orders:
        - type
        - text
        - content
        - marks
        - attrs
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteCreateReply:
      type: object
      properties:
        noteId:
          type: string
          description: 笔记ID
      x-apifox-orders:
        - noteId
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    Status:
      type: object
      properties:
        code:
          type: integer
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          format: int32
        message:
          type: string
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
        details:
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
      x-apifox-orders:
        - code
        - message
        - details
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    GoogleProtobufAny:
      type: object
      properties:
        '@type':
          type: string
          description: The type of the serialized message.
      additionalProperties: true
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      x-apifox-orders:
        - '@type'
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers: []
security: []

```


# 笔记编辑

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/open/api/v1/note/edit:
    post:
      summary: 笔记编辑
      deprecated: false
      description: |
        :::tip[限频：1]
        每个用户/每个API/每秒钟内请求 1 次，超出频率的请求会被拦截掉
        :::

        :::tip[配额：1000 次/天]
        调用成功才计为 1 次，**即：每天可以基于 API 编辑 1000 次**
        :::


        :::caution[限制]
        只有基于 API 创建的笔记，才能基于 API 做后续的编辑。**即：目前暂不支持使用 API 编辑小程序端创建的笔记**
        :::
      operationId: OpenApi_NoteEdit
      tags:
        - 笔记
        - OpenAPI
        - 笔记
      parameters:
        - name: Authorization
          in: header
          description: ''
          example: Bearer {{API-KEY}}
          schema:
            type: string
            default: Bearer {{API-KEY}}
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NoteEditRequest'
            examples: {}
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NoteEditReply'
          headers: {}
          x-apifox-name: 成功
        '500':
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 笔记
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6381454/apis/api-296486093-run
components:
  schemas:
    NoteEditRequest:
      type: object
      properties:
        noteId:
          type: string
          description: 笔记ID
        body:
          allOf:
            - &ref_0
              $ref: '#/components/schemas/NoteAtom'
          description: 笔记内容
      x-apifox-orders:
        - noteId
        - body
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteAtom:
      type: object
      properties:
        type:
          type: string
          description: |-
            节点类型： 必填
             * 根节点(顶层节点必须是根节点)： `doc`
             * 段落(block)： `paragraph`
             * 文本(inline)： `text`
             * 高亮(marks)： `highlight`
             * 链接(marks)： `link`
             * 加粗(marks)： `bold`
             * 引用(block)： `quote`
             * 内链笔记(block)： `note`
             * 图片(block)： `image`
             * 音频(block)： `audio`
             * PDF(block)： `pdf`
        text:
          type: string
          description: |-
            节点文本： 非必填
             通常用在 `text` 类型的节点中
        content:
          type: array
          items: *ref_0
          description: |-
            节点内容： 非必填
             通常用在 `block` 类型的节点中
        marks:
          type: array
          items: *ref_0
          description: |-
            节点标记： 非必填
             通常用在 `inline` 类型的节点中，用于描述样式
        attrs:
          type: object
          additionalProperties:
            type: string
          description: |-
            节点属性： 非必填
             与各种节点配合使用，用于描述属性信息
             * href: 链接地址，用于 `marks.link` 类型的节点
             * align: 对齐方式，用于 `image` 类型的节点，可选值：`left`、`center`、`right`
             * uuid: 
                  * 作为 `内链笔记的笔记 ID`，用于 `note` 类型的节点
                  * 作为 `图片文件 ID`，用于 `image` 类型的节点
                  * 作为 `PDF 文件 ID`，用于 `pdf` 类型的节点
             * alt:
                  * 作为图片描述，用于 `image` 类型的节点
             * show-note:
                  * 作为音频的 ShowNote，用于 `audio` 类型的节点
          x-apifox-orders: []
          properties: {}
          x-apifox-ignore-properties: []
      description: 笔记-原子节点信息
      x-apifox-orders:
        - type
        - text
        - content
        - marks
        - attrs
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteEditReply:
      type: object
      properties:
        noteId:
          type: string
          description: 笔记ID
      x-apifox-orders:
        - noteId
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    Status:
      type: object
      properties:
        code:
          type: integer
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          format: int32
        message:
          type: string
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
        details:
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
      x-apifox-orders:
        - code
        - message
        - details
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    GoogleProtobufAny:
      type: object
      properties:
        '@type':
          type: string
          description: The type of the serialized message.
      additionalProperties: true
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      x-apifox-orders:
        - '@type'
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers: []
security: []

```


# 笔记设置

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/open/api/v1/note/set:
    post:
      summary: 笔记设置
      deprecated: false
      description: |-
        :::tip[限频：1]
        每个用户/每个API/每秒钟内请求 1 次，超出频率的请求会被拦截掉
        :::

        :::tip[配额：100 次/天]
        调用成功才计为 1 次
        :::
      operationId: OpenApi_NoteSet
      tags:
        - 笔记
        - OpenApi
      parameters:
        - name: Authorization
          in: header
          description: ''
          example: Bearer {{API-KEY}}
          schema:
            type: string
            default: Bearer {{API-KEY}}
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NoteSetRequest'
            examples: {}
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/NoteSetReply'
          headers: {}
          x-apifox-name: 成功
        '500':
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 笔记
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6381454/apis/api-298137640-run
components:
  schemas:
    NoteSetRequest:
      type: object
      properties:
        noteId:
          type: string
          description: 笔记ID
        section:
          type: integer
          description: |-
            设置类别 
             `1` 笔记隐私，设置此类别时，需要设置 `settings.privacy`
          format: enum
        settings:
          allOf:
            - $ref: '#/components/schemas/NoteSettings'
          description: 设置项
      x-apifox-orders:
        - noteId
        - section
        - settings
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteSettings:
      type: object
      properties:
        privacy:
          allOf:
            - $ref: '#/components/schemas/NotePrivacySet'
          description: 笔记隐私设置
      description: 笔记设置项
      x-apifox-orders:
        - privacy
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NotePrivacySet:
      type: object
      properties:
        type:
          type: string
          description: |-
            隐私类型 
             `public`  完全公开
             `private` 私有
             `rule`    规则公开 
             PS: 规则公开时，需要设置规则，未设置隐私规则时（即取默认值），等同于完全公开
        rule:
          allOf:
            - $ref: '#/components/schemas/NotePrivacySet_Rule'
          description: 隐私规则
      x-apifox-orders:
        - type
        - rule
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NotePrivacySet_Rule:
      type: object
      properties:
        noShare:
          type: boolean
          description: 是否禁止分享与转发  默认值：false(允许分享与转发)
        expireAt:
          type: string
          description: 公开截止时间  时间戳(秒)，默认值：0(永久可见)
      description: 公开规则
      x-apifox-orders:
        - noShare
        - expireAt
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    NoteSetReply:
      type: object
      properties: {}
      x-apifox-orders: []
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    Status:
      type: object
      properties:
        code:
          type: integer
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          format: int32
        message:
          type: string
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
        details:
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
      x-apifox-orders:
        - code
        - message
        - details
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    GoogleProtobufAny:
      type: object
      properties:
        '@type':
          type: string
          description: The type of the serialized message.
      additionalProperties: true
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      x-apifox-orders:
        - '@type'
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers: []
security: []

```

# 说明

## 本地上传步骤

完成文件上传，需要 2 个步骤：

1. 先通过 [获取上传授权信息](https://mowen.apifox.cn/304801589e0.md)，获取到`文件的上传端点(endpoint)`以及相关的`授权信息`。 服务会根据请求来源，分配相应的上传端点，达到上传线路选择以及海外加速的目的。
2. 使用上一步骤获取到的相关的`授权信息`，通过程序，向上传端点`endpoint` 发起 Form 表单上传。服务会对授权信息、文件类型、文件大小等等进行规则校验，最终完成文件上传，返回文件信息。


### 步骤一： 获取授权信息以及上传端点

![CleanShot 2025-06-09 at 19.21.37@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532825/image-preview)

### 步骤二： 文件投递

可以使用 [文件投递示例](https://mowen.apifox.cn/306385915e0.md)，对步骤一获得授权信息进行验证、辅助联调、以及观察文件服务器的响应结果。

![CleanShot 2025-06-09 at 20.38.38@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532856/image-preview)

简单讲就是发起一个表单请求，表单要填的值通过第一步获取。

也可以通过 Apifox 工具获取相关的代码示例。

![CleanShot 2025-06-09 at 20.46.32@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532857/image-preview)

# 说明

## 本地上传步骤

完成文件上传，需要 2 个步骤：

1. 先通过 [获取上传授权信息](https://mowen.apifox.cn/304801589e0.md)，获取到`文件的上传端点(endpoint)`以及相关的`授权信息`。 服务会根据请求来源，分配相应的上传端点，达到上传线路选择以及海外加速的目的。
2. 使用上一步骤获取到的相关的`授权信息`，通过程序，向上传端点`endpoint` 发起 Form 表单上传。服务会对授权信息、文件类型、文件大小等等进行规则校验，最终完成文件上传，返回文件信息。


### 步骤一： 获取授权信息以及上传端点

![CleanShot 2025-06-09 at 19.21.37@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532825/image-preview)

### 步骤二： 文件投递

可以使用 [文件投递示例](https://mowen.apifox.cn/306385915e0.md)，对步骤一获得授权信息进行验证、辅助联调、以及观察文件服务器的响应结果。

![CleanShot 2025-06-09 at 20.38.38@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532856/image-preview)

简单讲就是发起一个表单请求，表单要填的值通过第一步获取。

也可以通过 Apifox 工具获取相关的代码示例。

![CleanShot 2025-06-09 at 20.46.32@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532857/image-preview)

# 说明

## 本地上传步骤

完成文件上传，需要 2 个步骤：

1. 先通过 [获取上传授权信息](https://mowen.apifox.cn/304801589e0.md)，获取到`文件的上传端点(endpoint)`以及相关的`授权信息`。 服务会根据请求来源，分配相应的上传端点，达到上传线路选择以及海外加速的目的。
2. 使用上一步骤获取到的相关的`授权信息`，通过程序，向上传端点`endpoint` 发起 Form 表单上传。服务会对授权信息、文件类型、文件大小等等进行规则校验，最终完成文件上传，返回文件信息。


### 步骤一： 获取授权信息以及上传端点

![CleanShot 2025-06-09 at 19.21.37@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532825/image-preview)

### 步骤二： 文件投递

可以使用 [文件投递示例](https://mowen.apifox.cn/306385915e0.md)，对步骤一获得授权信息进行验证、辅助联调、以及观察文件服务器的响应结果。

![CleanShot 2025-06-09 at 20.38.38@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532856/image-preview)

简单讲就是发起一个表单请求，表单要填的值通过第一步获取。

也可以通过 Apifox 工具获取相关的代码示例。

![CleanShot 2025-06-09 at 20.46.32@2x.png](https://api.apifox.com/api/v1/projects/6381454/resources/532857/image-preview)

# 文件投递示例

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /{endpoint}/:
    post:
      summary: 文件投递示例
      deprecated: false
      description: ''
      tags:
        - 文件上传/本地上传
      parameters:
        - name: endpoint
          in: path
          description: ''
          required: true
          schema:
            type: string
      requestBody:
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                key:
                  example: ''
                  type: string
                policy:
                  example: ''
                  type: string
                callback:
                  example: ''
                  type: string
                success_action_status:
                  example: ''
                  type: string
                x-oss-signature-version:
                  example: ''
                  type: string
                x-oss-credential:
                  example: ''
                  type: string
                x-oss-date:
                  example: ''
                  type: string
                x-oss-signature:
                  example: ''
                  type: string
                x-oss-meta-mo-uid:
                  example: ''
                  type: string
                x:file_name:
                  type: string
                  example: ''
                x:file_id:
                  example: ''
                  type: string
                x:file_uid:
                  example: ''
                  type: string
                file:
                  format: binary
                  type: string
                  example: ''
            examples: {}
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties: {}
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 文件上传/本地上传
      x-apifox-status: developing
      x-run-in-apifox: https://app.apifox.com/web/project/6381454/apis/api-306385915-run
components:
  schemas: {}
  securitySchemes: {}
servers: []
security: []

```


# 基于 URL 上传文件

## OpenAPI Specification

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /api/open/api/v1/upload/url:
    post:
      summary: 基于 URL 上传文件
      deprecated: false
      description: >
        :::tip[限频：1]

        每个用户/每个API/每秒钟内请求 1 次，超出频率的请求会被拦截掉。

        :::


        :::tip[配额：200 次/天]

        调用成功才计为 1 次，**即：每天可以上传 200 个文件（含图片、音频、PDF等）**

        :::


        :::caution[限制]


        | 类型 | 文件大小检测 | MIME检测 |

        | --- | --- | --- |

        | 图片 | 小于 50MB
        |image/gif<br>image/jpeg<br>image/jpg<br>image/png<br>image/webp |

        | 音频 | 小于 200MB |audio/mpeg<br>audio/mp4<br>audio/x-m4a<br>audio/m4a |

        | PDF | 小于 100MB |application/pdf<br>application/x-pdf |

        :::


        :::caution[声明]

        原理和本地文件上传类似，只是由墨问完成了远程文件的下载，而后上传到墨问。受限于远程文件的下载速度（可能会超时）、在墙外不可访问，或者远程站点有自己的防盗链、防下载机制等等原因，并不能保证一定会成功。开发者应该有自己的容错机制。


        不建议使用 URL 的方式远程上传较大的文件。

        :::
      operationId: OpenApi_UploadViaURL
      tags:
        - 文件上传/远程上传
        - OpenApi
      parameters:
        - name: Authorization
          in: header
          description: ''
          example: Bearer {{API-KEY}}
          schema:
            type: string
            default: Bearer {{API-KEY}}
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UploadViaURLRequest'
            examples: {}
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UploadViaURLReply'
          headers: {}
          x-apifox-name: 成功
        '500':
          description: Default error response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Status'
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 文件上传/远程上传
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/6381454/apis/api-304984752-run
components:
  schemas:
    UploadViaURLRequest:
      type: object
      properties:
        fileType:
          type: integer
          description: |-
            文件类型： 必填
             `1-图片` `2-音频` `3-PDF`
          format: enum
        url:
          type: string
          description: 文件URL
        fileName:
          type: string
          description: 文件名称： 选填（未填时，系统生成）
      x-apifox-orders:
        - fileType
        - url
        - fileName
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    UploadViaURLReply:
      type: object
      properties:
        file:
          allOf:
            - $ref: '#/components/schemas/UploadedFile'
          description: 文件信息
      x-apifox-orders:
        - file
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    UploadedFile:
      type: object
      properties:
        uid:
          type: string
          description: 用户 ID
        fileId:
          type: string
          description: 文件 ID
        name:
          type: string
          description: 文件名
        path:
          type: string
          description: 文件路径
        type:
          type: integer
          description: 文件类型 `1-图片` `2-音频` `3-PDF`
          format: sint32
        format:
          type: string
          description: 文件格式
        extra:
          type: string
          description: 文件附加信息
        size:
          type: string
          description: 文件大小
        mime:
          type: string
          description: 文件 MIME
        hash:
          type: string
          description: 文件 Hash
        url:
          type: string
          description: 文件 URL
        styleUrls:
          type: object
          additionalProperties:
            type: string
          description: 缩略图 URLs
          x-apifox-orders: []
          properties: {}
          x-apifox-ignore-properties: []
        risky:
          type: boolean
          description: 是否有风险
      x-apifox-orders:
        - uid
        - fileId
        - name
        - path
        - type
        - format
        - extra
        - size
        - mime
        - hash
        - url
        - styleUrls
        - risky
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    Status:
      type: object
      properties:
        code:
          type: integer
          description: >-
            The status code, which should be an enum value of
            [google.rpc.Code][google.rpc.Code].
          format: int32
        message:
          type: string
          description: >-
            A developer-facing error message, which should be in English. Any
            user-facing error message should be localized and sent in the
            [google.rpc.Status.details][google.rpc.Status.details] field, or
            localized by the client.
        details:
          type: array
          items:
            $ref: '#/components/schemas/GoogleProtobufAny'
          description: >-
            A list of messages that carry the error details.  There is a common
            set of message types for APIs to use.
      description: >-
        The `Status` type defines a logical error model that is suitable for
        different programming environments, including REST APIs and RPC APIs. It
        is used by [gRPC](https://github.com/grpc). Each `Status` message
        contains three pieces of data: error code, error message, and error
        details. You can find out more about this error model and how to work
        with it in the [API Design
        Guide](https://cloud.google.com/apis/design/errors).
      x-apifox-orders:
        - code
        - message
        - details
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
    GoogleProtobufAny:
      type: object
      properties:
        '@type':
          type: string
          description: The type of the serialized message.
      additionalProperties: true
      description: >-
        Contains an arbitrary serialized message along with a @type that
        describes the type of the serialized message.
      x-apifox-orders:
        - '@type'
      x-apifox-ignore-properties: []
      x-apifox-folder: ''
  securitySchemes: {}
servers: []
security: []

```



# python代码示例补充
```
## 获取上传授权信息

import http.client
import json

conn = http.client.HTTPSConnection("")
payload = json.dumps({
   "fileType": 0,
   "fileName": "string"
})
headers = {
   'Authorization': 'Bearer {{API-KEY}}',
   'Content-Type': 'application/json'
}
conn.request("POST", "/api/open/api/v1/upload/prepare", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


## 文件投递示例

import http.client
import mimetypes
from codecs import encode

conn = http.client.HTTPSConnection("")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=key;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=policy;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=callback;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=success_action_status;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x-oss-signature-version;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x-oss-credential;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x-oss-date;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x-oss-signature;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x-oss-meta-mo-uid;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x:file_name;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x:file_id;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=x:file_uid;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode(""))
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=file; filename={0}'.format('')))

fileType = mimetypes.guess_type('')[0] or 'application/octet-stream'
dataList.append(encode('Content-Type: {}'.format(fileType)))
dataList.append(encode(''))

with open('', 'rb') as f:
   dataList.append(f.read())
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary) 
}
conn.request("POST", "/", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


## 基于 URL 上传文件

import http.client
import json

conn = http.client.HTTPSConnection("")
payload = json.dumps({
   "fileType": 0,
   "url": "string",
   "fileName": "string"
})
headers = {
   'Authorization': 'Bearer {{API-KEY}}',
   'Content-Type': 'application/json'
}
conn.request("POST", "/api/open/api/v1/upload/url", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

```