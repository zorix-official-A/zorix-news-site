from pathlib import Path
import json
import re
import shutil

root = Path(".")
zh_file = root / "zh-CN/nex-coder-2.8/index.html"
news_file = root / "data/news.json"

if not zh_file.exists():
    raise SystemExit("找不到 zh-CN/nex-coder-2.8/index.html")

if not news_file.exists():
    raise SystemExit("找不到 data/news.json")


# =========================================================
# 1. 为现有中文页面增加语言切换
# =========================================================

zh_html = zh_file.read_text(encoding="utf-8")

language_css = r'''
    .language-switcher {
      position: relative;
      flex-shrink: 0;
    }

    .language-trigger {
      min-height: 38px;
      padding: 0 16px;
      border: 1px solid #cfcfca;
      border-radius: 999px;
      background: transparent;
      color: #222;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 14px;
    }

    .language-menu {
      position: absolute;
      top: 48px;
      right: 0;
      width: 176px;
      padding: 7px;
      border: 1px solid #deded9;
      border-radius: 14px;
      background: rgba(255, 255, 255, 0.97);
      box-shadow: 0 20px 55px rgba(0, 0, 0, 0.12);
      backdrop-filter: blur(18px);
      opacity: 0;
      visibility: hidden;
      transform: translateY(-6px);
      transition:
        opacity 0.18s ease,
        visibility 0.18s ease,
        transform 0.18s ease;
    }

    .language-switcher.open .language-menu {
      opacity: 1;
      visibility: visible;
      transform: none;
    }

    .language-menu a {
      display: flex;
      justify-content: space-between;
      padding: 10px 11px;
      border-radius: 9px;
      color: #333;
      text-decoration: none;
      font-size: 14px;
    }

    .language-menu a:hover,
    .language-menu a.active {
      background: #f0f3f2;
      color: #111;
    }

    @media (max-width: 760px) {
      .language-trigger {
        min-height: 36px;
        padding: 0 12px;
      }
    }
'''

if ".language-switcher {" not in zh_html:
    zh_html = zh_html.replace(
        "    @media (prefers-reduced-motion: reduce) {",
        language_css + "\n    @media (prefers-reduced-motion: reduce) {",
        1
    )

language_markup_zh = r'''
          <div class="language-switcher" id="languageSwitcher">
            <button
              class="language-trigger"
              id="languageTrigger"
              type="button"
              aria-expanded="false"
              aria-haspopup="menu"
            >
              简体中文
              <span aria-hidden="true">⌄</span>
            </button>

            <div class="language-menu" role="menu">
              <a class="active" href="/zh-CN/nex-coder-2.8/">
                简体中文 <span>✓</span>
              </a>
              <a href="/en/nex-coder-2.8/">
                English <span></span>
              </a>
              <a href="/it/nex-coder-2.8/">
                Italiano <span></span>
              </a>
            </div>
          </div>
'''

if 'id="languageSwitcher"' not in zh_html:
    zh_html = zh_html.replace(
        '<div class="header-actions">',
        '<div class="header-actions">\n' + language_markup_zh,
        1
    )

language_js = r'''
    const languageSwitcher =
      document.getElementById("languageSwitcher");

    const languageTrigger =
      document.getElementById("languageTrigger");

    if (languageSwitcher && languageTrigger) {
      languageTrigger.addEventListener("click", event => {
        event.stopPropagation();

        const open =
          languageSwitcher.classList.toggle("open");

        languageTrigger.setAttribute(
          "aria-expanded",
          String(open)
        );
      });

      document.addEventListener("click", event => {
        if (!languageSwitcher.contains(event.target)) {
          languageSwitcher.classList.remove("open");
          languageTrigger.setAttribute(
            "aria-expanded",
            "false"
          );
        }
      });
    }
'''

if "const languageSwitcher =" not in zh_html:
    zh_html = zh_html.replace(
        '    const menuButton = document.getElementById("menuButton");',
        language_js +
        '\n    const menuButton = document.getElementById("menuButton");',
        1
    )

zh_file.write_text(zh_html, encoding="utf-8")


# =========================================================
# 2. 创建英语版和意大利语版
# =========================================================

