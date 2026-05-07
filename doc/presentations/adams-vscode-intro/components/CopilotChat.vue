<template>
  <div class="chat-panel flex flex-col" style="height: 100%">
    <div class="chat-header">
      <span class="icon">⚙</span> GitHub Copilot &nbsp;<span class="dim session-title">Python script for wind turbine model</span>
    </div>
    <div class="chat-body flex-1 flex flex-col gap-3 pr-1">

      <div class="chat-msg user">
        <code>/adams-python-model-builder</code> Create a Python script in <code>agent_demo/</code> that builds a wind turbine. Use geometry elements. For the blades, use Adams beams + rigid parts to model flexibility with a discretized approach. Define constants at the top.
      </div>

      <div class="chat-msg assistant">
        <div class="chat-tool-call">📖 Read <span class="filepath">skills/adams-python-model-builder/references/api-classes/forces.md</span></div>
        <div class="chat-tool-call">📖 Read <span class="filepath">assets/python_scripts/parametric_chain.py</span></div>
        <div class="mt-1 plan-label">Plan: Wind Turbine Adams Python Model</div>
        <div class="plan-item">Tower (frustum on ground), Nacelle (Fixed to tower top), Hub (Revolute + JointMotion at 12 RPM)</div>
        <div class="plan-item">3 blades × 8 segments — Beam force elements between rigid parts</div>
        <div class="plan-item">Constants: tower 80 m, blade 40 m, GFRP material properties</div>
      </div>

      <div class="chat-msg user">
        Proceed. When done, use the Adams MCP server to run it. Build only first — no simulation yet.
      </div>

      <div class="chat-msg assistant">
        <div class="chat-tool-call">✏️ Created <span class="filepath">test/files/agent_demo/wind_turbine.py</span></div>
        <div class="chat-tool-call">🔧 <code>adams_run_batch</code> <span class="dim">— wind_turbine.py</span></div>
        <div class="chat-tool-call">🔧 <code>adams_batch_status</code> <span class="ok">✓ exit 0</span></div>
        <div class="mt-1">Model built cleanly. Fixed one issue: non-ASCII characters in comments caused a <code>UnicodeDecodeError</code> — Adams reads source files as cp1252. Replaced all Unicode with ASCII equivalents.</div>
      </div>

      <div class="chat-msg user">
        The model <em>looks</em> correct, but as soon as you simulate, all the blade elements fly off. Looking at the beam elements graphically, the I-beam symbol should be in the cross-section plane.
      </div>

      <div class="chat-msg assistant">
        <div class="mt-1">Root cause: beam markers were coincident — both endpoints at the same radial position. Adams computed 100% compression → explosive preload. Fix: connect <code>prev_in_mkr → in_mkr</code> so they are physically SEG_LEN apart.</div>
        <div class="chat-tool-call">✏️ Fixed beam connectivity in <span class="filepath">wind_turbine.py</span></div>
        <div class="chat-tool-call">🔧 <code>adams_run_batch</code> <span class="ok">✓ Simulation successful (4.2s)</span></div>
      </div>

      <div class="chat-msg user">
        It still won't solve. Look at the beam info vs yours — your modulus is 10× too low and your shear ratios are zero.
      </div>

      <div class="chat-msg assistant">
        <div class="mt-1">Found it: <code>createBeam()</code> silently drops <code>y_shear_ratio</code>/<code>z_shear_ratio</code> — zero shear area = singular beams. Switching to CMD bridge: <code>Adams.execute_cmd('force create element_like beam ...')</code></div>
      </div>

      <div class="chat-msg user">
        It's <code>y_shear_area_ratio</code>, not <code>y_shear_ratio</code>.
      </div>

      <div class="chat-msg assistant">
        <div class="chat-tool-call">✏️ Fixed parameter name → <code>y_shear_area_ratio = 1.0</code></div>
        <div class="chat-tool-call">🔧 <code>adams_run_batch</code></div>
      </div>

      <div class="chat-msg user">
        I ran a model verify — all beams report: <em>"The X distance from J→I is −5000. It must be positive."</em>
      </div>

      <div class="chat-msg assistant">
        <div class="mt-1">Adams Beam requires I to be the <strong>outboard</strong> end. Swapping I and J in every <code>create_beam</code> call.</div>
        <div class="chat-tool-call">✏️ Swapped i_marker ↔ j_marker</div>
        <div class="chat-tool-call">🔧 <code>adams_run_batch</code> <span class="ok">✓ Simulation successful — 10 s, 1.4s wall time</span></div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.chat-panel {
  background: rgba(15, 15, 30, 0.85);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  overflow: hidden;
}
.chat-header {
  background: rgba(99,102,241,0.15);
  border-bottom: 1px solid rgba(255,255,255,0.08);
  padding: 0.4rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #a5b4fc;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.chat-body {
  padding: 0.6rem 0.75rem;
  font-size: 0.7rem;
  overflow-y: auto;
}
.chat-msg {
  padding: 0.45rem 0.6rem;
  border-radius: 8px;
  line-height: 1.5;
}
.chat-msg.user {
  background: rgba(99,102,241,0.2);
  border: 1px solid rgba(99,102,241,0.3);
  color: #e0e7ff;
  margin-left: 10%;
}
.chat-msg.assistant {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  color: #cbd5e1;
  margin-right: 5%;
}
.chat-tool-call {
  font-size: 0.63rem;
  color: rgba(255,255,255,0.45);
  padding: 0.1rem 0;
}
.dim { color: rgba(255,255,255,0.3); }
.session-title { font-size: 0.65rem; font-weight: 400; }
.ok { color: #86efac; }
.filepath { color: #93c5fd; font-style: italic; }
.plan-label { font-weight: 600; color: #a5b4fc; margin-top: 0.25rem; margin-bottom: 0.15rem; }
.plan-item { font-size: 0.63rem; color: rgba(255,255,255,0.5); padding-left: 0.8rem; padding-bottom: 0.1rem; }
.plan-item::before { content: "• "; }
.highlight { color: #86efac; }
.mt-1 { margin-top: 0.35rem; }
</style>
