import json
import os
from datetime import datetime
import urllib.request
import urllib.error

def fetch_github_security_advisories():
    """從 GitHub Advisory Database 官方開源 API 抓取最新的資安漏洞與 IT 故障排解數據"""
    url = "https://api.github.com/advisories?per_page=5"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Richard-AI-Troubleshooter",
            "Accept": "application/vnd.github+json"
        }
    )
    
    fetched_errors = {}
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                for item in data:
                    summary = item.get("summary", "未知系統漏洞")
                    severity = item.get("severity", "MODERATE")
                    cve_id = item.get("cve_id") or item.get("ghsa_id", "CVE-UNKNOWN")
                    description = item.get("description", "系統元件發生異常，需要檢查依賴版本與安全性配置。")
                    
                    # 簡化描述作為根因
                    short_desc = description.split(".")[0] if description else "組件配置異常"
                    
                    fetched_errors[cve_id] = {
                        "category": f"Security / Advisory ({severity})",
                        "root_cause": f"發現漏洞/異常: {summary}。原因: {short_desc}。",
                        "quick_fix": f"請檢視相關套件版本並立即執行升級修補，參考編號: {cve_id}。"
                    }
                print("成功從 GitHub 官方開源安全庫抓取最新 IT 故障數據！")
    except Exception as e:
        print(f"線上抓取數據發生異常，將採用本地預設數據庫: {e}")
        
    return fetched_errors

def generate_troubleshooting_data():
    """生成 Richard AI 疑難排解的基礎數據庫（結合動態開源抓取與本地備用庫）"""
    os.makedirs("data", exist_ok=True)
    
    # 嘗試聯網抓取高質開源 IT 數據
    dynamic_errors = fetch_github_security_advisories()
    
    # 基礎常見故障庫
    base_errors = {
        "ModuleNotFoundError": {
            "category": "Python / Dependencies",
            "root_cause": "缺少相應的套件或未正確執行 pip install。",
            "quick_fix": "執行 pip install -r requirements.txt 或安裝對應模組。"
        },
        "ConnectionRefusedError": {
            "category": "Networking / API",
            "root_cause": "目標連接埠未開啟、防火牆阻擋或服務未正確啟動。",
            "quick_fix": "檢查服務監聽埠 (Port) 是否正確，並確認防火牆或反向代理設定。"
        },
        "502_Bad_Gateway": {
            "category": "DevOps / Nginx / Cloudflare",
            "root_cause": "上游應用程式伺服器 (App Server) 當機、逾時或未在指定 Socket/Port 運行。",
            "quick_fix": "檢查後端程式日誌 (Logs)，確認 Process 是否正常運行。"
        },
        "Docker_Container_Exited": {
            "category": "Docker / Containerization",
            "root_cause": "容器內部主程序執行完畢退出，或因配置錯誤導致啟動即崩潰。",
            "quick_fix": "使用 docker logs <container_id> 查看錯誤日誌並修復 ENTRYPOINT。"
        }
    }
    
    # 合併動態抓取數據與本地數據
    combined_errors = {**base_errors, **dynamic_errors}

    troubleshooting_db = {
        "status": "active_ready_with_live_feed",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "common_errors": combined_errors
    }

    with open("data/troubleshooting.json", "w", encoding="utf-8") as f:
        json.dump(troubleshooting_db, f, ensure_ascii=False, indent=4)
    print("成功生成: data/troubleshooting.json")

def generate_index_page():
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI - 智能故障排解平台</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">
    <header class="bg-slate-800 border-b border-cyan-500/30 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-cyan-400">⚡ Richard AI 智能排解平台</h1>
            <p class="text-xs text-slate-400 mt-1">資深 SRE 工程師級別的系統日誌與故障分析助手。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full">
        <div class="bg-slate-800 rounded-xl border border-cyan-500/30 p-6 shadow-lg space-y-4">
            <h2 class="text-lg font-bold text-cyan-300">系統即時診斷</h2>
            <p class="text-sm text-slate-300">貼上你的 Error Log、異常代碼或系統崩潰描述，由 Richard AI 為你進行根因分析（Root Cause Analysis）並提供修復步驟。</p>
            <div>
                <a href="it_chat.html" class="inline-block bg-cyan-600 hover:bg-cyan-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">進入對話排解頁面</a>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI System
    </footer>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: index.html")

