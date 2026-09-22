# 学习与修改指南

这个项目不是需要你一次读懂的成品，而是一条可以逐层追踪的数据链：

```text
用户操作 -> ui.py -> service.py -> repository.py -> database.py -> SQLite
                         |                 |
                    validators.py       model.py
```

## 第一阶段：先理解现有程序

### 1. 运行和观察

启动程序，依次测试添加、编辑、完成、搜索、筛选和删除。观察 `data/todo.db`
是在第一次运行时创建的。

### 2. 追踪“添加任务”

按照下面的顺序阅读：

1. `ui.py` 的 `TodoApp.add()` 获取表单数据。
2. `service.py` 的 `TaskService.add_task()` 组织业务流程。
3. `validators.py` 的 `validate_task_input()` 检查输入。
4. `repository.py` 的 `TaskRepository.create()` 执行参数化 SQL。
5. `database.py` 维护连接和数据库结构。
6. `model.py` 的 `Task` 是返回给各层的数据对象。

学习目标：能够说清楚每个文件的职责，以及为什么 UI 不应直接执行 SQL。

## 第二阶段：建议依次完成的修改

### 练习 1：逾期任务标色

需要学习：

- `ttk.Treeview` 的 tag
- 日期字符串比较的前提
- UI 如何调用 Service 中已有的 `is_overdue()`

建议步骤：

1. 在插入表格行时判断 `self.service.is_overdue(task)`。
2. 给逾期行增加 `overdue` tag。
3. 使用 `self.table.tag_configure()` 设置醒目的文字颜色。
4. 添加 Service 测试，验证已完成任务不会被判定为逾期。

验收：过去日期的未完成任务被标色，完成后恢复普通样式。

### 练习 2：按优先级筛选

需要学习：

- Combobox
- 列表推导式
- 函数参数和默认值
- 多条件筛选

建议步骤：

1. 在 UI 增加 `priority_filter_var` 和 Combobox。
2. 给 `TaskService.list_tasks()` 增加 `priority` 参数。
3. 在 Service 中进行筛选，不在 UI 中复制业务逻辑。
4. 为 All、High、Medium、Low 分别写测试。

验收：搜索、状态筛选和优先级筛选可以同时工作。

### 练习 3：增加任务分类

需要学习：

- 数据库 schema 修改
- `ALTER TABLE`
- dataclass 字段
- SQLite 数据迁移

修改顺序：

1. 在 `Task` 中增加 `category`。
2. 在数据库中增加列，并为旧数据设置默认值。
3. 修改 Repository 的 INSERT、SELECT 映射和 UPDATE。
4. 修改 Validator 和 Service。
5. 修改 UI 输入框和任务列表。
6. 增加数据库往返测试。

验收：升级前的数据库仍可打开，新分类能够在重启后保留。

### 练习 4：增加统计区

需要学习：

- 聚合查询 `COUNT`、`GROUP BY`
- 界面状态刷新
- 性能测量

建议显示：总任务数、未完成数、已完成数和逾期数。

## 第三阶段：你需要掌握的知识

### Tkinter

- `Tk`、`Frame`、`LabelFrame`
- `StringVar`
- `Entry`、`Combobox`、`Treeview`
- `grid` 与 `pack`
- `bind` 事件
- `messagebox`
- 控件状态和列表刷新

### SQLite

- `CREATE TABLE` 和约束
- 参数化 SQL
- INSERT、SELECT、UPDATE、DELETE
- 索引
- 事务、commit 和 rollback
- schema 迁移

### 软件设计

- 单一职责
- UI、业务逻辑和持久化分层
- 依赖方向
- 数据模型与数据库行之间的转换
- 输入验证放在哪一层
- 异常如何传递给 UI

### 测试

- Arrange、Act、Assert
- pytest fixture
- 临时数据库 `tmp_path`
- 正常路径、错误路径和边界条件
- 每次修复缺陷时先增加可复现测试

## 固定修改流程

每开发一个功能，都按这个循环进行：

1. 用一句话写清需求和验收条件。
2. 先在 `tests/` 增加失败测试。
3. 判断功能属于 Model、Validator、Repository、Service 还是 UI。
4. 从底层到界面逐层实现。
5. 运行 `python -m pytest -q`。
6. 手工操作 GUI。
7. 用 Git 提交这个完整的小功能。

不要在一个提交中同时增加多个不相关功能。

## 推荐 Git 节奏

```powershell
git switch -c feature/priority-filter
python -m pytest -q
git add .
git commit -m "feat: add priority filter"
```

一个功能一个分支、一个或少量聚焦提交。测试失败时不要提交为“完成”。

## 三天学习安排

### 第一天

- 跑通程序和测试。
- 追踪添加、编辑、删除三个流程。
- 完成“逾期任务标色”。

### 第二天

- 完成优先级筛选。
- 补充筛选组合测试。
- 检查输入验证和错误提示。

### 第三天

- 添加统计区或分类字段，二选一。
- 做 100、1000、10000 条任务的性能测试。
- 整理架构图、测试结果和质量评价报告。

## 不建议现在做的内容

- 登录注册
- 云同步
- 多用户权限
- 网络 API
- 通知服务
- 自己设计加密算法

这些内容会扩大范围，却不能明显提高本次软件质量实验的完成度。
