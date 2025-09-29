import 'package:get/get.dart';

import '../../features/auth/presentation/pages/login_page.dart';
import '../../features/home/presentation/pages/home_page.dart';
import '../../features/splash/presentation/pages/splash_page.dart';
import '../../features/users/presentation/pages/users_page.dart';
import '../../features/video_call/presentation/pages/video_call_page.dart';

class AppRoutes {
  static const String splash = '/';
  static const String login = '/login';
  static const String home = '/home';
  static const String users = '/users';
  static const String videoCall = '/video-call';

  static List<GetPage> routes = [
    GetPage(
      name: splash,
      page: () => const SplashPage(),
    ),
    GetPage(
      name: login,
      page: () => const LoginPage(),
    ),
    GetPage(
      name: home,
      page: () => const HomePage(),
    ),
    GetPage(
      name: users,
      page: () => const UsersPage(),
    ),
    GetPage(
      name: videoCall,
      page: () => VideoCallPage(meetingId: Get.arguments['meetingId'] ?? 'default-meeting'),
    ),
  ];
}