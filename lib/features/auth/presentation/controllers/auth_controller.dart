import 'package:get/get.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../../../core/utils/hive_boxes.dart';
import '../../data/models/user_model.dart';
import '../../data/services/auth_service.dart';

class AuthController extends GetxController {
  final AuthRepository _authRepository = AuthRepository();
  final Box _authBox = Hive.box(HiveBoxes.authBox);

  // Observable variables
  final RxBool _isLoading = false.obs;
  final Rx<UserModel?> _user = Rx<UserModel?>(null);
  final RxString _error = ''.obs;
  final RxBool _isAuthenticated = false.obs;

  // Getters
  bool get isLoading => _isLoading.value;
  UserModel? get user => _user.value;
  String get error => _error.value;
  bool get isAuthenticated => _isAuthenticated.value;

  @override
  void onInit() {
    super.onInit();
    _loadStoredAuth();
  }

  Future<void> _loadStoredAuth() async {
    try {
      final storedUser = _authBox.get('user');
      final storedToken = _authBox.get('token');
      
      if (storedUser != null && storedToken != null) {
        _user.value = UserModel.fromJson(Map<String, dynamic>.from(storedUser));
        _isAuthenticated.value = true;
      }
    } catch (e) {
      // Handle stored data corruption
      await logout();
    }
  }

  Future<void> login(String email, String password) async {
    _isLoading.value = true;
    _error.value = '';

    try {
      final response = await _authRepository.login(email, password);
      
      // Store auth data
      await _authBox.put('user', response.user.toJson());
      await _authBox.put('token', response.token);
      
      _user.value = response.user;
      _isAuthenticated.value = true;
      _isLoading.value = false;
      
      // Navigate to home
      Get.offAllNamed('/home');
    } catch (e) {
      _error.value = e.toString();
      _isLoading.value = false;
    }
  }

  Future<void> logout() async {
    await _authBox.clear();
    _user.value = null;
    _isAuthenticated.value = false;
    _error.value = '';
    
    // Navigate to login
    Get.offAllNamed('/login');
  }

  void clearError() {
    _error.value = '';
  }
}