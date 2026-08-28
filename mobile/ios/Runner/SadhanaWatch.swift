import Foundation

#if canImport(WatchConnectivity)
import WatchConnectivity

final class SadhanaWatchSession: NSObject, WCSessionDelegate {
  static let shared = SadhanaWatchSession()

  func session(
    _ session: WCSession,
    activationDidCompleteWith activationState: WCSessionActivationState,
    error: Error?
  ) {}

  #if os(iOS)
  func sessionDidBecomeInactive(_ session: WCSession) {}

  func sessionDidDeactivate(_ session: WCSession) {
    session.activate()
  }
  #endif
}

enum SadhanaWatch {
  static func startSession() -> Bool {
    guard WCSession.isSupported() else { return false }
    let session = WCSession.default
    session.delegate = SadhanaWatchSession.shared
    if session.activationState != .activated {
      session.activate()
    }
    return true
  }

  static func stopSession() {
    guard WCSession.isSupported() else { return }
    let session = WCSession.default
    if session.activationState == .activated {
      session.transferUserInfo(["running": false])
    }
  }
}
#else
enum SadhanaWatch {
  static func startSession() -> Bool { false }
  static func stopSession() {}
}
#endif
