import Foundation

#if canImport(ActivityKit)
import ActivityKit

struct SadhanaAttributes: ActivityAttributes {
  public struct ContentState: Codable, Hashable {
    var beads: Int
    var cycle: Int
  }

  var mantra: String
}

enum SadhanaLiveActivity {
  static func start(beads: Int, cycle: Int) -> Bool {
    if #available(iOS 16.1, *) {
      let attributes = SadhanaAttributes(mantra: "राम")
      let state = SadhanaAttributes.ContentState(beads: beads, cycle: cycle)
      do {
        _ = try Activity<SadhanaAttributes>.request(attributes: attributes, contentState: state)
        return true
      } catch {
        return false
      }
    }
    return false
  }

  static func update(beads: Int, cycle: Int) {
    if #available(iOS 16.1, *) {
      let state = SadhanaAttributes.ContentState(beads: beads, cycle: cycle)
      Task {
        for activity in Activity<SadhanaAttributes>.activities {
          await activity.update(using: state)
        }
      }
    }
  }
}
#else
enum SadhanaLiveActivity {
  static func start(beads: Int, cycle: Int) -> Bool { false }
  static func update(beads: Int, cycle: Int) {}
}
#endif
