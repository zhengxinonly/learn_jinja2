## 1 控制语句

### 回顾基础

基础代码

```
# filename:.flaskenv
FLASK_APP=01流程控制.py
FLASK_DEBUG=True
```



```
# filename:01流程控制.py
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/hello/<name>')
def index(name):

    return render_template('01流程控制.html', name='正心')

```



```html
<!--filename:01流程控制.html-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello Sample</title>
</head>
<body>

<hr>

<h2>变量</h2>
{% if name %}
    <h3>Hello {{ name }}!</h3>
{% else %}
    <h1>Hello World!</h1>
{% endif %}

<hr>

</body>
</html>
```

模板的表达式都是包含在分隔符`{{ }}`内的；控制语句都是包含在分隔符`{% %}`内的；另外，模板也支持注释，都是包含在分隔符`{# #}`内，支持块注释。

### 表达式

表达式一般有这么几种：

- 最常用的是变量，由Flask渲染模板时传过来，比如上例中的`name`
- 也可以是任意一种Python基础类型，比如字符串`{{ "Hello" }}`，用引号括起；或者数值，列表，元祖，字典，布尔值。直接显示基础类型没啥意义，一般配合其他表达式一起用
- 运算。包括算数运算，如`{{ 2 + 3 }}`；比较运算，如`{{ 2 > 1 }}`；逻辑运算，如`{{ False and True }}`
- 过滤器 `|` 和测试器 `is` 。这个在后面会介绍
- 函数调用，如`{{ current_time() }}`；数组下标操作，如`{{ arr[1] }}`
- `in`操作符，如`{{ 1 in [1,2,3] }}`
- 字符串连接符`~`，作用同Python中的`+`一样，如`{{ "Hello " ~ name ~ "!" }}`
- `if`关键字，如`{{ 'Hi, %s' % name if name }}`。这里的`if`不是条件控制语句。

表达式很像Python的语法很相似

```jinja2
<h2>表达式</h2>
<p>字符串: {{ "Hello" }}</p>
<p>字典: {{ {'id':'1', 'name':'hello'} }}</p>
<p>加法运算: {{ 1 + 2 }}</p>
<p>乘法运算: {{ 2 > 1 }}</p>
<p>逻辑运算: {{ False and True }}</p>
<p>成员运算: {{ 1 in [1,2,3] }}</p>

<hr>
```

### 控制语句

Jinja2 的控制语句主要就是条件控制语句`if`，和循环控制语句`for`，语法类似于Python。

我们先改下Python代码中的"hello"函数，让其传入一些参数。

```python
@app.route('/')
@app.route('/hello/<name>')
def index(name=None):
    if not name:
        name = '正心'
    return render_template('01流程控制.html',
                           name=name,
                           digits=[1, 2, 3, 4, 5],
                           users=[{'name': 'John'},
                                  {'name': 'Tom', 'hidden': True},
                                  {'name': 'Lisa'},
                                  {'name': 'Bob'}])
```

#### if判断

```jinja2
<h2>流程控制</h2>
<h3>if判断</h3>
{% if name and name == 'admin'  %}
    这是管理控制台
{% elif name %}
    欢迎回来 {{ name }}
{% else %}
    请登录
{% endif %}
```

上面是一个条件控制语句的例子，注意if控制语句要用`{% endif %}`来结束。模板中无法像代码中一样靠缩进来判断代码块的结束。

#### for循环

再来看个循环的例子

```jinja2
<h3>for循环</h3>
{% for digit in digits %}
    <li>{{ digit }}</li>
{% endfor %}
```

现在，可以看到数字”12345”被一起显示出来了。我们再来看个复杂的循环例子：

```jinja2
<dl>
    {% for user in users if not user.hidden %}
        {% if loop.first %}
            <div>用户列表:</div>
        {% endif %}
        <div class="{{ loop.cycle('odd', 'even') }}">
            <dd>用户 {{ loop.index }} : {{ user.name }}</dd>
        </div>
        {% if loop.last %}
            <dd>总用户数: {{ loop.length }}</dd>
        {% endif %}
    {% else %}
        <li>没有找到用户</li>
    {% endfor %}
</dl>
```

这里有三个知识点。首先for循环支持`else`语句，当待遍历的列表”users”为空或者为None时，就进入`else`语句。

其次，在for语句后使用if关键字，可以对循环中的项作过滤。本例中，所有`hidden`属性为True的”user”都会被过滤掉。

另外，for循环中可以访问Jinja2的循环内置变量。本例中，在第一项前显示标题，最后一项后显示总数，每一项显示序号。另外，奇偶项的HTML div元素会有不同的class。如果加入下面的CSS style，就能看到斑马线。

```
<style type="text/css">
    .odd {
        background-color: #BDF;
    }
</style>
```

Jinja2的循环内置变量主要有以下几个：

