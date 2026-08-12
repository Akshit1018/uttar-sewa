import React, { useRef, useState } from 'react';
import { HOLD_MS, DRAG_THRESHOLD_PX, DOUBLE_TAP_MS, progressLabel } from '../lib/mala';

const JapaOrb = ({ language, state, onTap, onHold, onUndo }) => {
  const pointer = useRef({ x: 0, y: 0, started: 0, dragging: false, lastTap: 0 });
  const [position, setPosition] = useState({ x: 20, y: 96 });
  const holdTimer = useRef(null);

  const label = language === 'hi' ? 'माला' : 'Mala';
  const countLabel = progressLabel(state);

  const clearHold = () => {
    if (holdTimer.current) {
      clearTimeout(holdTimer.current);
      holdTimer.current = null;
    }
  };

  const haptic = (pattern) => {
    if (navigator.vibrate) {
      navigator.vibrate(pattern);
    }
  };

  const onPointerDown = (event) => {
    event.currentTarget.setPointerCapture(event.pointerId);
    pointer.current = {
      x: event.clientX,
      y: event.clientY,
      started: Date.now(),
      dragging: false,
      lastTap: pointer.current.lastTap,
    };
    holdTimer.current = setTimeout(() => {
      clearHold();
      haptic(30);
      onHold();
    }, HOLD_MS);
  };

  const onPointerMove = (event) => {
    const dx = event.clientX - pointer.current.x;
    const dy = event.clientY - pointer.current.y;
    if (Math.hypot(dx, dy) > DRAG_THRESHOLD_PX) {
      pointer.current.dragging = true;
      clearHold();
      setPosition((current) => ({
        x: Math.max(8, current.x - dx),
        y: Math.max(8, current.y - dy),
      }));
      pointer.current.x = event.clientX;
      pointer.current.y = event.clientY;
    }
  };

  const onPointerUp = () => {
    const heldFor = Date.now() - pointer.current.started;
    const wasHold = !holdTimer.current && heldFor >= HOLD_MS;
    clearHold();
    if (pointer.current.dragging || wasHold) {
      return;
    }
    const now = Date.now();
    if (now - pointer.current.lastTap < DOUBLE_TAP_MS) {
      pointer.current.lastTap = 0;
      onUndo();
      haptic(15);
      return;
    }
    pointer.current.lastTap = now;
    const nextHint = (state.current_in_cycle || 0) + 1;
    onTap();
    haptic(nextHint >= 108 ? [20, 40, 40] : 10);
  };

  return (
    <button
      type="button"
      aria-label={`${label} ${countLabel}`}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={clearHold}
      className="japa-orb"
      style={{ right: position.x, bottom: position.y }}
    >
      <span className="japa-orb-count">{state.current_in_cycle || 0}</span>
      <span className="japa-orb-label">{label}</span>
      {state.completed_cycle ? (
        <span className="japa-orb-cycle">108</span>
      ) : null}
    </button>
  );
};

export default JapaOrb;
