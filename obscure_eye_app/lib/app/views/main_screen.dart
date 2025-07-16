import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../theme/cyberpunk_theme.dart';
import 'dashboard_page.dart';
import 'live_page.dart';
import 'alerts_page.dart';
import 'settings_page.dart';

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final RxInt _selectedIndex = 0.obs;
  final List<Widget> _pages = [
    DashboardPage(),
    LivePage(),
    AlertsPage(),
    SettingsPage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Obx(() => Scaffold(
      body: _pages[_selectedIndex.value],
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: darkPurple,
        selectedItemColor: neonLime,
        unselectedItemColor: neonPurple,
        currentIndex: _selectedIndex.value,
        onTap: (index) => _selectedIndex.value = index,
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.dashboard),
            label: 'Dashboard',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.videocam),
            label: 'Live',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.warning_amber_rounded),
            label: 'Alerts',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.settings),
            label: 'Settings',
          ),
        ],
      ),
    ));
  }
}