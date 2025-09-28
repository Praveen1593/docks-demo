import 'package:hive_flutter/hive_flutter.dart';

class HiveBoxes {
  static const String usersBox = 'users_box';
  static const String authBox = 'auth_box';
  static const String settingsBox = 'settings_box';
  
  static Future<void> init() async {
    await Hive.openBox(usersBox);
    await Hive.openBox(authBox);
    await Hive.openBox(settingsBox);
  }
}