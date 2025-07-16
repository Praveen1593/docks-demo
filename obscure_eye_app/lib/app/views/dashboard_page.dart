import 'package:flutter/material.dart';
import '../theme/cyberpunk_theme.dart';

class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Dashboard'),
        centerTitle: true,
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                _StatCard(
                  label: 'Active Cameras',
                  value: '4',
                  icon: Icons.videocam,
                  color: neonLime,
                ),
                SizedBox(width: 16),
                _StatCard(
                  label: 'Alerts Today',
                  value: '12',
                  icon: Icons.warning_amber_rounded,
                  color: neonPurple,
                ),
              ],
            ),
            SizedBox(height: 24),
            Text(
              'Quick Links',
              style: TextStyle(
                color: neonLime,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 12),
            Wrap(
              spacing: 16,
              runSpacing: 16,
              children: [
                _QuickLinkButton(
                  icon: Icons.videocam,
                  label: 'Live View',
                  onTap: () {},
                  color: neonLime,
                ),
                _QuickLinkButton(
                  icon: Icons.warning_amber_rounded,
                  label: 'Alerts',
                  onTap: () {},
                  color: neonPurple,
                ),
                _QuickLinkButton(
                  icon: Icons.settings,
                  label: 'Settings',
                  onTap: () {},
                  color: neonLime,
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;
  const _StatCard({required this.label, required this.value, required this.icon, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Card(
        color: darkPurple,
        elevation: 4,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              Icon(icon, color: color, size: 32),
              SizedBox(height: 8),
              Text(
                value,
                style: TextStyle(
                  color: color,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 4),
              Text(
                label,
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 14,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _QuickLinkButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;
  final Color color;
  const _QuickLinkButton({required this.icon, required this.label, required this.onTap, required this.color});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 110,
        height: 90,
        decoration: BoxDecoration(
          color: darkPurple,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: color, width: 2),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 32),
            SizedBox(height: 8),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontWeight: FontWeight.bold,
                fontSize: 15,
              ),
            ),
          ],
        ),
      ),
    );
  }
}