package sewa.uttar.uttar_sewa

import android.content.Intent
import android.net.Uri
import android.os.Build
import android.provider.Settings
import android.view.KeyEvent
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val channelName = "sewa.uttar/sadhana"
    private var channel: MethodChannel? = null

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        channel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, channelName)
        channel?.setMethodCallHandler { call, result ->
            when (call.method) {
                "startOverlay" -> {
                    val beads = call.argument<Int>("beads") ?: 0
                    val cycle = call.argument<Int>("cycle") ?: 108
                    result.success(startOverlay(beads, cycle))
                }
                "updateCount" -> {
                    val beads = call.argument<Int>("beads") ?: 0
                    val cycle = call.argument<Int>("cycle") ?: 108
                    updateOverlay(beads, cycle)
                    result.success(null)
                }
                "stopOverlay" -> {
                    stopService(Intent(this, JapaOverlayService::class.java))
                    result.success(null)
                }
                "startLiveActivity", "updateLiveActivity", "startWatchSession" ->
                    result.success(false)
                else -> result.notImplemented()
            }
        }
    }

    private fun startOverlay(beads: Int, cycle: Int): Boolean {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(this)) {
            startActivity(
                Intent(
                    Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:$packageName"),
                ),
            )
            return false
        }
        val intent = Intent(this, JapaOverlayService::class.java)
        intent.putExtra("beads", beads)
        intent.putExtra("cycle", cycle)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
        return true
    }

    private fun updateOverlay(beads: Int, cycle: Int) {
        val intent = Intent(this, JapaOverlayService::class.java)
        intent.action = JapaOverlayService.ACTION_UPDATE
        intent.putExtra("beads", beads)
        intent.putExtra("cycle", cycle)
        startService(intent)
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        if (keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN) {
            channel?.invokeMethod("volumeTap", null)
            return true
        }
        return super.onKeyDown(keyCode, event)
    }
}
