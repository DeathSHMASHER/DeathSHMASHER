import json
import datetime
import pathlib
import sys

def generate_svg(total: int, current: int, longest: int, sync_date: str) -> str:
    total_pct = min(100, int((total / 1000.0) * 100))
    current_pct = min(100, max(8, int((current / 30.0) * 100)))
    longest_pct = min(100, max(15, int((longest / 30.0) * 100)))

    eq_bars = []
    base_x = 36
    for i in range(46):
        x = base_x + i * 20
        color = "#00f0ff" if i % 3 == 0 else ("#a855f7" if i % 3 == 1 else "#10b981")
        eq_bars.append(f'    <rect class="eq eq-{i % 5}" x="{x}" y="244" width="8" height="12" rx="3" fill="{color}" opacity="0.85"/>')
    eq_markup = "\n".join(eq_bars)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="980" height="280" viewBox="0 0 980 280">
  <defs>
    <!-- Background Gradients -->
    <linearGradient id="cyber-bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080c16"/>
      <stop offset="50%" stop-color="#0d1424"/>
      <stop offset="100%" stop-color="#060911"/>
    </linearGradient>

    <linearGradient id="card-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#141c2e" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0e1524" stop-opacity="0.9"/>
    </linearGradient>

    <!-- Neon Accents -->
    <linearGradient id="cyan-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00f0ff"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>

    <linearGradient id="orange-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff7b00"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>

    <linearGradient id="purple-glow" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#c084fc"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>

    <linearGradient id="shimmer-sweep" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#ffffff" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <style>
      .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
      
      /* Radar Pulse Animation */
      @keyframes pulse-ring {{
        0% {{ r: 4px; opacity: 1; }}
        70% {{ r: 12px; opacity: 0.2; }}
        100% {{ r: 16px; opacity: 0; }}
      }}
      .radar-wave {{
        animation: pulse-ring 2.2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
        transform-origin: 902px 34px;
      }}
      
      /* Shimmer Beam Animation */
      @keyframes sweep {{
        0% {{ transform: translateX(-1000px); }}
        50%, 100% {{ transform: translateX(1000px); }}
      }}
      .shimmer {{
        animation: sweep 6s ease-in-out infinite;
      }}

      /* Equalizer Bar Animations */
      @keyframes eq-dance-0 {{ 0%, 100% {{ height: 6px; y: 250px; }} 50% {{ height: 18px; y: 238px; }} }}
      @keyframes eq-dance-1 {{ 0%, 100% {{ height: 14px; y: 242px; }} 50% {{ height: 6px; y: 250px; }} }}
      @keyframes eq-dance-2 {{ 0%, 100% {{ height: 8px; y: 248px; }} 50% {{ height: 22px; y: 234px; }} }}
      @keyframes eq-dance-3 {{ 0%, 100% {{ height: 20px; y: 236px; }} 50% {{ height: 9px; y: 247px; }} }}
      @keyframes eq-dance-4 {{ 0%, 100% {{ height: 11px; y: 245px; }} 50% {{ height: 16px; y: 240px; }} }}

      .eq-0 {{ animation: eq-dance-0 1.3s ease-in-out infinite; }}
      .eq-1 {{ animation: eq-dance-1 1.7s ease-in-out infinite; }}
      .eq-2 {{ animation: eq-dance-2 1.1s ease-in-out infinite; }}
      .eq-3 {{ animation: eq-dance-3 1.9s ease-in-out infinite; }}
      .eq-4 {{ animation: eq-dance-4 1.5s ease-in-out infinite; }}

      /* Number Glow Pulse */
      @keyframes glow-pulse {{
        0%, 100% {{ opacity: 0.95; filter: drop-shadow(0 0 6px rgba(56, 189, 248, 0.6)); }}
        50% {{ opacity: 1; filter: drop-shadow(0 0 14px rgba(56, 189, 248, 0.9)); }}
      }}
      .cyan-num {{ animation: glow-pulse 3s ease-in-out infinite; }}

      @keyframes flame-pulse {{
        0%, 100% {{ opacity: 0.95; filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.6)); }}
        50% {{ opacity: 1; filter: drop-shadow(0 0 14px rgba(245, 158, 11, 0.9)); }}
      }}
      .orange-num {{ animation: flame-pulse 2.6s ease-in-out infinite; }}

      @keyframes purple-pulse {{
        0%, 100% {{ opacity: 0.95; filter: drop-shadow(0 0 6px rgba(168, 85, 247, 0.6)); }}
        50% {{ opacity: 1; filter: drop-shadow(0 0 14px rgba(168, 85, 247, 0.9)); }}
      }}
      .purple-num {{ animation: purple-pulse 3.4s ease-in-out infinite; }}
    </style>
  </defs>

  <!-- Base Dashboard Canvas -->
  <rect x="2" y="2" width="976" height="276" rx="20" fill="url(#cyber-bg)" stroke="#223249" stroke-width="2"/>

  <!-- Shimmer Light Layer -->
  <g clip-path="url(#card-clip)">
    <rect class="shimmer" x="0" y="2" width="300" height="276" fill="url(#shimmer-sweep)"/>
  </g>

  <!-- Top Cyber Navigation Header -->
  <g transform="translate(32, 24)">
    <!-- Terminal Prompt Icon -->
    <rect x="0" y="2" width="22" height="22" rx="6" fill="#132034" stroke="#00f0ff" stroke-width="1.2"/>
    <path d="M7 8 L11 13 L7 18" fill="none" stroke="#00f0ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    
    <text x="32" y="18" fill="#f8fafc" class="mono" font-size="16" font-weight="800" letter-spacing="1.5">GITHUB // ACTIVITY TELEMETRY</text>
    <text x="352" y="18" fill="#00f0ff" class="mono" font-size="11" font-weight="600" opacity="0.85">[LIVE ENGINE v3.0]</text>
  </g>

  <!-- Status Pill (Carefully aligned, no overlapping) -->
  <g transform="translate(830, 22)">
    <rect x="0" y="0" width="118" height="26" rx="13" fill="#072318" stroke="#10b981" stroke-width="1.2"/>
    <circle class="radar-wave" cx="16" cy="13" r="5" fill="none" stroke="#10b981" stroke-width="1.5"/>
    <circle cx="16" cy="13" r="4.5" fill="#10b981"/>
    <text x="32" y="17" fill="#10b981" class="mono" font-size="11" font-weight="700" letter-spacing="0.5">SYNCED</text>
  </g>

  <!-- Divider Line -->
  <line x1="32" y1="56" x2="948" y2="56" stroke="#1c293d" stroke-width="1.2"/>

  <!-- Metric Card 1: TOTAL CONTRIBUTIONS -->
  <g transform="translate(32, 68)">
    <rect x="0" y="0" width="292" height="144" rx="14" fill="url(#card-grad)" stroke="#23354d" stroke-width="1.2"/>
    <path d="M0 14 Q0 0 14 0 L60 0" fill="none" stroke="#00f0ff" stroke-width="2.5"/>
    
    <text x="20" y="30" fill="#94a3b8" class="mono" font-size="11" font-weight="700" letter-spacing="1">&#x26A1; TOTAL CONTRIBUTIONS</text>
    <text x="20" y="82" fill="#00f0ff" class="mono cyan-num" font-size="44" font-weight="800">{total:,}</text>
    <text x="20" y="108" fill="#64748b" class="mono" font-size="11">from GitHub contribution calendar</text>
    
    <rect x="20" y="122" width="252" height="6" rx="3" fill="#152132"/>
    <rect x="20" y="122" width="{int(252 * (total_pct / 100.0))}" height="6" rx="3" fill="url(#cyan-glow)"/>
  </g>

  <!-- Metric Card 2: CURRENT STREAK -->
  <g transform="translate(344, 68)">
    <rect x="0" y="0" width="292" height="144" rx="14" fill="url(#card-grad)" stroke="#23354d" stroke-width="1.2"/>
    <path d="M0 14 Q0 0 14 0 L60 0" fill="none" stroke="#f59e0b" stroke-width="2.5"/>
    
    <text x="20" y="30" fill="#94a3b8" class="mono" font-size="11" font-weight="700" letter-spacing="1">&#x1F525; CURRENT STREAK</text>
    <text x="20" y="82" fill="#f59e0b" class="mono orange-num" font-size="44" font-weight="800">{current}</text>
    <text x="20" y="108" fill="#64748b" class="mono" font-size="11">consecutive active days</text>
    
    <rect x="20" y="122" width="252" height="6" rx="3" fill="#152132"/>
    <rect x="20" y="122" width="{int(252 * (current_pct / 100.0))}" height="6" rx="3" fill="url(#orange-glow)"/>
  </g>

  <!-- Metric Card 3: LONGEST STREAK -->
  <g transform="translate(656, 68)">
    <rect x="0" y="0" width="292" height="144" rx="14" fill="url(#card-grad)" stroke="#23354d" stroke-width="1.2"/>
    <path d="M0 14 Q0 0 14 0 L60 0" fill="none" stroke="#a855f7" stroke-width="2.5"/>
    
    <text x="20" y="30" fill="#94a3b8" class="mono" font-size="11" font-weight="700" letter-spacing="1">&#x1F3C6; LONGEST STREAK</text>
    <text x="20" y="82" fill="#c084fc" class="mono purple-num" font-size="44" font-weight="800">{longest}</text>
    <text x="20" y="108" fill="#64748b" class="mono" font-size="11">best consecutive run record</text>
    
    <rect x="20" y="122" width="252" height="6" rx="3" fill="#152132"/>
    <rect x="20" y="122" width="{int(252 * (longest_pct / 100.0))}" height="6" rx="3" fill="url(#purple-glow)"/>
  </g>

  <!-- Bottom Rhythm Visualizer & Telemetry Footer -->
  <g transform="translate(0, 0)">
{eq_markup}
    <!-- Status footer label -->
    <text x="36" y="268" fill="#475569" class="mono" font-size="10" font-weight="600">&#x25CF; LIVE TELEMETRY BUS // REFRESHED: {sync_date} &#x2022; GITHUB ACTIONS PIPELINE</text>
    <text x="944" y="268" text-anchor="end" fill="#00f0ff" class="mono" font-size="10" font-weight="600" opacity="0.8">RHYTHM: 100% HEALTHY</text>
  </g>
