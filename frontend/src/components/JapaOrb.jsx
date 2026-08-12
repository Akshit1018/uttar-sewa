import React, { useEffect, useRef, useState } from 'react';
import { HOLD_MS, DRAG_THRESHOLD_PX, DOUBLE_TAP_MS, progressLabel, resolveBeadsPerCycle, snapToRightOffset } from '../lib/mala';

const HAND_KEY = 'uttar_sewa_orb_hand';

const JapaOrb = ({ language, state, onTap, onHold, onUndo }) => {
  const pointer = useRef({ x: 0, y: 0, started: 0, dragging: false, lastTap: 0 });
  const [position, setPosition] = useState({ x: 20, y: null });
  const [idle, setIdle] = useState(false);
  const holdTimer = useRef(null);
  const idleTimer = useRef(null);

  const label = language === 'hi' ? 'माला' : 'Mala';
  const countLabel = progressLabel(state);

  useEffect(() => {
    try {
      const hand = localStorage.getItem(HAND_KEY) || 'right';
      const width = window.innerWidth || 360;
      setPosition((current) => ({
        ...current,
        x: hand === 'left' ? snapToRightOffset(width, width) : 20,
      }));
    } catch (error) {
      // ignore
    }
  }, []);

  const bumpIdle = () => {
    setIdle(false);
    if (idleTimer.current) clearTimeout(idleTimer.current);
    idleTimer.current = setTimeout(() => setIdle(true), 2500);
  };

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
    bumpIdle();
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

  const fallbackBottom = () => {
    const tab = document.querySelector('.app-tabbar');
    const tabHeight = tab && tab.offsetParent !== null ? tab.getBoundingClientRect().height : 0;
    return tabHeight + 16;
  };

  const onPointerMove = (event) => {
    const dx = event.clientX - pointer.current.x;
    const dy = event.clientY - pointer.current.y;
    if (Math.hypot(dx, dy) > DRAG_THRESHOLD_PX) {
      pointer.current.dragging = true;
      clearHold();
      bumpIdle();
      setPosition((current) => ({
        x: Math.max(8, current.x - dx),
        y: Math.max(8, (current.y ?? fallbackBottom()) - dy),
      }));
      pointer.current.x = event.clientX;
      pointer.current.y = event.clientY;
    }
  };

  const onPointerUp = () => {
    const heldFor = Date.now() - pointer.current.started;
    const wasHold = !holdTimer.current && heldFor >= HOLD_MS;
    clearHold();
    bumpIdle();
    if (pointer.current.dragging) {
      setPosition((current) => ({
        ...current,
        x: snapToRightOffset(current.x, window.innerWidth || 360),
      }));
      return;
    }
    if (wasHold) {
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
    const cycle = resolveBeadsPerCycle(state);
    const nextHint = (state.current_in_cycle || 0) + 1;
    onTap();
    haptic(nextHint >= cycle ? [20, 40, 40] : 10);
  };

  return (
    <button
      type="button"
      aria-label={`${label} ${countLabel}. ${language === 'hi' ? 'टैप मनका, देर दबाएँ प्रश्न' : 'Tap for a bead, hold to ask'}`}
      onPointerDown={onPointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={onPointerUp}
      onPointerCancel={clearHold}
      className={`japa-orb${idle ? ' japa-orb-idle' : ''}`}
      style={{
        right: position.x,
        ...(position.y != null ? { bottom: position.y } : {}),
      }}
    >
      <span className="japa-orb-count">{state.current_in_cycle || 0}</span>
      <span className="japa-orb-label">{label}</span>
      {state.completed_cycle ? (
        <span className="japa-orb-cycle">{resolveBeadsPerCycle(state)}</span>
      ) : null}
    </button>
  );
};

export default JapaOrb;
