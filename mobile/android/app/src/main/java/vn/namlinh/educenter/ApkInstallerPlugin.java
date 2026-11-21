package vn.namlinh.educenter;

import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import androidx.core.content.FileProvider;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Tải apk bản mới ngay trong app rồi mở hộp "Cài đặt" của Android (người dùng vẫn phải bấm Cài đặt một lần).
 * Android chỉ cài đè khi apk cùng khóa ký với app đang chạy, nên apk lạ không thể thay thế app.
 * JS gọi: ApkInstaller.install({ url }) và nghe sự kiện "progress" ({ percent }).
 */
@CapacitorPlugin(name = "ApkInstaller")
public class ApkInstallerPlugin extends Plugin {
    private volatile boolean running = false;

    @PluginMethod
    public void install(final PluginCall call) {
        final String link = call.getString("url");
        if (link == null || !link.startsWith("https://")) {
            call.reject("Địa chỉ tải không hợp lệ.", "bad_url");
            return;
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && !getContext().getPackageManager().canRequestPackageInstalls()) {
            // Lần đầu Android yêu cầu người dùng cho phép app này cài ứng dụng: mở đúng trang cài đặt rồi báo JS.
            Intent s = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES, Uri.parse("package:" + getContext().getPackageName()));
            s.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(s);
            call.reject("Cần cho phép cài ứng dụng.", "needs_permission");
            return;
        }
        if (running) { call.reject("Đang tải.", "busy"); return; }
        running = true;
        new Thread(new Runnable() {
            @Override public void run() {
                try {
                    File dir = new File(getContext().getCacheDir(), "update");
                    if (!dir.exists() && !dir.mkdirs()) throw new Exception("Không tạo được thư mục tạm.");
                    File out = new File(dir, "nam-linh-educenter.apk");
                    HttpURLConnection c = (HttpURLConnection) new URL(link).openConnection();
                    c.setConnectTimeout(20000); c.setReadTimeout(60000); c.setInstanceFollowRedirects(true);
                    if (c.getResponseCode() != 200) throw new Exception("HTTP " + c.getResponseCode());
                    long total = c.getContentLengthLong(); long done = 0; int last = -1;
                    try (InputStream in = c.getInputStream(); FileOutputStream fo = new FileOutputStream(out)) {
                        byte[] buf = new byte[64 * 1024]; int n;
                        while ((n = in.read(buf)) > 0) {
                            fo.write(buf, 0, n); done += n;
                            if (total > 0) {
                                int p = (int) (done * 100 / total);
                                if (p != last && (p - last >= 2 || p == 100)) { last = p; JSObject e = new JSObject(); e.put("percent", p); notifyListeners("progress", e); }
                            }
                        }
                    } finally { c.disconnect(); }
                    if (total > 0 && done != total) throw new Exception("Tải chưa đủ tệp.");
                    Uri uri = FileProvider.getUriForFile(getContext(), getContext().getPackageName() + ".fileprovider", out);
                    Intent i = new Intent(Intent.ACTION_VIEW);
                    i.setDataAndType(uri, "application/vnd.android.package-archive");
                    i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
                    getContext().startActivity(i);
                    call.resolve();
                } catch (Exception ex) {
                    call.reject(ex.getMessage() == null ? "Không tải được." : ex.getMessage(), "download_failed");
                } finally { running = false; }
            }
        }).start();
    }
}
