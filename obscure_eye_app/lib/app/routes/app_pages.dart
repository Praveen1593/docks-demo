import 'package:get/get.dart';
import '../views/splash_screen.dart';
import '../views/login_screen.dart';
import '../views/main_screen.dart';
import '../views/dashboard_page.dart';
import '../views/live_page.dart';
import '../views/alerts_page.dart';
import '../views/settings_page.dart';

part 'app_routes.dart';

class AppPages {
  static const INITIAL = Routes.SPLASH;

  static final routes = [
    GetPage(
      name: Routes.SPLASH,
      page: () => SplashScreen(),
    ),
    GetPage(
      name: Routes.LOGIN,
      page: () => LoginScreen(),
    ),
    GetPage(
      name: Routes.MAIN,
      page: () => MainScreen(),
    ),
    GetPage(
      name: Routes.DASHBOARD,
      page: () => DashboardPage(),
    ),
    GetPage(
      name: Routes.LIVE,
      page: () => LivePage(),
    ),
    GetPage(
      name: Routes.ALERTS,
      page: () => AlertsPage(),
    ),
    GetPage(
      name: Routes.SETTINGS,
      page: () => SettingsPage(),
    ),
  ];
}