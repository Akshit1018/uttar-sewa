import { useCallback, useEffect, useState } from 'react';
import { applyTap, applyUndo, emptyMalaState } from '../lib/mala';
import { readPractice } from '../lib/practice';
import { notificationService } from '../services/notificationService';

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
