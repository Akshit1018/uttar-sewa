from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID_MAIN = ROOT / "mobile/android/app/src/main/kotlin/sewa/uttar/uttar_sewa/MainActivity.kt"
ANDROID_OVERLAY = ROOT / "mobile/android/app/src/main/kotlin/sewa/uttar/uttar_sewa/JapaOverlayService.kt"
ANDROID_MANIFEST = ROOT / "mobile/android/app/src/main/AndroidManifest.xml"
IOS_DELEGATE = ROOT / "mobile/ios/Runner/AppDelegate.swift"
IOS_LIVE = ROOT / "mobile/ios/Runner/SadhanaLiveActivity.swift"
IOS_WATCH = ROOT / "mobile/ios/Watch/SadhanaWatch.swift"
IOS_PLIST = ROOT / "mobile/ios/Runner/Info.plist"


def test_android_volume_keys_and_overlay_channel():
    text = ANDROID_MAIN.read_text()
    assert "sewa.uttar/sadhana" in text
    assert "startOverlay" in text
    assert "KEYCODE_VOLUME_UP" in text
    assert "volumeTap" in text
    overlay = ANDROID_OVERLAY.read_text()
    assert "TYPE_APPLICATION_OVERLAY" in overlay
    manifest = ANDROID_MANIFEST.read_text()
    assert "SYSTEM_ALERT_WINDOW" in manifest
    assert "JapaOverlayService" in manifest


def test_ios_live_activity_and_watch_stubs():
    delegate = IOS_DELEGATE.read_text()
    assert "sewa.uttar/sadhana" in delegate
    assert "startLiveActivity" in delegate
    live = IOS_LIVE.read_text()
    assert "ActivityKit" in live
    assert "SadhanaAttributes" in live
    watch = IOS_WATCH.read_text()
    assert "WCSession" in watch or "WatchKit" in watch
    plist = IOS_PLIST.read_text()
    assert "NSSupportsLiveActivities" in plist