| 变量           | 内容                                                  |
| :------------- | :---------------------------------------------------- |
| loop.index     | 循环迭代计数（从1开始）                               |
| loop.index0    | 循环迭代计数（从0开始）                               |
| loop.revindex  | 循环迭代倒序计数（从len开始，到1结束）                |
| loop.revindex0 | 循环迭代倒序计数（从len－1开始，到0结束）             |
| loop.first     | 是否为循环的第一个元素                                |
| loop.last      | 是否为循环的最后一个元素                              |
| loop.length    | 循环序列中元素的个数                                  |
| loop.cycle     | 在给定的序列中轮循，如上例在”odd”和”even”两个值间轮循 |
| loop.depth     | 当前循环在递归中的层级（从1开始）                     |
| loop.depth0    | 当前循环在递归中的层级（从0开始）                     |

### 其他常用语句

#### 忽略模板语法

有时候，我们在页面上就是要显示`{{ }}`这样的符号怎么办？Jinja2提供了`raw`语句来忽略所有模板语法。

```html
{% raw %}
    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
{% endraw %}
```

#### 自动转义

我们将本文一开始的Flask代码`hello()`方法改动下：

```python
def hello(name=None):
    if name is None:
        name = '<em>World</em>'
	...
```

此时，访问`http://localhost:5000/hello`，页面上会显示`Welcome World!`，也就是这个HTML标签被自动转义了。

Flask会对”.html”, “.htm”, “.xml”, “.xhtml”这四种类型的模板文件开启HTML格式自动转义。这样也可以防止HTML语法注入。如果我们不想被转义怎么办？

```python
{% autoescape false %}
  <h1>Hello {{ name }}!</h1>
{% endautoescape %}
```

将`autoescape`开关设为`false`即可，反之，设为`true`即开启自动转义。使用`autoescape`开关前要启用`jinja2.ext.autoescape`扩展，在Flask框架中，这个扩展默认已启用。

#### 赋值

使用`set`关键字给变量赋值：

```python
<h3>赋值</h3>
{% set items = [1,2,3] %}
items: {{ items }}
```

#### with语句

类似于Python中的`with`关键字，它可以限制`with`语句块内对象的作用域：

```python
<h3>with语句</h3>
{% with foo = 1 %}
    {% set bar = 2 %}
    {{ foo + bar }}
{% endwith %}
{#在with外面调用直接报错#}
{#{{ foo + bar }}#}
```

使用`with`关键字前要启用`jinja2.ext.with_`扩展，在Flask框架中，这个扩展默认已启用。

#### 执行表达式

```python
<h3>执行表达式</h3>
{% with arr = ['Sunny'] %}
    {{ arr.append('Rainy') }}
    {{ arr }}
{% endwith %}

```

看上面这段代码，我们想执行列表的`append`操作，这时使用`{{ arr.append('Rainy') }}`页面会输出`None`，换成`{% %}`来执行，程序会报错，因为这是个表达式，不是语句。那怎么办？我们可以启用`jinja2.ext.do`扩展。然后在模板中执行`do`语句即可：

```jinja2
<br>
{% with arr = ['Sunny'] %}
  {% do arr.append('Rainy') %}
  {{ arr }}
{% endwith %}
```

## 2 上下文环境

Flask每个请求都有生命周期，在生命周期内请求有其上下文环境Request Context。作为在请求中渲染的模板，自然也在请求的生命周期内，所以Flask应用中的模板可以使用到请求上下文中的环境变量，及一些辅助函数。本文就会介绍下这些变量和函数。

### 标准上下文变量和函数

#### 请求对象request

request对象可以用来获取请求的方法`request.method`，表单`request.form`，请求的参数`request.args`，请求地址`request.url`等。它本身是一个字典。在模板中，你一样可以获取这些内容，只要用表达式符号`{{ }}`括起来即可。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>上下文环境</title>
</head>
<body>
<h3>上下文环境</h3>
<p>当前请求的url: {{ request.url }}</p>
</body>
</html>
```

在没有请求上下文的环境中，这个对象不可用。

#### 会话对象session

session对象可以用来获取当前会话中保存的状态，它本身是一个字典。在模板中，你可以用表达式符号`{{ }}`来获取这个对象。

Flask代码如下，别忘了设置会话密钥哦：

```python
app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def index():
    session['user'] = "游客"
    return render_template('02上下文环境.html')
```

模板代码：

```html
<h3>会话对象session</h3>
<p>用户: {{ session.user }}</p>
```

在没有请求上下文的环境中，这个对象不可用。

#### 全局对象g

全局变量g，用来保存请求中会用到全局内容，比如数据库连接。模板中也可以访问。

Flask代码：

```python
@app.route('/')
def index():
    session['user'] = "游客"
    g.db = "mysql"
    return render_template('02上下文环境.html')
