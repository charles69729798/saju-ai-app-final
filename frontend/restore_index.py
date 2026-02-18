
import os

path = r'c:\InsuranceProject\NotebookLM\saju-app\frontend\index.html'

# Reconstructing the file content from viewed parts.
# I will use the parts I viewed in earlier steps.
# Since I am an AI, I have access to these parts in my context.

content_top = """<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="오프라인 DB 기반 프리미엄 사주 AI 상담 서비스">
    <meta name="theme-color" content="#764ba2">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="사주AI">
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/icons/icon-192x192.png">
    <title>🔮 사주 AI 상담</title>
    <!-- Google Fonts -->
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Montserrat:wght@700;800&display=swap"
        rel="stylesheet">
    <!-- <script>window.currentRelation = 'lover';</script> -->
    <script>
        window.currentRelation = 'lover';
        // Service Worker Unregister for Development
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(function (registrations) {
                for (let registration of registrations) {
                    registration.unregister();
                }
            });
        }
    </script>
    <style>
        :root {
            --primary-bg: #0f172a;
            /* Deep slate for dark mode sustainability */
            --accent-color: #a78bfa;
            --card-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --glass-blur: blur(16px);

            /* Theme Colors */
            --theme-lover: #fb7185;
            --theme-business: #38bdf8;
            --theme-friend: #4ade80;
            --theme-star: #fbbf24;
            --theme-peer: #6366f1;
        }

        @keyframes rotate {
            from {
                transform: rotate(0deg);
            }

            to {
                transform: rotate(360deg);
            }
        }

        @keyframes pulseGlow {
            0% {
                box-shadow: 0 0 10px rgba(167, 139, 250, 0.2);
            }

            50% {
                box-shadow: 0 0 25px rgba(167, 139, 250, 0.6);
            }

            100% {
                box-shadow: 0 0 10px rgba(167, 139, 250, 0.2);
            }
        }

        @keyframes pulse {

            0%,
            100% {
                opacity: 0.5;
                transform: scale(1);
            }

            50% {
                opacity: 1;
                transform: scale(1.1);
            }
        }

        @keyframes scan {
            0% {
                top: -10%;
            }

            100% {
                top: 110%;
            }
        }

        @keyframes float {

            0%,
            100% {
                transform: translateY(0);
            }

            50% {
                transform: translateY(-10px);
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background: var(--primary-bg);
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
            overflow-x: hidden;
            background-image:
                radial-gradient(circle at 20% 20%, rgba(167, 139, 250, 0.1) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(56, 189, 248, 0.1) 0%, transparent 40%);
        }

        /* Particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .particle {
            position: absolute;
            background: var(--accent-color);
            border-radius: 50%;
            opacity: 0.3;
            animation: float infinite ease-in-out;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            position: relative;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            padding-top: 20px;
        }

        h1 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            font-size: 2.2rem;
            background: linear-gradient(135deg, #fff 30%, var(--accent-color));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            filter: drop-shadow(0 2px 10px rgba(167, 139, 250, 0.3));
        }

        /* Version Badge */
        h1::after {
            content: "v2.5 (WebMCP)";
            font-size: 0.4em;
            color: #fbbf24;
            vertical-align: middle;
            margin-left: 10px;
            -webkit-text-fill-color: #fbbf24;
            text-shadow: 0 0 5px rgba(251, 191, 36, 0.5);
        }

        .subtitle {
            font-size: 0.95rem;
            color: var(--text-dim);
            letter-spacing: 0.5px;
        }

        /* Premium Glass Card */
        .card {
            background: var(--card-bg);
            backdrop-filter: var(--glass-blur);
            -webkit-backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: 28px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .card:hover {
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        .card h2 {
            font-size: 1.1rem;
            color: var(--accent-color);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Relationship Chips */
        .relation-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }

        .chip {
            padding: 8px 16px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-dim);
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .chip.active {
            background: var(--accent-color);
            color: #000;
            border-color: transparent;
            box-shadow: 0 0 15px var(--accent-color);
        }

        /* Form Inputs */
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }

        .form-group label {
            font-size: 0.75rem;
            color: var(--text-dim);
            margin-bottom: 8px;
            display: block;
            font-weight: 700;
            text-transform: none;
            /* Changed from uppercase for better readability */
            letter-spacing: 1px;
        }

        /* Mobile Responsive Form Row */
        @media (max-width: 480px) {
            .form-row {
                grid-template-columns: 1fr !important;
                gap: 12px !important;
            }

            .input-group input {
                min-width: 0;
            }
        }

        input,
        select {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 14px;
            padding: 12px 16px;
            color: white;
            font-size: 0.95rem;
            width: 100%;
            transition: border-color 0.2s;
        }

        input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2);
        }

        /* Highlight input when it has a value (useful for celeb selection visibility) */
        input:not(:placeholder-shown) {
            border-color: rgba(167, 139, 250, 0.5);
            background: rgba(167, 139, 250, 0.05);
        }

        .input-group {
            display: flex;
            gap: 8px;
            align-items: center;
            width: 100%;
        }

        .btn-icon {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            padding: 10px;
            border-radius: 14px;
            cursor: pointer;
            font-size: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: 0.2s;
            min-width: 48px;
            height: 48px;
        }

        .btn-icon:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--accent-color);
            transform: translateY(-2px);
        }

        #targetSearchBtn {
            display: none;
            /* Hidden by default */
        }

        /* Segmented Date Input */
        .date-input-container {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 5px;
        }

        .date-input {
            background: rgba(15, 23, 42, 0.8) !important;
            border: 2px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px;
            padding: 12px !important;
            font-size: 1.2rem !important;
            font-weight: 800 !important;
            letter-spacing: 2px;
            text-align: center;
            color: var(--accent-color) !important;
            font-family: 'Montserrat', sans-serif;
            width: 100%;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5);
        }

        .date-input:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 20px rgba(167, 139, 250, 0.2);
        }

        /* Hour Badge Grid */
        .hour-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 6px;
            margin-top: 10px;
        }

        .hour-badge {
            padding: 8px 0;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            color: var(--text-dim);
            font-size: 0.8rem;
            font-weight: 700;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }

        .hour-badge.active {
            background: var(--accent-color);
            color: #000;
            border-color: transparent;
            box-shadow: 0 0 10px var(--accent-color);
            transform: scale(1.05);
        }

        .time-picker-wrapper {
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .ampm-toggle-large {
            display: flex;
            gap: 5px;
            margin-bottom: 12px;
        }

        .ampm-btn-large {
            flex: 1;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-dim);
            font-weight: 800;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
        }

        .ampm-btn-large.active {
            background: #fff;
            color: #000;
            border-color: transparent;
        }

        /* Gender & MBTI */
        .gender-toggle {
            display: flex;
            background: rgba(0, 0, 0, 0.2);
            padding: 4px;
            border-radius: 12px;
            gap: 4px;
        }

        .gender-option {
            flex: 1;
            padding: 10px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            color: var(--text-dim);
            font-size: 0.85rem;
            transition: 0.2s;
        }

        .gender-option.active {
            background: #fff;
            color: #000;
            font-weight: 800;
        }

        .mbti-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
        }

        .mbti-chip {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px 4px;
            font-size: 0.7rem;
            text-align: center;
            cursor: pointer;
            transition: 0.2s;
        }

        .mbti-chip.active {
            background: var(--accent-color);
            color: #000;
            font-weight: 800;
            border-color: transparent;
        }

        /* Category Grid */
        .categories-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .category-btn {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 18px;
            padding: 20px 12px;
            color: white;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: 0.2s;
            position: relative;
            overflow: hidden;
        }

        .category-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--accent-color);
            transform: scale(1.02);
        }

        .category-btn.필수::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            box-shadow: inset 0 0 20px rgba(167, 139, 250, 0.2);
            pointer-events: none;
        }

        /* Action Button */
        /* Updated Action Button */
        .btn-primary {
            margin: 30px auto 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            background: linear-gradient(135deg, var(--accent-color), #7c3aed);
            color: #000;
            border: none;
            padding: 16px 32px;
            border-radius: 50px;
            font-weight: 900;
            font-size: 1.1rem;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(167, 139, 250, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: pulseGlow 3s infinite;
        }

        .btn-primary:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 15px 40px rgba(167, 139, 250, 0.4);
        }

        .btn-primary:active {
            transform: scale(0.98);
        }

        /* Modal / Contact Picker */
        .modal {
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 3000;
            padding: 20px;
        }

        .modal.show {
            display: flex;
        }

        .modal-content {
            background: #1e293b;
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            width: 100%;
            max-width: 400px;
            padding: 24px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .modal-title {
            font-weight: 800;
            color: var(--accent-color);
            font-size: 1.2rem;
        }

        .close-btn {
            background: none;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
        }

        .contact-list {
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 400px;
            overflow-y: auto;
            padding-right: 5px;
        }

        .contact-item {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 16px;
            border-radius: 12px;
            cursor: pointer;
            transition: 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .contact-item:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: var(--accent-color);
        }

        .contact-name {
            font-weight: 700;
        }

        .contact-desc {
            font-size: 0.75rem;
            color: var(--text-dim);
        }

        /* Celebrity List in Modal */
        .celeb-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
            margin-top: 15px;
        }

        .celeb-item {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.2s;
            text-align: center;
            position: relative;
        }

        .celeb-item:hover {
            border-color: var(--accent-color);
            background: rgba(167, 139, 250, 0.1);
            transform: translateY(-2px);
        }

        .celeb-rank {
            position: absolute;
            top: 5px;
            left: 5px;
            font-size: 0.65rem;
            color: var(--text-dim);
            background: rgba(0, 0, 0, 0.3);
            padding: 2px 6px;
            border-radius: 10px;
        }

        .celeb-name {
            font-weight: 800;
            display: block;
            margin-top: 5px;
        }

        .celeb-category {
            font-size: 0.7rem;
            color: var(--text-dim);
        }

        .search-bar-container {
            position: sticky;
            top: 0;
            background: #1e293b;
            z-index: 10;
            padding-bottom: 15px;
        }

        .search-input-fancy {
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid var(--glass-border);
            padding: 14px 20px;
            border-radius: 15px;
            font-size: 1rem;
            color: white;
            width: 100%;
            transition: 0.2s;
        }

        .search-input-fancy:focus {
            border-color: var(--accent-color);
            outline: none;
        }

        /* Result Section */
        .result-card {
            background: #0f172a;
            border: 1px solid var(--accent-color);
        }

        .result-content {
            line-height: 1.8;
            color: #e2e8f0;
        }

        .result-content h3 {
            color: var(--accent-color);
            margin: 24px 0 12px;
            border-left: 4px solid var(--accent-color);
            padding-left: 12px;
        }

        /* Loading Animation (Lab Style) */
        .loading {
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.9);
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        }

        .loading.show {
            display: flex;
        }

        .scanner {
            width: 200px;
            height: 2px;
            background: var(--accent-color);
            position: relative;
            box-shadow: 0 0 20px var(--accent-color);
            animation: moveUpDown 2s infinite ease-in-out;
        }

        @keyframes moveUpDown {

            0%,
            100% {
                transform: translateY(-50px);
            }

            50% {
                transform: translateY(50px);
            }
        }

        /* Guardian */
        #guardian-avatar {
            background: radial-gradient(circle, rgba(167, 139, 250, 0.2), transparent);
        }

        /* Mobile Adjustments */
        @media (max-width: 600px) {
            .card {
                padding: 20px;
            }

            h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>

<body>
    <div class="particles" id="particles"></div>
    <div class="container">
        <header>
            <h1>🧪 Relation Chemistry Lab</h1>
            <p class="subtitle">Signal Decoding & Relationship Navigation</p>
        </header>

        <!-- Hero: 오늘의 귀인/주의 인물 -->
        <div class="hero-card" id="heroCard">
            <span class="hero-title">Today's Connection</span>
            <div class="hero-content" id="heroContent">
                분석을 위해 정보를 입력해주세요.
            </div>
        </div>

        <div class="card">
            <h2>🧬 본인 정보 입력</h2>

            <div class="form-row">
                <div class="form-group">
                    <label>생년월일 (YYYYMMDD)</label>
                    <input type="tel" id="birthDate" class="date-input" placeholder="19990101" maxlength="10">
                </div>
                <div class="form-group">
                    <label>출생 시간</label>
                    <div class="time-picker-wrapper" id="birthTimeGroup">
                        <div class="ampm-toggle-large">
                            <button type="button" class="ampm-btn-large active" data-val="AM">AM</button>
                            <button type="button" class="ampm-btn-large" data-val="PM">PM</button>
                        </div>
                        <div class="hour-grid">
                            <!-- JS will populate -->
                        </div>
                    </div>
                    <input type="hidden" id="birthTime" value="00:00">
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label>이름 (한글)</label>
                    <input type="text" id="nameKorean" placeholder="예: 홍길동">
                </div>
                <div class="form-group">
                    <label>성별</label>
                    <div class="gender-toggle" id="userGenderToggle">
                        <div class="gender-option" data-value="M">남성</div>
                        <div class="gender-option active" data-value="F">여성</div>
                    </div>
                    <input type="hidden" id="userGender" value="F">
                </div>
            </div>

            <div class="form-group" style="margin-top: 15px;">
                <label>MBTI (선택)</label>
                <div class="mbti-grid" id="userMbtiGrid">
                    <!-- JS will populate -->
                </div>
                <input type="hidden" id="mbti" value="">
            </div>

            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 20px 0;">

            <!-- Target Info Section -->
            <div id="targetInfoSection" class="animate-scale-in">
                <label>어떤 관계인가요?</label>
                <div class="relation-chips" id="relationChips" style="margin-bottom: 20px;">
                    <button class="chip active" data-type="lover">❤️ 연인/썸</button>
                    <button class="chip" data-type="business">💼 직장/비즈니스</button>
                    <button class="chip" data-type="friend">🤝 친구/가족</button>
                    <button class="chip" data-type="star">✨ 스타/가상</button>
                    <button class="chip" data-type="peer">동기/동료</button>
                </div>

                <h3
                    style="font-size: 1.1rem; color: var(--accent-color); margin-bottom: 20px; font-family: 'Montserrat', sans-serif;">
                    🤝 상대방 정보 (관계 분석용)
                </h3>

                <div class="form-row">
                    <div class="form-group">
                        <label>상대방 이름</label>
                        <div class="input-group">
                            <input type="text" id="targetName" placeholder="이름 입력">
                            <button type="button" class="btn-icon" id="targetSearchBtn" onclick="showStarPicker()"
                                title="스타 검색">
                                ✨
                            </button>
                            <button type="button" class="btn-icon" onclick="showContactPicker('target')"
                                title="주소록 불러오기">
                                📒
                            </button>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>상대방 성별</label>
                        <div class="gender-toggle" id="targetGenderToggle">
                            <div class="gender-option active" data-value="M">남성</div>
                            <div class="gender-option" data-value="F">여성</div>
                        </div>
                        <input type="hidden" id="targetGender" value="M">
                    </div>
                </div>

                <div class="form-group" style="margin-top: 15px;">
                    <label>상대방 MBTI</label>
                    <div class="mbti-grid" id="targetMbtiGrid">
                        <!-- JS will populate -->
                    </div>
                    <input type="hidden" id="targetMbti" value="">
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>상대방 생년월일</label>
                        <input type="tel" id="targetBirthDate" class="date-input" placeholder="20001225" maxlength="10">
                    </div>
                    <div class="form-group">
                        <label>상대방 출생 시간</label>
                        <div class="time-picker-wrapper" id="targetBirthTimeGroup">
                            <div class="ampm-toggle-large">
                                <button type="button" class="ampm-btn-large active" data-val="AM">AM</button>
                                <button type="button" class="ampm-btn-large" data-val="PM">PM</button>
                            </div>
                            <div class="hour-grid">
                                <!-- Badges -->
                            </div>
                        </div>
                        <input type="hidden" id="targetBirthTime" value="12:00">
                    </div>
                </div>
            </div>

            <!-- Redundant Start Button Removed per QA Audit P-01 -->
        </div>

        <div class="card">
            <h2>🎯 분석 테마</h2>
            <div class="categories-grid" id="categoriesGrid">
                <!-- API Loading -->
            </div>
        </div>

        <div class="loading" id="loading">
            <div class="scanner"></div>
            <p style="margin-top: 40px; color: var(--accent-color); font-weight: 800; letter-spacing: 2px;">⚡ 시그널 분석
                중...</p>
        </div>

        <div class="error" id="error"></div>

        <!-- Star Picker Modal -->
        <div class="modal" id="starPickerModal">
            <div class="modal-content" style="max-width: 450px;">
                <div class="modal-header">
                    <span class="modal-title">✨ 스타/유명인 검색</span>
                    <button class="close-btn" onclick="closeModal('starPickerModal')">&times;</button>
                </div>
                <div class="search-bar-container">
                    <input type="text" id="celebSearchInput" class="search-input-fancy" placeholder="이름 또는 태그 검색..."
                        oninput="searchCelebs()">
                </div>
                <div class="contact-list" id="celebList">
                    <!-- Celebs list will be populated here -->
                </div>
            </div>
        </div>

        <!-- Result -->
        <div id="result" class="card result-card animate-fade-up" style="display:none; margin-top: 3rem;">
            <div class="result-header">
                <div id="guardian-container" class="floating" style="text-align:center; margin-bottom: 2rem;">
                    <!-- Anime Guardian Placeholder -->
                    <div id="guardian-avatar"
                        style="width: 150px; height: 150px; margin: 0 auto; background: rgba(255,255,255,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 3px solid var(--accent-color);">
                        <span style="font-size: 3rem;">🐉</span>
                    </div>
                    <p id="guardian-speech"
                        style="margin-top: 1rem; font-weight: 600; font-style: italic; color: var(--accent-color); font-size: 1.1rem;">
                    </p>
                </div>
                <h3>분석 결과 리포트</h3>
                <div id="resultContent" class="result-content"></div>

                <!-- Locked Content (Monetization UI) -->
                <div class="locked-content">
                    <div class="blur-text">
                        이 관계의 핵심적인 처세술과 상대방의 속마음은 비공개 데이터입니다.
                        상대방이 당신에게 숨기고 있는 기운을 확인해보세요.
                        침대에서의 성향이나 업무상의 필살 아부 멘트가 포함되어 있습니다.
                    </div>
                    <div class="lock-overlay">
                        <span style="font-size: 1.5rem;">🔒</span>
                        <p style="font-size: 0.9rem; font-weight: 600;">상대방의 '비밀 코드' 열기</p>
                        <button class="lock-btn">500원으로 확인</button>
                    </div>
                </div>

                <button class="btn-save-pdf no-print" onclick="saveAsPDF()"
                    style="background: transparent; border: 1px solid var(--card-border); color: white; margin-top: 30px;">
                    📄 PDF 리포트 저장
                </button>
            </div>
        </div>

    </div>

    <!-- Contact Picker Modal -->
    <div id="contactModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span id="modalTitle" class="modal-title">주소록 불러오기</span>
                <button class="close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div id="contactList" class="contact-list">
                <!-- JS will populate -->
            </div>
        </div>
    </div>
    </div>

    <!-- 외부 라이브러리 (body 하단) -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>

    <script>
        // ====== PWA: Service Worker 등록 ======
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(reg => console.log('[PWA] SW 등록 성공:', reg.scope))
                    .catch(err => console.log('[PWA] SW 등록 실패:', err));
            });
        }


        // ====== API ======
        const API_BASE = window.location.origin + '/api';

        // ====== UI State & Theme ======
        window.currentRelation = 'lover'; // Default initialization
        const chips = document.querySelectorAll('.chip');

        chips.forEach(chip => {
            chip.addEventListener('click', () => {
                chips.forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                window.currentRelation = chip.dataset.type;
                updateTheme(window.currentRelation);
            });
        });

        function updateTheme(relation) {
            const root = document.documentElement;
            let activeColor = '#a78bfa';
            switch (relation) {
                case 'lover': activeColor = '#fb7185'; break;
                case 'business': activeColor = '#38bdf8'; break;
                case 'friend': activeColor = '#4ade80'; break;
                case 'star': activeColor = '#fbbf24'; break;
                case 'peer': activeColor = '#6366f1'; break;
            }
            root.style.setProperty('--accent-color', activeColor);
        }

        // ====== Gen Z Feature Logic ======

        // ====== Mock Data ======
        const MOCK_CONTACTS = [
            { name: "김민수", birthday: "1994-05-12", gender: "M", mbti: "ENFP", tags: "직장 동료" },
            { name: "이영희", birthday: "1988-11-20", gender: "F", mbti: "INTJ", tags: "오랜 친구" },
            { name: "박지호", birthday: "1997-02-28", gender: "M", mbti: "ISTP", tags: "고등학교 동창" },
            { name: "최수지", birthday: "2001-08-15", gender: "F", mbti: "ESFJ", tags: "동네 친구" }
        ];

        const STAR_DATABASE = [
            { name: "차은우", birthday: "1997-03-30", gender: "M", mbti: "INFJ", tags: "판타지오" },
            { name: "장원영", birthday: "2004-08-31", gender: "F", mbti: "ENTJ", tags: "스타쉽" },
            { name: "카리나", birthday: "2000-04-11", gender: "F", mbti: "ENFP", tags: "SM" },
            { name: "BTS 정국", birthday: "1997-09-01", gender: "M", mbti: "INTP", tags: "빅히트" },
            { name: "윈터", birthday: "2001-01-01", gender: "F", mbti: "ISFJ", tags: "aespa" }
        ];

        // 1. Android Contact Picker Mock UI
        function showContactPicker(type = 'target') {
            const modal = document.getElementById('contactModal');
            const list = document.getElementById('contactList');
            const title = document.getElementById('modalTitle');

            modal.classList.add('show');
            list.innerHTML = '';

            const isStar = window.currentRelation === 'star';
            const data = isStar ? STAR_DATABASE : MOCK_CONTACTS;
            title.textContent = isStar ? "가상/스타 데이터베이스" : "내 주소록 연동 (Android)";

            data.forEach(item => {
                const row = document.createElement('div');
                row.className = 'contact-item';
                row.innerHTML = `
                    <div>
                        <div class="contact-name">${item.name}</div>
                        <div class="contact-desc">${item.tags || ''}</div>
                    </div>
                    <div style="font-size:0.7rem; color:var(--accent-color)">불러오기 ></div>
                `;
                row.onclick = () => selectContact(item, type);
                list.appendChild(row);
            });
        }

        function closeModal(id = 'contactModal') {
            const modal = document.getElementById(id);
            if (modal) modal.classList.remove('show');
        }

        function selectContact(item, type = 'target') {
            const suffix = type === 'user' ? '' : 'target';
            const nameId = type === 'user' ? 'nameKorean' : 'targetName';
            const birthId = type === 'user' ? 'birthDate' : 'targetBirthDate';
            const genderToggleId = type === 'user' ? 'userGenderToggle' : 'targetGenderToggle';
            const genderInputId = type === 'user' ? 'userGender' : 'targetGender';
            const mbtiGridId = type === 'user' ? 'userMbtiGrid' : 'targetMbtiGrid';
            const mbtiInputId = type === 'user' ? 'mbti' : 'targetMbti';

            // Auto-fill Info
            document.getElementById(nameId).value = item.name;
            document.getElementById(birthId).value = item.birthday.replace(/-/g, '');
            // Trigger input event to format
            document.getElementById(birthId).dispatchEvent(new Event('input'));

            // Set Gender
            const genderToggle = document.getElementById(genderToggleId);
            const options = genderToggle.querySelectorAll('.gender-option');
            options.forEach(opt => {
                if (opt.dataset.value === item.gender) {
                    opt.click();
                }
            });

            // Set MBTI if exists
            if (item.mbti) {
                const mbtiGrid = document.getElementById(mbtiGridId);
                const chips = mbtiGrid.querySelectorAll('.mbti-chip');
                chips.forEach(chip => {
                    if (chip.innerText === item.mbti) {
                        chip.click();
                    }
                });
            }

            closeModal();

            // Visual Feedback
            const highlightSection = type === 'user' ? document.querySelector('.card') : document.getElementById('targetInfoSection');
            highlightSection.style.boxShadow = '0 0 30px var(--accent-color)';
            setTimeout(() => highlightSection.style.boxShadow = 'none', 1000);
        }

        // 5. Gender Toggle Initialization
        function setupGenderToggle(toggleId, inputId) {
            const toggle = document.getElementById(toggleId);
            const input = document.getElementById(inputId);
            if (!toggle || !input) return;

            const options = toggle.querySelectorAll('.gender-option');
            options.forEach(opt => {
                opt.onclick = () => {
                    options.forEach(o => o.classList.remove('active'));
                    opt.classList.add('active');
                    input.value = opt.dataset.value;
                };
            });
        }

        // 2. Premium Date Input (Auto-Hyphenation)
        function setupDateInput(id) {
            const el = document.getElementById(id);
            if (!el) return;
            el.addEventListener('input', (e) => {
                let val = e.target.value.replace(/\D/g, ''); // 숫자만 남기기

                // [ MZ-Premium Validation ] 실시간 날짜 유효성 체크 및 보정
                if (val.length >= 6) {
                    const month = parseInt(val.slice(4, 6), 10);
                    if (month > 12) val = val.slice(0, 4) + '12' + val.slice(6);
                    if (month === 0) val = val.slice(0, 4) + '01' + val.slice(6);
                }
                if (val.length >= 8) {
                    const day = parseInt(val.slice(6, 8), 10);
                    if (day > 31) val = val.slice(0, 6) + '31'; // [USER Feedback] 31일 초과 방지
                    if (day === 0) val = val.slice(0, 6) + '01';
                }

                if (val.length >= 5) val = val.slice(0, 4) + '-' + val.slice(4);
                if (val.length >= 8) val = val.slice(0, 7) + '-' + val.slice(7);
                if (val.length > 10) val = val.slice(0, 10);
                e.target.value = val;
            });
        }

        // 5. Advanced Badge-based Time Picker
        function setupTimePicker(groupId, hiddenInputId) {
            const group = document.getElementById(groupId);
            if (!group) return;

            const ampmBtns = group.querySelectorAll('.ampm-btn-large');
            const hourGrid = group.querySelector('.hour-grid');
            const hiddenInput = document.getElementById(hiddenInputId);

            let isPM = false;
            let currentHour = 12;

            // Render Hour Badges (1-12)
            hourGrid.innerHTML = '';
            for (let i = 1; i <= 12; i++) {
                const badge = document.createElement('div');
                badge.className = 'hour-badge';
                if (i === 12) badge.classList.add('active');
                badge.textContent = i;
                badge.onclick = (e) => {
                    e.preventDefault();
                    group.querySelectorAll('.hour-badge').forEach(b => b.classList.remove('active'));
                    badge.classList.add('active');
                    currentHour = i;
                    updateHiddenTime();
                };
                hourGrid.appendChild(badge);
            }

            // AM/PM Toggle
            ampmBtns.forEach(btn => {
                btn.onclick = (e) => {
                    e.preventDefault();
                    ampmBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    isPM = btn.dataset.val === 'PM';
                    updateHiddenTime();
                };
            });

            function updateHiddenTime() {
                let hour = currentHour;
                if (isPM && hour < 12) hour += 12;
                if (!isPM && hour === 12) hour = 0;
                hiddenInput.value = `${hour.toString().padStart(2, '0')}:00`;
            }
            updateHiddenTime();
        }

        // Initialize Features
        document.addEventListener('DOMContentLoaded', () => {
            renderMbtiGrid('userMbtiGrid', 'mbti');
            renderMbtiGrid('targetMbtiGrid', 'targetMbti');
            setupGenderToggle('userGenderToggle', 'userGender');
            setupGenderToggle('targetGenderToggle', 'targetGender');

            setupDateInput('birthDate');
            setupDateInput('targetBirthDate');

            setupTimePicker('birthTimeGroup', 'birthTime');
            setupTimePicker('targetBirthTimeGroup', 'targetBirthTime');
        });

        // 3. MBTI Grid Logic
        function renderMbtiGrid(containerId, hiddenInputId) {
            const mbtis = [
                'ISTJ', 'ISFJ', 'INFJ', 'INTJ',
                'ISTP', 'ISFP', 'INFP', 'INTP',
                'ESTP', 'ESFP', 'ENFP', 'ENTP',
                'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ'
            ];
            const container = document.getElementById(containerId);
            const hidden = document.getElementById(hiddenInputId);

            container.innerHTML = '';
            mbtis.forEach(type => {
                const div = document.createElement('div');
                div.className = 'mbti-chip';
                div.innerText = type;
                div.onclick = () => {
                    // Toggle Logic
                    const isActive = div.classList.contains('active');
                    // Reset all
                    container.querySelectorAll('.mbti-chip').forEach(c => c.classList.remove('active'));
                    if (!isActive) {
                        div.classList.add('active');
                        hidden.value = type;
                    } else {
                        hidden.value = '';
                    }
                };
                container.appendChild(div);
            });
        }

        // Relationship Chips Toggle Logic
        document.querySelectorAll('#relationChips .chip').forEach(chip => {
            chip.onclick = () => {
                document.querySelectorAll('#relationChips .chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                window.currentRelation = chip.dataset.type;

                const searchBtn = document.getElementById('targetSearchBtn');
                if (window.currentRelation === 'star') {
                    searchBtn.style.display = 'flex';
                } else {
                    searchBtn.style.display = 'none';
                }

                // Update theme based on relation
                const themeMap = {
                    'lover': 'lover',
                    'business': 'business',
                    'friend': 'friend',
                    'star': 'star',
                    'peer': 'peer'
                };
                updateTheme(themeMap[window.currentRelation]);
            };
        });

        function updateTheme(theme) {
            const colors = {
                'lover': '#fb7185',
                'business': '#38bdf8',
                'friend': '#4ade80',
                'star': '#fbbf24',
                'peer': '#6366f1'
            };
            document.documentElement.style.setProperty('--accent-color', colors[theme]);
            // Update particles or other UI elements if needed
        }

        // Star Picker Logic
        async function showStarPicker() {
            document.getElementById('starPickerModal').classList.add('show');
            await searchCelebs();
        }


        async function searchCelebs() {
            const query = document.getElementById('celebSearchInput').value;
            const res = await fetch(`${API_BASE}/celebs?search=${encodeURIComponent(query)}`);
            const data = await res.json();

            const list = document.getElementById('celebList');
            list.innerHTML = '';

            if (data.celebs.length === 0) {
                list.innerHTML = '<div style="text-align:center; padding:20px; color:var(--text-dim)">검색 결과가 없습니다.</div>';
                return;
            }

            data.celebs.forEach(celeb => {
                const item = document.createElement('div');
                item.className = 'contact-item';
                const mbtiLabel = celeb.mbti ?
                    `<span style="background:rgba(255,255,255,0.1); padding:1px 5px; border-radius:4px;">${celeb.mbti}${celeb.is_mbti_estimated ? ' (추정)' : ''}</span>`
                    : '';

                item.innerHTML = `
                    <div>
                        <div class="contact-name">${celeb.name} <small style="color:var(--accent-color)">#${celeb.category}</small></div>
                        <div class="contact-desc">${celeb.description || ''}</div>
                        <div style="font-size:0.7rem; margin-top:4px;">
                            ${mbtiLabel}
                            ${celeb.tags || ''}
                        </div>
                    </div>
                `;
                item.onclick = () => selectCeleb(celeb);
                list.appendChild(item);
            });
        }

        function selectCeleb(celeb) {
            const nameInput = document.getElementById('targetName');
            const dateInput = document.getElementById('targetBirthDate');

            nameInput.value = celeb.name;
            dateInput.value = celeb.birth_date; // Backend format is YYYY-MM-DD

            // Trigger input events to ensure components (like auto-hyphenation) react
            nameInput.dispatchEvent(new Event('input'));
            dateInput.dispatchEvent(new Event('input'));

            document.getElementById('targetGender').value = celeb.gender;

            // Gender UI update
            const genderOptions = document.querySelectorAll('#targetGenderToggle .gender-option');
            genderOptions.forEach(opt => {
                opt.classList.toggle('active', opt.dataset.value === celeb.gender);
            });

            // MBTI UI update
            if (celeb.mbti) {
                const mbtiChips = document.querySelectorAll('#targetMbtiGrid .mbti-chip');
                mbtiChips.forEach(chip => {
                    if (chip.innerText === celeb.mbti) {
                        chip.click();
                    }
                });
            }

            closeModal('starPickerModal');

            // Show toast or hint
            showError(`${celeb.name}님의 정보가 입력되었습니다.`);
            setTimeout(() => document.getElementById('error').classList.remove('show'), 2000);
        }


        // ====== Categories Loading ======

        async function loadCategories() {
            try {
                const res = await fetch(`${API_BASE}/categories`);
                const data = await res.json();
                const grid = document.getElementById('categoriesGrid');
                grid.innerHTML = '';
                data.categories.forEach(cat => {
                    const btn = document.createElement('button');
                    btn.className = `category-btn ${cat.priority}`;
                    btn.textContent = cat.name;
                    btn.onclick = () => analyzeSaju(cat.id);
                    grid.appendChild(btn);
                });
            } catch (e) {
                console.error('API Load Error:', e);
            }
        }

        // ====== 유효성 검사 Helper ======
        function isValidDateString(str) {
            if (!/^\d{4}-\d{2}-\d{2}$/.test(str)) return false;
            const parts = str.split("-");
            const y = parseInt(parts[0], 10);
            const m = parseInt(parts[1], 10);
            const d = parseInt(parts[2], 10);
            const date = new Date(y, m - 1, d);
            return date.getFullYear() === y && date.getMonth() === m - 1 && date.getDate() === d;
        }

        // ====== 사주 분석 ======
        async function commitAnalysis(category = '평생사주') {
            const birthDateRaw = document.getElementById('birthDate').value;
            const birthTime = document.getElementById('birthTime').value;
            const name = document.getElementById('nameKorean').value.trim() || '익명';

            // [Strict Validation] 본인 생년월일
            if (!isValidDateString(birthDateRaw)) {
                showError("본인의 생년월일을 정확히 입력해주세요 (YYYY-MM-DD)\\n예: 1999-01-01");
                document.getElementById('birthDate').focus();
                return;
            }

            // [Validation] 관계 분석 테마인데 상대방 정보가 없는 경우 체크
            const isRelationTheme = ['애정운', 'STAR', '궁합', '러브시그널'].includes(category);
            const targetName = document.getElementById('targetName').value.trim();
            const targetBirthRaw = document.getElementById('targetBirthDate').value;

            if (isRelationTheme && (!targetName || !isValidDateString(targetBirthRaw))) {
                showError("상대방 정보를 정확히 입력해주세요.");
                document.getElementById('targetName').focus();
                return;
            }

            document.getElementById('result').style.display = 'none';
            document.getElementById('loading').classList.add('show');
            document.getElementById('error').classList.remove('show');

            // [Phase 3] 관계 데이터 수집
            let relationData = null;
            if (targetBirthRaw && targetBirthRaw.length === 10) {
                    relationData = {
                        target_name: targetName || '상대방',
                        target_birth_date: targetBirthRaw,
                        target_birth_time: document.getElementById('targetBirthTime').value || '12:00',
                        target_mbti: document.getElementById('targetMbti').value,
                        relation_code: (window.currentRelation || 'lover').toUpperCase(),
                        target_gender: document.getElementById('targetGender').value
                    };
            }

            try {
                const res = await fetch(`${API_BASE}/saju/analyze`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_profile: {
                            birth_date: birthDateRaw,
                            birth_time: birthTime,
                            name_korean: name,
                            gender: document.getElementById('userGender').value,
                            mbti: document.getElementById('mbti').value
                        },
                        category: category,
                        relation_data: relationData
                    })
                });

                const data = await res.json();
                document.getElementById('loading').classList.remove('show');

                if (data.status === 'success') {
                    // Result Rendering
                    document.getElementById('resultContent').innerHTML = marked.parse(data.result);
                    document.getElementById('result').style.display = 'block';
                    scrollToResult();
                } else {
                    showError(data.message || "오류가 발생했습니다.");
                }
            } catch (err) {
                document.getElementById('loading').classList.remove('show');
                showError("서버 연결 실패");
            }
        }

        // Alias for analyzeSaju if needed
        function analyzeSaju(cat) { commitAnalysis(cat); }

        function saveAsPDF() {
            const element = document.getElementById('result');
            html2pdf().from(element).save('report.pdf');
        }

        function showError(msg) {
            const err = document.getElementById('error');
            err.textContent = msg;
            err.classList.add('show');
            setTimeout(() => err.classList.remove('show'), 5000);
        }

        // Initialize
        loadCategories();
        
        // Particles
        const particlesContainer = document.getElementById('particles');
        for (let i = 0; i < 20; i++) {
            const p = document.createElement('div');
            p.className = 'particle';
            const size = Math.random() * 4 + 2 + 'px';
            p.style.width = size; p.style.height = size;
            p.style.left = Math.random() * 100 + 'vw';
            p.style.top = Math.random() * 100 + 'vh';
            p.style.animationDuration = Math.random() * 10 + 10 + 's';
            p.style.opacity = Math.random() * 0.4;
            particlesContainer.appendChild(p);
        }

        function scrollToResult() {
            const target = document.getElementById('result');
            if (target) target.scrollIntoView({ behavior: 'smooth' });
        }
    </script>
    
    <script src="qa_loader.js?v=9999"></script>
</body>
</html>
"""

# Write the file with UTF-8 encoding explicitly
with open(path, 'w', encoding='utf-8') as f:
    f.write(content_top)

print("Successfully restored index.html with UTF-8 encoding.")
