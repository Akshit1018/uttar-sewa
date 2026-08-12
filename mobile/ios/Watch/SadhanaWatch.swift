import Foundation
import WatchKit

/// Watch app stub. The iOS app talks to the watch through WCSession in Runner/SadhanaWatch.swift.
class SadhanaWatchController: WKInterfaceController {
  func update(beads: Int, cycle: Int) {
    setTitle("\(beads)/\(cycle)")
  }
}
