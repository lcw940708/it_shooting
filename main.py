import json
import os
from datetime import datetime
import urllib.request
import urllib.error
import gzip

def fetch_it_support_solutions():
    """從 Stack Exchange (Super User) 公開 API 抓取最新的 IT 支援與疑難排解問題"""
    url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=activity&site=superuser&pagesize=5"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Richard-AI-Helpdesk-Bot"}
    )
    
    fetched_solutions = {}
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                raw_data = response.read()
                try:
                    decompressed_data = gzip.decompress(raw_data).decode("utf-8")
                except:
                    decompressed_data = raw_data.decode("utf-8")
                    
                data = json.loads(decompressed_data)
                for item in data.get("items", []):
                    title = item.get("title", "未知 IT 支援問題")
                    question_id = str(item.get("question_id", "SU-000"))
                    link = item.get("link", "#")
                    
                    fetched_solutions[f"SU-{question_id}"] = {
                        "category": "IT Helpdesk / Community Super User",
                        "root_cause": f"用戶回報終端技術障礙: {title}",
                        "quick_fix": f"請參考社群技術支援指引進行排除，詳細討論請參閱: {link}"
                    }
                print("成功從 Stack Exchange 抓取最新 IT 支援問題！")
    except Exception as e:
        print(f"線上抓取數據發生異常，將採用本地預設 IT Helpdesk 數據庫: {e}")
        
    return fetched_solutions

def generate_troubleshooting_data():
    """生成 Richard AI Helpdesk 支援數據庫（結合 Stack Exchange 動態抓取與常見 IT 支援庫）"""
    os.makedirs("data", exist_ok=True)
    
    dynamic_solutions = fetch_it_support_solutions()
    
    base_helpdesk_issues = {
        "Printer_Offline": {
            "category": "Hardware / Peripheral Support",
            "root_cause": "印表機通訊埠連線中斷或網段設定變更，導致傳輸佇列卡住。",
            "quick_fix": "重新啟動印表機電源，並在控制台清除暫存佇列後重新加入網路印表機。"
        },
        "VPN_Connection_Failed": {
            "category": "Network / Remote Access Support",
            "root_cause": "憑證過期、閘道器位址變更或使用者網域密碼輸入錯誤。",
            "quick_fix": "檢查 VPN 用戶端設定檔，確認伺服器位址正確並重新整理認證憑證。"
        },
        "Outlook_Not_Syncing": {
            "category": "Software / Email Support",
            "root_cause": "本機郵件資料檔 (.ost/.pst) 損壞或 Exchange 伺服器連線超時。",
            "quick_fix": "建立新的 Outlook 設定檔，或以安全模式啟動並重建快取檔案。"
        },
        "Blue_Screen_Crash": {
            "category": "OS / Hardware Support",
            "root_cause": "近期安裝的驅動程式衝突或硬體記憶體模組讀取異常。",
            "quick_fix": "進入安全模式解除安裝最新動態驅動程式，並執行記憶體診斷工具。"
        }
    }
    
    combined_solutions = {**base_helpdesk_issues, **dynamic_solutions}

    helpdesk_db = {
        "status": "helpdesk_active_ready",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "common_errors": combined_solutions
    }

    with open("data/troubleshooting.json", "w", encoding="utf-8") as f:
        json.dump(helpdesk_db, f, ensure_ascii=False, indent=4)
    print("成功生成: data/troubleshooting.json")