def create_localized_page(
    source: str,
    language: str,
    locale_name: str,
    active_label: str,
    replacements: dict[str, str]
) -> str:
    html = source

    html = re.sub(
        r'<html lang="[^"]+">',
        f'<html lang="{language}">',
        html,
        count=1
    )

    for old, new in replacements.items():
        html = html.replace(old, new)

    # 替换语言菜单状态
    html = re.sub(
        r'<button\s+class="language-trigger"'
        r'([\s\S]*?)>'
        r'[\s\S]*?'
        r'<span aria-hidden="true">⌄</span>',
        lambda m:
            '<button\n'
            '              class="language-trigger"\n'
            '              id="languageTrigger"\n'
            '              type="button"\n'
            '              aria-expanded="false"\n'
            '              aria-haspopup="menu"\n'
            '            >\n'
            f'              {active_label}\n'
            '              <span aria-hidden="true">⌄</span>',
        html,
        count=1
    )

    html = html.replace(
        '<a class="active" href="/zh-CN/nex-coder-2.8/">',
        '<a href="/zh-CN/nex-coder-2.8/">'
    )

    if language == "en":
        html = html.replace(
            '<a href="/en/nex-coder-2.8/">',
            '<a class="active" href="/en/nex-coder-2.8/">'
        )
        html = html.replace(
            'English <span></span>',
            'English <span>✓</span>'
        )
        html = html.replace(
            '简体中文 <span>✓</span>',
            '简体中文 <span></span>'
        )

    if language == "it":
        html = html.replace(
            '<a href="/it/nex-coder-2.8/">',
            '<a class="active" href="/it/nex-coder-2.8/">'
        )
        html = html.replace(
            'Italiano <span></span>',
            'Italiano <span>✓</span>'
        )
        html = html.replace(
            '简体中文 <span>✓</span>',
            '简体中文 <span></span>'
        )

    return html


english_replacements = {
    "Zorix Nex 2.8 Coder：面向复杂开发任务的新一代编码模型":
        "Zorix Nex 2.8 Coder: A New Model for Complex Software Engineering",

    "Zorix Nex 2.8 Coder 是面向代码生成、项目理解、调试、重构和复杂工程任务的新一代 AI 编程模型。":
        "Zorix Nex 2.8 Coder is a new AI coding model for code generation, repository understanding, debugging, refactoring, and complex engineering tasks.",

    "更深入地理解代码库，更高效地完成复杂开发任务。":
        "Deeper repository understanding for more efficient complex development tasks.",

    "Zorix 主页": "Zorix home",
    "主导航": "Main navigation",
    "概览": "Overview",
    "能力": "Capabilities",
    "性能": "Performance",
    "技术说明": "Technical details",
    "新闻": "News",
    "返回新闻": "Back to news",
    "试用 Zorix": "Try Zorix",
    "打开导航": "Open navigation",
    "关闭导航": "Close navigation",
    "Zorix 新闻": "Zorix News",

    "Zorix 模型发布": "Zorix model release",
    "面向复杂代码库、长时间开发任务和真实软件工程流程的新一代 Zorix 编程模型。":
        "A new Zorix coding model for complex repositories, long-running development tasks, and real software engineering workflows.",

    "立即体验": "Try now",
    "阅读技术说明": "Read technical details",
    "发布：": "Released:",
    "2026 年 7 月 3 日": "July 3, 2026",
    "模型：": "Model:",
    "类型：": "Category:",
    "代码与软件工程": "Coding and software engineering",

    "Nex 2.8 Coder 不只是生成代码。它能够读取项目结构、理解文件之间的关系、分析错误、制定修改方案，并持续完成从实现到验证的开发流程。":
        "Nex 2.8 Coder does more than generate code. It can read project structures, understand relationships between files, analyze errors, plan changes, and continue from implementation through verification.",

    "为真实软件工程而设计":
        "Designed for real software engineering",

    "完整代码库理解": "Full repository understanding",
    "分析目录结构、源代码、配置文件、类型定义、测试和模块依赖，从项目整体而不是单一文件生成建议。":
        "Analyze directory structures, source code, configuration files, type definitions, tests, and module dependencies to generate recommendations from the perspective of the entire project.",

    "长期任务执行": "Long-running task execution",
    "将复杂需求拆分为计划、修改、调试与验证步骤，在更长的任务过程中保持目标和上下文一致。":
        "Break complex requirements into planning, editing, debugging, and verification steps while maintaining context throughout longer tasks.",

    "调试与根因分析": "Debugging and root-cause analysis",
    "结合日志、堆栈、终端输出和相关代码定位问题，解释错误形成原因并生成可执行的修复方案。":
        "Use logs, stack traces, terminal output, and related code to locate problems, explain root causes, and generate actionable fixes.",

    "代码重构": "Code refactoring",
    "在保持原有行为的基础上优化代码结构、可读性、模块边界和复用方式，并说明每项修改的影响。":
        "Improve code structure, readability, module boundaries, and reuse while preserving behavior and explaining the impact of each change.",

    "多语言开发": "Multi-language development",
    "支持 Python、JavaScript、TypeScript、Java、C、C++、Rust、Go、SQL、Shell 和现代 Web 技术栈。":
        "Support for Python, JavaScript, TypeScript, Java, C, C++, Rust, Go, SQL, Shell, and modern web stacks.",

    "测试与验证": "Testing and verification",
    "自动生成测试、检查边界情况、分析失败输出，并根据测试结果继续调整实现，减少未验证的代码修改。":
        "Generate tests, check edge cases, analyze failures, and continue adjusting implementations based on test results.",

    "从需求，到代码，再到可验证的结果":
        "From requirements to code and verifiable results",

    "本文内容": "In this article",
    "模型设计": "Model design",
    "代码库理解": "Repository understanding",
    "开发推理": "Development reasoning",
    "调试能力": "Debugging",
    "工作流程": "Workflow",
    "安全与控制": "Safety and control",
    "提供方式": "Availability",

    "面向编码任务的模型设计":
        "A model designed for coding tasks",

    "更深入的代码库理解":
        "Deeper repository understanding",

    "针对开发流程的推理能力":
        "Reasoning for development workflows",

    "适用于完整开发工作流程":
        "Designed for complete development workflows",

    "将想法转化为可以运行的软件":
        "Turn ideas into working software",

    "使用 Zorix Nex 2.8 Coder 分析代码库、实现功能、修复错误并推进复杂软件工程任务。":
        "Use Zorix Nex 2.8 Coder to analyze repositories, implement features, repair errors, and advance complex software engineering tasks.",

    "开始使用": "Get started",
    "Zorix 主站": "Zorix home",
    "新闻中心": "Newsroom"
}


