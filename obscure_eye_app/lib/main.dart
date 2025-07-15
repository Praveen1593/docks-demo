import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(ObscureEyeApp());

class ObscureEyeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Obscure Eye',
      home: DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List alerts = [];
  String videoUrl = "";

  @override
  void initState() {
    super.initState();
    fetchAlerts();
    fetchVideoUrl();
  }

  void fetchAlerts() async {
    final response = await http.get(Uri.parse('http://10.0.2.2:8000/api/alerts'));
    if (response.statusCode == 200) {
      setState(() {
        alerts = json.decode(response.body);
      });
    }
  }

  void fetchVideoUrl() async {
    final response = await http.get(Uri.parse('http://10.0.2.2:8000/api/video'));
    if (response.statusCode == 200) {
      setState(() {
        videoUrl = json.decode(response.body)['url'];
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Obscure Eye Dashboard')),
      body: SingleChildScrollView(
        child: Column(
          children: [
            Text('Live Video', style: TextStyle(fontSize: 20)),
            videoUrl.isNotEmpty
                ? Image.network(videoUrl)
                : CircularProgressIndicator(),
            SizedBox(height: 20),
            Text('Alerts', style: TextStyle(fontSize: 20)),
            ...alerts.map((alert) => ListTile(
                  title: Text('${alert['type'].toUpperCase()}: ${alert['message']}'),
                  subtitle: Text(alert['timestamp']),
                )),
          ],
        ),
      ),
    );
  }
}