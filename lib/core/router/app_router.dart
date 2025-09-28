import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/presentation/screens/login_screen.dart';
import '../../features/auth/presentation/providers/auth_provider.dart';
import '../../features/home/presentation/screens/home_screen.dart';
import '../../features/users/presentation/screens/users_screen.dart';
import '../../features/video_call/presentation/screens/video_call_screen.dart';
import '../../features/splash/presentation/screens/splash_screen.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: AppRouter.splash,
    redirect: (context, state) {
      final authState = ref.read(authStateProvider);
      final isLoggedIn = authState.isAuthenticated;
      final isLoggingIn = state.location == AppRouter.login;
      final isAtSplash = state.location == AppRouter.splash;

      if (isAtSplash) {
        return null; // Let splash screen handle navigation
      }

      if (!isLoggedIn && !isLoggingIn) {
        return AppRouter.login;
      }
      
      if (isLoggedIn && isLoggingIn) {
        return AppRouter.home;
      }

      return null;
    },
    routes: [
      GoRoute(
        path: AppRouter.splash,
        name: 'splash',
        builder: (context, state) => const SplashScreen(),
      ),
      GoRoute(
        path: AppRouter.login,
        name: 'login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: AppRouter.home,
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
      GoRoute(
        path: AppRouter.users,
        name: 'users',
        builder: (context, state) => const UsersScreen(),
      ),
      GoRoute(
        path: AppRouter.videoCall,
        name: 'video-call',
        builder: (context, state) {
          final meetingId = state.uri.queryParameters['meetingId'] ?? 'default-meeting';
          return VideoCallScreen(meetingId: meetingId);
        },
      ),
    ],
  );
});

class AppRouter {
  static const String splash = '/';
  static const String login = '/login';
  static const String home = '/home';
  static const String users = '/users';
  static const String videoCall = '/video-call';
}