class AppConfig {
  static const String appName = 'VideoCall App';
  static const String appVersion = '1.0.0';
  
  // API Configuration
  static const String baseUrl = 'https://reqres.in/api';
  static const Duration apiTimeout = Duration(seconds: 30);
  
  // Chime SDK Configuration
  static const String region = 'us-east-1';
  static const String meetingId = 'test-meeting-123';
  
  // Cache Configuration
  static const Duration cacheExpiration = Duration(hours: 24);
  
  // Mock credentials for testing
  static const String mockEmail = 'test@example.com';
  static const String mockPassword = 'password123';
}