def generate_chat_page():
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI - 診斷室</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-slate-800 border-b border-cyan-500/30 py-6">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div>
                <a href="index.html" class="text-xs text-cyan-400 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
                <h1 class="text-2xl font-bold text-cyan-400 mt-1">🛠️ Richard AI 智能診斷</h1>
                <p class="text-xs text-slate-400 mt-1">精確解析錯誤日誌，給出標準修復方案。</p>
            </div>
            <div id="live-clock" class="text-right text-xs font-mono text-cyan-300 bg-slate-900 px-3 py-2 rounded-lg border border-cyan-500/30">
                載入中...
            </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-4">
        <div class="bg-slate-800 rounded-xl border border-cyan-500/30 p-6 shadow-lg space-y-4">
            <div>
                <label for="error-input" class="block text-xs font-bold text-cyan-300 mb-1">請貼上 Error Log、錯誤碼或故障描述:</label>
                <textarea id="error-input" rows="4" placeholder="例如：ModuleNotFoundError: No module named 'requests' 或 502 Bad Gateway..." class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 font-mono"></textarea>
            </div>
            <div>
                <button onclick="diagnoseError()" id="send-btn" class="w-full bg-cyan-600 hover:bg-cyan-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition shadow-md">讓 Richard AI 進行排解分析</button>
            </div>
        </div>

        <div id="chat-container" class="bg-slate-800 rounded-xl border border-cyan-500/30 p-6 shadow-lg space-y-4 min-h-[350px] max-h-[500px] overflow-y-auto">
            <div class="flex items-start space-x-3">
                <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]">
                    「你好！我是 Richard AI。請把你的錯誤日誌或者系統崩潰情況貼上來，我會為你提供根本原因分析與逐步解決方案。」
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI System
    </footer>

    <script>
        function updateClock() {
            const now = new Date();
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
            document.getElementById('live-clock').innerText = now.toLocaleString('zh-HK', options);
        }
        setInterval(updateClock, 1000);
        updateClock();

        async function diagnoseError() {
            const errorField = document.getElementById('error-input');
            const chatContainer = document.getElementById('chat-container');
            const sendBtn = document.getElementById('send-btn');
            
            const errorText = errorField.value.trim();

            if (!errorText) {
                alert('請先輸入或貼上錯誤日誌！');
                return;
            }

            let systemData = {};
            try {
                const res = await fetch('data/troubleshooting.json');
                systemData = await res.json();
            } catch (e) {
                systemData = { status: "fallback" };
            }

            const currentDateTimeStr = new Date().toLocaleString('zh-HK', { hour12: false });

            chatContainer.innerHTML += `
                <div class="flex items-start justify-end space-x-3">
                    <div class="bg-slate-700 text-slate-100 rounded-lg p-3 text-sm max-w-[80%] font-mono whitespace-pre-line">${escapeHtml(errorText)}</div>
                    <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">你</div>
                </div>
            `;
            
            errorField.disabled = true;
            sendBtn.disabled = true;
            sendBtn.innerText = 'Richard AI 診斷分析中...';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatContainer.innerHTML += `
                <div id="${loadingId}" class="flex items-start space-x-3">
                    <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                    <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-400 italic">正在解析錯誤日誌並比對常見故障庫...</div>
                </div>
            `;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            try {
                const response = await fetch('https://itshooting.lcw940708.workers.dev/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        issue: errorText, 
                        systemData: systemData,
                        requestTime: currentDateTimeStr,
                        prompt: "請以 Richard AI 身份，用專業、嚴謹的香港繁體書面語回答。嚴禁使用任何廣東話口語（如：呢、啲、咁、冇），必須使用標準書面語（如：這、這些、這樣、沒有）。請列出根本原因（Root Cause）與清晰的逐步修復步驟（Step-by-step Fix）。" 
                    })
                });

                const data = await response.json();
                document.getElementById(loadingId).remove();

                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                        <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]" style="white-space: pre-line;">${escapeHtml(data.content || '系統暫時無法回應，請稍後重試。')}</div>
                    </div>
                `;

            } catch (error) {
                document.getElementById(loadingId).remove();
                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">系統</div>
                        <div class="bg-red-900/50 border border-red-700 text-red-200 rounded-lg p-3 text-sm max-w-[80%]">連線出錯，請檢查 Worker 設定。</div>
                    </div>
                `;
            }

            errorField.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerText = '讓 Richard AI 進行排解分析';
            errorField.value = '';
            errorField.focus();
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""
    with open("it_chat.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: it_chat.html")

if __name__ == "__main__":
    print("開始執行 Richard AI 平台生成程序（結合開源 API 數據抓取）...")
    generate_troubleshooting_data()
    generate_index_page()
    generate_chat_page()
    print("全部 Richard AI 排解平台檔案生成完畢！")