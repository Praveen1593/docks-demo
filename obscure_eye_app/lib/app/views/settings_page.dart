import 'package:flutter/material.dart';
import '../theme/cyberpunk_theme.dart';

class SettingsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Settings'),
        centerTitle: true,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Card(
              color: darkPurple,
              elevation: 4,
              child: ListTile(
                leading: Icon(Icons.person, color: neonLime, size: 32),
                title: Text('Admin User', style: TextStyle(color: neonLime, fontWeight: FontWeight.bold)),
                subtitle: Text('admin@obscureeye.ai', style: TextStyle(color: neonPurple)),
              ),
            ),
            SizedBox(height: 24),
            Card(
              color: darkPurple,
              elevation: 4,
              child: SwitchListTile(
                activeColor: neonLime,
                inactiveThumbColor: neonPurple,
                title: Text('Dark Mode', style: TextStyle(color: neonLime, fontWeight: FontWeight.bold)),
                value: true,
                onChanged: (val) {}, // Mock toggle
              ),
            ),
            SizedBox(height: 24),
            Card(
              color: darkPurple,
              elevation: 4,
              child: ListTile(
                leading: Icon(Icons.logout, color: neonPurple, size: 32),
                title: Text('Logout', style: TextStyle(color: neonPurple, fontWeight: FontWeight.bold)),
                onTap: () {
                  // Mock logout
                  Navigator.of(context).popUntil((route) => route.isFirst);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}