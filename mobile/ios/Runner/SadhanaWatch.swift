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
}
#else
enum SadhanaWatch {
  static func startSession() -> Bool { false }
}
#endif