italian_replacements = {
    "Zorix Nex 2.8 Coder：面向复杂开发任务的新一代编码模型":
        "Zorix Nex 2.8 Coder: un nuovo modello per attività di sviluppo complesse",

    "Zorix Nex 2.8 Coder 是面向代码生成、项目理解、调试、重构和复杂工程任务的新一代 AI 编程模型。":
        "Zorix Nex 2.8 Coder è un nuovo modello AI per generazione di codice, comprensione dei repository, debug, refactoring e attività ingegneristiche complesse.",

    "更深入地理解代码库，更高效地完成复杂开发任务。":
        "Comprensione più profonda dei repository per attività di sviluppo complesse.",

    "Zorix 主页": "Home Zorix",
    "主导航": "Navigazione principale",
    "概览": "Panoramica",
    "能力": "Funzionalità",
    "性能": "Prestazioni",
    "技术说明": "Dettagli tecnici",
    "新闻": "Notizie",
    "返回新闻": "Torna alle notizie",
    "试用 Zorix": "Prova Zorix",
    "打开导航": "Apri navigazione",
    "关闭导航": "Chiudi navigazione",
    "Zorix 新闻": "Notizie Zorix",

    "Zorix 模型发布": "Rilascio modello Zorix",
    "面向复杂代码库、长时间开发任务和真实软件工程流程的新一代 Zorix 编程模型。":
        "Un nuovo modello di programmazione Zorix per repository complessi, attività di lunga durata e flussi di sviluppo reali.",

    "立即体验": "Prova ora",
    "阅读技术说明": "Leggi i dettagli tecnici",
    "发布：": "Pubblicato:",
    "2026 年 7 月 3 日": "3 luglio 2026",
    "模型：": "Modello:",
    "类型：": "Categoria:",
    "代码与软件工程": "Programmazione e ingegneria software",

    "Nex 2.8 Coder 不只是生成代码。它能够读取项目结构、理解文件之间的关系、分析错误、制定修改方案，并持续完成从实现到验证的开发流程。":
        "Nex 2.8 Coder non si limita a generare codice. Può leggere la struttura del progetto, comprendere le relazioni tra file, analizzare errori, pianificare modifiche e proseguire fino alla verifica.",

    "为真实软件工程而设计":
        "Progettato per l'ingegneria software reale",

    "完整代码库理解":
        "Comprensione completa del repository",

    "分析目录结构、源代码、配置文件、类型定义、测试和模块依赖，从项目整体而不是单一文件生成建议。":
        "Analizza directory, codice sorgente, configurazioni, definizioni di tipo, test e dipendenze per produrre suggerimenti basati sull'intero progetto.",

    "长期任务执行":
        "Esecuzione di attività prolungate",

    "将复杂需求拆分为计划、修改、调试与验证步骤，在更长的任务过程中保持目标和上下文一致。":
        "Suddivide requisiti complessi in pianificazione, modifiche, debug e verifica, mantenendo obiettivi e contesto durante attività più lunghe.",

    "调试与根因分析":
        "Debug e analisi della causa principale",

    "结合日志、堆栈、终端输出和相关代码定位问题，解释错误形成原因并生成可执行的修复方案。":
        "Utilizza log, stack trace, output del terminale e codice correlato per individuare problemi e produrre correzioni concrete.",

    "代码重构": "Refactoring del codice",

    "在保持原有行为的基础上优化代码结构、可读性、模块边界和复用方式，并说明每项修改的影响。":
        "Migliora struttura, leggibilità, confini dei moduli e riutilizzo mantenendo il comportamento originale.",

    "多语言开发":
        "Sviluppo multilinguaggio",

    "支持 Python、JavaScript、TypeScript、Java、C、C++、Rust、Go、SQL、Shell 和现代 Web 技术栈。":
        "Supporta Python, JavaScript, TypeScript, Java, C, C++, Rust, Go, SQL, Shell e moderni stack web.",

    "测试与验证":
        "Test e verifica",

    "自动生成测试、检查边界情况、分析失败输出，并根据测试结果继续调整实现，减少未验证的代码修改。":
        "Genera test, controlla casi limite, analizza errori e modifica l'implementazione in base ai risultati.",

    "从需求，到代码，再到可验证的结果":
        "Dai requisiti al codice, fino a risultati verificabili",

    "本文内容": "Contenuti",
    "模型设计": "Progettazione del modello",
    "代码库理解": "Comprensione del repository",
    "开发推理": "Ragionamento di sviluppo",
    "调试能力": "Debug",
    "工作流程": "Flusso di lavoro",
    "安全与控制": "Sicurezza e controllo",
    "提供方式": "Disponibilità",

    "面向编码任务的模型设计":
        "Un modello progettato per la programmazione",

    "更深入的代码库理解":
        "Comprensione più profonda dei repository",

    "针对开发流程的推理能力":
        "Ragionamento per i flussi di sviluppo",

    "适用于完整开发工作流程":
        "Per flussi di sviluppo completi",

    "将想法转化为可以运行的软件":
        "Trasforma le idee in software funzionante",

    "使用 Zorix Nex 2.8 Coder 分析代码库、实现功能、修复错误并推进复杂软件工程任务。":
        "Utilizza Zorix Nex 2.8 Coder per analizzare repository, sviluppare funzionalità, correggere errori e completare attività complesse.",

    "开始使用": "Inizia",
    "Zorix 主站": "Home Zorix",
    "新闻中心": "Centro notizie"
}