def generate_index_page():
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI - 綜合支援與吹水平台</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">
    <header class="bg-slate-800 border-b border-cyan-500/30 py-6">
        <div class="max-w-3xl mx-auto px-4">
            <h1 class="text-2xl font-bold text-cyan-400">🎧 Richard AI - 綜合支援與吹水中心</h1>
            <p class="text-xs text-slate-400 mt-1">結合嚴肅 IT Helpdesk 與無限上下文白卡吹水聊天的雙軌平台。</p>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-8 flex-grow w-full space-y-6">
        <div class="bg-slate-800 rounded-xl border border-cyan-500/30 p-6 shadow-lg space-y-4">
            <h2 class="text-lg font-bold text-cyan-300">提交 IT 支援請求 (單次診斷)</h2>
            <p class="text-sm text-slate-300">連接至 itshooting 專用 Worker，由 Richard AI 單次為您提供專業的解決方案。</p>
            <div>
                <a href="it_chat.html" class="inline-block bg-cyan-600 hover:bg-cyan-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">進入 IT Helpdesk 診斷對話</a>
            </div>
        </div>

        <div class="bg-slate-800 rounded-xl border border-emerald-500/30 p-6 shadow-lg space-y-4">
            <h2 class="text-lg font-bold text-emerald-300">對話模式 (Richard AI 吹水聊天室)</h2>
            <p class="text-sm text-slate-300">連接至 talking 專用 Worker，具備上下文記憶功能，支援無限期與 Richard 瘋狂對話吹水。</p>
            <div>
                <a href="richard_chat.html" class="inline-block bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition">進入 Richard AI 連續吹水室</a>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI Helpdesk System
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
    <title>Richard AI - IT Helpdesk 支援室</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-slate-800 border-b border-cyan-500/30 py-6">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div>
                <a href="index.html" class="text-xs text-cyan-400 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
                <h1 class="text-2xl font-bold text-cyan-400 mt-1">🛠️ Richard AI - IT Helpdesk </h1>
                <p class="text-xs text-slate-400 mt-1">即時支援與疑難排除專線 (itshooting worker)。</p>
            </div>
            <div id="live-clock" class="text-right text-xs font-mono text-cyan-300 bg-slate-900 px-3 py-2 rounded-lg border border-cyan-500/30">
                載入中...
            </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-4">
        <div class="bg-slate-800 rounded-xl border border-cyan-500/30 p-6 shadow-lg space-y-4">
            <div>
                <label for="error-input" class="block text-xs font-bold text-cyan-300 mb-1">請描述您的 IT 支援問題或錯誤狀況:</label>
                <textarea id="error-input" rows="4" placeholder="例如：公司印表機印唔到嘢、VPN 連唔上、Outlook 收唔到信..." class="w-full bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-cyan-500 font-mono"></textarea>
            </div>
            <div>
                <button onclick="diagnoseError()" id="send-btn" class="w-full bg-cyan-600 hover:bg-cyan-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition shadow-md">讓 Richard AI 進行支援分析</button>
            </div>
        </div>

        <div id="chat-container" class="bg-slate-800 rounded-xl border border-cyan-500/30 p-6 shadow-lg space-y-4 min-h-[350px] max-h-[500px] overflow-y-auto">
            <div class="flex items-start space-x-3">
                <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]">
                    「你好！我是 Richard AI Helpdesk 支援專員。請話我知你遇到咩辦公或電腦問題，我會為你提供解決方案。」
                </div>
            </div>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI Helpdesk System
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
                alert('請先輸入你遇到的支援問題！');
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
            sendBtn.innerText = 'Richard AI 支援分析中...';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatContainer.innerHTML += `
                <div id="${loadingId}" class="flex items-start space-x-3">
                    <div class="bg-cyan-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                    <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-400 italic">正在檢索 Helpdesk 支援數據庫...</div>
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
                        prompt: "請以 Richard AI Helpdesk 身份進行支援回覆。" 
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
                        <div class="bg-red-900/50 border border-red-700 text-red-200 rounded-lg p-3 text-sm max-w-[80%]">連線出錯，請檢查 itshooting Worker 設定。</div>
                    </div>
                `;
            }

            errorField.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerText = '讓 Richard AI 進行支援分析';
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

