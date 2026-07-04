from pathlib import Path
import json
import re

app_path = Path("assets/app.js")
css_path = Path("assets/style.css")
json_path = Path("data/news.json")

for path in (app_path, css_path, json_path):
    if not path.exists():
        raise SystemExit(f"找不到文件：{path}")

# 1. 删除 app.js 中之前加入的分类、筛选、排序和视图工具栏
app = app_path.read_text(encoding="utf-8")

start_marker = "  // ZORIX_NEWSROOM_TOOLBAR_V3"
end_marker = "  const escapeHtml = value =>"

if start_marker in app and end_marker in app:
    start = app.index(start_marker)
    end = app.index(end_marker, start)
    app = app[:start] + app[end:]

app_path.write_text(app, encoding="utf-8")

# 2. 添加覆盖样式，彻底隐藏可能残留的分类工具栏
css = css_path.read_text(encoding="utf-8")

css_marker = "/* REMOVE NEWSROOM CATEGORIES V4 */"
css_patch = r'''
/* REMOVE NEWSROOM CATEGORIES V4 */
.newsroom-controls,
.newsroom-categories,
.newsroom-tools {
  display: none !important;
}

.news-panel {
  margin-top: 18px;
}

.news-grid {
  padding-top: 0;
}
'''

if css_marker not in css:
    css += "\n" + css_patch

css_path.write_text(css, encoding="utf-8")

# 3. 扩充新闻正文
data = json.loads(json_path.read_text(encoding="utf-8"))

items = data.get("news", [])
target = next(
    (
        item for item in items
        if item.get("id") == "zorix-nex-coder-2-8-release"
    ),
    None
)

if target is None:
    raise SystemExit("找不到新闻：zorix-nex-coder-2-8-release")

target["summary"] = {
    "zh-CN": "Zorix 正式发布 Nex Coder 2.8。本次版本围绕代码理解、上下文处理、响应速度、代码审查和开发工具兼容性进行了全面升级。",
    "en": "Zorix officially releases Nex Coder 2.8, introducing major improvements to code understanding, context processing, response speed, code review, and development-tool compatibility.",
    "it": "Zorix pubblica ufficialmente Nex Coder 2.8, con importanti miglioramenti nella comprensione del codice, nella gestione del contesto, nella velocità di risposta, nella revisione del codice e nella compatibilità con gli strumenti di sviluppo."
}

