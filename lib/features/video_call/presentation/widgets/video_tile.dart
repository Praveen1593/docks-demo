import 'package:flutter/material.dart';

class VideoTile extends StatelessWidget {
  final bool isLocal;
  final bool isEnabled;
  final String tileId;

  const VideoTile({
    super.key,
    required this.isLocal,
    required this.isEnabled,
    required this.tileId,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.grey[900],
      child: Stack(
        fit: StackFit.expand,
        children: [
          // Video placeholder (in a real app, this would be the actual video stream)
          _buildVideoPlaceholder(),
          
          // User info overlay
          if (isLocal) _buildLocalUserOverlay(),
          
          // Video disabled indicator
          if (!isEnabled) _buildVideoDisabledIndicator(),
        ],
      ),
    );
  }

  Widget _buildVideoPlaceholder() {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            Colors.blue.shade800,
            Colors.purple.shade600,
          ],
        ),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              isLocal ? Icons.person : Icons.person_outline,
              size: 80,
              color: Colors.white70,
            ),
            const SizedBox(height: 8),
            Text(
              isLocal ? 'You' : 'Remote Participant',
              style: const TextStyle(
                color: Colors.white70,
                fontSize: 16,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLocalUserOverlay() {
    return Positioned(
      top: 8,
      left: 8,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        decoration: BoxDecoration(
          color: Colors.black54,
          borderRadius: BorderRadius.circular(12),
        ),
        child: const Text(
          'You',
          style: TextStyle(
            color: Colors.white,
            fontSize: 12,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),
    );
  }

  Widget _buildVideoDisabledIndicator() {
    return Container(
      color: Colors.black54,
      child: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.videocam_off,
              size: 60,
              color: Colors.white54,
            ),
            SizedBox(height: 8),
            Text(
              'Camera Off',
              style: TextStyle(
                color: Colors.white54,
                fontSize: 16,
              ),
            ),
          ],
        ),
      ),
    );
  }
}