import { useCallback, useEffect, useState } from 'react';
import { applyTap, applyUndo, emptyMalaState } from '../lib/mala';

const dayKey = () => {
  const now = new Date();
  const stamp = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
  return `uttar_sewa_mala_${stamp}`;
};

const readState = () => {
  try {
    const raw = localStorage.getItem(dayKey());
    if (!raw) return emptyMalaState();
    return { ...emptyMalaState(), ...JSON.parse(raw) };
  } catch (error) {
    return emptyMalaState();
  }
};

const writeState = (state) => {
  try {
    localStorage.setItem(dayKey(), JSON.stringify(state));
  } catch (error) {
    // private mode
  }
};

export const useMala = () => {
  const [state, setState] = useState(emptyMalaState);

  useEffect(() => {
    setState(readState());
  }, []);

  const commit = useCallback((next) => {
    writeState(next);
    setState(next);
    return next;
  }, []);

  const tap = useCallback(() => commit(applyTap(readState())), [commit]);
  const undo = useCallback(() => commit(applyUndo(readState())), [commit]);
  const recordQuestion = useCallback(() => {
    const current = readState();
    return commit({ ...current, questions_today: (current.questions_today || 0) + 1 });
  }, [commit]);

  return { state, tap, undo, recordQuestion };
};
