import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';

import '../models/user_model.dart';

part 'auth_service.g.dart';

@RestApi(baseUrl: 'https://reqres.in/api')
abstract class AuthService {
  factory AuthService(Dio dio, {String baseUrl}) = _AuthService;

  @POST('/login')
  Future<AuthResponse> login(@Body() LoginRequest request);

  @GET('/users')
  Future<Map<String, dynamic>> getUsers(@Query('page') int page);
}

class AuthRepository {
  final AuthService _authService;

  AuthRepository(this._authService);

  Future<AuthResponse> login(String email, String password) async {
    try {
      // For demo purposes, we'll use mock authentication
      // In real app, this would call the actual API
      await Future.delayed(const Duration(seconds: 1)); // Simulate network delay
      
      // Mock successful login
      return AuthResponse(
        token: 'mock_token_${DateTime.now().millisecondsSinceEpoch}',
        user: UserModel(
          id: 1,
          email: email,
          firstName: 'John',
          lastName: 'Doe',
          avatar: 'https://reqres.in/img/faces/1-image.jpg',
        ),
      );
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<List<UserModel>> getUsers() async {
    try {
      final response = await _authService.getUsers(1);
      final List<dynamic> usersData = response['data'] as List<dynamic>;
      
      return usersData.map((user) => UserModel.fromJson(user)).toList();
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  String _handleError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return 'Connection timeout. Please check your internet connection.';
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        switch (statusCode) {
          case 400:
            return 'Invalid request. Please check your credentials.';
          case 401:
            return 'Unauthorized. Please login again.';
          case 404:
            return 'Service not found.';
          case 500:
            return 'Server error. Please try again later.';
          default:
            return 'Something went wrong. Please try again.';
        }
      case DioExceptionType.cancel:
        return 'Request cancelled.';
      case DioExceptionType.connectionError:
        return 'No internet connection.';
      default:
        return 'An unexpected error occurred.';
    }
  }
}