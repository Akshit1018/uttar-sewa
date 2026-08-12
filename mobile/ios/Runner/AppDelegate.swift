import Flutter
import UIKit

@main
@objc class AppDelegate: FlutterAppDelegate, FlutterImplicitEngineDelegate {
  private var sadhanaChannel: FlutterMethodChannel?

  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  func didInitializeImplicitFlutterEngine(_ engineBridge: FlutterImplicitEngineBridge) {
    GeneratedPluginRegistrant.register(with: engineBridge.pluginRegistry)
    let channel = FlutterMethodChannel(
      name: "sewa.uttar/sadhana",
      binaryMessenger: engineBridge.applicationRegistrar.messenger()
    )
    sadhanaChannel = channel
    channel.setMethodCallHandler { call, result in
      let beads = (call.arguments as? [String: Any])?["beads"] as? Int ?? 0
      let cycle = (call.arguments as? [String: Any])?["cycle"] as? Int ?? 108
      switch call.method {
      case "startOverlay", "updateCount", "stopOverlay":
        result(false)
      case "startLiveActivity":
        result(SadhanaLiveActivity.start(beads: beads, cycle: cycle))
      case "updateLiveActivity":
        SadhanaLiveActivity.update(beads: beads, cycle: cycle)
        result(nil)
      case "startWatchSession":
        result(SadhanaWatch.startSession())
      default:
        result(FlutterMethodNotImplemented)
      }
    }
  }
}