```

模板代码：

```html
<h3>全局对象g</h3>
<p>数据库: {{ g.db }}</p>
```

`g`对象是保存在[应用上下文环境](http://www.bjhee.com/flask-ad1.html)中的，也只在一个请求生命周期内有效。在没有应用上下文的环境中，这个对象不可用。

#### Flask配置对象config

这个配置对象在模板中也可以访问。

```html
<h3>config对象</h3>
<p>配置对象: {{ config.DEBUG }}</p>
```

`config`是全局对象，离开了请求生命周期也可以访问。

#### 消息闪现

`get_flashed_messages()` 函数是用来获取消息闪现的。这也是一个全局可使用的函数。这个就不演示了

### 自定义上下文变量和函数

#### 自定义变量

除了Flask提供的标准上下文变量和函数，我们还可以自己定义。下面我们就来先定义一个上下文变量，在Flask应用代码中，加入下面的函数：

```python
@app.context_processor
def appinfo():
    data = {
        'cate1':'爬虫',
        'cate2':'数据分析',
        'cate3':'人工智能'
    }
    return dict(data=data)
```

函数返回的是一个字典，里面有一个属性`data` 

函数用`@app.context_processor`装饰器修饰，它是一个上下文处理器，它的作用是在模板被渲染前运行其所修饰的函数，并将函数返回的字典导入到模板上下文环境中，与模板上下文合并。然后，在模板中`data`就如同上节介绍的`request`, `session`一样，成为了可访问的上下文对象。我们可以在模板中将其输出：

```html
<hr>

<h2>自定义上下文变量和函数</h2>
<h3>自定义变量</h3>
{% for item in data %}
    <li>{{ data[item] }}</li>
{% endfor %}
```

#### 自定义函数

同理可以自定义上下文函数，只需将上例中返回字典的属性指向一个函数即可，下面我们就来定义一个上下文函数来获取系统当前时间：

```python
import time

@app.context_processor
def get_current_time():
    def get_time(timeFormat="%Y-%m-%d - %H:%M:%S"):
        return time.strftime(timeFormat)

    return dict(current_time=get_time)
```

我们可以试下在模板中将其输出：

```html
<h3>自定义函数</h3>
<p>当前时间: {{ current_time() }}</p>
<p>当前日期: {{ current_time("%Y-%m-%d") }}</p>
```

上下文处理器可以修饰多个函数，也就是我们可以定义多个上下文环境变量和函数。

## 3 过滤器

大部分模板引擎都会提供类似Jinja2过滤器的功能，只不过叫法不同罢了。比如PHP Smarty中的Modifiers（变量调节器或修饰器），FreeMarker中的Build-ins（内建函数），连AngularJS这样的前端框架也提供了Filter过滤器。它们都是用来在变量被显示或使用前，对其作转换处理的。可以把它认为是一种转换函数，输入的参数就是其所修饰的变量，返回的就是变量转换后的值。

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    hello = "hello world !"
    return render_template('03过滤器.html', hello=hello)

```

### 过滤器使用

```html
<h2>过滤器使用</h2>
大写过滤器:{{ hello | upper }}
```

你会看到 hello 的输出都变成大写了。这就是过滤器，只需在待过滤的变量后面加上”|“符号，再加上过滤器名称，就可以对该变量作过滤转换。上面例子就是转换成全大写字母。过滤器可以连续使用

```html
<br>
多个过滤条件: {{ hello | upper | truncate(6, True) }}!
```

现在hello变量不但被转换为大写，而且当它的长度大于3后，只显示前3个字符，后面默认用”…“显示。过滤器`truncate`有3个参数，第一个是字符截取长度；第二个决定是否保留截取后的子串，默认是`False`，也就是当字符大于3后，只显示”…“，截取部分也不出现；第三个是省略符号，默认是”…“。

其实从例子中我们可以猜到，过滤器本质上就是一个转换函数，它的第一个参数就是待过滤的变量，在模板中使用时可以省略去。如果它有第二个参数，模板中就必须传进去。

### 内置过滤器

> Builtin Filters

Jinja2模板引擎提供了丰富的内置过滤器。这里介绍几个常用的。

#### 字符串操作

```jinja2
<h2>内置过滤器</h2>
<h3>字符串过滤器</h3>
<p>当变量未定义时，显示默认字符串，可以缩写为d: {{ hello | default('No hello', true) }}</p>

<p>单词首字母大写: {{ 'hello' | capitalize }}</p>

<p>单词全小写: {{ 'XML' | lower }}</p>

<p>去除字符串前后的空白字符: {{ '  hello  ' | trim }}</p>

<p>字符串反转: {{ 'hello' | reverse }}</p>

<p>格式化输出: {{ '%s is %d' | format("Number", 2) }}</p>

<p>关闭HTML自动转义: {{ '<em>name</em>' | safe }}</p>

{% autoescape false %}
<p>HTML转义,autoescape关了也转义，可以缩写为e: {{ '<em>name</em>' | escape }}</p>
{% endautoescape %}
```

