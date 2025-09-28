# VideoCall App - Flutter Video Calling Application

A comprehensive Flutter application that demonstrates video calling capabilities using Amazon Chime SDK, REST API integration, and modern app architecture patterns.

## 🚀 Features

### Core Features
- **Authentication & Login**: Secure login with email/password validation
- **Video Calling**: One-to-one video calls using Amazon Chime SDK
- **User Management**: Browse users from REST API with offline caching
- **Screen Sharing**: Share your screen during video calls
- **Real-time Controls**: Mute/unmute audio, enable/disable video

### Technical Features
- **State Management**: Clean architecture with Riverpod
- **Offline Support**: Cached data for offline functionality
- **Responsive UI**: Adaptive design for different screen sizes
- **Permissions Handling**: Graceful camera and microphone permissions
- **Error Handling**: Comprehensive error handling and user feedback
- **App Lifecycle**: Proper handling of background/foreground states

## 📱 Screenshots

### Authentication Screen
- Clean login interface with validation
- Demo credentials provided
- Material Design 3 components

### Home Screen
- Quick access to video calls and user list
- User profile display
- Intuitive navigation

### Video Call Screen
- Local and remote video tiles
- Meeting controls (mute, video, screen share, leave)
- Orientation support
- Real-time meeting status

### Users Screen
- User list with avatars and names
- Offline mode indicator
- Pull-to-refresh functionality

## 🛠️ Tech Stack

- **Framework**: Flutter 3.16.0+
- **State Management**: Riverpod 2.4.9
- **Video SDK**: Amazon Chime SDK 0.19.0
- **HTTP Client**: Dio 5.4.0 with Retrofit
- **Local Storage**: Hive 2.2.3
- **Navigation**: GoRouter 12.1.3
- **UI**: Material Design 3
- **Permissions**: Permission Handler 11.2.0

## 📋 Prerequisites

Before running the application, ensure you have:

- Flutter SDK 3.16.0 or higher
- Dart SDK 3.0.0 or higher
- Android Studio / Xcode for mobile development
- Git for version control

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/flutter-video-call-app.git
cd flutter-video-call-app
```

### 2. Install Dependencies

```bash
flutter pub get
```

### 3. Generate Code

```bash
flutter packages pub run build_runner build --delete-conflicting-outputs
```

### 4. Run the Application

```bash
# For development
flutter run

# For release build
flutter run --release
```

## 📱 Platform Setup

### Android Setup

1. **Minimum SDK**: Android API 21 (Android 5.0)
2. **Target SDK**: Android API 34
3. **Permissions**: Automatically configured in AndroidManifest.xml

### iOS Setup

1. **Minimum iOS Version**: iOS 11.0
2. **Permissions**: Camera and microphone permissions configured in Info.plist
3. **Orientation**: Supports all orientations

## 🔧 Configuration

### Amazon Chime SDK Setup

1. **Create AWS Account**: Sign up for AWS if you don't have an account
2. **Set up Chime SDK**: Follow [Amazon Chime SDK documentation](https://docs.aws.amazon.com/chime/latest/dg/meetings-sdk.html)
3. **Configure Backend**: Set up meeting creation endpoints
4. **Update Configuration**: Modify `AppConfig` in `lib/core/config/app_config.dart`

### API Configuration

The app uses ReqRes API for demo purposes. To use your own API:

1. Update `baseUrl` in `AppConfig`
2. Modify API models if needed
3. Update authentication logic

## 🏗️ Architecture

### Project Structure

```
lib/
├── core/
│   ├── config/          # App configuration
│   ├── router/          # Navigation setup
│   ├── theme/           # App theming
│   └── utils/           # Utilities
├── features/
│   ├── auth/            # Authentication feature
│   ├── home/            # Home screen
│   ├── users/           # User management
│   ├── video_call/      # Video calling
│   └── splash/          # Splash screen
└── main.dart           # App entry point
```

### State Management Pattern

- **Providers**: Service and repository providers
- **Notifiers**: State management with StateNotifier
- **Models**: Data models with JSON serialization
- **Services**: API and external service integrations

## 🧪 Testing

### Run Tests

```bash
# Run all tests
flutter test

# Run tests with coverage
flutter test --coverage

# Generate coverage report
genhtml coverage/lcov.info -o coverage/html
```

### Test Coverage

The project includes:
- Unit tests for business logic
- Widget tests for UI components
- Integration tests for user flows

## 📦 Building for Production

### Android

```bash
# Build APK
flutter build apk --release

# Build App Bundle (for Play Store)
flutter build appbundle --release
```

### iOS

```bash
# Build for iOS
flutter build ios --release

# Archive for App Store
flutter build ipa --release
```

## 🚀 Deployment

### Android Play Store

1. Build App Bundle: `flutter build appbundle --release`
2. Sign with your release keystore
3. Upload to Google Play Console
4. Configure store listing and release

### iOS App Store

1. Build IPA: `flutter build ipa --release`
2. Archive in Xcode
3. Upload to App Store Connect
4. Configure app metadata and release

## 🔒 Security Considerations

- **API Keys**: Store sensitive keys in environment variables
- **Authentication**: Implement proper token management
- **Permissions**: Request only necessary permissions
- **Data Encryption**: Encrypt sensitive local data
- **Network Security**: Use HTTPS for all API calls

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- **Chime SDK**: Currently using mock implementation for demo
- **Screen Sharing**: Simulated for demonstration purposes
- **Push Notifications**: Not implemented in current version

## 🔮 Future Enhancements

- [ ] Real Amazon Chime SDK integration
- [ ] Push notifications for incoming calls
- [ ] Group video calling
- [ ] Chat functionality
- [ ] Call recording
- [ ] Advanced screen sharing
- [ ] Custom backgrounds and filters

## 📞 Support

For support and questions:

- Create an issue in the GitHub repository
- Check the documentation
- Review the code comments

## 🙏 Acknowledgments

- Amazon Chime SDK team for the video calling SDK
- Flutter team for the amazing framework
- Riverpod for state management
- All contributors and testers

---

**Note**: This is a demonstration project for interview purposes. In a production environment, additional security measures, testing, and optimizations would be required.