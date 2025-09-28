import 'package:flutter/material.dart';

class MeetingControls extends StatelessWidget {
  final bool isAudioMuted;
  final bool isVideoEnabled;
  final bool isScreenSharing;
  final VoidCallback onToggleAudio;
  final VoidCallback onToggleVideo;
  final VoidCallback onToggleScreenShare;
  final VoidCallback onLeave;

  const MeetingControls({
    super.key,
    required this.isAudioMuted,
    required this.isVideoEnabled,
    required this.isScreenSharing,
    required this.onToggleAudio,
    required this.onToggleVideo,
    required this.onToggleScreenShare,
    required this.onLeave,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      decoration: BoxDecoration(
        color: Colors.black54,
        borderRadius: BorderRadius.circular(25),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          // Audio toggle
          _buildControlButton(
            icon: isAudioMuted ? Icons.mic_off : Icons.mic,
            isActive: !isAudioMuted,
            onPressed: onToggleAudio,
            backgroundColor: isAudioMuted ? Colors.red : Colors.white,
            iconColor: isAudioMuted ? Colors.white : Colors.black,
          ),
          
          // Video toggle
          _buildControlButton(
            icon: isVideoEnabled ? Icons.videocam : Icons.videocam_off,
            isActive: isVideoEnabled,
            onPressed: onToggleVideo,
            backgroundColor: isVideoEnabled ? Colors.white : Colors.red,
            iconColor: isVideoEnabled ? Colors.black : Colors.white,
          ),
          
          // Screen share toggle
          _buildControlButton(
            icon: isScreenSharing ? Icons.stop_screen_share : Icons.screen_share,
            isActive: isScreenSharing,
            onPressed: onToggleScreenShare,
            backgroundColor: isScreenSharing ? Colors.orange : Colors.white,
            iconColor: isScreenSharing ? Colors.white : Colors.black,
          ),
          
          // Leave meeting
          _buildControlButton(
            icon: Icons.call_end,
            isActive: false,
            onPressed: onLeave,
            backgroundColor: Colors.red,
            iconColor: Colors.white,
          ),
        ],
      ),
    );
  }

  Widget _buildControlButton({
    required IconData icon,
    required bool isActive,
    required VoidCallback onPressed,
    required Color backgroundColor,
    required Color iconColor,
  }) {
    return GestureDetector(
      onTap: onPressed,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: backgroundColor,
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Icon(
          icon,
          color: iconColor,
          size: 24,
        ),
      ),
    );
  }
}