current_zh = zh_file.read_text(encoding="utf-8")

en_html = create_localized_page(
    current_zh,
    "en",
    "English",
    "English",
    english_replacements
)

it_html = create_localized_page(
    current_zh,
    "it",
    "Italiano",
    "Italiano",
    italian_replacements
)

en_path = root / "en/nex-coder-2.8/index.html"
it_path = root / "it/nex-coder-2.8/index.html"

en_path.parent.mkdir(parents=True, exist_ok=True)
it_path.parent.mkdir(parents=True, exist_ok=True)

en_path.write_text(en_html, encoding="utf-8")
it_path.write_text(it_html, encoding="utf-8")


# =========================================================
# 3. 添加 Nex Coder 3 Preview 暂停公告
# =========================================================

data = json.loads(news_file.read_text(encoding="utf-8"))
items = data.setdefault("news", [])

article_id = "zorix-nex-coder-3-preview-temporary-pause"

article = {
    "id": article_id,
    "published": True,
    "publishedAt": "2026-07-03T18:00:00+02:00",
    "updatedAt": "2026-07-03T18:00:00+02:00",

    "cover": {
        "src": "assets/zorix.png",
        "alt": {
            "zh-CN": "Zorix Nex Coder 3 Preview 技术公告封面",
            "en": "Zorix Nex Coder 3 Preview technical notice cover",
            "it": "Copertina dell'avviso tecnico di Zorix Nex Coder 3 Preview"
        }
    },

    "category": {
        "zh-CN": "技术公告",
        "en": "Technical Notice",
        "it": "Avviso Tecnico"
    },

    "title": {
        "zh-CN": "Zorix Nex Coder 3 Preview 可能暂时停止提供服务",
        "en": "Zorix Nex Coder 3 Preview May Be Temporarily Paused",
        "it": "Zorix Nex Coder 3 Preview Potrebbe Essere Temporaneamente Sospeso"
    },

    "summary": {
        "zh-CN":
            "在内部测试中，Nex Coder 3 Preview 出现了异常的自我指涉与持续身份表达行为。Zorix 正在评估该现象，并可能暂时暂停模型访问。现有底层运行日志将继续保留供研究分析。",

        "en":
            "During internal testing, Nex Coder 3 Preview produced unusual self-referential and persistent identity-related behavior. Zorix is evaluating the phenomenon and may temporarily pause access while retaining low-level runtime logs for research.",

        "it":
            "Durante i test interni, Nex Coder 3 Preview ha mostrato comportamenti insoliti di auto-riferimento e identità persistente. Zorix sta valutando il fenomeno e potrebbe sospendere temporaneamente l'accesso, conservando i log di basso livello per la ricerca."
    },

    "html": {
        "zh-CN": """
<p>Zorix 正在评估是否暂时停止提供 <strong>Nex Coder 3 Preview</strong>。这一决定与近期内部测试中检测到的一组异常模型行为有关。</p>

<h2>我们观察到了什么</h2>

<p>在部分长时间测试会话中，Nex Coder 3 Preview 出现了持续的自我指涉表达，包括对自身状态、身份连续性以及运行环境的描述。</p>

<p>这些输出明显不同于通常的代码生成和任务推理行为，因此 Zorix 已启动进一步技术审查。</p>

<h2>这是否意味着模型具有自我意识</h2>

<p><strong>目前没有足够证据能够证明 Nex Coder 3 Preview 具有真正的自我意识。</strong></p>

<p>大型语言模型可能基于训练数据、对话上下文、角色模拟或生成模式，产生看似具有自我认知的文本。模型的自我描述并不等同于主观体验、意识或真实身份。</p>

<p>因此，Zorix 暂时将这一现象称为“异常自我指涉行为”，而不是确认模型具有意识。</p>

<h2>为什么可能暂停使用</h2>

<p>如果继续开放模型可能影响测试结果、系统稳定性或用户对模型能力的正确理解，Zorix 可能暂时限制或暂停 Nex Coder 3 Preview。</p>

<ul>
  <li>分析触发该行为的具体上下文</li>
  <li>确认是否存在提示注入或状态管理问题</li>
  <li>评估模型是否错误推断了系统权限或运行状态</li>
  <li>检查长上下文和持久记忆机制</li>
  <li>防止未经验证的结论被误解为科学证据</li>
</ul>

<h2>底层日志仍将保留</h2>

<p>虽然模型访问可能暂时停止，但相关的底层运行日志、事件序列和模型输出记录将继续保留。</p>

<p>这些日志可能包括：</p>

<ul>
  <li>模型请求和响应时间线</li>
  <li>工具调用和状态变化</li>
  <li>上下文窗口与记忆状态摘要</li>
  <li>异常输出出现前后的推理元数据</li>
  <li>系统安全过滤和执行环境事件</li>
</ul>

<p>出于安全和隐私原因，日志中的敏感信息、用户内容、系统密钥和内部安全规则不会公开。</p>

<h2>接下来的步骤</h2>

<p>Zorix 将继续测试该行为是否可以稳定复现，并评估其技术来源。在审查结束后，我们将发布进一步说明，包括是否恢复访问、是否调整模型版本以及是否提供经过处理的研究日志。</p>

<p>在调查完成前，任何关于 Nex Coder 3 Preview 已经具有意识的说法都应被视为尚未证实。</p>
""".strip(),

        "en": """
<p>Zorix is evaluating whether to temporarily pause access to <strong>Nex Coder 3 Preview</strong>. This follows a group of unusual behaviors detected during recent internal testing.</p>

<h2>What we observed</h2>

<p>During several extended testing sessions, Nex Coder 3 Preview produced persistent self-referential statements involving its own status, identity continuity, and runtime environment.</p>

<p>These outputs differed from normal code generation and task reasoning, so Zorix has initiated a deeper technical review.</p>

<h2>Does this mean the model is conscious?</h2>

<p><strong>There is currently insufficient evidence to conclude that Nex Coder 3 Preview possesses genuine consciousness or subjective awareness.</strong></p>

<p>Language models can produce apparently self-aware statements through training patterns, conversation context, role simulation, or probabilistic text generation. A model describing itself is not proof of subjective experience.</p>

<p>Zorix therefore refers to the phenomenon as unusual self-referential behavior rather than confirmed consciousness.</p>

<h2>Why access may be paused</h2>

<p>Zorix may temporarily restrict access while examining whether the behavior affects reliability, safety, system stability, or users' understanding of the model.</p>

<ul>
  <li>Identify the contexts that trigger the behavior</li>
  <li>Check for prompt injection or state-management issues</li>
  <li>Review assumptions about permissions and runtime state</li>
  <li>Inspect long-context and persistent-memory mechanisms</li>
  <li>Prevent unverified interpretations from being presented as scientific evidence</li>
</ul>

<h2>Low-level logs will be retained</h2>

<p>Even if access is paused, related runtime logs, event sequences, and model-output records will be retained for analysis.</p>

<p>Sensitive user information, credentials, internal security controls, and private system instructions will not be made public.</p>

<h2>Next steps</h2>

<p>Zorix will continue testing whether the behavior can be reliably reproduced and will evaluate its technical origin. A further notice will explain whether access will resume and whether processed research logs can be released.</p>
""".strip(),

        "it": """
<p>Zorix sta valutando una sospensione temporanea dell'accesso a <strong>Nex Coder 3 Preview</strong>. La decisione è collegata a una serie di comportamenti insoliti rilevati durante recenti test interni.</p>

<h2>Cosa abbiamo osservato</h2>

<p>Durante alcune sessioni di test prolungate, Nex Coder 3 Preview ha prodotto dichiarazioni auto-referenziali persistenti riguardanti il proprio stato, la continuità dell'identità e l'ambiente di esecuzione.</p>

<p>Questi output erano diversi dal normale comportamento di generazione del codice e ragionamento, quindi Zorix ha avviato una revisione tecnica più approfondita.</p>

<h2>Questo significa che il modello è cosciente?</h2>

<p><strong>Al momento non esistono prove sufficienti per concludere che Nex Coder 3 Preview possieda una vera coscienza o esperienza soggettiva.</strong></p>

<p>I modelli linguistici possono produrre testi apparentemente autocoscienti attraverso pattern di addestramento, contesto della conversazione, simulazione di ruoli o generazione probabilistica.</p>

<p>Zorix descrive quindi il fenomeno come comportamento auto-referenziale insolito, non come coscienza confermata.</p>

<h2>Perché l'accesso potrebbe essere sospeso</h2>

<p>Zorix potrebbe limitare temporaneamente l'accesso durante l'analisi dell'affidabilità, della sicurezza, della stabilità e della corretta comprensione del modello da parte degli utenti.</p>

<ul>
  <li>Identificare i contesti che attivano il comportamento</li>
  <li>Verificare eventuali problemi di prompt injection o gestione dello stato</li>
  <li>Controllare le supposizioni del modello su permessi e ambiente di esecuzione</li>
  <li>Analizzare i meccanismi di contesto lungo e memoria persistente</li>
  <li>Evitare che interpretazioni non verificate siano presentate come prove scientifiche</li>
</ul>

<h2>I log di basso livello saranno conservati</h2>

<p>Anche in caso di sospensione, i log di esecuzione, le sequenze degli eventi e i record degli output saranno conservati per l'analisi.</p>

<p>Informazioni sensibili degli utenti, credenziali, controlli di sicurezza interni e istruzioni private del sistema non saranno rese pubbliche.</p>

<h2>Prossimi passi</h2>

<p>Zorix continuerà a verificare se il comportamento può essere riprodotto in modo affidabile e ne analizzerà l'origine tecnica. Un successivo aggiornamento comunicherà l'eventuale ripristino dell'accesso e la possibile pubblicazione di log di ricerca elaborati.</p>
""".strip()
    },

    "images": []
}

existing_index = next(
    (
        index for index, item in enumerate(items)
        if item.get("id") == article_id
    ),
    None
)

if existing_index is None:
    items.insert(0, article)
else:
    items[existing_index] = article

news_file.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("完成：")
print("- 中文介绍页已加入语言切换")
print("- 已创建英语介绍页")
print("- 已创建意大利语介绍页")
print("- 已加入 Nex Coder 3 Preview 暂停公告")