</svg>"""
    return svg

def main():
    json_path = pathlib.Path("contribution-data.json")
    today = datetime.date.today()
    sync_date = today.isoformat()

    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            user_data = data.get("data", {}).get("user")
            if not user_data:
                print("Warning: user data not found in contribution-data.json, using defaults")
                total, current, longest = 493, 1, 12
            else:
                cal = user_data["contributionsCollection"]["contributionCalendar"]
                days = []
                for week in cal["weeks"]:
                    for day in week["contributionDays"]:
                        days.append((day["date"], int(day["contributionCount"])))
                days.sort()

                total = int(cal["totalContributions"])

                longest = 0
                run = 0
                for _, count in days:
                    if count > 0:
                        run += 1
                        longest = max(longest, run)
                    else:
                        run = 0

                by_date = {datetime.date.fromisoformat(d): c for d, c in days}
                cursor = today if by_date.get(today, 0) > 0 else today - datetime.timedelta(days=1)
                current = 0
                while by_date.get(cursor, 0) > 0:
                    current += 1
                    cursor -= datetime.timedelta(days=1)
        except Exception as e:
            print(f"Error parsing contribution-data.json: {e}")
            total, current, longest = 493, 1, 12
    else:
        # Default or fallback values
        total, current, longest = 493, 1, 12

    svg_content = generate_svg(total=total, current=current, longest=longest, sync_date=sync_date)
    out_dir = pathlib.Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "github-dashboard.svg"
    out_file.write_text(svg_content, encoding="utf-8")
    print(f"Successfully generated {out_file} (Total: {total}, Current Streak: {current}, Longest Streak: {longest})")

if __name__ == "__main__":
    main()
