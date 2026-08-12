import 'package:flutter_test/flutter_test.dart';

import 'package:uttar_sewa/models.dart';

void main() {
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
}
