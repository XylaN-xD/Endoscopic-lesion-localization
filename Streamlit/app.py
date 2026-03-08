"""
ELL Research System — Streamlit Version
Endoscopic Lesion Localization · Research Prototype · Phase 1
Features: DNA Helix canvas animation + Real Anthropic AI chatbot
"""

import streamlit as st
import random
from datetime import datetime

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ELL Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #05050f; color: #e2e8f0; }
.stApp > header { background: transparent !important; }

[data-testid="stSidebar"] {
    background: #080810;
    border-right: 1px solid #1a1a2e;
}
[data-testid="stSidebar"] .stRadio label { font-size:0.82rem; color:#94a3b8; }

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px; padding: 1.1rem 1.25rem; margin-bottom: 0.75rem;
    transition: border-color .2s;
}
.card:hover { border-color: rgba(0,200,255,0.2); }

.glow-card {
    background: rgba(0,200,255,0.04);
    border: 1px solid rgba(0,200,255,0.18);
    border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 0.75rem;
}

.stat-card { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07); border-radius:10px; padding:1rem; text-align:center; }
.stat-val  { font-size:1.8rem; font-weight:700; color:#e2e8f0; }
.stat-label{ font-size:.68rem; color:#64748b; letter-spacing:.08em; text-transform:uppercase; }
.stat-sub  { font-size:.7rem; color:#475569; margin-top:.25rem; }

.badge-active  { display:inline-flex;align-items:center;gap:.35rem;background:rgba(0,255,180,.08);border:1px solid rgba(0,255,180,.2);color:#00ffb4;font-size:.65rem;font-family:monospace;padding:.2rem .55rem;border-radius:999px;letter-spacing:.08em; }
.badge-research{ display:inline-flex;align-items:center;gap:.35rem;background:rgba(0,200,255,.08);border:1px solid rgba(0,200,255,.2);color:#00c8ff;font-size:.65rem;font-family:monospace;padding:.2rem .55rem;border-radius:999px;letter-spacing:.08em; }
.badge-planned { background:rgba(148,163,184,.06);border:1px solid rgba(148,163,184,.15);color:#64748b;font-size:.65rem;font-family:monospace;padding:.2rem .55rem;border-radius:999px;letter-spacing:.08em;display:inline-block; }

.section-label { font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;color:#00c8ff;font-family:monospace;font-weight:500; }

.pipe-block { background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-left:3px solid #00c8ff;border-radius:8px;padding:1rem 1.1rem;margin-bottom:.4rem; }
.pipe-connector { width:2px;height:20px;background:linear-gradient(to bottom,#00c8ff,transparent);margin:0 auto 0 1.4rem; }

.drop-zone { border:2px dashed rgba(0,200,255,.22);border-radius:12px;padding:2.5rem;text-align:center;color:#64748b;background:rgba(0,200,255,.03); }

.metric-pill { background:rgba(0,200,255,.07);border:1px solid rgba(0,200,255,.18);border-radius:8px;padding:.65rem .9rem;text-align:center; }
.metric-val  { font-size:1.3rem;font-weight:700;color:#00c8ff;font-family:monospace; }
.metric-lbl  { font-size:.7rem;color:#94a3b8; }
.metric-wk   { font-size:.65rem;color:#475569;font-family:monospace; }

.prompt-card { background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:.9rem 1rem;margin-bottom:.5rem; }

.stButton > button {
    background: rgba(0,200,255,.07) !important;
    border: 1px solid rgba(0,200,255,.25) !important;
    color: #94a3b8 !important;
    border-radius: 8px !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: rgba(0,200,255,.15) !important;
    border-color: rgba(0,200,255,.5) !important;
    color: #e2e8f0 !important;
}
[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, rgba(0,200,255,.2), rgba(140,80,255,.15)) !important;
    border: 1px solid rgba(0,200,255,.45) !important;
    color: #e2e8f0 !important;
}

#MainMenu, footer { visibility:hidden; }
.stDeployButton { display:none; }
</style>
""", unsafe_allow_html=True)

# ─── DNA Helix Canvas ──────────────────────────────────────────────────────────
DNA_HTML = """
<div style="position:relative;width:100%;height:500px;overflow:hidden;background:#05050f;">
  <canvas id="dnaCanvas" style="position:absolute;top:0;left:0;width:100%;height:100%;"></canvas>
  <!-- radial vignette -->
  <div style="position:absolute;inset:0;pointer-events:none;
    background:radial-gradient(ellipse at center, transparent 25%, #05050f 80%);"></div>
  <!-- top/bottom fade -->
  <div style="position:absolute;top:0;left:0;right:0;height:80px;pointer-events:none;
    background:linear-gradient(to bottom,#05050f,transparent);"></div>
  <div style="position:absolute;bottom:0;left:0;right:0;height:80px;pointer-events:none;
    background:linear-gradient(to top,#05050f,transparent);"></div>
</div>

<script>
(function(){
  const canvas = document.getElementById('dnaCanvas');
  const ctx    = canvas.getContext('2d');

  function resize(){
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
  }
  resize();
  new ResizeObserver(resize).observe(canvas);

  // floating ambient particles
  const particles = Array.from({length:55},()=>({
    x: Math.random()*1200, y: Math.random()*500,
    r: Math.random()*1.4+0.3,
    vx:(Math.random()-.5)*.15, vy:(Math.random()-.5)*.15,
    a: Math.random()*.4+.15,
  }));

  let t = 0;

  function draw(){
    const W=canvas.width, H=canvas.height;
    ctx.clearRect(0,0,W,H);

    /* ─ grid dots ─ */
    for(let x=0;x<W;x+=38)for(let y=0;y<H;y+=38){
      ctx.beginPath(); ctx.arc(x,y,.7,0,Math.PI*2);
      ctx.fillStyle='rgba(255,255,255,.03)'; ctx.fill();
    }

    /* ─ ambient particles ─ */
    particles.forEach(p=>{
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0)p.x=W; if(p.x>W)p.x=0;
      if(p.y<0)p.y=H; if(p.y>H)p.y=0;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(0,200,255,${p.a})`; ctx.fill();
    });

    /* ─ DNA helix ─ */
    const cx  = W/2;
    const amp = Math.min(130, W*0.18);
    const wl  = 190;       // wavelength px
    const N   = 250;
    const y0  = -30, y1 = H+30;
    const dy  = (y1-y0)/N;

    const sA=[], sB=[];
    for(let i=0;i<=N;i++){
      const y   = y0+i*dy;
      const ang = (y/wl)*Math.PI*2 + t;
      sA.push({x:cx+Math.sin(ang)*amp,           y});
      sB.push({x:cx+Math.sin(ang+Math.PI)*amp,   y});
    }

    /* rungs */
    for(let i=0;i<=N;i+=7){
      const a=sA[i],b=sB[i];
      const d=(Math.sin((a.y/wl)*Math.PI*2+t)+1)/2;
      ctx.save();
      ctx.globalAlpha=.05+d*.18;
      ctx.strokeStyle='rgba(0,200,255,.9)';
      ctx.lineWidth=.8; ctx.setLineDash([2,4]);
      ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
      ctx.restore();
    }

    /* strand A – cyan */
    ctx.save();
    const gradA=ctx.createLinearGradient(0,0,0,H);
    gradA.addColorStop(0,'rgba(0,200,255,0)');
    gradA.addColorStop(.2,'rgba(0,200,255,.8)');
    gradA.addColorStop(.8,'rgba(0,200,255,.8)');
    gradA.addColorStop(1,'rgba(0,200,255,0)');
    ctx.beginPath();
    sA.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
    ctx.strokeStyle=gradA; ctx.lineWidth=1.8;
    ctx.shadowBlur=16; ctx.shadowColor='#00c8ff';
    ctx.globalAlpha=.85; ctx.stroke();
    ctx.restore();

    /* strand B – violet */
    ctx.save();
    const gradB=ctx.createLinearGradient(0,0,0,H);
    gradB.addColorStop(0,'rgba(140,80,255,0)');
    gradB.addColorStop(.2,'rgba(140,80,255,.7)');
    gradB.addColorStop(.8,'rgba(140,80,255,.7)');
    gradB.addColorStop(1,'rgba(140,80,255,0)');
    ctx.beginPath();
    sB.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
    ctx.strokeStyle=gradB; ctx.lineWidth=1.8;
    ctx.shadowBlur=16; ctx.shadowColor='#8c50ff';
    ctx.globalAlpha=.8; ctx.stroke();
    ctx.restore();

    /* nodes A */
    for(let i=0;i<=N;i+=7){
      const p=sA[i];
      const d=(Math.sin((p.y/wl)*Math.PI*2+t)+1)/2;
      const r=2+d*2.2;
      ctx.save(); ctx.globalAlpha=.35+d*.65;
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,r*4.5);
      g.addColorStop(0,'rgba(0,200,255,.55)'); g.addColorStop(1,'rgba(0,200,255,0)');
      ctx.beginPath(); ctx.arc(p.x,p.y,r*4.5,0,Math.PI*2);
      ctx.fillStyle=g; ctx.fill();
      ctx.beginPath(); ctx.arc(p.x,p.y,r,0,Math.PI*2);
      ctx.fillStyle='#00c8ff'; ctx.shadowBlur=14; ctx.shadowColor='#00c8ff'; ctx.fill();
      ctx.restore();
    }
    /* nodes B */
    for(let i=0;i<=N;i+=7){
      const p=sB[i];
      const d=(Math.sin((p.y/wl)*Math.PI*2+t+Math.PI)+1)/2;
      const r=2+d*2.2;
      ctx.save(); ctx.globalAlpha=.35+d*.65;
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,r*4.5);
      g.addColorStop(0,'rgba(140,80,255,.55)'); g.addColorStop(1,'rgba(140,80,255,0)');
      ctx.beginPath(); ctx.arc(p.x,p.y,r*4.5,0,Math.PI*2);
      ctx.fillStyle=g; ctx.fill();
      ctx.beginPath(); ctx.arc(p.x,p.y,r,0,Math.PI*2);
      ctx.fillStyle='#8c50ff'; ctx.shadowBlur=14; ctx.shadowColor='#8c50ff'; ctx.fill();
      ctx.restore();
    }
  }

  function loop(){ t+=0.011; draw(); requestAnimationFrame(loop); }
  loop();
})();
</script>
"""

# ─── Anthropic API call ────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a research assistant for the ELL (Endoscopic Lesion Localization) Research System — a prototype exploring spatial localization of ITB (Intestinal Tuberculosis) mucosal lesions in endoscopic imaging.

Answer questions about:
- The research pipeline: CLIP + SAM2, YOLOv8 fine-tuning, explainability layer, late fusion
- Datasets: Kvasir-Capsule (4.7M frames, 47k BBoxes), HyperKvasir, CVC-ClinicDB — real data only, no synthetic
- Medical concepts: ITB vs Crohn's disease, endoscopy, lesion types, granulomas
- Technical methods: zero-shot detection, segmentation, GradCAM, BioBERT, SNOMED-CT mapping

Key facts:
- CLIP uses ViT-L/14, 768-dim embeddings, cosine similarity, no fine-tuning needed
- SAM2 generates dense pixel masks from CLIP attention prompts
- ITB: transverse ulcers at ileocaecal junction | Crohn's: longitudinal ulcers
- Targets: Detection F1 ≥ 0.85, Dice ≥ 0.80, YOLOv8 F1 ≥ 0.91, Multimodal AUC ≥ 0.90
- No synthetic data (professor constraint)

Always clarify: this is a research prototype, not a clinical tool. Never provide medical advice."""


def call_anthropic(messages: list, api_key: str) -> str:
    import urllib.request, json
    body = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": messages,
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]
    except Exception as e:
        err = str(e)
        if "401" in err: return "❌ Invalid API key. Please check your key in the sidebar."
        if "529" in err or "overload" in err.lower(): return "⏳ Claude is busy right now — please try again in a moment."
        return f"❌ Error contacting Claude: {err}"


# ─── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("chat_messages", []),
    ("uploaded_files_list", []),
    ("page", "landing"),
    ("api_key", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
def landing_page():
    # DNA canvas
    st.components.v1.html(DNA_HTML, height=500, scrolling=False)

    # Title overlay (negative margin to sit on top of canvas)
    st.markdown("""
    <div style="margin-top:-440px;position:relative;z-index:10;text-align:center;padding:0 1rem 1rem;">

      <div style="display:inline-flex;align-items:center;gap:.5rem;margin-bottom:1.4rem;
                  background:rgba(0,200,255,.06);border:1px solid rgba(0,200,255,.2);
                  border-radius:999px;padding:.28rem .85rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00c8ff;
                     box-shadow:0 0 8px #00c8ff;display:inline-block;"></span>
        <span style="font-family:monospace;font-size:.65rem;color:#00c8ff;letter-spacing:.14em;">
          ELL RESEARCH SYSTEM &nbsp;·&nbsp; RESEARCH PROTOTYPE &nbsp;·&nbsp; PHASE 1
        </span>
      </div>

      <h1 style="font-size:clamp(2.2rem,5vw,3.8rem);font-weight:800;line-height:1.08;
                 margin-bottom:.7rem;letter-spacing:-.02em;">
        <span style="background:linear-gradient(130deg,#00c8ff 0%,#8c50ff 100%);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                     filter:drop-shadow(0 0 24px rgba(0,200,255,.35));">
          Endoscopic Lesion
        </span><br/>
        <span style="color:#f1f5f9;text-shadow:0 0 40px rgba(0,200,255,.12);">
          Localization
        </span>
      </h1>

      <p style="font-family:monospace;font-size:.78rem;color:#00c8ff;margin-bottom:.55rem;
                text-shadow:0 0 18px rgba(0,200,255,.45);letter-spacing:.06em;">
        CLIP + SAM2 &nbsp;·&nbsp; Zero-Shot Detection &nbsp;·&nbsp; ITB Visual Analysis
      </p>

      <p style="color:#475569;font-size:.85rem;max-width:480px;margin:0 auto 1.6rem;line-height:1.75;">
        An exploratory research interface for visual analysis and spatial
        reasoning in endoscopic imaging datasets.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # CTA buttons
    _, c1, c2, _ = st.columns([1, 1.4, 1.4, 1])
    with c1:
        if st.button("🔬  Enter Research Workspace", use_container_width=True, type="primary"):
            st.session_state.page = "workspace"
            st.rerun()
    with c2:
        if st.button("⎇  View System Architecture", use_container_width=True):
            st.session_state.page = "workspace"
            st.session_state.active_tab = "Workflow"
            st.rerun()

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # Feature cards
    cards = [
        ("🗄️", "Dataset Ingestion", "Upload and organize endoscopic imaging datasets for exploratory analysis."),
        ("👁️", "Visual Exploration", "High-resolution viewing with experimental lesion overlay capabilities."),
        ("⚗️", "Analytical Tools", "Descriptive summaries and compositional analysis of datasets."),
        ("🔬", "Research Context", "Glossary, workflow docs, and conceptual references for ITB research."),
        ("🤖", "CLIP + SAM2 Pipeline", "Zero-shot classification via visual-text embedding and dense segmentation."),
        ("🎯", "Lesion Localization", "Bounding box + segmentation mask overlays with attention heatmaps."),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="card">
              <div style="font-size:1.2rem;margin-bottom:.35rem;">{icon}</div>
              <div style="font-size:.81rem;font-weight:600;color:#e2e8f0;margin-bottom:.28rem;">{title}</div>
              <div style="font-size:.72rem;color:#64748b;line-height:1.6;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center;font-family:monospace;font-size:.6rem;color:#1e293b;margin-top:1.2rem;'>"
        "⚠ For research and educational use only · Not intended for clinical diagnosis or medical decision-making</p>",
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# WORKSPACE
# ══════════════════════════════════════════════════════════════════════════════
def workspace_page():
    with st.sidebar:
        st.markdown("""
        <div style="padding:.3rem 0 .6rem;">
          <div style="display:flex;align-items:center;gap:.45rem;margin-bottom:.9rem;">
            <span style="width:6px;height:6px;border-radius:50%;background:#00c8ff;
                         box-shadow:0 0 6px #00c8ff;display:inline-block;"></span>
            <span style="font-family:monospace;font-size:.65rem;color:#00c8ff;letter-spacing:.12em;">ELL WORKSPACE</span>
          </div>
        </div>""", unsafe_allow_html=True)

        tabs = ["Overview","Dataset","Analysis","Image Explorer","Workflow","Assistant"]
        icons = ["📋","📂","📊","🖼️","⎇","💬"]
        default_tab = getattr(st.session_state, "active_tab", "Overview")
        default_idx = tabs.index(default_tab) if default_tab in tabs else 0

        raw = st.radio("Nav", [f"{icons[i]}  {tabs[i]}" for i in range(len(tabs))],
                       index=default_idx, label_visibility="collapsed")
        active_tab = raw.split("  ",1)[1]

        st.markdown("<hr style='border-color:#1a1a2e;margin:.7rem 0;'>", unsafe_allow_html=True)

        # API key
        st.markdown("<span style='font-family:monospace;font-size:.62rem;color:#00c8ff;letter-spacing:.1em;'>ANTHROPIC API KEY</span>", unsafe_allow_html=True)
        api_in = st.text_input("key", value=st.session_state.api_key, type="password",
                               placeholder="sk-ant-...", label_visibility="collapsed",
                               help="Required for Assistant tab. Get one at console.anthropic.com")
        if api_in != st.session_state.api_key:
            st.session_state.api_key = api_in

        if st.session_state.api_key:
            st.markdown("<span class='badge-active'>● API Key Set</span>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='font-size:.63rem;color:#334155;font-family:monospace;margin-top:.25rem;'>Needed for Assistant tab</p>", unsafe_allow_html=True)

        st.markdown("<hr style='border-color:#1a1a2e;margin:.7rem 0;'>", unsafe_allow_html=True)
        st.markdown("<span class='badge-research'>Research Prototype · Phase 1</span>", unsafe_allow_html=True)
        st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
        if st.button("← Back to Landing"):
            st.session_state.page = "landing"
            if hasattr(st.session_state, "active_tab"):
                del st.session_state.active_tab
            st.rerun()

    dispatch = {
        "Overview": tab_overview, "Dataset": tab_dataset, "Analysis": tab_analysis,
        "Image Explorer": tab_image_explorer, "Workflow": tab_workflow,
        "Assistant": tab_assistant
    }
    dispatch.get(active_tab, tab_overview)()


# ─── OVERVIEW ─────────────────────────────────────────────────────────────────
def tab_overview():
    st.markdown("<span class='section-label'>System Overview</span>", unsafe_allow_html=True)
    st.markdown("""<h2 style='font-size:2rem;font-weight:700;margin:.35rem 0 .55rem;'>
        <span style='background:linear-gradient(135deg,#00c8ff,#8c50ff);
                     -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>Endoscopic Lesion</span>
        <span style='color:#e2e8f0;'> Localization</span></h2>""", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8;max-width:640px;line-height:1.7;font-size:.88rem;margin-bottom:1rem;'>A research prototype for exploring spatial localization patterns in endoscopic imaging datasets. Built on CLIP + SAM2 architecture for zero-shot and few-shot detection of ITB mucosal lesions.</p>", unsafe_allow_html=True)
    st.markdown("<span class='badge-active'>● Active</span> &nbsp;<span class='badge-research'>Research Prototype · Phase 1</span> &nbsp;<span style='font-family:monospace;font-size:.63rem;color:#1e293b;'>CLIP + SAM2 · Unimodal → Multimodal</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    cards = [
        ("🗄️","Dataset Ingestion","Upload and organize endoscopic imaging datasets for exploratory analysis."),
        ("👁️","Visual Exploration","High-resolution viewing with experimental overlay capabilities."),
        ("⚗️","Analytical Tools","Descriptive summaries and compositional analysis of datasets."),
        ("🔬","Research Context","Glossary, workflow documentation, and conceptual references."),
        ("🤖","CLIP + SAM2 Pipeline","Zero-shot classification with visual-text embedding and dense segmentation."),
        ("🎯","Lesion Localization","Bounding box + segmentation mask overlays with attention heatmaps."),
    ]
    cols = st.columns(3)
    for i,(icon,title,desc) in enumerate(cards):
        with cols[i%3]:
            st.markdown(f"""<div class="card"><div style="font-size:1.1rem;margin-bottom:.35rem;">{icon}</div>
            <div style="font-size:.81rem;font-weight:600;color:#e2e8f0;margin-bottom:.28rem;">{title}</div>
            <div style="font-size:.72rem;color:#64748b;line-height:1.6;">{desc}</div></div>""", unsafe_allow_html=True)

    st.markdown("""<div class="glow-card" style="margin-top:.5rem;">
    <div style="display:flex;align-items:center;gap:.5rem;margin-bottom:.4rem;">
        <span>🎯</span><span style="font-size:.77rem;font-weight:600;color:#e2e8f0;">Key Research Differential</span>
    </div>
    <p style="font-size:.76rem;color:#94a3b8;line-height:1.7;margin:0;">
        ITB shows <strong style='color:#00c8ff;'>transverse ulcers</strong> at the ileocaecal junction.
        Crohn's disease shows <strong style='color:#8c50ff;'>longitudinal ulcers</strong>.
        The model must learn orientation-sensitive features to distinguish between these conditions.
    </p></div>""", unsafe_allow_html=True)
    st.markdown("""<div style="background:rgba(0,200,255,.03);border-left:3px solid rgba(0,200,255,.22);
    border-radius:0 8px 8px 0;padding:.7rem 1rem;margin-top:.4rem;">
    <p style="font-family:monospace;font-size:.68rem;color:#334155;margin:0;line-height:1.7;">
    ⚠ Research prototype for exploratory analysis only. Not intended for clinical diagnosis or medical decision-making.</p></div>""", unsafe_allow_html=True)


# ─── DATASET ──────────────────────────────────────────────────────────────────
def tab_dataset():
    st.markdown("<span class='section-label'>Dataset Management</span>", unsafe_allow_html=True)
    st.markdown("## Upload & Organize")
    st.markdown("<p style='color:#94a3b8;font-size:.86rem;'>Ingest imaging datasets and structured files for exploration and analysis.</p>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Files", accept_multiple_files=True,
                                type=["jpg","jpeg","png","json","csv","zip"], label_visibility="collapsed")
    if uploaded:
        for f in uploaded:
            entry = {"name":f.name,"size":f.size,"time":datetime.now().strftime("%H:%M:%S")}
            if not any(e["name"]==f.name for e in st.session_state.uploaded_files_list):
                st.session_state.uploaded_files_list.append(entry)

    if st.session_state.uploaded_files_list:
        st.markdown(f"<div style='font-family:monospace;font-size:.68rem;color:#64748b;margin-bottom:.4rem;'>{len(st.session_state.uploaded_files_list)} file(s) loaded</div>", unsafe_allow_html=True)
        for i,f in enumerate(st.session_state.uploaded_files_list):
            sz = f"{f['size']} B" if f["size"]<1024 else f"{f['size']/1024:.1f} KB" if f["size"]<1048576 else f"{f['size']/1048576:.1f} MB"
            c1,c2,c3,c4 = st.columns([4,1.2,1.2,.5])
            with c1: st.markdown(f"<span style='font-size:.81rem;color:#e2e8f0;'>{f['name']}</span>", unsafe_allow_html=True)
            with c2: st.markdown(f"<span style='font-family:monospace;font-size:.7rem;color:#64748b;'>{sz}</span>", unsafe_allow_html=True)
            with c3: st.markdown(f"<span style='font-family:monospace;font-size:.68rem;color:#475569;'>{f['time']}</span>", unsafe_allow_html=True)
            with c4:
                if st.button("✕",key=f"del_{i}"):
                    st.session_state.uploaded_files_list.pop(i); st.rerun()
            st.divider()
    else:
        st.markdown("""<div class="drop-zone"><div style='font-size:1.8rem;margin-bottom:.4rem;'>📁</div>
        <p style='font-size:.83rem;font-weight:500;color:#94a3b8;margin-bottom:.2rem;'>No files loaded</p>
        <p style='font-size:.73rem;color:#475569;'>Supports JPG, PNG, JSON, CSV, ZIP</p></div>""", unsafe_allow_html=True)


# ─── ANALYSIS ─────────────────────────────────────────────────────────────────
def tab_analysis():
    st.markdown("<span class='section-label'>Analysis Dashboard</span>", unsafe_allow_html=True)
    st.markdown("## Dataset Analytics")
    c1,c2,c3,c4 = st.columns(4)
    for col,label,val,sub in [(c1,"Total Files","—","No dataset loaded"),(c2,"Images","—","Upload to populate"),(c3,"Annotations","—","Awaiting data"),(c4,"Avg. Resolution","—","Pending analysis")]:
        with col:
            st.markdown(f"""<div class="stat-card"><div class="stat-label">{label}</div>
            <div class="stat-val">{val}</div><div class="stat-sub">{sub}</div></div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    ca,cb = st.columns(2)
    for col,icon,title,msg in [(ca,"📊","File Type Distribution","Upload a dataset to view distribution"),(cb,"🗄️","Dataset Composition","No composition data available")]:
        with col:
            st.markdown(f"""<div class="card" style="height:200px;display:flex;flex-direction:column;
            align-items:center;justify-content:center;text-align:center;">
            <div style='font-size:1.8rem;opacity:.22;margin-bottom:.5rem;'>{icon}</div>
            <div style='font-size:.76rem;font-weight:600;color:#64748b;margin-bottom:.25rem;'>{title}</div>
            <div style='font-family:monospace;font-size:.65rem;color:#334155;'>{msg}</div></div>""", unsafe_allow_html=True)


# ─── IMAGE EXPLORER ───────────────────────────────────────────────────────────
def tab_image_explorer():
    st.markdown("<span class='section-label'>Visual Analysis</span>", unsafe_allow_html=True)
    st.markdown("## Image Explorer")
    img_file = st.file_uploader("Image", type=["jpg","jpeg","png"], label_visibility="collapsed")
    if img_file:
        c1,c2 = st.columns([2,1])
        with c1: st.image(img_file, caption=img_file.name, use_container_width=True)
        with c2:
            st.markdown(f"""<div class="card"><b style='color:#e2e8f0;'>File Info</b><br><br>
            <span style='font-family:monospace;font-size:.73rem;color:#64748b;'>
            Name: {img_file.name}<br>Size: {img_file.size/1024:.1f} KB<br>Type: {img_file.type}
            </span></div>""", unsafe_allow_html=True)
            st.markdown("""<div class="card"><div style='font-size:.77rem;font-weight:600;color:#e2e8f0;margin-bottom:.35rem;'>🎯 Overlay Controls</div>
            <p style='font-size:.7rem;color:#475569;line-height:1.6;'>Bounding box + segmentation overlays require the CLIP+SAM2 backend (Phase 2).</p></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="drop-zone" style='height:280px;display:flex;flex-direction:column;
        align-items:center;justify-content:center;'>
        <div style='font-size:2.2rem;margin-bottom:.6rem;'>🖼️</div>
        <p style='font-size:.85rem;font-weight:500;color:#64748b;'>No image loaded</p>
        <p style='font-size:.72rem;color:#334155;'>Upload a JPG or PNG frame to begin</p></div>""", unsafe_allow_html=True)


# ─── WORKFLOW ─────────────────────────────────────────────────────────────────
def tab_workflow():
    st.markdown("<span class='section-label'>Architecture</span>", unsafe_allow_html=True)
    st.markdown("## Research Pipeline & Architecture")
    st.markdown("<p style='color:#94a3b8;font-size:.86rem;'>CLIP + SAM2 · Unimodal → Multimodal · Zero / Few-Shot · No Synthetic Data</p>", unsafe_allow_html=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<a href="https://itbworkflow.vercel.app" target="_blank" style="text-decoration:none;">
        <div class="glow-card" style="cursor:pointer;display:flex;align-items:center;justify-content:space-between;">
        <div style="display:flex;align-items:center;gap:.7rem;"><span style="font-size:1.2rem;">⎇</span>
        <div><div style="font-size:.8rem;font-weight:600;color:#e2e8f0;">Interactive System Workflow</div>
        <div style="font-family:monospace;font-size:.66rem;color:#64748b;margin-top:.15rem;">Full pipeline flowchart →</div></div>
        </div><span style="color:#64748b;">↗</span></div></a>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="glow-card" style="display:flex;align-items:center;justify-content:space-between;">
        <div style="display:flex;align-items:center;gap:.7rem;"><span style="font-size:1.2rem;">📅</span>
        <div><div style="font-size:.8rem;font-weight:600;color:#e2e8f0;">Gantt Chart — Project Timeline</div>
        <div style="font-family:monospace;font-size:.66rem;color:#64748b;margin-top:.15rem;">Milestones & schedule</div></div>
        </div><span style="color:#334155;">↗</span></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.7rem'></div>", unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    for col,val,lbl,wk in [(m1,"≥ 0.85","Detection F1","Week 1"),(m2,"≥ 0.80","Seg. Dice","Week 2"),(m3,"≥ 0.91","YOLOv8 F1","Week 3"),(m4,"≥ 0.90","Multimodal AUC","Week 4")]:
        with col:
            st.markdown(f"""<div class="metric-pill"><div class="metric-val">{val}</div>
            <div class="metric-lbl">{lbl}</div><div class="metric-wk">{wk}</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:.9rem'></div>", unsafe_allow_html=True)
    st.markdown("<span class='section-label'>8-Stage Research Pipeline</span>", unsafe_allow_html=True)
    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    pipeline = [
        ("01","Multimodal Data Sources","Data Collection",True,
         "Starting unimodal · Endoscopy-first · Real data only — no synthetic",
         ["Colonoscopy / Capsule — Kvasir-Capsule 4.7M frames · 47k BBoxes",
          "CT Enterography — Cross-sectional imaging, wall thickening, stricture",
          "Histopathology — Whole-slide images, caseating granulomas",
          "Clinical Text — TB contact history, symptom chronology"]),
        ("02","Modality-Specific Preprocessing","Preprocessing",True,
         "Normalization · Augmentation · Standardization",
         ["Endoscopy — CLAHE + specularity masking + elastic deformation",
          "CT — HU windowing W:400 L:50 · 3–5mm slice standardization",
          "Histology — 256×256 tiling at 20× magnification",
          "Clinical Text — SNOMED-CT term mapping + negation resolution"]),
        ("03","CLIP Encoder — Zero-Shot Classification","Phase 1",True,
         "openai/clip-vit-large-patch14 · 768-dim visual embedding · No fine-tuning",
         ["ViT-L/14 backbone — 768-dim embedding",
          "Zero-shot image-text cosine similarity",
          "ITB-specific text prompts for lesion detection",
          "Decision Gate — Confidence ≥ θ (default 0.25)"]),
        ("04","SAM2 — Segment Anything Model 2","Phase 2",False,
         "facebook/sam2-hiera-large · Dense segmentation mask + bounding box overlay",
         ["CLIP → SAM2 bridge via attention map point prompts",
          "Dense pixel-wise mask + multi-granularity output",
          "NMS + mask refinement + temperature scaling",
          "Decision Gate — Detection F1 ≥ 0.85"]),
        ("05","YOLOv8 Fine-Tuning","Phase 3",False,
         "Manual gastroenterologist labels · Frozen CLIP backbone · Crohn's as hard negatives",
         ["Image-level binary labels — cheapest annotation strategy",
          "Orientation-aware loss: transverse vs longitudinal ulcers",
          "Real samples only: Kvasir-Capsule · HyperKvasir",
          "Target: Fine-Tuned F1 ≥ 0.91"]),
        ("06","Explainability Layer","Phase 4",False,
         "GradCAM heatmaps · Molmo visual reasoning · BioBERT structured report",
         ["GradCAM / Attention Rollout — heatmap overlay on frames",
          "Molmo (allenai/molmo-7b-d) — visual QA + reasoning",
          "BioBERT — structured clinical report generation",
          "Verify model attends to lesion features, not artifacts"]),
        ("07","Late Fusion — Cross-Modal Attention","Multimodal",False,
         "Missing modality tolerant · Quality-aware weighting · Phased upgrade",
         ["Phase 1: Score-level logistic fusion — robust for <200 patients",
          "Phase 2: Embedding-level attention — upgrade at 200+ patients",
          "Quality-aware modality weighting",
          "Endoscopy + CT + WSI + Text → Fused embedding"]),
        ("08","Output & Explainability","Outputs",False,
         "Calibrated · Localized · Actionable research decision support",
         ["Lesion Localization — BBox + seg. mask overlays",
          "ITB Suspicion Score — Calibrated patient-level probability",
          "Modality Attribution — Per-modality attention weights",
          "Three-tier threshold: Low / Moderate / High"]),
    ]

    for bid,title,phase,active,desc,details in pipeline:
        badge = "<span class='badge-active' style='font-size:.58rem;'>● Active</span>" if active else "<span class='badge-planned'>Planned</span>"
        dh = "".join(f"<div style='display:flex;align-items:flex-start;gap:.35rem;margin-bottom:.18rem;'><span style='width:4px;height:4px;border-radius:50%;background:rgba(0,200,255,.35);margin-top:.45rem;flex-shrink:0;display:inline-block;'></span><span style='font-size:.68rem;color:#475569;line-height:1.5;'>{d}</span></div>" for d in details)
        st.markdown(f"""<div class="pipe-block">
        <div style="display:flex;align-items:flex-start;gap:.7rem;">
            <div style="flex-shrink:0;"><div style="background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);border-radius:6px;padding:.35rem .5rem;font-size:.68rem;color:#00c8ff;font-family:monospace;">{bid}</div></div>
            <div style="flex:1;">
                <div style="display:flex;align-items:center;flex-wrap:wrap;gap:.35rem;margin-bottom:.28rem;">
                    <span style="font-size:.8rem;font-weight:600;color:#e2e8f0;">{title}</span>
                    {badge}
                    <span style="font-family:monospace;font-size:.58rem;color:rgba(0,200,255,.32);">{phase}</span>
                </div>
                <p style="font-size:.71rem;color:#64748b;margin-bottom:.4rem;line-height:1.5;">{desc}</p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:.1rem .4rem;">{dh}</div>
            </div>
        </div></div>""", unsafe_allow_html=True)
        if bid != "08":
            st.markdown("<div class='pipe-connector'></div>", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(0,200,255,.02);border-left:2px solid rgba(0,200,255,.18);
    border-radius:0 8px 8px 0;padding:.6rem .9rem;margin-top:.4rem;">
    <p style="font-family:monospace;font-size:.65rem;color:#1e293b;margin:0;line-height:1.6;">
    ⚠ No synthetic data — professor constraint. Real Kvasir-Capsule / HyperKvasir / CVC-ClinicDB samples only.</p></div>""", unsafe_allow_html=True)


# ─── ASSISTANT ────────────────────────────────────────────────────────────────
def tab_assistant():
    st.markdown("<span class='section-label'>Research Assistant</span>", unsafe_allow_html=True)
    st.markdown("## AI Chat")

    if not st.session_state.api_key:
        st.markdown("""<div class="glow-card" style="text-align:center;padding:2.5rem 1rem;">
        <div style="font-size:2.5rem;margin-bottom:.7rem;">🔑</div>
        <p style="font-size:.88rem;font-weight:600;color:#e2e8f0;margin-bottom:.4rem;">Anthropic API Key Required</p>
        <p style="font-size:.76rem;color:#64748b;line-height:1.65;max-width:380px;margin:0 auto;">
            Enter your key in the <strong style='color:#00c8ff;'>sidebar</strong> to enable the AI assistant.
            Get one free at <strong style='color:#00c8ff;'>console.anthropic.com</strong>
        </p></div>""", unsafe_allow_html=True)
        return

    st.markdown("<p style='color:#64748b;font-size:.83rem;margin-bottom:.8rem;'>Powered by Claude · Ask anything about ELL, ITB, CLIP+SAM2, or the research pipeline.</p>", unsafe_allow_html=True)

    # Suggested prompts
    if not st.session_state.chat_messages:
        st.markdown("**Suggested questions:**")
        suggestions = [
            "What is CLIP + SAM2?",
            "Explain the research pipeline",
            "ITB vs Crohn's disease differences",
            "How does zero-shot detection work?",
            "What datasets are used?",
            "Explain GradCAM and explainability",
        ]
        cols = st.columns(3)
        for i, s in enumerate(suggestions):
            with cols[i % 3]:
                if st.button(s, key=f"sugg_{i}", use_container_width=True):
                    st.session_state.chat_messages.append({"role":"user","content":s})
                    with st.spinner("Claude is thinking..."):
                        resp = call_anthropic(st.session_state.chat_messages, st.session_state.api_key)
                    st.session_state.chat_messages.append({"role":"assistant","content":resp})
                    st.rerun()
        st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)

    # Chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message("user" if msg["role"]=="user" else "assistant", avatar=None if msg["role"]=="user" else "🔬"):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Ask about ITB, CLIP+SAM2, the pipeline, datasets...")
    if user_input:
        st.session_state.chat_messages.append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant", avatar="🔬"):
            with st.spinner("Claude is thinking..."):
                resp = call_anthropic(st.session_state.chat_messages, st.session_state.api_key)
            st.markdown(resp)
        st.session_state.chat_messages.append({"role":"assistant","content":resp})

    if st.session_state.chat_messages:
        if st.button("🗑️ Clear conversation"):
            st.session_state.chat_messages = []
            st.rerun()

    st.markdown("<p style='font-family:monospace;font-size:.6rem;color:#1e293b;text-align:center;margin-top:.4rem;'>Research exploration only · No medical advice · Powered by Claude</p>", unsafe_allow_html=True)

# ─── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == "landing":
    landing_page()
else:
    workspace_page()
