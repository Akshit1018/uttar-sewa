package sewa.uttar.uttar_sewa

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.graphics.Color
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.WindowManager
import android.widget.TextView

class JapaOverlayService : Service() {
    private var windowManager: WindowManager? = null
    private var bubble: TextView? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        startAsForeground()
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        val view = TextView(this).apply {
            text = "0"
            textSize = 18f
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.parseColor("#CC2A2A2A"))
            setPadding(36, 28, 36, 28)
            gravity = Gravity.CENTER
        }
        bubble = view
        val type =
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            } else {
                @Suppress("DEPRECATION")
                WindowManager.LayoutParams.TYPE_PHONE
            }
        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.WRAP_CONTENT,
            WindowManager.LayoutParams.WRAP_CONTENT,
            type,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE,
            PixelFormat.TRANSLUCENT,
        )
        params.gravity = Gravity.BOTTOM or Gravity.END
        params.x = 24
        params.y = 120
        windowManager?.addView(view, params)
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val beads = intent?.getIntExtra("beads", 0) ?: 0
        val cycle = intent?.getIntExtra("cycle", 108) ?: 108
        bubble?.text = "$beads / $cycle"
        return START_STICKY
    }

    override fun onDestroy() {
        bubble?.let { windowManager?.removeView(it) }
        bubble = null
        super.onDestroy()
    }

    private fun startAsForeground() {
        val channelId = "japa_overlay"
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(channelId, "Japa", NotificationManager.IMPORTANCE_LOW)
            getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
            val notification = Notification.Builder(this, channelId)
                .setContentTitle("उत्तर सेवा")
                .setContentText("माला")
                .setSmallIcon(android.R.drawable.star_on)
                .build()
            startForeground(1, notification)
        }
    }

    companion object {
        const val ACTION_UPDATE = "sewa.uttar.UPDATE_JAPA"
    }
}
