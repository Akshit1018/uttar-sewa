import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

import 'api_client.dart';
import 'models.dart';
import 'native_sadhana.dart';

class AppState extends ChangeNotifier {
  AppState({ApiClient? api, NativeSadhana? native})
      : api = api ?? ApiClient(),
        native = native ?? NativeSadhana();

  final ApiClient api;
  final NativeSadhana native;
  String language = 'hi';
  String channelId = 'all';
  String deviceId = 'device';
  List<ChannelItem> channels = const [];
  List<Map<String, dynamic>> pinned = const [];
  List<Map<String, dynamic>> gaps = const [];
  List<Map<String, dynamic>> catalog = const [];
  List<CompanionCard> companions = const [];
  TodayEnrichment? today;
  MalaState mala = const MalaState();
  ControlDashboard? dashboard;
  Map<String, dynamic>? health;
  String? error;
  bool loading = false;
  bool askRequested = false;

  bool overlayOn = false;
  bool liveActivityOn = false;
  bool watchOn = false;

  bool get isHindi => language == 'hi';

  String t(String hi, String en) => isHindi ? hi : en;

  Future<void> boot() async {
    final prefs = await SharedPreferences.getInstance();
    language = prefs.getString('language') ?? 'hi';
    channelId = prefs.getString('channelId') ?? 'all';
    deviceId = prefs.getString('deviceId') ?? DateTime.now().millisecondsSinceEpoch.toString();
    await prefs.setString('deviceId', deviceId);
    mala = MalaState(
      beadsToday: prefs.getInt('beads') ?? 0,
      cyclesToday: prefs.getInt('cycles') ?? 0,
      currentInCycle: prefs.getInt('current') ?? 0,
      questionsToday: prefs.getInt('questions') ?? 0,
      beadsPerCycle: prefs.getInt('cycle') ?? 108,
      mantraId: prefs.getString('mantra') ?? 'ram',
    );
    try {
      channels = await api.channels();
      health = await api.health();
      await refreshDashboard();
      try {
        today = await api.today(language: language);
        catalog = await api.enrichCatalog();
      } catch (_) {}
    } catch (err) {
      error = err.toString();
    }
    native.onVolumeTap = tapBead;
    native.attach();
    notifyListeners();
  }

  void openAsk() {
    askRequested = true;
    notifyListeners();
  }

  void consumeAskRequest() {
    askRequested = false;
  }

  Future<void> setLanguage(String value) async {
    language = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('language', value);
    try {
      await api.saveSettings({'language': value});
    } catch (_) {}
    notifyListeners();
  }

  Future<void> setChannel(String value) async {
    channelId = value;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('channelId', value);
    notifyListeners();
  }

  Future<void> persistMala() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt('beads', mala.beadsToday);
    await prefs.setInt('cycles', mala.cyclesToday);
    await prefs.setInt('current', mala.currentInCycle);
    await prefs.setInt('questions', mala.questionsToday);
    await prefs.setInt('cycle', mala.beadsPerCycle);
    await prefs.setString('mantra', mala.mantraId);
    final now = DateTime.now();
    final day =
        '${now.year}-${now.month.toString().padLeft(2, '0')}-${now.day.toString().padLeft(2, '0')}';
    try {
      await api.syncMala(deviceId: deviceId, day: day, state: mala);
    } catch (_) {}
  }

  Future<void> tapBead() async {
    mala = await api.tap(mala);
    await persistMala();
    await native.updateCount(beads: mala.currentInCycle, cycle: mala.beadsPerCycle);
    if (liveActivityOn) {
      await native.updateLiveActivity(beads: mala.currentInCycle, cycle: mala.beadsPerCycle);
    }
    notifyListeners();
  }

  Future<void> undoBead() async {
    mala = await api.undo(mala);
    await persistMala();
    notifyListeners();
  }

  Future<AskResult> ask(String query, List<String> history) async {
    final result = await api.ask(query: query, language: language, history: history);
    mala = mala.copyWith(questionsToday: mala.questionsToday + 1);
    await persistMala();
    notifyListeners();
    final allow = asBool(dashboard?.controls['public_companions'], true);
    if (allow) {
      try {
        companions = await api.companions(query: query, language: language);
        notifyListeners();
      } catch (_) {}
    }
    return result;
  }

  Future<List<SearchHit>> search(String query, List<String> history) {
    return api.search(query: query, language: language, channelId: channelId, history: history);
  }

  Future<void> refreshDashboard() async {
    dashboard = await api.dashboard();
    final settings = dashboard!.controls;
    mala = mala.copyWith(
      beadsPerCycle: asInt(settings['beads_per_cycle'], mala.beadsPerCycle),
      mantraId: settings['mantra_id'] as String? ?? mala.mantraId,
    );
    try {
      pinned = await api.pinned();
      gaps = await api.gaps();
      health = await api.health();
      error = null;
    } catch (err) {
      error = err.toString();
    }
    notifyListeners();
  }

  Future<void> updateControl(Map<String, dynamic> patch) async {
    await api.saveSettings(patch);
    await refreshDashboard();
    await persistMala();
  }

  Future<void> pinHit(SearchHit hit) async {
    await api.pinQa(hit);
    await refreshDashboard();
  }

  Future<void> openUrl(String url) async {
    if (url.isEmpty) return;
    await launchUrl(Uri.parse(url), mode: LaunchMode.externalApplication);
  }

  Future<void> toggleOverlay() async {
    if (overlayOn) {
      await native.stopOverlay();
      overlayOn = false;
    } else {
      overlayOn = await native.startOverlay(
        beads: mala.currentInCycle,
        cycle: mala.beadsPerCycle,
      );
    }
    notifyListeners();
  }

  Future<void> toggleLiveActivity() async {
    liveActivityOn = await native.startLiveActivity(
      beads: mala.currentInCycle,
      cycle: mala.beadsPerCycle,
    );
    notifyListeners();
  }

  Future<void> toggleWatch() async {
    watchOn = await native.startWatchSession();
    notifyListeners();
  }
}
