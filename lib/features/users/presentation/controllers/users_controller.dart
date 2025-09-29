import 'package:get/get.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:dio/dio.dart';

import '../../../core/utils/hive_boxes.dart';
import '../../data/models/user_model.dart';
import '../../data/services/auth_service.dart';

class UsersController extends GetxController {
  final Box _usersBox = Hive.box(HiveBoxes.usersBox);

  // Observable variables
  final RxBool _isLoading = false.obs;
  final RxList<UserModel> _users = <UserModel>[].obs;
  final RxString _error = ''.obs;
  final RxBool _isOffline = false.obs;

  // Getters
  bool get isLoading => _isLoading.value;
  List<UserModel> get users => _users;
  String get error => _error.value;
  bool get isOffline => _isOffline.value;

  @override
  void onInit() {
    super.onInit();
    loadUsers();
  }

  Future<void> loadUsers() async {
    _isLoading.value = true;
    _error.value = '';

    try {
      final users = await _getUsersFromAPI();
      _users.value = users;
      _isOffline.value = false;
      _isLoading.value = false;
    } catch (e) {
      // Try to load cached data
      try {
        final cachedUsers = await _getCachedUsers();
        _users.value = cachedUsers;
        _isOffline.value = true;
        _error.value = 'Using offline data. Check your internet connection.';
        _isLoading.value = false;
      } catch (cacheError) {
        _error.value = 'Failed to load users. Please check your internet connection.';
        _isLoading.value = false;
      }
    }
  }

  Future<List<UserModel>> _getUsersFromAPI() async {
    try {
      final authService = AuthService(Dio());
      final response = await authService.getUsers(1);
      final List<dynamic> usersData = response['data'] as List<dynamic>;
      
      final users = usersData.map((user) => UserModel.fromJson(user)).toList();
      
      // Cache the data
      await _cacheUsers(users);
      
      return users;
    } catch (e) {
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

  Future<void> refresh() async {
    await loadUsers();
  }

  void clearError() {
    _error.value = '';
  }
}