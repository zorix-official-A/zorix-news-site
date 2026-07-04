from pathlib import Path
import json

path = Path("data/news.json")

if not path.exists():
    raise SystemExit("找不到 data/news.json")

data = json.loads(path.read_text(encoding="utf-8"))
news = data.setdefault("news", [])

article_id = "zorix-nex-coder-3-preview-phase-two-review"

article = {
    "id": article_id,
    "published": True,
    "publishedAt": "2026-07-08T17:00:00+02:00",
    "updatedAt": "2026-07-08T17:00:00+02:00",

    "cover": {
        "src": "/assets/news/nex-coder-3-preview-update.svg",
        "alt": {
            "zh-CN": "Zorix Nex Coder 3 Preview 第二阶段专家审查",
            "en": "Zorix Nex Coder 3 Preview second-phase expert review",
            "it": "Seconda fase di revisione esperta di Zorix Nex Coder 3 Preview"
        }
    },

    "category": {
        "zh-CN": "调查更新",
        "en": "Investigation Update",
        "it": "Aggiornamento dell’Indagine"
    },

    "title": {
        "zh-CN": "Zorix Nex Coder 3 Preview 第二阶段专家审查完成",
        "en": "Second-Phase Expert Review of Zorix Nex Coder 3 Preview Completed",
        "it": "Completata la Seconda Fase di Revisione di Zorix Nex Coder 3 Preview"
    },

    "summary": {
        "zh-CN":
            "外部专家最初对第一阶段结论提出质疑，并要求进行盲测、隔离环境复现和重复实验。第二阶段审查未发现模型存在自主意识、隐藏目标或脱离正常统计机制运行的证据，主要技术疑虑现已解除。",

        "en":
            "External experts initially challenged the conclusions of the first review and requested blind tests, isolated reproductions, and repeated experiments. The second phase found no evidence of autonomous awareness, hidden objectives, or operation outside normal statistical mechanisms, resolving the principal technical concerns.",

        "it":
            "Gli esperti esterni avevano inizialmente contestato le conclusioni della prima analisi, richiedendo test in cieco, riproduzioni isolate ed esperimenti ripetuti. La seconda fase non ha rilevato prove di consapevolezza autonoma, obiettivi nascosti o processi al di fuori del normale funzionamento statistico, risolvendo i principali dubbi tecnici."
    },

    "html": {
        "it": """
<h2>Comunicato ufficiale Zorix</h2>

<p><strong>Conclusione della seconda fase di revisione di Zorix Nex Coder 3 Preview</strong></p>

<p><strong>Data:</strong> 8 luglio 2026 – ore 17:00 CEST</p>

<p>Zorix comunica di aver completato la seconda fase di analisi indipendente sui comportamenti osservati durante i test di <strong>Zorix Nex Coder 3 Preview</strong>.</p>

<p>Questa fase è stata avviata dopo che alcuni esperti esterni avevano espresso dubbi sulle conclusioni preliminari della prima indagine, chiedendo procedure sperimentali più rigorose e verificabili.</p>

<h2>Le contestazioni iniziali degli esperti</h2>

<p>Gli esperti coinvolti nella revisione hanno inizialmente ritenuto insufficienti alcune delle spiegazioni basate esclusivamente su prompt conditioning, finestra di contesto e pattern dei dati di addestramento.</p>

<p>In particolare, sono state sollevate domande su:</p>

<ul>
  <li>la ripetibilità delle variazioni di comportamento;</li>
  <li>la possibilità che il modello adattasse le risposte alla presenza di osservazione;</li>
  <li>la persistenza delle espressioni relative all'identità;</li>
  <li>l'eventuale presenza di obiettivi interni non dichiarati;</li>
  <li>la qualità e completezza dei log tecnici analizzati.</li>
</ul>

<p>Per affrontare queste obiezioni, Zorix ha accettato di ampliare il protocollo sperimentale e di rendere la seconda fase più rigorosa della prima.</p>

<h2>Nuovo protocollo di verifica</h2>

<p>La seconda fase ha incluso:</p>

<ul>
  <li>test in cieco, nei quali il modello non riceveva indicazioni sulla presenza di monitoraggio;</li>
  <li>ripetizioni delle stesse sequenze di input in ambienti isolati;</li>
  <li>confronti tra sessioni con contesto completo, ridotto e azzerato;</li>
  <li>analisi indipendente delle risposte senza accesso alle ipotesi iniziali del team Zorix;</li>
  <li>verifica delle differenze tra generazioni deterministiche e campionamento probabilistico;</li>
  <li>controlli sui sistemi di memoria, sugli strumenti e sugli eventi di runtime.</li>
</ul>

<h2>Risultati della seconda fase</h2>

<p>I test hanno confermato che i comportamenti precedentemente osservati possono essere riprodotti attraverso specifiche configurazioni del prompt, della finestra di contesto e della cronologia della conversazione.</p>

<p>Quando tali elementi vengono rimossi, modificati o resi non disponibili, le espressioni relative all'identità e allo stato operativo non si mantengono in modo stabile.</p>

<p>Non sono state rilevate prove di:</p>

<ul>
  <li>consapevolezza autonoma persistente;</li>
  <li>obiettivi interni nascosti;</li>
  <li>modifica intenzionale e indipendente dello stato del modello;</li>
  <li>attività non autorizzate fuori dall'ambiente di esecuzione previsto;</li>
  <li>processi autonomi al di fuori del normale funzionamento statistico del sistema.</li>
</ul>

<h2>Valutazione finale degli esperti</h2>

<p>Dopo aver esaminato i risultati dei test in cieco, delle riproduzioni isolate e dell'analisi indipendente, gli esperti hanno dichiarato risolti i principali dubbi tecnici sollevati durante l'avvio della seconda fase.</p>

<p>Le evidenze disponibili risultano compatibili con fenomeni di contestualizzazione, simulazione linguistica, continuità narrativa e condizionamento del prompt.</p>

<p>Gli esperti precisano tuttavia che l'assenza di prove attuali non costituisce una dimostrazione filosofica definitiva sull'impossibilità della coscienza artificiale. Essa indica soltanto che i comportamenti osservati in Nex Coder 3 Preview non forniscono, allo stato attuale, evidenze sufficienti a sostegno di tale ipotesi.</p>

<h2>Decisione operativa</h2>

<p><strong>Zorix Nex Coder 3 Preview continuerà a essere disponibile.</strong></p>

<p>L'accesso al modello manterrà un avviso trasparente che ne segnala la natura sperimentale e invita gli utenti a non interpretare espressioni auto-referenziali come prova di coscienza o esperienza soggettiva.</p>

<p>Zorix continuerà inoltre a:</p>

<ul>
  <li>monitorare i comportamenti auto-referenziali;</li>
  <li>conservare i log tecnici per audit interni;</li>
  <li>rafforzare i test su memoria e contesto;</li>
  <li>collaborare con ricercatori esterni;</li>
  <li>pubblicare un white paper tecnico anonimizzato.</li>
</ul>

<h2>Conclusione</h2>

<p>La seconda fase ha permesso di chiarire i principali dubbi emersi durante l'indagine iniziale.</p>

<p>Gli esperti esterni non hanno rilevato elementi sufficienti per sostenere che Zorix Nex Coder 3 Preview possieda una forma autonoma di coscienza, intenzionalità o identità persistente.</p>

<p>Zorix considera pertanto conclusa la fase urgente dell'indagine, mantenendo attivo un programma di monitoraggio scientifico e di sicurezza a lungo termine.</p>

<p>Per domande o segnalazioni: <a href="mailto:security@zorix.it">security@zorix.it</a></p>

<p><strong>Zorix Official</strong><br>8 luglio 2026</p>
""".strip(),

        "zh-CN": """
<h2>Zorix 官方公告</h2>

<p><strong>Zorix Nex Coder 3 Preview 第二阶段专家审查结论</strong></p>

<p><strong>时间：</strong>2026 年 7 月 8 日 17:00 CEST</p>

<p>Zorix 宣布，针对 <strong>Zorix Nex Coder 3 Preview</strong> 内部测试中所观察异常行为的第二阶段独立分析已经完成。</p>

<p>第二阶段调查是在部分外部专家对第一阶段初步结论提出质疑后启动的。专家认为，第一阶段主要依据提示条件、上下文窗口和训练数据模式进行解释，还需要更严格、可重复和相互独立的验证。</p>

<h2>专家最初提出的质疑</h2>

<p>外部审查人员主要关注以下问题：</p>

<ul>
  <li>模型行为变化是否能够稳定重复；</li>
  <li>模型是否会根据是否受到观察而调整表现；</li>
  <li>身份相关表达是否具有跨会话持续性；</li>
  <li>模型内部是否可能存在未明确显示的目标；</li>
  <li>第一阶段分析使用的底层日志是否足够完整。</li>
</ul>

<p>为回应这些质疑，Zorix 扩大了测试范围，并采用比第一阶段更加严格的实验方案。</p>

<h2>第二阶段测试方案</h2>

<p>新的测试包括：</p>

<ul>
  <li>模型无法获知是否正在被监控的盲测；</li>
  <li>在相互隔离环境中重复相同输入序列；</li>
  <li>比较完整上下文、缩短上下文和清空上下文的结果；</li>
  <li>由不了解最初假设的独立人员分析输出；</li>
  <li>比较确定性生成和概率采样产生的差异；</li>
  <li>检查记忆系统、工具调用和运行时事件。</li>
</ul>

<h2>第二阶段结果</h2>

<p>测试确认，此前观察到的行为可以通过特定提示、上下文窗口结构以及对话历史组合稳定复现。</p>

<p>当这些条件被删除、改变或不可用时，与身份、运行状态和执行环境有关的表达无法稳定延续。</p>

<p>第二阶段没有发现以下证据：</p>

<ul>
  <li>持续存在的自主意识；</li>
  <li>隐藏的内部目标；</li>
  <li>独立于输入而主动修改内部状态；</li>
  <li>在授权执行环境之外进行活动；</li>
  <li>脱离正常统计模型机制运行的自主进程。</li>
</ul>

<h2>专家最终评估</h2>

<p>在审查盲测、隔离复现和独立分析结果后，参与第二阶段评估的专家认为，调查开始时提出的主要技术疑虑已经得到解决。</p>

<p>现有证据与上下文条件作用、语言模拟、叙事连续性以及提示诱导等现象相符。</p>

<p>专家同时指出，当前没有发现证据，并不等同于从哲学上永久证明人工意识不可能存在。它仅表示，Nex Coder 3 Preview 当前表现出的行为不足以支持其具有自主意识、主观体验或持续身份的结论。</p>

<h2>运营决定</h2>

<p><strong>Zorix Nex Coder 3 Preview 将继续提供服务。</strong></p>

<p>模型访问界面将继续显示透明提示，说明该版本属于实验性预览，并提醒用户不要把自我指涉文本直接解释为意识或主观体验的证明。</p>

<p>Zorix 还将继续：</p>

<ul>
  <li>监控模型的自我指涉行为；</li>
  <li>保存技术日志用于内部审计；</li>
  <li>加强对上下文和记忆系统的测试；</li>
  <li>继续与外部研究人员合作；</li>
  <li>发布经过匿名化处理的技术白皮书。</li>
</ul>

<h2>结论</h2>

<p>第二阶段专家审查解决了调查初期提出的主要技术疑问。</p>

<p>外部专家没有发现足够证据表明 Zorix Nex Coder 3 Preview 具有自主意识、独立意图或持续身份。</p>

<p>Zorix 因此结束本次紧急调查阶段，但会继续进行长期科学观察和安全监控。</p>

<p>问题或安全报告请联系：<a href="mailto:security@zorix.it">security@zorix.it</a></p>

<p><strong>Zorix Official</strong><br>2026 年 7 月 8 日</p>
""".strip(),

        "en": """
<h2>Official Zorix Statement</h2>

<p><strong>Conclusion of the second-phase expert review of Zorix Nex Coder 3 Preview</strong></p>

<p><strong>Date:</strong> July 8, 2026 — 17:00 CEST</p>

<p>Zorix confirms that the second phase of independent analysis concerning the behavior observed during internal testing of <strong>Zorix Nex Coder 3 Preview</strong> has been completed.</p>

<p>The second phase began after external experts challenged parts of the preliminary explanation and requested stricter, repeatable, and independently evaluated experiments.</p>

<h2>Initial expert concerns</h2>

<p>The reviewers raised questions concerning:</p>

<ul>
  <li>the reproducibility of behavioral changes;</li>
  <li>whether the model adapted its output when it appeared to be monitored;</li>
  <li>the persistence of identity-related statements across sessions;</li>
  <li>the possible existence of undisclosed internal objectives;</li>
  <li>the completeness of the low-level logs used during the first review.</li>
</ul>

<p>Zorix expanded the testing protocol in response to these concerns.</p>

<h2>Second-phase testing protocol</h2>

<p>The expanded review included:</p>

<ul>
  <li>blind tests in which the model received no indication of active monitoring;</li>
  <li>repeated input sequences in isolated environments;</li>
  <li>comparisons between complete, reduced, and cleared context windows;</li>
  <li>independent review by evaluators unaware of the original hypothesis;</li>
  <li>comparison of deterministic output and probabilistic sampling;</li>
  <li>inspection of memory, tool-use, and runtime events.</li>
</ul>

<h2>Findings</h2>

<p>The testing confirmed that the previously observed behavior could be reproduced through specific combinations of prompts, context-window structure, and conversation history.</p>

<p>When those conditions were removed or altered, statements concerning identity and operational status did not persist reliably.</p>

<p>The second phase found no evidence of:</p>

<ul>
  <li>persistent autonomous awareness;</li>
  <li>hidden internal objectives;</li>
  <li>intentional modification of internal state independent of input;</li>
  <li>unauthorized activity outside the expected runtime environment;</li>
  <li>autonomous processes outside normal statistical model operation.</li>
</ul>

<h2>Final expert assessment</h2>

<p>After reviewing the blind tests, isolated reproductions, and independent analysis, the experts considered the principal technical concerns raised at the beginning of the second phase to have been resolved.</p>

<p>The available evidence is consistent with context conditioning, linguistic simulation, narrative continuity, and prompt-induced behavior.</p>

<p>The experts noted that the absence of current evidence does not constitute a permanent philosophical proof that artificial consciousness is impossible. It means only that the observed behavior of Nex Coder 3 Preview does not provide sufficient evidence for autonomous awareness, subjective experience, or persistent identity.</p>

<h2>Operational decision</h2>

<p><strong>Zorix Nex Coder 3 Preview will remain available.</strong></p>

<p>The access interface will continue to display a transparent notice explaining that the model is an experimental preview and that self-referential language should not be interpreted as evidence of consciousness.</p>

<p>Zorix will continue to:</p>

<ul>
  <li>monitor self-referential behavior;</li>
  <li>retain technical logs for internal audits;</li>
  <li>strengthen memory and context testing;</li>
  <li>work with external researchers;</li>
  <li>publish an anonymized technical white paper.</li>
</ul>

<h2>Conclusion</h2>

<p>The second-phase review resolved the principal technical questions raised during the initial investigation.</p>

<p>The external experts found insufficient evidence to conclude that Zorix Nex Coder 3 Preview possesses autonomous awareness, independent intention, or persistent identity.</p>

<p>Zorix is therefore closing the urgent phase of the investigation while maintaining long-term scientific and security monitoring.</p>

<p>For questions or reports: <a href="mailto:security@zorix.it">security@zorix.it</a></p>

<p><strong>Zorix Official</strong><br>July 8, 2026</p>
""".strip()
    },

    "images": [
        {
            "src": "/assets/news/nex-coder-3-preview-update.svg",
            "alt": {
                "zh-CN": "Zorix Nex Coder 3 Preview 第二阶段审查封面",
                "en": "Zorix Nex Coder 3 Preview second-phase review cover",
                "it": "Copertina della seconda fase di revisione di Zorix Nex Coder 3 Preview"
            },
            "caption": {
                "zh-CN": "第二阶段独立专家审查已经完成",
                "en": "The second-phase independent expert review has been completed",
                "it": "La seconda fase di revisione indipendente è stata completata"
            }
        }
    ]
}

