# Torabot

[Torabot](http://torabot.aip.io)是一个二次元(已经混入了一些三次元的异端 bgm38)事件的(邮件)通知工具. 目前实现了4个模块(mod):

1. Pixiv榜单订阅, 画师订阅. 邮件里附带缩略图.
2. Bilibili新番订阅.
3. 虎穴同人本上架/预售通知. 可以用来抢本子.
4. 人人影视RSS订阅(作为撰写模块的tutorial).

Torabot旨在提供一个可扩展的通知更新框架(虽然最初目的并不是这个...), 可以用于服务终端用户, 或为其它内容聚合服务提供一个独立的通知更新接口(计划中).

本项目目前仍处于原型设计阶段, 其接口在正式版`0.1.0`发布之前可能会有较大改动.

# Install

首先你需要一台linux机器. OSX没试过, 理论上是可以的. Windows的话, 呵呵...

## Python

因为scrapy和fabric不支持Python3, 本站需要两个Python环境: Python `3.3.4+`(前端和后台任务), Python `2.7.6`(scrapy, fabric). 如果你不需要远程部署, 请忽略fabric. 建议使用[pyenv](https://github.com/yyuu/pyenv)和[virtualenvwrapper](https://github.com/yyuu/pyenv-virtualenvwrapper)管理多个Python环境. 本站默认的Python3 virtualenv为torabot, Python2 virtualenv为www27.

在源码根目录下(后文若不特别说明, 脚本执行路径均在源码根目录下):

```
pyenv shell 2.7.6
workon www27
pip install -r dependencies-27.txt
pyenv shell 3.3.4
workon torabot
pip install -r dependencies.txt
pip install -e .
```

最后一句用于注册模块的entry points.

## Scrapy

```
pyenv shell 2.7.6
workon www27
scrapyd &
./deployspy
```

注意每次修改模块的`spy`目录之后都需要重新`deployspy`.

## PostgreSQL

数据库采用PostgreSQL `9.3.4`(没测试过其它版本). 设置好PostgreSQL用户之后:

```
createdb torabot-dev
psql torabot-dev < torabot/db/migrate/schema.0.1.0-33-gc2fbf24.sql
```

其中最后一句需要换成`torabot/db/migrate`目录下具有最新版本号后缀的sql文件. 当然你也可以先导入`torabot/db/schema.sql`然后根据`torabot/db/migrate`目录下的sql文件的版本号后缀依次打上补丁.

## Redis

Redis `2.8.8`(其它版本没试过). 用于进程间通信, 缓存和运行时信息存储.

# Run

首先你需要在根目录下添加`toraconf.py`, 用于保存私有配置, 例如:

```
from torabot.conf import *


TORABOT_REPORT_EMAIL = 'torabot+report@aip.io'
TORABOT_EMAIL_USERNAME = 'torabot@aip.io'
TORABOT_EMAIL_PASSWORD = 'guess it'
TORABOT_ADMIN_IDS = [1]
TORABOT_MOD_PIXIV_SPY_PHPSESSID = 'get it from pixiv cookies'
```

除了上述配置, 可以参考`torabot/conf.py`覆盖其中的默认配置. 其中用于发送通知的邮箱必须是google的.

## Test

```
pyenv shell 2.7.6
workon www27
scrapyd &
pyenv shell 3.3.4
workon torabot
nosetests
```

## Local

```
pyenv shell 2.7.6
workon www27
scrapyd &
pyenv shell 3.3.4
workon torabot
celery worker -A torabot &
celery beat -A torabot &
python run.py
```

如果你需要多线程, 最后一句可以换成:

```
gunicorn -b 0.0.0.0:5000 -k gunicorn_worker.Worker gunicorn_app:app
```

## Remote

参考根据自己的需要修改fabfile.py, 然后使用`fab gunicorn`部署.

# Mod

(本节内容有待完善)

Torabot的最主要目的是提供一个可扩展的通知更新框架. "可扩展"包括:

1. 来源可扩展. 即支持订阅不同的站点.
2. 渲染方式可扩展. 即可以将站点的搜索结果和通知内容在不同的媒体上表现出来(目前实现了web和email, 后续可能加入移动平台客户端).
3. 通知方式可扩展. 这一点和2是相关的, 目前实现了邮件通知.

模块(mod)定义了1和2, 其接口参见`torabot/mods/base.py`. 其中1对应的接口包括`spy`和`changes`. 前者定义了如何抓取一个查询(字符串)对应的界面结构(返回`torabot.ut.bunch.Bunch`, 即一个经过包装的`dict`), 默认采用scrapy抓取; 后者定义了如何比较两个`spy`返回的页面结构, 并返回表示更新的结构(也是`Bunch`的序列). 2对应一系列的`format_xxx`接口, 这些接口均包含一个`view`(字符串)参数, 用于表示渲染目标("web"或"email").

Torabot本身并不限制上述所有`Bunch`的结构, 你可以往其中加入任何东西, 但是每个mod需要负责各自的`Bunch`的构造和解析. Torabot也不限制页面的抓取方法, 虽然默认采用scrapy, 但是对于简单的抓取, 你也可以直接用[requests](http://docs.python-requests.org/en/latest/)等库. 但是请注意, 某些站点的页面并不规范, 解析时可能会有性能问题和内存泄漏(lxml), 建议将抓取逻辑放在独立进程里, 或者采用scrapy.

推荐的写法参见`torabot/mods/yyets`.

创建mod的一般步骤为:

1. `mkdir torabot/mods/foo`
2. `pushd torabot/mods/foo & scrapy startproject foo & mv foo spy & popd`
3. 参考`torabot/mods/yyets`做相应修改.
4. 编辑`setup.py`加入对应的entry point.
5. `deployspy`.

# License

MIT
