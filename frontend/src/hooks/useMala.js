import { useCallback, useEffect, useState } from 'react';
import { applyTap, applyUndo, emptyMalaState } from '../lib/mala';
import { readPractice } from '../lib/practice';
import { notificationService } from '../services/notificationService';
import { API } from '../lib/backend';

const dayStamp = () => {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
};

const storageKey = (mantraId) => `uttar_sewa_mala_${dayStamp()}_${mantraId || 'ram'}`;
const legacyKey = () => `uttar_sewa_mala_${dayStamp()}`;

const readState = (mantraId, beadsPerCycle) => {
  try {
    const raw = localStorage.getItem(storageKey(mantraId)) || localStorage.getItem(legacyKey());
    if (!raw) {
      return { ...emptyMalaState(), mantra_id: mantraId, beads_per_cycle: beadsPerCycle };
    }
    const parsed = {
      ...emptyMalaState(),
      ...JSON.parse(raw),
      mantra_id: mantraId,
      beads_per_cycle: beadsPerCycle,
    };
    if (parsed.current_in_cycle >= beadsPerCycle) {
      parsed.current_in_cycle = Math.max(0, beadsPerCycle - 1);
    }
    return parsed;
  } catch (error) {
    return { ...emptyMalaState(), mantra_id: mantraId, beads_per_cycle: beadsPerCycle };
  }
};

const writeState = (mantraId, state) => {
  try {
    localStorage.setItem(storageKey(mantraId), JSON.stringify(state));
  } catch (error) {
    // private mode
  }
};

const deviceId = () => {
  try {
    let id = localStorage.getItem('uttar_sewa_device_id');
    if (!id) {
      id = `pwa-${Date.now()}`;
      localStorage.setItem('uttar_sewa_device_id', id);
    }
    return id;
  } catch (error) {
    return 'pwa-anonymous';
  }
};

const syncMala = (state) => {
  fetch(`${API}/mala/sync`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      device_id: deviceId(),
      day: dayStamp(),
      mantra_id: state.mantra_id || 'ram',
      beads_today: state.beads_today || 0,
      cycles_today: state.cycles_today || 0,
      current_in_cycle: state.current_in_cycle || 0,
      questions_today: state.questions_today || 0,
      beads_per_cycle: state.beads_per_cycle || 108,
      completed_cycle: !!state.completed_cycle,
    }),
  }).catch(() => null);
};

export const useMala = (language = 'hi') => {
  const [practice, setPractice] = useState(readPractice);
  const [state, setState] = useState(() => readState(practice.mantraId, practice.beadsPerCycle));

  const reload = useCallback(() => {
    const nextPractice = readPractice();
    setPractice(nextPractice);
    setState(readState(nextPractice.mantraId, nextPractice.beadsPerCycle));
  }, []);

  useEffect(() => {
    reload();
    const onStorage = () => reload();
    window.addEventListener('uttar-sewa-practice', onStorage);
    window.addEventListener('storage', onStorage);
    return () => {
      window.removeEventListener('uttar-sewa-practice', onStorage);
      window.removeEventListener('storage', onStorage);
    };
  }, [reload]);

  const commit = useCallback((next) => {
    writeState(next.mantra_id || practice.mantraId, next);
    setState(next);
    syncMala(next);
    return next;
  }, [practice.mantraId]);

  const tap = useCallback(() => {
    const current = readState(practice.mantraId, practice.beadsPerCycle);
    const next = applyTap(current);
    if (next.completed_cycle) {
      notificationService.showMalaCompleteNotification(next.cycles_today, language);
    }
    return commit(next);
  }, [commit, language, practice.beadsPerCycle, practice.mantraId]);

  const undo = useCallback(() => {
    return commit(applyUndo(readState(practice.mantraId, practice.beadsPerCycle)));
  }, [commit, practice.beadsPerCycle, practice.mantraId]);

  const recordQuestion = useCallback(() => {
    const current = readState(practice.mantraId, practice.beadsPerCycle);
    return commit({ ...current, questions_today: (current.questions_today || 0) + 1 });
  }, [commit, practice.beadsPerCycle, practice.mantraId]);

  return { state, tap, undo, recordQuestion, practice, reload };
};
