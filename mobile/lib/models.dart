String malaDayKey([DateTime? now]) {
  final day = now ?? DateTime.now();
  return '${day.year}-${day.month.toString().padLeft(2, '0')}-${day.day.toString().padLeft(2, '0')}';
}

bool malaNeedsRollover(String storedDay, String today) {
  return storedDay.isNotEmpty && storedDay != today;
}

int asInt(Object? value, [int fallback = 0]) {
  if (value is int) return value;
  if (value is num) return value.toInt();
  if (value is String) return int.tryParse(value) ?? fallback;
  return fallback;
}

bool asBool(Object? value, [bool fallback = false]) {
  if (value is bool) return value;
  if (value is num) return value != 0;
  if (value is String) {
    final normalized = value.toLowerCase();
    if (normalized == 'true' || normalized == '1') return true;
    if (normalized == 'false' || normalized == '0') return false;
  }
  return fallback;
}

class SearchHit {
  const SearchHit({
    required this.question,
    required this.answer,
    required this.videoId,
    required this.videoTitle,
    required this.startTime,
    required this.timestampUrl,
    this.related = const [],
  });

  final String question;
  final String answer;
  final String videoId;
  final String videoTitle;
  final double startTime;
  final String timestampUrl;
  final List<String> related;

  factory SearchHit.fromJson(Map<String, dynamic> json) {
    return SearchHit(
      question: json['question'] as String? ?? '',
      answer: json['answer'] as String? ?? '',
      videoId: json['video_id'] as String? ?? '',
      videoTitle: json['video_title'] as String? ?? '',
      startTime: (json['start_time'] as num?)?.toDouble() ?? 0,
      timestampUrl: json['timestamp_url'] as String? ?? '',
      related: (json['related_questions'] as List?)?.map((e) => '$e').toList() ?? const [],
    );
  }
}

class AskResult {
  const AskResult({required this.answer, required this.refused, required this.clips, this.companions = const []});

  final String answer;
  final bool refused;
  final List<SearchHit> clips;
  final List<CompanionCard> companions;

  factory AskResult.fromJson(Map<String, dynamic> json) {
    final clips = <SearchHit>[];
    for (final item in (json['clips'] as List? ?? const [])) {
      if (item is Map) {
        clips.add(SearchHit.fromJson({
          'question': item['source_question'],
          'answer': item['source_answer'] ?? json['answer'],
          'video_id': item['video_id'],
          'video_title': item['video_title'],
          'start_time': item['start_time'],
          'timestamp_url': item['timestamp_url'],
        }));
      }
    }
    final companions = <CompanionCard>[];
    for (final item in (json['companions'] as List? ?? const [])) {
      if (item is Map) {
        companions.add(CompanionCard.fromJson(Map<String, dynamic>.from(item)));
      }
    }
    return AskResult(
      answer: json['answer'] as String? ?? '',
      refused: asBool(json['refused']),
      clips: clips,
      companions: companions,
    );
  }
}

class CompanionCard {
  const CompanionCard({
    required this.kind,
    required this.title,
    required this.text,
    required this.url,
    required this.attribution,
  });

  final String kind;
  final String title;
  final String text;
  final String url;
  final String attribution;

  factory CompanionCard.fromJson(Map<String, dynamic> json) {
    return CompanionCard(
      kind: json['kind'] as String? ?? 'public',
      title: json['title'] as String? ?? '',
      text: json['text'] as String? ?? '',
      url: json['url'] as String? ?? '',
      attribution: json['attribution'] as String? ?? 'public text — not from videos',
    );
  }
}

class TodayEnrichment {
  const TodayEnrichment({this.gita, this.sandhya, this.disclaimer = ''});

  final CompanionCard? gita;
  final CompanionCard? sandhya;
  final String disclaimer;

  factory TodayEnrichment.fromJson(Map<String, dynamic> json) {
    CompanionCard? card(Object? raw) {
      if (raw is Map && (raw['text'] as String? ?? '').isNotEmpty) {
        return CompanionCard.fromJson(Map<String, dynamic>.from(raw));
      }
      return null;
    }

    return TodayEnrichment(
      gita: card(json['gita']),
      sandhya: card(json['sandhya']),
      disclaimer: json['disclaimer'] as String? ?? '',
    );
  }
}

class NamedMala {
  const NamedMala({required this.id, required this.nameHi, required this.nameEn});

  final String id;
  final String nameHi;
  final String nameEn;

  factory NamedMala.fromJson(Map<String, dynamic> json) {
    return NamedMala(
      id: json['id'] as String? ?? 'ram',
      nameHi: json['name_hi'] as String? ?? json['name'] as String? ?? 'राम राम',
      nameEn: json['name_en'] as String? ?? json['name'] as String? ?? 'Ram Ram',
    );
  }

  String label(bool hindi) => hindi ? nameHi : nameEn;
}

class ControlDashboard {
  const ControlDashboard({
    required this.ready,
    required this.database,
    required this.stats,
    required this.controls,
    this.namedMalas = const [],
    this.allowedCycles = const [11, 27, 54, 108],
  });

