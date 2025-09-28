import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:dio/dio.dart';

import '../../../../core/utils/hive_boxes.dart';
import '../../../auth/data/models/user_model.dart';
import '../../../auth/data/services/auth_service.dart';

// Services
final usersRepositoryProvider = Provider<UsersRepository>((ref) {
  return UsersRepository();
});

// State
final usersStateProvider = StateNotifierProvider<UsersNotifier, UsersState>((ref) {
  return UsersNotifier(ref.watch(usersRepositoryProvider));
});

class UsersState {
  final bool isLoading;
  final List<UserModel> users;
  final String? error;
  final bool isOffline;

  const UsersState({
    this.isLoading = false,
    this.users = const [],
    this.error,
    this.isOffline = false,
  });

  UsersState copyWith({
    bool? isLoading,
    List<UserModel>? users,
    String? error,
    bool? isOffline,
  }) {
    return UsersState(
      isLoading: isLoading ?? this.isLoading,
      users: users ?? this.users,
      error: error,
      isOffline: isOffline ?? this.isOffline,
    );
  }
}

class UsersRepository {
  final Box _usersBox = Hive.box(HiveBoxes.usersBox);

  Future<List<UserModel>> getUsers() async {
    try {
      // Try to get fresh data from API
      final authService = AuthService(Dio());
      final response = await authService.getUsers(1);
      final List<dynamic> usersData = response['data'] as List<dynamic>;
      
      final users = usersData.map((user) => UserModel.fromJson(user)).toList();
      
      // Cache the data
      await _cacheUsers(users);
      
      return users;
    } catch (e) {
      // If API fails, try to get cached data
      final cachedUsers = await _getCachedUsers();
      if (cachedUsers.isNotEmpty) {
        throw Exception('Offline mode: Using cached data');
      }
      rethrow;
    }
  }

  Future<void> _cacheUsers(List<UserModel> users) async {
    final usersJson = users.map((user) => user.toJson()).toList();
    await _usersBox.put('users', usersJson);
    await _usersBox.put('last_updated', DateTime.now().millisecondsSinceEpoch);
  }

  Future<List<UserModel>> _getCachedUsers() async {
    final usersData = _usersBox.get('users') as List<dynamic>?;
    if (usersData == null) return [];
    
    return usersData.map((user) => UserModel.fromJson(Map<String, dynamic>.from(user))).toList();
  }

  Future<bool> isDataStale() async {
    final lastUpdated = _usersBox.get('last_updated') as int?;
    if (lastUpdated == null) return true;
    
    final now = DateTime.now().millisecondsSinceEpoch;
    final difference = now - lastUpdated;
    return difference > (24 * 60 * 60 * 1000); // 24 hours
  }
}

class UsersNotifier extends StateNotifier<UsersState> {
  final UsersRepository _usersRepository;

  UsersNotifier(this._usersRepository) : super(const UsersState()) {
    loadUsers();
  }

  Future<void> loadUsers() async {
    state = state.copyWith(isLoading: true, error: null);

    try {
      final users = await _usersRepository.getUsers();
      state = state.copyWith(
        isLoading: false,
        users: users,
        isOffline: false,
      );
    } catch (e) {
      // Try to load cached data
      try {
        final cachedUsers = await _usersRepository._getCachedUsers();
        state = state.copyWith(
          isLoading: false,
          users: cachedUsers,
          isOffline: true,
          error: 'Using offline data. Check your internet connection.',
        );
      } catch (cacheError) {
        state = state.copyWith(
          isLoading: false,
          error: 'Failed to load users. Please check your internet connection.',
        );
      }
    }
  }

  Future<void> refresh() async {
    await loadUsers();
  }
}