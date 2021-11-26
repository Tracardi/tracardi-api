# 核心概念定义

为了更好地了解 Trakardi CDP 是如何运作，你需要学习以下概念的定义。

## 资源 | Resource

为了你能够使用 Tracardi 正常的启动你的新项目，你必须创建一个新的资源。资源将为你提供一个标识符，当用户触发追踪锚点时 Tracardi 会收集用户信息，标识符可以在这个过程中与用户进行绑定方便辨识用户。 资源有两种类型：

1. 事件资源。事件资源通常以各类脚本的形式寄生在载体（宿主）上，宿主可以是网页中、短信或邮件中的跳转连接、kafka 队列的有效负载等。这类资源可以在每次宿主触发指定事件时与 Tracardi 进行交互。
2. 数据资源，例如数据库。数据资源无法通过事件触发与 Tracardi 的交互，必须由 Tracardi 通过主动行为对它进行操作。

具体场景举例：用户在访问寄宿了事件资源的网页时触发了指定事件，Tracardi 收到一个带有用户标识的事件信息，然后利用用户标识和 MySQL 资源进行查询，获取了这个用户的更多信息。

一些事件资源的宿主可能需要用户同意才能进行数据收集，例如：一个网页需要征得用户的同意来收集和储存他或她的数据。

**译者个人理解：**事件资源可以视为一种事件监听器，最常见的就是插入在网页中用来监听用户行为的 JavaScript 代码。数据资源基本上就是数据库连接器，通过配置数据库连接属性保持一个连接池。

## 会话 | Session

会话：一个能在一段时间内记住与服务器上的客户端连接的细节的对象。会话的一个特点是，分配给它的数据通常是临时的、不稳定的。

## 事件 | Event

事件代表了特定时间事件资源的宿主发生的特定的事情（有时间戳属性），例如特定的网页操作行为（点击、浏览等)，这可以用来追踪访问者的行为。你也可以利用事件传递额外的数据，如用户名、购买的物品、查看的页面等。

当特定的 JavaScript 代码被寄存在特定网页后，这个网页的特定行为就会引发事件。同理当一个带有追踪效果的脚本被安装在宿主中之后，它就形成了一个事件监听器。需要监听的事件和它的类型都由你来设定，同时你也可以设定在事件发生时发送那些数据到 Tracardi。

事件可以存储在 Tracardi 或者直接传递给工作流在 Tracardi 的外部进行处理。

## 规则 | Rule

规则定义了当一个事件进入到 Tracardi 系统时那个工作流会被执行。规则由一个条件和一个工作流名称构成，如果条件被满足工作流就会开始运行。条件由事件类型和资源两部分组成，即当某个指定资源发生某个指定事件时条件达成，工作流被触发。其中资源是可选项，如果在定义规则时将资源省略，所有资源在触发指定事件类型的事件时都会执行指定工作流。

## 工作流 | Flows (short for workflows)

Flow is a graph of actions that will run when an event is matched with workflow. Actions may run one after another or in
parallel. Workflow is represented as a graph of nodes and connections between them. Actions are assigned to nodes. Data
flow from action to action is represented by connections between nodes. Actions may perform different tasks such as
copying data from the event to profile, save profile, query for additional data, send to another system or emit another
event.

## Actions

Action is a single task in the workflow. Actions consist of input and output ports. Input ports are used to receive
data. On the other hand, output ports send data via connection to another action. Action is basically a code in the
system. Input ports are mapped to input parameters of a function in code when output ports are mapped to the return
values. Tracardi can be extended by programmers who write code and map it with action, which later on is visible in the
workflow editor as nodes.

## Profile

A profile is a set of data that represents user data. Profiles are updated based on incoming events and data from
external systems. The profile has public and private data. Private data is usually sensitive data such as Name, surname,
e-mail, age, total purchases. Public data is data e.g. on the segment to which the user belongs, last visit, number of
visits, etc.

The profile is updated by the workflow, and more precisely by the actions performed within the workflow. Data from
profiles can be used for marketing campaigns, etc.

## Segment

The segment is the result of the segmentation of customer profiles. A segment can be described by a simple logical rule
or by more complex AI models. The segment is part of the profile. A segment defined in the Tracardi system can be used
in the segmentation workflow. The segment is represented by a simple sentence such as "Customers with high volume of
purchases". 
  
