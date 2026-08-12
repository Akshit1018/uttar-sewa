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
  const AskResult({required this.answer, required this.refused, required this.clips});

  final String answer;
  final bool refused;
  final List<SearchHit> clips;

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
    return AskResult(
      answer: json['answer'] as String? ?? '',
      refused: asBool(json['refused']),
      clips: clips,
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
