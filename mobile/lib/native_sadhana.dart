import 'package:flutter/services.dart';

const String sadhanaChannelName = 'sewa.uttar/sadhana';

class NativeSadhana {
  NativeSadhana({MethodChannel? channel})
      : channel = channel ?? const MethodChannel(sadhanaChannelName);

  final MethodChannel channel;
  VoidCallback? onVolumeTap;
  bool listening = false;

  Future<bool> startOverlay({required int beads, required int cycle}) async {
    return await _invoke<bool>('startOverlay', {'beads': beads, 'cycle': cycle}) ?? false;
  }

  Future<void> updateCount({required int beads, required int cycle}) async {
    await _invoke<void>('updateCount', {'beads': beads, 'cycle': cycle});
  }

  Future<void> stopOverlay() async {
    await _invoke<void>('stopOverlay');
  }

  Future<bool> startLiveActivity({required int beads, required int cycle}) async {
    return await _invoke<bool>('startLiveActivity', {'beads': beads, 'cycle': cycle}) ?? false;
  }

  Future<void> updateLiveActivity({required int beads, required int cycle}) async {
    await _invoke<void>('updateLiveActivity', {'beads': beads, 'cycle': cycle});
  }

  Future<bool> startWatchSession() async {
    return await _invoke<bool>('startWatchSession') ?? false;
  }

  Future<void> stopLiveActivity() async {
    await _invoke<void>('stopLiveActivity');
  }

  Future<void> stopWatchSession() async {
    await _invoke<void>('stopWatchSession');
  }

  void attach() {
    if (listening) {
      return;
    }
    listening = true;
    channel.setMethodCallHandler((MethodCall call) async {
      if (call.method == 'volumeTap') {
        onVolumeTap?.call();
      }
    });
  }

  void detach() {
    if (!listening) {
      return;
    }
    listening = false;
    channel.setMethodCallHandler(null);
  }

  Future<T?> _invoke<T>(String method, [Map<String, dynamic>? arguments]) async {
    try {
      return await channel.invokeMethod<T>(method, arguments);
    } on MissingPluginException {
      return null;
    } on PlatformException {
      return null;
    }
  }
}
