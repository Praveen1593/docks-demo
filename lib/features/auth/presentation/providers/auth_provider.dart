import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:dio/dio.dart';

import '../../data/models/user_model.dart';
import '../../data/services/auth_service.dart';
import '../../../core/utils/hive_boxes.dart';

// Services
final authServiceProvider = Provider<AuthService>((ref) {
  return AuthService(Dio());
});

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  return AuthRepository(ref.watch(authServiceProvider));
});

// State
final authStateProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.watch(authRepositoryProvider));
});

class AuthState {
  final bool isLoading;
  final UserModel? user;
  final String? error;
  final bool isAuthenticated;

  const AuthState({
    this.isLoading = false,
    this.user,
    this.error,
    this.isAuthenticated = false,
  });

  AuthState copyWith({
    bool? isLoading,
    UserModel? user,
    String? error,
    bool? isAuthenticated,
  }) {
    return AuthState(
      isLoading: isLoading ?? this.isLoading,
      user: user ?? this.user,
      error: error,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _authRepository;
  final Box _authBox;

  AuthNotifier(this._authRepository) : _authBox = Hive.box(HiveBoxes.authBox), super(const AuthState()) {
    _loadStoredAuth();
  }

  Future<void> _loadStoredAuth() async {
    try {
      final storedUser = _authBox.get('user');
      final storedToken = _authBox.get('token');
      
      if (storedUser != null && storedToken != null) {
        state = state.copyWith(
          user: UserModel.fromJson(Map<String, dynamic>.from(storedUser)),
          isAuthenticated: true,
        );
      }
    } catch (e) {
      // Handle stored data corruption
      await logout();
    }
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final response = await _authRepository.login(email, password);
      
      // Store auth data
      await _authBox.put('user', response.user.toJson());
      await _authBox.put('token', response.token);
      
      state = state.copyWith(
        isLoading: false,
        user: response.user,
        isAuthenticated: true,
        error: null,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        error: e.toString(),
      );
    }
  }

  Future<void> logout() async {
    await _authBox.clear();
    state = const AuthState();
  }

  void clearError() {
    state = state.copyWith(error: null);
  }
}