#### 数值操作

```jinja2
<hr>
<h3>数值操作</h3>
<p>12.8888 四舍五入取整: {{ 12.8888 | round }}</p>

<p>向下截取到小数点后2位: {{ 12.8888 | round(2, 'floor') }}</p>

<p>-12 绝对值: {{ -12 | abs }}</p>
```

#### 列表操作

```jinja2
<h3>列表操作</h3>
{% set arr = [1,2,3,4,5]  %}
{{ arr }}
<p>取第一个元素: {{ arr | first }}</p>

<p>取最后一个元素: {{ arr | last }}</p>

<p>返回列表长度: {{ arr | length }}</p>

<p>列表求和: {{ arr | sum }}</p>

<p>列表排序，默认为升序: {{ arr | sort }}</p>

<p>合并为字符串: {{ arr | join(' | ') }}</p>

{# 这里可以用upper,lower，但capitalize无效 #}
<p>列表中所有元素都全大写: {{ ['tom','bob','ada'] | upper }}</p>
```

#### 字典列表操作

```python
<hr>

<h3>字典列表操作</h3>

{% set users=[{'name':'Tom','gender':'M','age':20},
              {'name':'John','gender':'M','age':18},
              {'name':'Mary','gender':'F','age':24},
              {'name':'Bob','gender':'M','age':31},
              {'name':'Lisa','gender':'F','age':19}]
%}

<h4>字典排序</h4>
{# 按指定字段排序，这里设reverse为true使其按降序排 #}
<ul>
{% for user in users | sort(attribute='age', reverse=true) %}
     <li>用户名: {{ user.name }}, 用户年龄: {{ user.age }}</li>
{% endfor %}
</ul>

<h4>列表分组</h4>
{# 列表分组，每组是一个子列表，组名就是分组项的值 #}
<ul>
{% for group in users|groupby('gender') %}
    <li>所属分组: {{ group.grouper }}<ul>
    {% for user in group.list %}
        <li>用户名: {{ user.name }}</li>
    {% endfor %}</ul></li>
{% endfor %}
</ul>

<h4>获取字典某个字段</h4>
{# 取字典中的某一项组成列表，再将其连接起来 #}
<p>{{ users | map(attribute='name') | join(', ') }}</p>
```

更全的内置过滤器介绍可以从[Jinja2的官方文档](http://jinja.pocoo.org/docs/dev/templates/#builtin-filters)中找到。

### Flask内置过滤器

Flask提供了一个内置过滤器`tojson`，它的作用是将变量输出为JSON字符串。这个在配合Javascript使用时非常有用。我们延用上节字典列表操作中定义的”users”变量

```html
<script type="text/javascript">
    var users = {{ users | tojson | safe }};
    console.log(users[0].name);
</script>
```

注意，这里要避免HTML自动转义，所以加上safe过滤器。

### 语句块过滤

Jinja2 还可以对整块的语句使用过滤器。

```html
{% filter upper %}
    This is a Flask Jinja2 introduction.
{% endfilter %}
```

不过上述这种场景不经常用到。

### 自定义过滤器

内置的过滤器不满足需求怎么办？自己写呗。过滤器说白了就是一个函数嘛，我们马上就来写一个。回到Flask应用代码中：

```python
def double_filter(l):
    r = filter(lambda x: x % 2 == 0, l)
    return list(r)
```

我们定义了一个`double_filter`函数，返回输入列表的偶数位元素（第0位，第2位,..）。怎么把它加到模板中当过滤器用呢？Flask应用对象提供了`add_template_filter`方法来帮我们实现。我们加入下面的代码：

```python
app.add_template_filter(double_filter, 'double_step')
```

函数的第一个参数是过滤器函数，第二个参数是过滤器名称。然后，我们就可以愉快地在模板中使用这个叫`double_step`的过滤器了：

```python
<h2>自定义过滤器</h2>
<p>偶数过滤器: {{ [1,2,3,4,5] | double_step }}</p>
```

Flask还提供了添加过滤器的装饰器`template_filter`，使用起来更简单。

```python
@app.template_filter('double_step')
def double_filter(l):
    r = filter(lambda x: x % 2 == 0, l)
    return list(r)
```

Flask添加过滤器的方法实际上是封装了对Jinja2环境变量的操作。上述添加`double_step`过滤器的方法，等同于下面的代码。

```python
app.jinja_env.filters['double_step'] = double_filter
```

我们在Flask应用中，不建议直接访问Jinja2的环境变量。如果离开Flask环境直接使用Jinja2的话，就可以通过`jinja2.Environment`来获取环境变量，并添加过滤器。