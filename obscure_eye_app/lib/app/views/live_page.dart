import 'package:flutter/material.dart';
import '../theme/cyberpunk_theme.dart';

class LivePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Live View'),
        centerTitle: true,
        elevation: 0,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 320,
              height: 200,
              decoration: BoxDecoration(
                color: darkPurple,
                border: Border.all(color: neonLime, width: 3),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Center(
                child: Icon(Icons.videocam, color: neonPurple, size: 64),
              ),
            ),
            SizedBox(height: 24),
            Text(
              'Live camera feed (mock)',
              style: TextStyle(
                color: neonLime,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}