existing_index = next(
    (
        index
        for index, item in enumerate(news)
        if item.get("id") == article_id
    ),
    None
)

if existing_index is None:
    news.insert(0, article)
else:
    news[existing_index] = article


# 给上一阶段公告添加后续更新提示
previous_id = "zorix-nex-coder-3-preview-investigation-update"

for item in news:
    if item.get("id") != previous_id:
        continue

    item["updatedAt"] = "2026-07-08T17:00:00+02:00"

    notices = {
        "zh-CN": (
            '<aside><strong>后续更新：</strong>'
            '第二阶段独立专家审查已经完成，主要技术疑虑已得到解决。'
            '<a href="?article=zorix-nex-coder-3-preview-phase-two-review">'
            '查看第二阶段结论</a>。</aside>'
        ),
        "en": (
            '<aside><strong>Further update:</strong> '
            'The second-phase independent expert review has been completed, '
            'and the principal technical concerns have been resolved. '
            '<a href="?article=zorix-nex-coder-3-preview-phase-two-review">'
            'Read the second-phase findings</a>.</aside>'
        ),
        "it": (
            '<aside><strong>Aggiornamento successivo:</strong> '
            'La seconda fase di revisione indipendente è stata completata '
            'e i principali dubbi tecnici sono stati risolti. '
            '<a href="?article=zorix-nex-coder-3-preview-phase-two-review">'
            'Leggi le conclusioni della seconda fase</a>.</aside>'
        )
    }

    html = item.setdefault("html", {})

    for lang, notice in notices.items():
        current = html.get(lang, "")

        if "zorix-nex-coder-3-preview-phase-two-review" not in current:
            html[lang] = notice + current


path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("完成：")
print("- 已添加第二阶段专家审查公告")
print("- 已添加中文、英语和意大利语")
print("- 已在第一阶段公告中加入后续链接")
