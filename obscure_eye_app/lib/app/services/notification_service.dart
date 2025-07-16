import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/material.dart';

class NotificationService {
  static final FirebaseMessaging _messaging = FirebaseMessaging.instance;

  static Future<void> init() async {
    // Initialize Firebase (should be called before runApp in main.dart)
    await Firebase.initializeApp();

    // Request permissions (iOS)
    await _messaging.requestPermission();

    // Get the device token (print this and use in your backend for testing)
    String? token = await _messaging.getToken();
    print('FCM Device Token: $token');

    // Listen for foreground messages
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      print('Received a message: ${message.notification?.title} - ${message.notification?.body}');
      // Optionally, show a dialog or local notification here
    });

    // Listen for background/terminated messages (when user taps notification)
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      print('Notification clicked!');
      // Optionally, navigate to a specific page
    });
  }
}