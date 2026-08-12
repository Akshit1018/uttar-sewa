export const PRACTICE_KEY = 'uttar_sewa_practice';
export const SETTINGS_KEY = 'uttar_sewa_settings';

export const NAMED_MALAS = [
  { id: 'ram', name_hi: 'राम राम', name_en: 'Ram Ram' },
  { id: 'hare_krishna', name_hi: 'हरे कृष्ण', name_en: 'Hare Krishna' },
  { id: 'om', name_hi: 'ॐ', name_en: 'Om' },
];

export function defaultPractice() {
  return {
    mantraId: 'ram',
    beadsPerCycle: 108,
    sandhya: true,
    japaFocus: false,
  };
}

export function defaultSettings() {
  return {
    notifications: true,
    autoDownload: false,
    darkMode: true,
  };
}

export function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return fallback;
    return { ...fallback, ...JSON.parse(raw) };
  } catch (error) {
    return fallback;
  }
}

export function writeJson(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    // private mode
  }
}

export function readPractice() {
  return readJson(PRACTICE_KEY, defaultPractice());
}

export function writePractice(value) {
  writeJson(PRACTICE_KEY, { ...defaultPractice(), ...value });
}

export function readSettings() {
  return readJson(SETTINGS_KEY, defaultSettings());
}

export function writeSettings(value) {
  writeJson(SETTINGS_KEY, { ...defaultSettings(), ...value });
}

export function mantraLabel(mantraId, language) {
  const found = NAMED_MALAS.find((item) => item.id === mantraId) || NAMED_MALAS[0];
  return language === 'hi' ? found.name_hi : found.name_en;
}

export function formatShareCard({ question, answer, timestampUrl }) {
  const parts = [String(question || '').trim(), String(answer || '').trim().slice(0, 220)];
  if (timestampUrl) parts.push(String(timestampUrl).trim());
  return parts.filter(Boolean).join('\n\n');
}

export async function shareCard(payload) {
  const text = formatShareCard(payload);
  if (navigator.share) {
    await navigator.share({ title: 'Uttar Sewa', text });
    return 'shared';
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    await navigator.clipboard.writeText(text);
    return 'copied';
  }
  return 'unsupported';
}

export function nextSandhya(now = new Date()) {
  const morning = new Date(now);
  morning.setHours(6, 0, 0, 0);
  const evening = new Date(now);
  evening.setHours(18, 0, 0, 0);
  if (now < morning) return { kind: 'morning', at: morning };
  if (now < evening) return { kind: 'evening', at: evening };
  const nextMorning = new Date(morning);
  nextMorning.setDate(nextMorning.getDate() + 1);
  return { kind: 'morning', at: nextMorning };
}

export function msUntil(date, now = new Date()) {
  return Math.max(0, date.getTime() - now.getTime());
}

export function readLocalPracticeStats() {
  let favorites = 0;
  let searches = 0;
  let beads = 0;
  try {
    favorites = JSON.parse(localStorage.getItem('spiritual_qa_favorites') || '[]').length;
    searches = JSON.parse(localStorage.getItem('spiritual_qa_search_history') || '[]').length;
    for (let index = 0; index < localStorage.length; index += 1) {
      const key = localStorage.key(index);
      if (key && key.startsWith('uttar_sewa_mala_')) {
        const state = JSON.parse(localStorage.getItem(key) || '{}');
        beads += Number(state.beads_today || 0);
      }
    }
  } catch (error) {
    // ignore
  }
  return { favorites, searches, beads };
}
