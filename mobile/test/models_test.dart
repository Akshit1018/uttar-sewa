import 'package:flutter_test/flutter_test.dart';

import 'package:uttar_sewa/models.dart';

void main() {
  test('applyTap completes a cycle of 11 without calling an API', () {
    var state = const MalaState(beadsPerCycle: 11, currentInCycle: 10, beadsToday: 10);
    state = state.applyTap();
    expect(state.beadsToday, 11);
    expect(state.cyclesToday, 1);
    expect(state.currentInCycle, 0);
    expect(state.completedCycle, isTrue);
  });

  test('applyUndo restores the previous bead in a completed cycle', () {
    var state = const MalaState(beadsPerCycle: 11, currentInCycle: 10, beadsToday: 10);
    state = state.applyTap().applyUndo();
    expect(state.beadsToday, 10);
    expect(state.cyclesToday, 0);
    expect(state.currentInCycle, 10);
    expect(state.completedCycle, isFalse);
  });

  test('mala json roundtrip keeps cycle length', () {
    const state = MalaState(beadsToday: 10, beadsPerCycle: 27, mantraId: 'om');
    final copy = MalaState.fromJson(state.toJson());
    expect(copy.beadsToday, 10);
    expect(copy.beadsPerCycle, 27);
    expect(copy.mantraId, 'om');
  });

  test('ask result maps clip-first cards', () {
    final result = AskResult.fromJson({
      'answer': 'जप करें',
      'refused': false,
      'clips': [
        {
          'source_question': 'मन?',
          'source_answer': 'नाम जप',
          'video_id': 'abc',
          'video_title': 'Satsang',
          'start_time': 90,
          'timestamp_url': 'https://www.youtube.com/watch?v=abc&t=90',
        }
      ],
    });
    expect(result.clips.single.timestampUrl, contains('t=90'));
    expect(result.refused, isFalse);
  });

  test('companion cards stay labeled public', () {
    final card = CompanionCard.fromJson({
      'kind': 'gita',
      'title': 'Bhagavad Gita 2.47',
      'text': 'कर्म',
      'url': 'https://vedicscriptures.github.io/slok/2/47',
      'attribution': 'not from Uttar Sewa videos',
    });
    expect(card.kind, 'gita');
    expect(card.attribution, contains('not from Uttar Sewa videos'));
  });

  test('control dashboard parses stats and named malas', () {
    final dash = ControlDashboard.fromJson({
      'ready': true,
      'database': 'uttar_sewa',
      'stats': {'total_videos': 2, 'total_qa_pairs': 9, 'pinned_qa': 1},
      'controls': {
        'beads_per_cycle': 27,
        'named_malas': [
          {'id': 'ram', 'name_hi': 'राम राम', 'name_en': 'Ram Ram'}
        ],
        'allowed_cycle_lengths': [11, 27, 54, 108],
      },
    });
    expect(dash.ready, isTrue);
    expect(dash.stats['total_qa_pairs'], 9);
    expect(dash.namedMalas.single.id, 'ram');
    expect(dash.allowedCycles, contains(27));
  });

  test('asInt accepts json numbers', () {
    expect(asInt(27.0), 27);
    expect(asInt('108', 11), 108);
    expect(asBool('true'), isTrue);
  });

  test('mala day key rolls over across calendar days', () {
    expect(malaDayKey(DateTime(2026, 8, 23)), '2026-08-23');
    expect(malaNeedsRollover('2026-08-22', '2026-08-23'), isTrue);
    expect(malaNeedsRollover('', '2026-08-23'), isFalse);
    expect(malaNeedsRollover('2026-08-23', '2026-08-23'), isFalse);
  });
}