def generate_richard_chat_page():
    html_content = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Richard AI - 連續吹水聊天室</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col justify-between">

    <header class="bg-slate-800 border-b border-emerald-500/30 py-6">
        <div class="max-w-3xl mx-auto px-4 flex justify-between items-center">
            <div>
                <a href="index.html" class="text-xs text-emerald-400 hover:underline mb-1 inline-block">&larr; 返回主頁</a>
                <h1 class="text-2xl font-bold text-emerald-400 mt-1">🗣️ Richard AI - 連續吹水聊天室</h1>
                <p class="text-xs text-slate-400 mt-1">具備上下文記憶功能，連接至 talking worker，無限期與 Richard 瘋狂對話。</p>
            </div>
            <div id="live-clock" class="text-right text-xs font-mono text-emerald-300 bg-slate-900 px-3 py-2 rounded-lg border border-emerald-500/30">
                載入中...
            </div>
        </div>
    </header>

    <main class="max-w-3xl mx-auto px-4 py-6 flex-grow w-full space-y-4 flex flex-col">
        <div id="chat-container" class="bg-slate-800 rounded-xl border border-emerald-500/30 p-6 shadow-lg space-y-4 flex-grow min-h-[400px] max-h-[550px] overflow-y-auto">
            <div class="flex items-start space-x-3">
                <div class="bg-emerald-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]">
                    「你好，我是 Richard。有咩問題隨便講，我同你傾過夠。」
                </div>
            </div>
        </div>

        <div class="bg-slate-800 rounded-xl border border-emerald-500/30 p-4 shadow-lg flex space-x-2">
            <input type="text" id="user-input" placeholder="隨便同 Richard 吹水..." class="flex-grow bg-slate-900 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500 font-mono" onkeypress="handleKeyPress(event)">
            <button onclick="sendChatMessage()" id="send-btn" class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition shadow-md">發送</button>
        </div>
    </main>

    <footer class="border-t border-slate-800 py-4 text-center text-xs text-slate-500 bg-slate-900">
        © 2026 Richard AI Helpdesk System
    </footer>

    <script>
        function updateClock() {
            const now = new Date();
            const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
            document.getElementById('live-clock').innerText = now.toLocaleString('zh-HK', options);
        }
        setInterval(updateClock, 1000);
        updateClock();

        // 儲存對話歷史（支援上下文記憶）
        let chatHistory = [];

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendChatMessage();
            }
        }

        async function sendChatMessage() {
            const inputField = document.getElementById('user-input');
            const chatContainer = document.getElementById('chat-container');
            const sendBtn = document.getElementById('send-btn');
            
            const userText = inputField.value.trim();
            if (!userText) return;

            // 1. 將用戶輸入加入歷史
            chatHistory.push({ role: "user", content: userText });

            // 限制歷史長度，避免超出 Token 上限（最多保留最近 15 句）
            if (chatHistory.length > 15) {
                chatHistory = chatHistory.slice(-15);
            }

            // 顯示用戶訊息
            chatContainer.innerHTML += `
                <div class="flex items-start justify-end space-x-3">
                    <div class="bg-slate-700 text-slate-100 rounded-lg p-3 text-sm max-w-[80%] font-mono whitespace-pre-line">${escapeHtml(userText)}</div>
                    <div class="bg-emerald-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">你</div>
                </div>
            `;
            
            inputField.value = '';
            inputField.disabled = true;
            sendBtn.disabled = true;
            sendBtn.innerText = '思考中...';
            chatContainer.scrollTop = chatContainer.scrollHeight;

            const loadingId = 'loading-' + Date.now();
            chatContainer.innerHTML += `
                <div id="${loadingId}" class="flex items-start space-x-3">
                    <div class="bg-emerald-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                    <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-400 italic">正在接收精神波段分析中...</div>
                </div>
            `;
            chatContainer.scrollTop = chatContainer.scrollHeight;

            let systemData = {};
            try {
                const res = await fetch('data/troubleshooting.json');
                systemData = await res.json();
            } catch (e) {
                systemData = { status: "fallback" };
            }

            const currentDateTimeStr = new Date().toLocaleString('zh-HK', { hour12: false });

            try {
                // 將整個 chatHistory 傳給 talking worker 實現上下文記憶
                const response = await fetch('https://talking.lcw940708.workers.dev/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        messages: chatHistory, 
                        systemData: systemData,
                        requestTime: currentDateTimeStr
                    })
                });

                const data = await response.json();
                document.getElementById(loadingId).remove();

                const aiReply = data.content || '系統暫時無法回應。';

                // 將 AI 回覆加入歷史
                chatHistory.push({ role: "assistant", content: aiReply });

                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-emerald-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">Richard AI</div>
                        <div class="bg-slate-900 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 max-w-[80%]" style="white-space: pre-line;">${escapeHtml(aiReply)}</div>
                    </div>
                `;

            } catch (error) {
                document.getElementById(loadingId).remove();
                chatContainer.innerHTML += `
                    <div class="flex items-start space-x-3">
                        <div class="bg-emerald-600 text-white text-xs px-2.5 py-1 rounded-full font-bold">系統</div>
                        <div class="bg-red-900/50 border border-red-700 text-red-200 rounded-lg p-3 text-sm max-w-[80%]">連線出錯，請檢查 talking Worker 設定。</div>
                    </div>
                `;
            }

            inputField.disabled = false;
            sendBtn.disabled = false;
            sendBtn.innerText = '發送';
            inputField.focus();
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        function escapeHtml(text) {
            return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        }
    </script>
</body>
</html>
"""
    with open("richard_chat.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("成功生成: richard_chat.html")

if __name__ == "__main__":
    print("開始執行 Richard AI Helpdesk 平台生成程序...")
    generate_troubleshooting_data()
    generate_index_page()
    generate_chat_page()
    generate_richard_chat_page()
    print("全部 Richard AI Helpdesk 平台檔案生成完畢！")