  final bool ready;
  final String database;
  final Map<String, dynamic> stats;
  final Map<String, dynamic> controls;
  final List<NamedMala> namedMalas;
  final List<int> allowedCycles;

  factory ControlDashboard.fromJson(Map<String, dynamic> json) {
    final controls = Map<String, dynamic>.from(json['controls'] as Map? ?? const {});
    final named = <NamedMala>[];
    for (final item in (controls['named_malas'] as List? ?? const [])) {
      if (item is Map) {
        named.add(NamedMala.fromJson(Map<String, dynamic>.from(item)));
      }
    }
    final cycles = (controls['allowed_cycle_lengths'] as List? ?? const [11, 27, 54, 108])
        .map((item) => asInt(item, 108))
        .toList();
    return ControlDashboard(
      ready: asBool(json['ready']),
      database: json['database'] as String? ?? 'uttar_sewa',
      stats: Map<String, dynamic>.from(json['stats'] as Map? ?? const {}),
      controls: controls,
      namedMalas: named,
      allowedCycles: cycles.isEmpty ? const [11, 27, 54, 108] : cycles,
    );
  }
}

class ChannelItem {
  const ChannelItem({required this.id, required this.name, required this.nameHi});

  final String id;
  final String name;
  final String nameHi;

  factory ChannelItem.fromJson(Map<String, dynamic> json) {
    return ChannelItem(
      id: json['id'] as String? ?? 'all',
      name: json['name'] as String? ?? '',
      nameHi: json['name_hi'] as String? ?? json['name'] as String? ?? '',
    );
  }
}

class MalaState {
  const MalaState({
    this.beadsToday = 0,
    this.cyclesToday = 0,
    this.currentInCycle = 0,
    this.questionsToday = 0,
    this.completedCycle = false,
    this.beadsPerCycle = 108,
    this.mantraId = 'ram',
  });

  final int beadsToday;
  final int cyclesToday;
  final int currentInCycle;
  final int questionsToday;
  final bool completedCycle;
  final int beadsPerCycle;
  final String mantraId;

  Map<String, dynamic> toJson() => {
        'beads_today': beadsToday,
        'cycles_today': cyclesToday,
        'current_in_cycle': currentInCycle,
        'questions_today': questionsToday,
        'completed_cycle': completedCycle,
        'beads_per_cycle': beadsPerCycle,
        'mantra_id': mantraId,
      };

  factory MalaState.fromJson(Map<String, dynamic> json) {
    return MalaState(
      beadsToday: asInt(json['beads_today']),
      cyclesToday: asInt(json['cycles_today'] ?? json['malas_today']),
      currentInCycle: asInt(json['current_in_cycle']),
      questionsToday: asInt(json['questions_today']),
      completedCycle: asBool(json['completed_cycle']),
      beadsPerCycle: asInt(json['beads_per_cycle'] ?? json['cycle_length'], 108),
      mantraId: json['mantra_id'] as String? ?? 'ram',
    );
  }

  static const allowedCycleLengths = [11, 27, 54, 108];

  int get resolvedCycle =>
      allowedCycleLengths.contains(beadsPerCycle) ? beadsPerCycle : 108;

  MalaState applyTap() {
    final cycle = resolvedCycle;
    var nextCurrent = currentInCycle + 1;
    var nextCycles = cyclesToday;
    var completed = false;
    if (nextCurrent >= cycle) {
      nextCycles += 1;
      nextCurrent = 0;
      completed = true;
    }
    return copyWith(
      beadsToday: beadsToday + 1,
      cyclesToday: nextCycles,
      currentInCycle: nextCurrent,
      completedCycle: completed,
      beadsPerCycle: cycle,
    );
  }

  MalaState applyUndo() {
    final cycle = resolvedCycle;
    if (beadsToday <= 0) {
      return copyWith(beadsPerCycle: cycle, completedCycle: false);
    }
    var nextCurrent = currentInCycle;
    var nextCycles = cyclesToday;
    if (nextCurrent == 0 && nextCycles > 0) {
      nextCycles -= 1;
      nextCurrent = cycle - 1;
    } else {
      nextCurrent = nextCurrent > 0 ? nextCurrent - 1 : 0;
    }
    return copyWith(
      beadsToday: beadsToday - 1,
      cyclesToday: nextCycles,
      currentInCycle: nextCurrent,
      completedCycle: false,
      beadsPerCycle: cycle,
    );
  }

  MalaState copyWith({
    int? beadsToday,
    int? cyclesToday,
    int? currentInCycle,
    int? questionsToday,
    bool? completedCycle,
    int? beadsPerCycle,
    String? mantraId,
  }) {
    return MalaState(
      beadsToday: beadsToday ?? this.beadsToday,
      cyclesToday: cyclesToday ?? this.cyclesToday,
      currentInCycle: currentInCycle ?? this.currentInCycle,
      questionsToday: questionsToday ?? this.questionsToday,
      completedCycle: completedCycle ?? this.completedCycle,
      beadsPerCycle: beadsPerCycle ?? this.beadsPerCycle,
      mantraId: mantraId ?? this.mantraId,
    );
  }
}
