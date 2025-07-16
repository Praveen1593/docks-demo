import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:google_fonts/google_fonts.dart';
import 'app/routes/app_pages.dart';
import 'app/theme/cyberpunk_theme.dart';
import 'app/views/splash_screen.dart';
import 'app/services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NotificationService.init();
  runApp(ObscureEyeApp());
}

class ObscureEyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: 'Obscure Eye',
      debugShowCheckedModeBanner: false,
      theme: cyberpunkTheme,
      initialRoute: AppPages.INITIAL,
      getPages: AppPages.routes,
      home: SplashScreen(),
    );
  }
}