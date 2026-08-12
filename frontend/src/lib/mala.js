export const BEADS_PER_CYCLE = 108;
export const HOLD_MS = 2500;
export const DRAG_THRESHOLD_PX = 12;
export const DOUBLE_TAP_MS = 320;

export function emptyMalaState() {
  return {
    beads_today: 0,
    cycles_today: 0,
    current_in_cycle: 0,
    questions_today: 0,
    completed_cycle: false,
  };
}

export function applyTap(state) {
  const next = { ...(state || emptyMalaState()) };
  next.beads_today = (next.beads_today || 0) + 1;
  next.current_in_cycle = (next.current_in_cycle || 0) + 1;
  next.completed_cycle = false;
  if (next.current_in_cycle >= BEADS_PER_CYCLE) {
    next.cycles_today = (next.cycles_today || 0) + 1;
    next.current_in_cycle = 0;
    next.completed_cycle = true;
  }
  return next;
}

export function applyUndo(state) {
  const next = { ...(state || emptyMalaState()) };
  const beads = next.beads_today || 0;
  const current = next.current_in_cycle || 0;
  const cycles = next.cycles_today || 0;
  if (beads <= 0) return next;
  if (current === 0 && cycles > 0) {
    next.cycles_today = cycles - 1;
    next.current_in_cycle = BEADS_PER_CYCLE - 1;
  } else {
    next.current_in_cycle = Math.max(0, current - 1);
  }
  next.beads_today = beads - 1;
  next.completed_cycle = false;
  return next;
}

export function progressLabel(state) {
  const current = (state && state.current_in_cycle) || 0;
  return `${current}/${BEADS_PER_CYCLE}`;
}

export function snapToRightOffset(currentRight, viewportWidth, orbSize = 72, margin = 16) {
  const width = viewportWidth || 360;
  const centerFromRight = (currentRight || 0) + orbSize / 2;
  const onRightHalf = centerFromRight < width / 2;
  return onRightHalf ? margin : Math.max(margin, width - orbSize - margin);
}

export function sankalpaRemaining(malasToday, vowMalas) {
  const vow = Math.max(0, Number(vowMalas) || 0);
  const done = Math.max(0, Number(malasToday) || 0);
  return Math.max(0, vow - done);
}

