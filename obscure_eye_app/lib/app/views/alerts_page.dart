import 'package:flutter/material.dart';
import '../theme/cyberpunk_theme.dart';

final List<Map<String, String>> mockAlerts = [
  {
    'type': 'Theft',
    'message': 'Theft detected in Zone A',
    'time': '10:24 AM',
  },
  {
    'type': 'Emotion',
    'message': 'Angry person detected',
    'time': '09:58 AM',
  },
  {
    'type': 'Object',
    'message': 'Knife detected',
    'time': '09:45 AM',
  },
];

class AlertsPage extends StatefulWidget {
  @override
  _AlertsPageState createState() => _AlertsPageState();
}

class _AlertsPageState extends State<AlertsPage> {
  List<Map<String, String>> alerts = List.from(mockAlerts);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Alerts'),
        centerTitle: true,
        elevation: 0,
      ),
      body: ListView.builder(
        padding: EdgeInsets.all(16),
        itemCount: alerts.length,
        itemBuilder: (context, index) {
          final alert = alerts[index];
          return Dismissible(
            key: Key(alert['message']!),
            direction: DismissDirection.endToStart,
            onDismissed: (direction) {
              setState(() {
                alerts.removeAt(index);
              });
            },
            background: Container(
              alignment: Alignment.centerRight,
              padding: EdgeInsets.only(right: 24),
              color: neonPurple,
              child: Icon(Icons.delete, color: neonLime, size: 32),
            ),
            child: Card(
              color: darkPurple,
              elevation: 4,
              margin: EdgeInsets.only(bottom: 16),
              child: ListTile(
                leading: Icon(
                  alert['type'] == 'Theft'
                      ? Icons.warning_amber_rounded
                      : alert['type'] == 'Emotion'
                          ? Icons.mood_bad
                          : Icons.dangerous,
                  color: alert['type'] == 'Theft' ? neonLime : neonPurple,
                  size: 32,
                ),
                title: Text(
                  alert['type']!,
                  style: TextStyle(
                    color: neonLime,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                subtitle: Text(
                  alert['message']!,
                  style: TextStyle(color: neonPurple),
                ),
                trailing: Text(
                  alert['time']!,
                  style: TextStyle(color: neonLime, fontSize: 13),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}