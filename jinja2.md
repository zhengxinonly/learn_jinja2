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

## 4 测试器

Jinja2中的测试器Test和过滤器非常相似，区别是测试器总是返回一个布尔值，它可以用来测试一个变量或者表达式，你需要使用”is”关键字来进行测试。测试器一般都是跟着if控制语句一起使用的。下面我们就来深入了解下这个测试器。

### 测试器使用

再次取回开篇的例子，我们在模板中对变量 hello 作如下判断：

```html
<h3>基本测试器</h3>
{% if hello is lower %}
    小写测试器: {{ hello }}
{% endif %}
<br>
```

当`hello`变量中的字母都是小写时，这段文字就会显示。这就是测试器，在`if`语句中，变量或表达式的后面加上`is`关键字，再加上测试器名称，就可以对该变量或表达式作测试，并根据其测试结果的真或假，来决定是否进入`if`语句块。测试器也可以有参数，用括号括起。当其只有一个参数时，可以省去括号。

```html
{% if 6 is divisibleby 3 %}
    除法测试器: {{ 6/3 }}
{% endif %}
<br>
```

上例中，测试器`divisibleby`可以判断其所接收的变量是否可以被其参数整除。因为它只有一个参数，我们就可以用空格来分隔测试器和其参数。上面的调用同`divisibleby(3)`效果一致。测试器也可以配合`not`关键字一起使用：

```html
{% if 6 is not divisibleby(4) %}
    除法测试器:{{ 6/4 }}
{% endif %}
```

显然测试器本质上也是一个函数，它的第一个参数就是待测试的变量，在模板中使用时可以省略去。如果它有第二个参数，模板中就必须传进去。测试器函数返回的必须是一个布尔值，这样才可以用来给if语句作判断。

### 内置测试器 Builtin Tests

同过滤器一样，Jinja2模板引擎提供了丰富的内置测试器。这里介绍几个常用的。

```jinja2
h2>内置测试器</h2>
{% if hello is defined %}
    <p>检查变量是否被定义，也可以用undefined检查是否未被定义: {{ name }}</p>
{% endif %}

{% if hello is not none %}
    检查变量是否为空:name
{% endif %}

<br>
{% if hello is string %}
    检查变量是否为字符串:{{ hello }}
{% endif %}
<br>
{% if 2 is even %}
    也可以用odd检查是否为奇数
{% endif %}
<br>
{% if [1,2,3] is iterable %}
    检查变量是否可被迭代循环,也可以用sequence检查是否是序列
{% endif %}
<br>
{% if {'name':'test'} is mapping %}
    检查变量是否是字典
{% endif %}

```