target["html"] = {
    "zh-CN": """
<p>Zorix 正式宣布，<strong>Nex Coder 2.8</strong> 现已面向开发者开放。此次更新不仅提升了代码生成速度，还重新设计了模型处理大型项目、跨文件依赖和复杂开发任务的方式。</p>

<p>Nex Coder 2.8 的开发目标，是让 AI 编程助手从简单的代码补全工具，进一步发展为能够理解项目结构、分析问题并参与完整软件开发流程的智能开发系统。</p>

<h2>更深入的项目理解能力</h2>

<p>在过去的代码助手中，模型通常只能读取当前文件或较短的上下文。当项目包含大量模块、依赖关系和配置文件时，生成结果可能缺少对整体架构的理解。</p>

<p>Nex Coder 2.8 加强了多文件上下文处理能力，可以同时分析相关源代码、接口定义、配置文件和项目目录结构，从而提供更符合现有工程规范的建议。</p>

<ul>
  <li>识别跨文件函数、类和模块之间的引用关系</li>
  <li>根据项目现有代码风格生成一致的代码</li>
  <li>分析接口调用、数据结构和依赖关系</li>
  <li>在修改一个模块时提示可能受影响的其他文件</li>
</ul>

<h2>响应速度与稳定性提升</h2>

<p>本次更新对核心推理流程进行了优化。在常见代码补全、错误解释和函数生成任务中，平均响应速度较上一版本有所提升。</p>

<p>对于较长的开发对话，Nex Coder 2.8 也改进了上下文管理方式，减少模型遗忘早期要求或重复生成已经完成内容的情况。</p>

<ul>
  <li>优化首个响应内容的生成速度</li>
  <li>减少长代码任务中的重复输出</li>
  <li>提升大型代码块生成的稳定性</li>
  <li>改善长时间连续对话中的上下文一致性</li>
</ul>

<h2>智能代码审查</h2>

<p>Nex Coder 2.8 可以协助开发者检查代码中的潜在问题，包括逻辑缺陷、异常处理不足、重复实现、类型不一致以及可能影响性能的写法。</p>

<p>代码审查功能会尽量结合当前项目的实际上下文，而不是只根据单个代码片段给出通用建议。</p>

<ul>
  <li>发现可能导致运行时错误的代码路径</li>
  <li>识别未处理的异常和边界条件</li>
  <li>提供更容易维护的重构建议</li>
  <li>解释修改的原因以及可能带来的影响</li>
</ul>

<h2>调试和错误分析</h2>

<p>开发者可以向 Nex Coder 2.8 提供错误日志、堆栈信息、终端输出和相关代码。系统会分析错误出现的位置，并给出可能的原因和修复步骤。</p>

<p>对于复杂问题，Nex Coder 2.8 会将排查过程分解为多个阶段，包括确认问题、缩小范围、验证假设和提供修改方案。</p>

<h2>语言和框架支持</h2>

<p>本次版本进一步改善了对现代开发语言和工具链的支持，其中包括 Python、JavaScript、TypeScript、Java、C、C++、Rust、Go、HTML、CSS、SQL 和 Shell。</p>

<p>针对 Python 3.12 和 TypeScript 5.6，Nex Coder 2.8 加强了新语法、类型系统和项目配置的理解能力。同时，它也改善了对常见前端框架、Node.js 服务端项目和命令行工具的支持。</p>

<h2>适用于不同开发场景</h2>

<p>Nex Coder 2.8 可以用于多个软件开发阶段：</p>

<ul>
  <li><strong>项目创建：</strong>生成基础目录、配置文件和初始代码</li>
  <li><strong>功能开发：</strong>根据需求实现页面、接口和业务逻辑</li>
  <li><strong>错误修复：</strong>分析日志并提供可执行的修改方案</li>
  <li><strong>代码重构：</strong>改善结构、可读性和可维护性</li>
  <li><strong>文档生成：</strong>生成函数说明、接口文档和项目介绍</li>
  <li><strong>代码学习：</strong>解释复杂代码和技术概念</li>
</ul>

<h2>安全与开发者控制</h2>

<p>Zorix 建议开发者在将 AI 生成的代码应用到生产环境前进行人工审查、测试和安全验证。Nex Coder 2.8 提供的是开发辅助能力，最终的软件发布决定仍应由开发团队负责。</p>

<p>对于涉及账号权限、支付、身份认证、数据库迁移或敏感信息处理的代码，应进行额外检查，并避免直接使用未经验证的生成结果。</p>

<h2>如何使用</h2>

<p>开发者可以通过 Zorix 平台调用 Nex Coder 2.8，也可以将其集成到支持的开发工具和工作流程中。</p>

<p>用户可以提交自然语言需求、现有代码、终端错误或项目结构，让 Nex Coder 2.8 根据实际任务生成建议。</p>

<h2>未来计划</h2>

<p>Zorix 将继续改善大型代码库理解、长期任务执行、自动测试、代码验证和开发工具集成能力。</p>

<p>Nex Coder 2.8 是 Zorix AI 编程产品路线中的重要版本，也为后续更完整的智能开发工作流奠定基础。</p>

<h2>正式上线</h2>

<p><strong>Zorix Nex Coder 2.8 现已正式发布。</strong>开发者可以通过 Zorix 官方服务体验新版本，并关注后续发布的技术文档、更新日志和功能公告。</p>
""".strip(),

    "en": """
<p>Zorix officially announces the release of <strong>Nex Coder 2.8</strong>. This update improves not only code-generation speed, but also the way the model understands large projects, cross-file dependencies, and complex engineering tasks.</p>

<p>The goal of Nex Coder 2.8 is to move beyond basic code completion and provide a development assistant capable of understanding project structure, analyzing problems, and participating in complete software-development workflows.</p>

<h2>Deeper project understanding</h2>

<p>Nex Coder 2.8 introduces improved multi-file context processing. It can analyze source files, interface definitions, configuration files, and project structures together to produce suggestions that better match an existing codebase.</p>

<ul>
  <li>Understands references between files, functions, classes, and modules</li>
  <li>Follows existing coding conventions</li>
  <li>Analyzes interfaces, data structures, and dependencies</li>
  <li>Identifies files that may be affected by a change</li>
</ul>

<h2>Performance and stability</h2>

<p>The core inference workflow has been optimized for faster completion, explanation, and code-generation tasks. Context management has also been improved for longer development conversations.</p>

<ul>
  <li>Faster initial responses</li>
  <li>Less repeated output in long tasks</li>
  <li>More stable generation of large code blocks</li>
  <li>Better consistency across extended conversations</li>
</ul>

<h2>Intelligent code review</h2>

<p>Nex Coder 2.8 can help identify logic problems, missing error handling, duplicated implementations, type inconsistencies, and potentially inefficient code.</p>

<p>Recommendations are generated using the available project context rather than only the isolated code fragment.</p>

<h2>Debugging and error analysis</h2>

<p>Developers can provide logs, stack traces, terminal output, and related code. Nex Coder 2.8 analyzes the likely cause and proposes practical debugging and repair steps.</p>

<h2>Languages and frameworks</h2>

<p>The release improves support for Python, JavaScript, TypeScript, Java, C, C++, Rust, Go, HTML, CSS, SQL, and Shell workflows.</p>

<p>Support for Python 3.12 and TypeScript 5.6 has been expanded, alongside improvements for modern frontend frameworks, Node.js services, and command-line applications.</p>

<h2>Development use cases</h2>

<ul>
  <li>Project initialization and configuration</li>
  <li>Feature implementation</li>
  <li>Error diagnosis and repair</li>
  <li>Code refactoring</li>
  <li>Documentation generation</li>
  <li>Code explanation and learning</li>
</ul>

<h2>Safety and developer control</h2>

<p>Zorix recommends reviewing, testing, and validating AI-generated code before production deployment. Special attention should be given to authentication, payments, permissions, database migrations, and sensitive information.</p>

<h2>Availability</h2>

<p><strong>Zorix Nex Coder 2.8 is now officially available.</strong> Additional technical documentation, release notes, and product updates will be published through the Zorix information center.</p>
""".strip(),

    "it": """
<p>Zorix annuncia ufficialmente il rilascio di <strong>Nex Coder 2.8</strong>. Questo aggiornamento migliora la velocità di generazione del codice e il modo in cui il modello comprende progetti estesi, dipendenze tra file e attività di sviluppo complesse.</p>

<p>L'obiettivo di Nex Coder 2.8 è superare il semplice completamento del codice e offrire un assistente capace di comprendere la struttura del progetto, analizzare problemi e partecipare all'intero flusso di sviluppo software.</p>

<h2>Comprensione più profonda dei progetti</h2>

<p>Nex Coder 2.8 introduce una gestione migliorata del contesto multi-file. Può analizzare insieme file sorgente, definizioni di interfacce, configurazioni e struttura del progetto.</p>

<ul>
  <li>Comprensione dei riferimenti tra file, funzioni, classi e moduli</li>
  <li>Rispetto dello stile già utilizzato nel progetto</li>
  <li>Analisi di interfacce, strutture dati e dipendenze</li>
  <li>Identificazione dei file interessati da una modifica</li>
</ul>

<h2>Prestazioni e stabilità</h2>

<p>Il processo di inferenza principale è stato ottimizzato per rendere più rapide le attività di completamento, spiegazione e generazione del codice.</p>

<ul>
  <li>Risposte iniziali più rapide</li>
  <li>Minore ripetizione nei compiti lunghi</li>
  <li>Generazione più stabile di grandi blocchi di codice</li>
  <li>Maggiore coerenza nelle conversazioni estese</li>
</ul>

<h2>Revisione intelligente del codice</h2>

<p>Nex Coder 2.8 può aiutare a identificare problemi logici, gestione insufficiente degli errori, codice duplicato, incoerenze di tipo e possibili problemi di prestazioni.</p>

<h2>Debug e analisi degli errori</h2>

<p>Gli sviluppatori possono fornire log, stack trace, output del terminale e codice correlato. Il sistema analizza le possibili cause e propone passaggi concreti per la risoluzione.</p>

<h2>Linguaggi e framework</h2>

<p>La versione migliora il supporto per Python, JavaScript, TypeScript, Java, C, C++, Rust, Go, HTML, CSS, SQL e Shell.</p>

<p>È stato inoltre ampliato il supporto per Python 3.12, TypeScript 5.6, framework frontend moderni, servizi Node.js e strumenti da riga di comando.</p>

<h2>Possibili utilizzi</h2>

<ul>
  <li>Creazione e configurazione di progetti</li>
  <li>Sviluppo di nuove funzionalità</li>
  <li>Diagnosi e correzione degli errori</li>
  <li>Refactoring del codice</li>
  <li>Generazione della documentazione</li>
  <li>Spiegazione e apprendimento del codice</li>
</ul>

<h2>Sicurezza e controllo dello sviluppatore</h2>

<p>Zorix consiglia di verificare, testare e validare il codice generato dall'IA prima della pubblicazione in produzione, soprattutto per autenticazione, pagamenti, permessi, migrazioni di database e dati sensibili.</p>

<h2>Disponibilità</h2>

<p><strong>Zorix Nex Coder 2.8 è ora ufficialmente disponibile.</strong> Ulteriore documentazione tecnica, note di rilascio e aggiornamenti saranno pubblicati nel centro informazioni Zorix.</p>
""".strip()
}

json_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

# 4. 更新缓存参数
for html_path in Path(".").glob("*/news/index.html"):
    html = html_path.read_text(encoding="utf-8")

    html = re.sub(
        r'assets/style\.css(?:\?v=[^"]+)?',
        'assets/style.css?v=20260703-9',
        html
    )

    html = re.sub(
        r'assets/app\.js(?:\?v=[^"]+)?',
        'assets/app.js?v=20260703-9',
        html
    )

    html_path.write_text(html, encoding="utf-8")

print("完成：")
print("- 已删除顶部分类栏")
print("- 已删除筛选、排序和视图按钮")
print("- 已补充完整中文、英文和意大利语文章")
print("- 已更新浏览器缓存版本")
