# 指令管理器使用教程

## 这是什么？

这是一个以aiotieba库为基础二次开发的实用工具

只需要在贴吧发送一条以@v_guard开头的回复，就能完成各种吧务管理操作

**它可以极大提高吧务操作的效率**

## 先看使用案例

### 案例1

*如何删除一个主题帖并顺便封楼主十天*

发现一个违规主题帖

<img width="40%" alt="1_1" src="https://user-images.githubusercontent.com/48282276/171667469-6a70703e-08ca-4df7-aa7a-de5cb8b11e40.jpg">

先`@v_guard`并确保@变蓝

<img width="40%" alt="1_2" src="https://user-images.githubusercontent.com/48282276/171667750-0cde4816-c755-4565-9d22-e1688a563dd7.jpg">

再输入

**指令类型**: [`drop`](#drop-删封)<br>
**参数1**: `test1234` (可选的封禁理由)

并发布回复

<img width="40%" alt="1_3_1" src="https://user-images.githubusercontent.com/48282276/171667893-68643002-8abb-47a1-87d6-72090c8f5a41.jpg">

<img width="40%" alt="1_3_2" src="https://user-images.githubusercontent.com/48282276/171670836-2a575815-be7f-45fe-8f3c-a5b32e57e10a.jpg">

指令生效<br>
主题帖被删除<br>
楼主`v_guard`被封十天

<img width="80%" alt="1_4_1" src="https://user-images.githubusercontent.com/48282276/171667952-fec55cfc-1a65-426a-8b2f-7941f626a441.png">

<img width="80%" alt="1_4_2" src="https://user-images.githubusercontent.com/48282276/171668105-2d4115c8-e63a-447d-a827-42159477658e.png">

<img width="80%" alt="1_4_3" src="https://user-images.githubusercontent.com/48282276/171668249-798c08f6-2fba-4fea-8186-079937a291e8.png">

### 案例2

*如何在app不依赖任何现有发言封禁任意用户十天*

先在目标用户的个人主页复制包含其[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串

<img width="40%" alt="2_1" src="https://user-images.githubusercontent.com/48282276/160992857-c4f29b1c-1b46-4074-b1c5-b6f83a62de46.jpg">

在这个吧的任何位置拉起一个回复框<br>
先`@v_guard`并确保@变蓝<br>
再输入

**指令类型**: [`block`](#block-封禁)<br>
**参数1**: `刚刚复制的那坨东西` (用户id: 包含[tieba_uid](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串)

点击回复

<img width="40%" alt="2_2" src="https://user-images.githubusercontent.com/48282276/160992862-341c666c-5a45-40f2-ab75-ab098b456235.jpg">

指令生效

`tieba_uid=316431307`的用户`kk不好玩`被封十天

<img width="80%" alt="2_3" src="https://user-images.githubusercontent.com/48282276/160992854-04d2128b-934c-4ba1-9a22-11d768c6989d.png">

### 案例3

*如何删除一条违规回复并顺便封层主三天*

点一下需要删除的楼层拉起回复框<br>
先`@v_guard`并确保@变蓝<br>
再输入

**指令类型**: [`drop3`](#drop-删封)

点击回复

<img width="40%" alt="3_1" src="https://user-images.githubusercontent.com/48282276/160995393-903511ae-9ec3-4055-890e-e144a7540fac.jpg">

指令生效<br>
楼层被删<br>
层主`v_guard`被封三天

<img width="80%" alt="3_2_1" src="https://user-images.githubusercontent.com/48282276/160995720-e8a288ae-e1d7-477a-a5d0-3a5622d30b1d.png">

<img width="80%" alt="3_2_2" src="https://user-images.githubusercontent.com/48282276/160995724-63c9afd8-bf41-454b-8647-7858461d6c72.png">

### 案例4

*网页端如何解封任意用户*

点开用户主页，在链接里找到一串`tb.1.`开头的东西，这个东西叫[`portrait`](https://aiotieba.cc/tutorial/start#portrait)<br>
每个用户都有唯一的[`portrait`](https://aiotieba.cc/tutorial/start#portrait)<br>
把它复制出来

<img width="80%" alt="4_1" src="https://user-images.githubusercontent.com/48282276/160996223-8afa7be5-1051-4cdd-9d4c-0e05044774e9.png">

在这个吧的任何位置拉起一个回复框<br>
先`@v_guard`并确保@变蓝<br>
再输入

**指令类型**: [`unblock`](#unblock-解封)<br>
**参数1**: `刚刚复制的那坨东西` (用户id: portrait)

点击回复

<img width="80%" alt="4_2" src="https://user-images.githubusercontent.com/48282276/160996234-67fb1940-9276-4069-8eb7-c67f532620d5.png">

指令生效<br>
`portrait=tb.1.8277e641.gUE2cTq4A4z5fi2EHn5k3Q`的用户`kk不好玩`被解封

<img width="80%" alt="4_3" src="https://user-images.githubusercontent.com/48282276/160996957-66f0976a-976a-42f4-8166-2d461561c45a.png">

## 总结使用方法

在启用了指令管理器的贴吧的特定位置发送以下文字就能使用指令

```text
@v_guard <指令类型> [参数1] [参数2] ...
```

例如在封禁指令[`block`](#block-封禁)

```text
@v_guard block 李彦宏 封禁测试
```

中，`block`表示**指令类型**，`李彦宏`为**参数1** (待封禁用户的id: 用户名)，`封禁测试`为**参数2** (可选的封禁理由)

需要注意的是一定要使@变蓝，才能确保监听账号`v_guard`收到指令请求

若你的指令完全执行成功，指令会被删除并进入吧务后台供其他吧务监督

## 权限级别说明

权限级别可以通过指令[`set`](#set-设置权限) [`white`](#white-白名单) [`black`](#black-黑名单) [`reset`](#reset-重置权限)修改

任何修改权限的操作都包含了越界检查，即低权限无法修改高权限，也无法将其他用户修改为高权限

各权限级别的含义如下

+ `50` 后台管理员 - 可以指定其他非5级用户的权限级别<br>
+ `40` 大吧主 - 可以添加脚本黑名单 贴吧黑名单<br>
+ `30` 高权限吧务 - 可以置顶 撤置顶 解贴吧黑名单 解脚本黑名单<br>
+ `20` 普通吧务 - 可以删 封 解封 加精 撤精 屏蔽 解屏蔽 拒绝申诉<br>
+ `10` 非吧务的优秀创作者 - 可以使用[`recommend`](#recommend-首页推荐) [`get`](#get-用户信息) [`ping`](#ping-可用性测试)指令<br>
+ `0` 普通吧友(默认值) 一般不需要特别指定<br>
+ `-10` 不允许使用指令的用户<br>
+ `-20 ~ -40` 可自定义的惩罚标记<br>
+ `-50` 等价于十循

---

## 所有指令集

### delete 删帖

```text
@v_guard delete
```

***功能***

如果这条指令是一条`回复`，那么指令所在主题帖会被*删除*<br>
如果这条指令是一条`楼中楼`，那么指令所在回复会被*删除*<br>
如果这条指令是一条`转发了另一主题帖的主题帖`，那么被转发的主题帖会被*删除*<br>
在使用该指令时请**特别注意指令的发送位置**，以免产生意料之外的效果

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*删帖*是贴吧一项重要的传统功能<br>
大部分贴吧都移除了该功能的调用界面且无法删除视频帖<br>
因此我开发了这个指令以方便吧务使用*删帖*功能并支持删除视频帖

---

### recover 恢复删帖

```text
@v_guard recover [tid/pid]
```

***功能***

恢复删帖

***参数说明***

`tid/pid`: 待恢复主题帖的[`thread_id`](https://aiotieba.cc/tutorial/start/#thread_id)或回复的[`post_id`](https://aiotieba.cc/tutorial/start/#post_id)

***举例***

```text
@v_guard recover 144609176381
```

意为恢复`pid=144609176381`的回复

```text
@v_guard recover 7902166405
```

意为恢复`tid=7902166405`的主题帖

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

为了方便将恢复删帖权限快速下放，我开发了这个指令

---

### hide 屏蔽

```text
@v_guard hide
```

***功能***

*屏蔽*`指令所在主题帖`

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*屏蔽*是贴吧app12+新增的功能<br>
极速版/内部版或其他第三方贴吧app可能无法直接使用该功能<br>
因此我开发了这个指令以方便使用这些贴吧app的吧务使用*屏蔽*功能

---

### unhide 解屏蔽

```text
@v_guard unhide
```

***功能***

解除`指令所在主题帖`的*屏蔽*状态

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*屏蔽*是贴吧app12+新增的功能<br>
*解除屏蔽*需要进吧务后台操作，非常麻烦<br>
因此我开发了这个指令。在原帖直接操作可以大幅提高操作效率

---

### block 封禁

```text
@v_guard block [id] [reason]
@v_guard blockx [id] [reason]
```

***功能***

block: *封禁*`id`对应的用户10天<br>
blockx: *封禁*`id`对应的用户x天，x是1~90的任意整数

***参数说明***

`x`: 若吧务账号无svip则仅可封禁1/3/10天，分别对应`block1` `block3` `block/block10`。若因无svip导致封禁失败则会再次尝试封禁10天

`reason`: 可选参数，封禁理由

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串，它们都可以用来唯一地确定一个贴吧用户

+ [`用户名`](https://aiotieba.cc/tutorial/start#user_name): 请注意将其与可重复的`昵称`相区分。每个贴吧用户的用户名都是唯一的，但用户可以没有用户名<br>
+ [`portrait`](https://aiotieba.cc/tutorial/start#portrait): 一般是以`tb.1.`开头的一串字符串<br>
用网页端处理用户时，推荐使用这个[`portrait`](https://aiotieba.cc/tutorial/start#portrait)方法予以精准定位<br>
+ 包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串: [`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)需要被两个`#`号包围，如`#12345678#`<br>
在较新版贴吧app的用户主页的用户头像下方有个长得像`ID:12345678`的东西，点它右侧的那个复制按钮复制出来的一串东西，就能作为这里的参数<br>
用app处理无用户名的用户，或者用户名很复杂的用户时，推荐使用这个包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串方法予以精准定位<br>
+ 包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串: 每个贴吧用户都有且仅有一个[`user_id`](https://aiotieba.cc/tutorial/start#user_id)。[`user_id`](https://aiotieba.cc/tutorial/start#user_id)需要被两个`/`号包围，如`/12345678/`<br>
一般仅用于吧务通过后台数据表中记录的[`user_id`](https://aiotieba.cc/tutorial/start#user_id)反查用户信息，普通用户接触不到<br>

后面还会频繁使用到这个参数`id`的概念，**请记住它**！

***举例***

```text
@v_guard block 李彦宏
@v_guard block tb.1.8c1d7226.-pTUqhuXLOiqu7xbSIIx-A
@v_guard block @Starry@给你分享了贴吧号#10055118#整段复制后打开贴吧即可找到Ta
@v_guard block #10055118#
@v_guard block /79/
```

以上五条指令实现的效果完全一致，均为将李彦宏封禁十天

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*封禁*是贴吧一项重要的传统功能<br>
不使用第三方工具的吧务需要找到用户在吧里的发帖才能调出封禁选项，而且除大吧主外的其他吧务的用户界面没有3/10天的封禁天数选项，而且吧务不能方便地自定义封禁理由<br>
因此我开发了这个指令以方便吧务通过`id`执行3/10天封禁并支持自定义封禁理由

---

### unblock 解封

```text
@v_guard unblock [id]
```

***功能***

解除`id`对应的用户的封禁状态

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*解封*是贴吧一项重要的传统功能<br>
*解封*需要进吧务后台操作，对于封禁列表较长的巨型贴吧显得操作不便<br>
因此我开发了这个指令。吧务在处理用户申诉时可直接通过`id`解封，提高上述情境下的操作效率

---

### drop 删封

```text
@v_guard drop [reason]
@v_guard dropx [reason]
```

***功能***

如果这条指令是一条`回复`，那么指令所在主题帖会被*删除*，并且楼主会被*封禁*<br>
如果这条指令是一条`楼中楼`，那么指令所在回复会被*删除*，并且层主会被*封禁*<br>
如果这条指令是一条`转发了另一主题帖的主题帖`，那么被转发的主题帖会被*删除*，并且该主题帖的楼主会被*封禁*<br>
drop: 对应10天封禁<br>
dropx: 对应x天封禁<br>
在使用该指令时请**特别注意指令的发送位置**，以免产生意料之外的效果

***参数说明***

`x`: 若吧务账号无svip则仅可封禁1/3/10天，分别对应`drop1` `drop3` `drop/drop10`。若因无svip导致封禁失败则会再次尝试封禁10天

`reason`: 可选参数，封禁理由

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

[`block`](#block-封禁)和[`delete`](#delete-删帖)的组合，用于提升删封操作效率

---

### recommend 首页推荐

```text
@v_guard recommend
```

***功能***

对`指令所在主题帖`执行`大吧主首页推荐`操作

***能使用该指令的最低权限级别***

10 非吧务的优秀创作者

***开发者说***

`大吧主首页推荐`是一项聊胜于无的内容管理功能<br>
百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### move 移动分区

```text
@v_guard move [tab_name]
```

***功能***

将`指令所在主题帖`移动至`tab_name`指定的分区

***参数说明***

`tab_name`: 目标分区的名称

***举例***

```text
@v_guard move 无关水
```

若该指令生效，指令所在主题帖将会被移动到`无关水`分区

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

帖子分区是贴吧app11+新增的功能<br>
百度并未将移动帖子所属分区的功能的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### good 加精

```text
@v_guard good [cname]
```

***功能***

将`指令所在主题帖`添加或移动到`cname`指定的精品分区，俗称*加精*

***参数说明***

`cname`: 目标精品分区的名称。将该参数留空则不分区，帖子会被添加或完全移动到精品区的`全部`中

***举例***

```text
@v_guard good 优质二创
```

若该指令生效，指令所在主题帖将会被添加或移动到`优质二创`分区

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*加精*是贴吧一项重要的传统功能<br>
可惜的是百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### ungood 撤精

```text
@v_guard ungood
```

***功能***

撤销`指令所在主题帖`的精华，俗称*撤精*

***能使用该指令的最低权限级别***

20 普通吧务

***开发者说***

*撤精*是贴吧一项重要的传统功能<br>
可惜的是百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### top 置顶

```text
@v_guard top
```

***功能***

置顶`指令所在主题帖`

***能使用该指令的最低权限级别***

40 大吧主

***开发者说***

*置顶*是贴吧一项重要的传统功能<br>
可惜的是百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### untop 撤置顶

```text
@v_guard untop
```

***功能***

取消`指令所在主题帖`的置顶

***能使用该指令的最低权限级别***

30 高权限吧务

***开发者说***

*取消置顶*是贴吧一项重要的传统功能<br>
可惜的是百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### black 黑名单

```text
@v_guard black [id] [note]
```

***功能***

将`id`对应的用户的权限级别设为`-50`，等同于加入脚本黑名单

需要配合云审查工具才能产生效果

当云审查工具发现权限级别为`-50`的用户时，会立即删帖并封十天，效果等同于十循

操作者的权限级别必须大于被操作者的权限级别

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串<br>
`note`: 可选参数，操作理由，方便日后查阅

***能使用该指令的最低权限级别***

40 大吧主

***开发者说***

对于十循列表较长的巨型贴吧，大量的循环封禁操作会污染后台日志<br>
因此我开发了脚本黑名单功能用于配合云审查工具实现“软十循”

---

### white 白名单

```text
@v_guard white [id] [note]
```

***功能***

将`id`对应的用户的权限级别设为`10`，等同于加入脚本白名单<br>
需要配合云审查工具才能产生效果<br>
云审查工具不会删除任何权限级别大于等于`10`的用户发布的内容<br>
修改权限时，操作者的权限级别必须大于被操作者的权限级别

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串<br>
`note`: 可选参数，操作理由，方便日后查阅

***能使用该指令的最低权限级别***

30 高权限吧务

***开发者说***

云审查工具可能会误删吧务或其他创作者发布的长篇内容<br>
因此我开发了脚本白名单功能用于帮助这些用户绕过云审查工具

---

### reset 重置权限

```text
@v_guard reset [id]
```

***功能***

需要配合云审查工具才能产生效果<br>
清除`id`对应的用户的的权限级别，即重置成普通用户<br>
修改权限时，操作者的权限级别必须大于被操作者的权限级别

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串

***能使用该指令的最低权限级别***

30 高权限吧务

---

### exdrop 删封循

```text
@v_guard exdrop [note]
```

***功能***

如果这条指令是一条`回复`，那么指令所在主题帖会被*删除*，楼主的权限级别会被设为`-50`并*封禁*90天<br>
如果这条指令是一条`楼中楼`，那么指令所在回复会被*删除*，层主的权限级别会被设为`-50`并*封禁*90天<br>
如果这条指令是一条`转发了另一主题帖的主题帖`，那么被转发的主题帖会被*删除*，该主题帖的楼主的权限级别会被设为`-50`并*封禁*90天<br>
在使用该指令时请**特别注意指令的发送位置**，以免产生意料之外的效果<br>
修改权限时，操作者的权限级别必须大于被操作者的权限级别。若操作者权限不足则修改权限的请求被拒绝而其余请求正常执行

***参数说明***

`note`: 可选参数，操作理由，方便日后查阅

***能使用该指令的最低权限级别***

40 大吧主

***开发者说***

指令[`block`](#block-封禁) [`delete`](#delete-删帖) [`black`](#black-黑名单)的组合，用于提升删封循操作效率

---

### avada_kedavra 抹除

```text
@v_guard avada_kedavra [note]
```

***功能***

在[`exdrop`](#exdrop-删封循)的基础上追加*清空*发帖人主页显示的在当前吧的所有主题帖<br>
在使用该指令时请**特别注意指令的发送位置**，以免产生意料之外的效果<br>
修改权限时，操作者的权限级别必须大于被操作者的权限级别。由于该指令风险较高，若操作者权限不足则所有请求都将被驳回

***参数说明***

`note`: 可选参数，操作理由，方便日后查阅

***能使用该指令的最低权限级别***

50 后台管理员

***开发者说***

<font color="red">**Avada Kedavra！**</font>

---

### set 设置权限

```text
@v_guard set [id] [permission] [note]
```

***功能***

将`id`对应的用户的权限级别设置为`permission`

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串<br>
`permission`: 目标用户的新权限级别<br>
`note`: 可选参数，操作理由，方便日后查阅

修改权限时，操作者的权限级别必须大于被操作者的当前和修改后的权限级别

***能使用该指令的最低权限级别***

30 高权限吧务

---

### get 用户信息

```text
@v_guard get [id]
```

***功能***

获取贴吧用户的标记信息和个人信息

***举例***

```text
@v_guard get 李彦宏
```

若该指令生效，指令管理器后台将会打印一条日志

```
用户权限级别=0
备注=
被记录的时间=1970-01-01 00:00:00
详细用户信息=UserInfo_pf(user_id=79, portrait='tb.1.8c1d7226.-pTUqhuXLOiqu7xbSIIx-A', user_name='李彦宏', nick_name_new='白皮松林🍁', tieba_uid=10055118, glevel=1, gender=<Gender.MALE: 1>, age=20.4, post_num=126, agree_num=8965, fan_num=12636323, follow_num=92, forum_num=7, sign='', ip='北京', icons=['baiyang'], vimage=VirtualImage_pf(enabled=False, state=''), is_vip=False, is_god=True, is_blocked=False, priv_like=<PrivLike.PUBLIC: 1>, priv_reply=<PrivReply.ALL: 1>)
```

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串

***能使用该指令的最低权限级别***

10 非吧务的优秀创作者

---

### tb_black 贴吧黑名单

```text
@v_guard tb_black [id]
```

***功能***

将`id`对应的用户加入**贴吧黑名单**（无法**签到**，发帖无**经验**）

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串

***能使用该指令的最低权限级别***

40 大吧主

***开发者说***

**添加黑名单**是贴吧的一项传统功能<br>
百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### tb_reset 解贴吧黑名单

```text
@v_guard tb_reset [id]
```

***功能***

将`id`对应的用户移出**贴吧黑名单**

***参数说明***

`id`: [`用户名`](https://aiotieba.cc/tutorial/start#user_name)或[`portrait`](https://aiotieba.cc/tutorial/start#portrait)或包含[`tieba_uid`](https://aiotieba.cc/tutorial/start#tieba_uid)的字符串或包含[`user_id`](https://aiotieba.cc/tutorial/start#user_id)的字符串

***能使用该指令的最低权限级别***

30 高权限吧务

***开发者说***

**解除黑名单**是贴吧的一项传统功能<br>
百度并未将它的执行权限开放给除大吧主以外的其他吧务<br>
大吧主可以通过启用这个指令将权限下放给其他吧务

---

### ping 可用性测试

```text
@v_guard ping
```

***功能***

不执行任何操作。该指令被删除仅说明指令管理器的服务端存活

***能使用该指令的最低权限级别***

10 非吧务的优秀创作者