更全的内置测试器介绍可以从[Jinja2的官方文档](http://jinja.pocoo.org/docs/dev/templates/#builtin-tests)中找到。

### 自定义测试器

如果内置测试器不满足需求，我们就来自己写一个。写法很类似于过滤器，先在Flask应用代码中定义测试器函数，然后通过`add_template_test`将其添加为模板测试器：

```python
import re
def has_number(str):
    return re.match(r'.*\d+', str)
app.add_template_test(has_number,'contain_number')
```

我们定义了一个`has_number`函数，用正则来判断输入参数是否包含数字。然后调用`app.add_template_test`方法，第一个参数是测试器函数，第二个是测试器名称。之后，我们就可以在模板中使用`contain_number`测试器了：

```python
import re


def has_number(str):
    return re.match('.*\d+', str)


app.add_template_test(has_number, 'contain_number')
```

同过滤器一样，Flask提供了添加测试器的装饰器`template_test`。下面的代码就添加了一个判断字符串是否以某一子串结尾的测试器。装饰器的参数定义了该测试器的名称`end_with`：

```python
@app.template_test('end_with')
def end_with(str, suffix):
    return str.lower().endswith(suffix.lower())
```

我们在模板中可以这样使用它：

```python
{% if hello is end_with "!" %}
  <p>自定义结尾过滤器: {{ hello }}</p>
{% endif %}
```

Flask添加测试器的方法是封装了对Jinja2环境变量的操作。上述添加`end_with`测试器的方法，等同于下面的代码。

```python
app.jinja_env.tests['end_with'] = end_with
```

我们在Flask应用中，不建议直接访问 `Jinja2` 的环境变量。如果离开Flask环境直接使用`Jinja2` 的话，就可以通过`jinja2.Environment`来获取环境变量，并添加测试器。

## 5 全局函数

介绍完了过滤器和测试器，接下来要讲的是Jinja2模板引擎的另一个辅助函数功能，即全局函数Global Functions。如果说过滤器是一个变量转换函数，测试器是一个返回布尔值的函数，那全局函数就可以是任意函数。可以在任一场景使用，没有输入和输出值的限制。本篇我们就来阐述下这个全局函数。

### 全局函数使用

继续之前的开篇的代码，我们在模板中加入下面的代码：

```python
<h2>全局函数使用</h2>
<h3>range</h3>
<ul>
    {% for num in range(10, 20, 2) %}
        <li>for遍历: {{ num }}</li>
    {% endfor %}
</ul>
```

页面上会显示”10,12,14,16,18”5个列表项。全局函数`range()`的作用同Python里的一样，返回指定范围内的数值序列。三个参数分别是开始值，结束值（不包含），间隔。如果只传两个参数，那间隔默认为1；如果只传1个参数，那开始值默认为0。

由此可见，全局函数如同其名字一样，就是全局范围内可以被使用的函数。其同[第二篇](http://www.bjhee.com/jinja2-context.html)介绍的上下文环境中定义的函数不同，没有请求生命周期的限制。

### 内置全局函数

演示几个常用的内置全局函数。

- `dict()`函数，方便生成字典型变量

```jinja2
<h3>dict</h3>
{% set user = dict(name='Mike',age=15) %}
<p>{{ user | tojson | safe }}</p>
```

- `joiner()`函数，神奇的辅助函数。它可以初始化为一个分隔符，然后第一次调用时返回空字符串，以后再调用则返回分隔符。对分隔循环中的内容很有帮助

```jinja2
<h3>joiner</h3>
{% set sep = joiner("|") %}
{% for val in range(5) %}
    {{ sep() }} <span>{{ val }}</span>
{% endfor %}
```

- `cycler()`函数，作用同[第一篇](http://www.bjhee.com/jinja2-statement.html)介绍的循环内置变量`loop.cycle`类似，在给定的序列中轮循

```jinja2
<h3>cycle</h3>
{% set cycle = cycler('odd', 'even') %}
<ul>
{% for num in range(10, 20, 2) %}
    <li class="{{ cycle.next() }}">编号: {{ num }},
    当前的累名 {{ cycle.current }} </li>
{% endfor %}
</ul>
```

基于上一节的例子，加上`cycler()`函数的使用，你会发现列表项``的`class`在”odd”和”even”两个值间轮循。加入[第一篇](http://www.bjhee.com/jinja2-statement.html)中的CSS style，就可以看到斑马线了。

`cycler()`函数返回的对象可以做如下操作

1. `next()`，返回当前值，并往下一个值轮循
2. `reset()`，重置为第一个值
3. `current`，当前轮循到的值

更全的内置全局函数介绍可以从[Jinja2的官方文档](http://jinja.pocoo.org/docs/dev/templates/#list-of-global-functions)中找到。

### 自定义全局函数

我们当然也可以写自己的全局函数，方法同之前介绍的过滤器啦，测试器啦都很类似。就是将Flask应用代码中定义的函数，通过`add_template_global`将其传入模板即可：

```python
import re


def accept_pattern(pattern_str):
    pattern = re.compile(pattern_str, re.S)

    def search(content):
        return pattern.findall(content)

    return dict(search=search, current_pattern=pattern_str)


app.add_template_global(accept_pattern, 'accept_pattern')
```

上例中的`accept_pattern`函数会先预编译一个正则，然后返回的字典中包含一个查询函数`search`，之后调用`search`函数就可以用编译好的正则来搜索内容了。`app.add_template_global`方法的第一个参数是自定义的全局函数，第二个是全局函数名称。现在，让我们在模板中使用`accept_pattern`全局函数：

```jinja2
<h2>自定义全局函数</h2>
{% with pattern = accept_pattern("<li>(.*?)</li>") %}
  {% set founds = pattern.search("<li>Tom</li><li>Bob</li>") %}
  <ul>
  {% for item in founds %}
    <li>找到一个内容: {{ item }}</li>
  {% endfor %}
  </ul>
  <p>正则规则: {{ pattern.current_pattern }}</p>
{% endwith %}
```

“Tom”和”Bob”被抽取出来了，很牛掰的样子。你还可以根据需要在`accept_pattern`的返回字典里定义更多的方法。

Flask同样提供了添加全局函数的装饰器`template_global`，以方便全局函数的添加。我们来用它将第二篇中取系统当前时间的函数`current_time`定义为全局函数。

```python
@app.template_global('current_time')
def current_time(timeFormat="%Y-%m-%d - %H:%M:%S"):
    return time.strftime(timeFormat)
```

同[第二篇](http://www.bjhee.com/jinja2-context.html)中的一样，我们在模板中可以这样使用它：

```html
<br>
<p>当前时间: {{ current_time() }}</p>
<p>当前日期: {{ current_time("%Y-%m-%d") }}</p>
```

Flask添加全局函数的方法是封装了对Jinja2环境变量的操作。上述添加`current_time`全局函数的方法，等同于下面的代码。

```python
app.jinja_env.globals['current_time'] = current_time
```

我们在Flask应用中，不建议直接访问 Jinja2 的环境变量。如果离开Flask环境直接使用 Jinja2 的话，就可以通过`jinja2.Environment`来获取环境变量，并添加全局函数。

## 6 块和宏

考虑到模板代码的重用，Jinja2提供了块 (Block)和宏 (Macro)的功能。块功能有些类似于C语言中的宏，原理就是代码替换；而宏的功能有些类似于函数，可以传入参数。本篇我们就来介绍下块和宏的用法。

### 块 (Block)

前面介绍模板时，我们提到了模板的继承。我们在子模板的开头定义了`{% extend 'parent.html' %}`语句来声明继承，此后在子模板中由`{% block block_name %}`和`{% endblock %}`所包括的语句块，将会替换父模板中同样由`{% block block_name %}`和`{% endblock %}`所包括的部分。

这就是块的功能，模板语句的替换。这里要注意几个点：

1. 模板不支持多继承，也就是子模板中定义的块，不可能同时被两个父模板替换。
2. 模板中不能定义多个同名的块，子模板和父模板都不行，因为这样无法知道要替换哪一个部分的内容。

另外，我们建议在`endblock`关键字后也加上块名，比如`{% endblock block_name %}`。虽然对程序没什么作用，但是当有多个块嵌套时，可读性好很多。

#### 保留父模板块的内容

如果父模板中的块里有内容不想被子模板替换怎么办？我们可以使用`super()`方法。定义一个父模板 `06块和宏/layout.html` 改为：

```html
<!DOCTYPE>
<head>
    {% block head %}
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
        <title>{% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body>
<div class="page">
    {% block body %}
    {% endblock %}
</div>

{% include ['06块和宏/footer.html','06块和宏/bottom.html'] ignore missing %}
</body>
```

并在子模板(`06块和宏.html`)里，加上 `head` 块和 `title` 块：

```html
{% extends "06块和宏/layout.html" %}
{% block title %}Block Sample{% endblock %}
{% block head %}
    {{ super() }}
    <style type="text/css">
        h1 {
            color: #336699;
        }
    </style>
{% endblock %}
```

父模板同子模板的 `head` 块中都有内容。运行后，你可以看到，父模板中的 `head` 块语句先被加载，而后是子模板中的”head”块语句。这就得益于我们在子模板的”head”块中加上了表达式`{{ super() }}`。效果有点像Java中的`super()`吧。

#### 块内语句的作用域

默认情况下，块内语句是无法访问块外作用域中的变量。比如我们在`06块和宏/layout.htm`加上一个循环：

```html
{% for item in range(5) %}
    <li>{% block list scoped %}{% endblock %}</li>
{% endfor %}
```

然后在子模板(`06块和宏.html`)中定义”list”块并访问循环中的”item”变量：

```html
{% block list %}
    <em>{{ item }}</em>
{% endblock %}
```

你会发现页面上什么数字也没显示。如果你想在块内访问这个块外的变量，你就需要在块声明时添加`scoped`关键字。比如我们在`06块和宏/layout.htm`中这样声明 `lis` 块即可：

```html
{% for item in range(5) %}
    <li>{% block list scoped %}{% endblock %}</li>
{% endfor %}
```

### 宏 (Macro)

文章的开头我们就讲过，Jinja2的宏功能有些类似于传统程序语言中的函数，既然是函数就有其声明和调用两个部分。那就让我们先声明一个宏：

```jinja2
{# 定义input宏 #}
{% macro input(name, type='text', value='') -%}
    <input type="{{ type }}" name="{{ name }}" value="{{ value|e }}">
{%- endmacro %}
```

代码中，宏的名称就是”input”，它有三个参数分别是”name”, “type”和”value”，后两个参数有默认值。现在可以直接使用表达式来调用这个宏：

```html
<p>{{ input('username', value='user') }}</p>
<p>{{ input('password', 'password') }}</p>
<p>{{ input('submit', 'submit', 'Submit') }}</p>
```

大家可以在页面上看到一个文本输入框，一个密码输入框及一个提交按钮。是不是同函数一样啊？其实它还有比函数更丰富的功能，之后我们来介绍。

#### 宏的导入

一个宏可以被不同的模板使用，所以我们建议将其声明在一个单独的模板文件中。需要使用时导入进来即可，而导入的方法也非常类似于Python中的”import”。让我们将第一个例子中”input”宏的声明放到一个”form.html”模板文件中，然后将调用的代码改为：

```python
{% block body %}
    <hr>
    <h2>宏 (Macro)</h2>
    {% import '06块和宏/form.html' as form %}
    <p>{{ form.input('username', value='user') }}</p>
    <p>{{ form.input('password', 'password') }}</p>
    <p>{{ form.input('submit', 'submit', 'Submit') }}</p>
    {% from '06块和宏/form.html' import input %}
    <p>{{ input('username', value='user') }}</p>
    <p>{{ input('password', 'password') }}</p>
    <hr>
{% endblock body %}
```

运行下，效果是不是同之前的一样？

#### 宏的内部变量

上例中，我们看到宏的内部可以使用`caller( )`方法获取调用者的内容。此外宏还提供了两个内部变量：

- varargs
  这是一个列表。如果调用宏时传入的参数多于宏声明时的参数，多出来的**没指定参数名**的参数就会保存在这个列表中。
- kwargs
  这是一个字典。如果调用宏时传入的参数多于宏声明时的参数，多出来的**指定了参数名**的参数就会保存在这个字典中。

让我们回到第一个例子`input`宏，在调用时增加其传入的参数，并在宏内将上述两个变量打印出来：

```jinja2
{% macro input(name, type='text', value='') -%}
    <input type="{{ type }}" name="{{ name }}" value="{{ value|e }}">
    <br /> {{ varargs }}
    <br /> {{ kwargs }}
{%- endmacro %}


<p>{{ input('submit', 'submit', 'Submit', 'more arg1', 'more arg2', ext='more arg3') }}</p>
```

可以看到，`varargs`变量存了参数列表`['more arg1', 'more arg2']`，而kwargs字典存了参数`{'ext':'more arg3'}`。

#### 访问调用者内容

我们先来创建个宏”list_users”：

```jinja2
{% macro list_users(users) -%}
    <table>
        <tr>
            <th>姓名</th>
            <th>操作</th>
        </tr>
        {%- for user in users %}
            <tr>
                <td>{{ user.name |e }}</td>
                {{ caller() }}</tr>
        {%- endfor %}
    </table>
{%- endmacro %}
```

宏的作用就是将用户列表显示在表格里，表格每一行用户名称后面调用了`{{ caller( ) }}`方法，这个有什么用呢？先别急，我们来写调用者的代码：

```jinja2
{% set users=[{'name':'Tom','gender':'M','age':20},
              {'name':'John','gender':'M','age':18},
              {'name':'Mary','gender':'F','age':24}]
%}

{% call list_users(users) %}
    <td><input name="delete" type="button" value="Delete"></td>
{% endcall %}
```

与上例不同，这里我们使用了`{% call %}`语句块来调用宏，语句块中包括了一段生成”Delete”按钮的代码。运行下试试，你会发现每个用户名后面都出现了”Delete”按钮，也就是`{{ caller( ) }}`部分被调用者`{% call %}`语句块内部的内容替代了。不明觉厉吧！其实吧，这个跟函数传个参数进去没啥大区别，个人觉得，主要是有些时候HTML语句太复杂（如上例），不方便写在调用参数上，所以就写在`{% call %}`语句块里了。

Jinja2的宏不但能访问调用者语句块的内容，还能给调用者传递参数。嚯，这又是个什么鬼？我们来扩展下上面的例子。首先，我们将表格增加一列性别，并在宏里调用`caller()`方法时，传入一个变量`user.gender`：

```html
{% macro list_users2(users) -%}
    <table>
        <tr>
            <th>姓名</th>
            <th>性别</th>
            <th>操作</th>
        </tr>
        {%- for user in users %}
            <tr>
                <td>{{ user.name |e }}</td>
                {{ caller(user.gender) }}</tr>
        {%- endfor %}
    </table>
{%- endmacro %}
```

然后，我们修改下调用者语句块：

```html
{% call(gender) list_users(users) %}
    <td>
    {% if gender == 'M' %}
    <img src="{{ url_for('static', filename='img/male.png') }}" width="20px">
    {% else %}
    <img src="{{ url_for('static', filename='img/female.png') }}" width="20px">
    {% endif %}
    </td>
    <td><input name="delete" type="button" value="Delete"></td>
{% endcall %}
```

大家注意到，我们在使用`{% call %}`语句时，将其改为了`{% call(gender) ... %}`，这个括号中的`gender`就是用来接受宏里传来的`user.gender`变量。因此我们就可以在`{% call %}`语句中使用这个`gender`变量来判断用户性别。这样宏就成功地向调用者传递了参数。

### 包含 (Include)

这里我们再介绍一个Jinja2模板中代码重用的功能，就是包含 (Include)，使用的方法就是`{% include %}`语句。其功能就是将另一个模板加载到当前模板中，并直接渲染在当前位置上。它同导入”import”不一样，”import”之后你还需要调用宏来渲染你的内容，”include”是直接将目标模板渲染出来。它同block块继承也不一样，它一次渲染整个模板文件内容，不分块。

我们可以创建一个"footer.html"模板，并在"06块和宏/layout.html"中包含这个模板：

```html
<body>
    ...
    {% include 'footer.html' %}
</body>
```

当”include”的模板文件不存在时，程序会抛出异常。你可以加上”ignore missing”关键字，这样如果模板不存在，就会忽略这段`{% include %}`语句。

```python
{% include '06块和宏/footer.html' %}
```

`{% include %}`语句还可以跟一个模板列表：

```jinja2
{% include ['footer.html','bottom.html','end.html'] ignore missing %}
```

上例中，程序会按顺序寻找模板文件，第一个被找到的模板即被加载，而其后的模板都会被忽略。如果都没找到，那整个语句都会被忽略。