import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:uttar_sewa/native_sadhana.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  late MethodChannel channel;
  late NativeSadhana native;
  late List<MethodCall> log;

  setUp(() {
    channel = const MethodChannel(sadhanaChannelName);
    native = NativeSadhana(channel: channel);
    log = <MethodCall>[];
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      channel,
      (MethodCall call) async {
        log.add(call);
        if (call.method == 'startOverlay' ||
            call.method == 'startLiveActivity' ||
            call.method == 'startWatchSession') {
          return true;
        }
        return null;
      },
    );
  });

  tearDown(() {
    native.detach();
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      channel,
      null,
    );
  });

  test('startOverlay sends beads and cycle', () async {
    expect(await native.startOverlay(beads: 12, cycle: 108), isTrue);
    expect(log.single.method, 'startOverlay');
    expect(log.single.arguments['beads'], 12);
    expect(log.single.arguments['cycle'], 108);
  });

  test('updateCount and stopOverlay use the same channel', () async {
    await native.updateCount(beads: 13, cycle: 108);
    await native.stopOverlay();
    expect(log.map((call) => call.method), ['updateCount', 'stopOverlay']);
    expect(log.first.arguments['beads'], 13);
  });

  test('live activity and watch session methods exist', () async {
    expect(await native.startLiveActivity(beads: 1, cycle: 27), isTrue);
    expect(await native.startWatchSession(), isTrue);
    await native.updateLiveActivity(beads: 2, cycle: 27);
    expect(log.map((call) => call.method), [
      'startLiveActivity',
      'startWatchSession',
      'updateLiveActivity',
    ]);
  });

  test('volumeTap from native fires onVolumeTap', () async {
    var taps = 0;
    native.onVolumeTap = () => taps += 1;
    native.attach();
    await TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.handlePlatformMessage(
      channel.name,
      const StandardMethodCodec().encodeMethodCall(const MethodCall('volumeTap')),
      (ByteData? _) {},
    );
    expect(taps, 1);
  });

  test('missing plugin does not throw', () async {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      channel,
      null,
    );
    expect(await native.startOverlay(beads: 0, cycle: 108), isFalse);
  });
}
