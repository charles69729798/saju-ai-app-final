
// ==========================================
// 🚀 [WebMCP Integration] AI Agent Support (External Loader)
// ==========================================

console.log("✅ QA Loader Script Loaded Successfully!");

// Force Unregister Service Worker to clear old cache
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(function (registrations) {
        for (let registration of registrations) {
            console.log("🧹 Unregistering Service Worker:", registration);
            registration.unregister();
        }
    });
}

// 1. Core Logic (Exposed Globally for Manual QA)
window.run_saju_analysis_tool = async (params) => {
    console.log(`🤖 Analyzing ${params.category} for ${params.name}`);
    const nameInput = document.getElementById('nameKorean');
    const dateInput = document.getElementById('birthDate');
    const timeInput = document.getElementById('birthTime');

    if (nameInput) nameInput.value = params.name;
    if (dateInput) dateInput.value = params.birthDate;
    if (timeInput) timeInput.value = params.birthTime || "12:00";

    try {
        if (typeof commitAnalysis === 'function') {
            await commitAnalysis(params.category);
            return `Started analysis for ${params.category}`;
        } else {
            return "Error: commitAnalysis function not found in window scope.";
        }
    } catch (e) {
        return `Error: ${e.message}`;
    }
};

window.test_all_features = async () => {
    const categories = ["평생사주", "재물운", "직업운", "건강운", "애정운"];
    const report = [];
    console.log("🚀 Starting Full QA Test Sequence...");

    const showToast = (msg) => {
        const toast = document.createElement('div');
        toast.style.position = 'fixed';
        toast.style.bottom = '20px';
        toast.style.right = '20px';
        toast.style.background = 'rgba(0,0,0,0.8)';
        toast.style.color = '#fff';
        toast.style.padding = '10px 20px';
        toast.style.borderRadius = '5px';
        toast.style.zIndex = '9999';
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 2000);
    };

    for (const cat of categories) {
        console.log(`🧪 Testing Category: ${cat}...`);
        showToast(`Run Test: ${cat}`);
        try {
            // Dummy Data Load
            const nameInput = document.getElementById('nameKorean');
            if (nameInput) {
                nameInput.value = "WebMCP 테스터";
                document.getElementById('birthDate').value = "2000-01-01";
                document.getElementById('birthTime').value = "12:00";

                // Trigger
                await commitAnalysis(cat);

                // 3초 대기 (결과 렌더링 시간 확보)
                await new Promise(r => setTimeout(r, 3000));

                // 결과 확인 Logic
                const resultElement = document.getElementById('resultContent');
                if (resultElement) {
                    const resultText = resultElement.innerText;
                    if (resultText && resultText.length > 50) {
                        report.push(`✅ ${cat}: PASS (Len: ${resultText.length})`);
                    } else {
                        report.push(`❌ ${cat}: FAIL (Empty)`);
                    }
                } else {
                    report.push(`❌ ${cat}: FAIL (Result Element Not Found)`);
                }

                // 에러 모달 닫기 (만약 떴다면)
                const errorModal = document.getElementById('error');
                if (errorModal && errorModal.classList.contains('show')) {
                    report.push(`❌ ${cat}: FAIL (Error Modal Shown: ${errorModal.textContent})`);
                    errorModal.classList.remove('show'); // 다음 테스트를 위해 닫기
                }
            } else {
                report.push(`❌ ${cat}: FAIL (Input Elements Not Found)`);
            }

        } catch (e) {
            report.push(`❌ ${cat}: CRITICAL FAIL (${e.message})`);
        }
    }

    console.table(report);
    const finalReport = report.join("\n");
    alert(`QA Complete!\n\n${finalReport}`);
    return finalReport;
};

// 2. Register to WebMCP (If Available)
if (navigator.modelContext) {
    console.log("✅ WebMCP Service Found!");
    navigator.modelContext.registerTool({
        name: "run_saju_analysis",
        description: "Run specific saju analysis",
        parameters: {
            type: "object",
            properties: {
                category: { type: "string" },
                name: { type: "string" },
                birthDate: { type: "string" },
                birthTime: { type: "string" }
            },
            required: ["category", "name", "birthDate"]
        },
        execute: window.run_saju_analysis_tool
    });

    navigator.modelContext.registerTool({
        name: "test_all_features",
        description: "Run full automated QA test",
        execute: window.test_all_features
    });
} else {
    console.warn("⚠️ WebMCP API not found. You can still run 'await test_all_features()' manually in console.");
}
