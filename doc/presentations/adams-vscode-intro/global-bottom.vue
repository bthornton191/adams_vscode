<template>
  <div class="abs-footer">
    <img src="/logo.svg" class="cadence-logo" alt="Cadence" />
    <div class="footer-divider" />
    <span class="footer-label">Adams VS Code Extension</span>
  </div>
</template>

<style scoped>
.abs-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 20px;
  pointer-events: none;
  background: linear-gradient(to top, rgba(0,0,0,0.35) 0%, transparent 100%);
}
.cadence-logo {
  height: 14px;
  opacity: 0.55;
  filter: brightness(0) invert(1);
}
.footer-divider {
  width: 1px;
  height: 14px;
  background: rgba(255,255,255,0.25);
}
.footer-label {
  font-size: 11px;
  color: rgba(255,255,255,0.45);
  letter-spacing: 0.04em;
}
</style>
