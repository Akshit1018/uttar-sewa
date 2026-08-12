import 'dart:convert';

import 'package:http/http.dart' as http;

import 'models.dart';

class ApiException implements Exception {
  ApiException(this.status, this.body);
  final int status;
  final String body;

  @override
  String toString() => 'API $status';
}

class ApiClient {
  ApiClient({String? baseUrl}) : baseUrl = baseUrl ?? _fromEnv();

  final String baseUrl;

  static String _fromEnv() {
    const defined = String.fromEnvironment('API_BASE');
    if (defined.isNotEmpty) return defined;
    return 'http://127.0.0.1:8000/api';
  }

  Uri _u(String path, [Map<String, String>? query]) {
    return Uri.parse('$baseUrl$path').replace(queryParameters: query);
  }

  dynamic _decode(http.Response response) {
    if (response.statusCode >= 400) {
      throw ApiException(response.statusCode, response.body);
    }
    if (response.body.isEmpty) return <String, dynamic>{};
    return jsonDecode(response.body);
  }

  Future<Map<String, dynamic>> _get(String path, [Map<String, String>? query]) async {
    final response = await http.get(_u(path, query));
    return Map<String, dynamic>.from(_decode(response) as Map);
  }

  Future<dynamic> _post(String path, Map<String, dynamic> body) async {
    final response = await http.post(
      _u(path),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );
    return _decode(response);
  }

  Future<Map<String, dynamic>> _put(String path, Map<String, dynamic> body) async {
    final response = await http.put(
      _u(path),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );
    return Map<String, dynamic>.from(_decode(response) as Map);
  }

  Future<Map<String, dynamic>> health() => _get('/health');

  Future<List<ChannelItem>> channels() async {
    final data = await _get('/channels');
    final items = data['channels'] as List? ?? const [];
    return items.map((item) => ChannelItem.fromJson(Map<String, dynamic>.from(item as Map))).toList();
  }

  Future<List<SearchHit>> search({
    required String query,
    required String language,
    String? channelId,
    List<String> history = const [],
  }) async {
    final data = await _post('/search', {
      'query': query,
      'language': language,
      'limit': 5,
      'channel_id': channelId == 'all' ? null : channelId,
      'conversation_history': history,
    });
    return (data as List).map((item) => SearchHit.fromJson(Map<String, dynamic>.from(item as Map))).toList();
  }

  Future<AskResult> ask({
    required String query,
    required String language,
    List<String> history = const [],
  }) async {
    final data = await _post('/ask', {
      'query': query,
      'language': language,
      'limit': 3,
      'conversation_history': history,
    }) as Map<String, dynamic>;
    return AskResult.fromJson(data);
  }

  Future<ControlDashboard> dashboard() async {
    return ControlDashboard.fromJson(await _get('/control/dashboard'));
  }

  Future<Map<String, dynamic>> settings() => _get('/control/settings');

  Future<Map<String, dynamic>> saveSettings(Map<String, dynamic> patch) => _put('/control/settings', patch);

  Future<List<Map<String, dynamic>>> pinned() async {
    final data = await _get('/control/qa/pinned');
    return (data['items'] as List? ?? const [])
        .map((item) => Map<String, dynamic>.from(item as Map))
        .toList();
  }

  Future<List<Map<String, dynamic>>> gaps() async {
    final data = await _get('/control/library/gaps');
    return (data['items'] as List? ?? const [])
        .map((item) => Map<String, dynamic>.from(item as Map))
        .toList();
  }

  Future<Map<String, dynamic>> startProcessing() async {
    return await _post('/process/start', {}) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> clearProcessing() async {
    return await _post('/process/clear', {}) as Map<String, dynamic>;
  }

  Future<MalaState> tap(MalaState state) async {
    final data = await _post('/mala/tap', state.toJson()) as Map<String, dynamic>;
    return MalaState.fromJson(data);
  }

  Future<MalaState> undo(MalaState state) async {
    final data = await _post('/mala/undo', state.toJson()) as Map<String, dynamic>;
    return MalaState.fromJson(data);
  }

  Future<void> syncMala({required String deviceId, required String day, required MalaState state}) async {
    await _post('/mala/sync', {
      'device_id': deviceId,
      'day': day,
      ...state.toJson(),
    });
  }

  Future<Map<String, dynamic>> pinQa(SearchHit hit) async {
    return await _post('/control/qa/pin', {
      'question': hit.question,
      'answer': hit.answer,
      'video_id': hit.videoId,
      'video_title': hit.videoTitle,
      'start_time': hit.startTime,
      'timestamp_url': hit.timestampUrl,
    }) as Map<String, dynamic>;
  }

  Future<TodayEnrichment> today({required String language}) async {
    return TodayEnrichment.fromJson(await _get('/enrich/today', {'language': language}));
  }

  Future<List<CompanionCard>> companions({required String query, required String language}) async {
    final data = await _post('/enrich/companions', {'query': query, 'language': language}) as Map<String, dynamic>;
    return (data['items'] as List? ?? const [])
        .whereType<Map>()
        .map((item) => CompanionCard.fromJson(Map<String, dynamic>.from(item)))
        .toList();
  }

  Future<Map<String, dynamic>> scrape(String url) async {
    return await _post('/control/scrape', {'url': url}) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> videoMeta(String videoId) async {
    return await _post('/control/enrich/video', {'video_id': videoId}) as Map<String, dynamic>;
  }

  Future<List<Map<String, dynamic>>> enrichCatalog() async {
    final data = await _get('/enrich/catalog');
    return (data['items'] as List? ?? const [])
        .map((item) => Map<String, dynamic>.from(item as Map))
        .toList();
  }
}
