import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:uuid/uuid.dart';

import '../controllers/video_call_controller.dart';
import '../widgets/video_tile.dart';
import '../widgets/meeting_controls.dart';

class VideoCallPage extends StatefulWidget {
  final String meetingId;

  const VideoCallPage({
    super.key,
    required this.meetingId,
  });

  @override
  State<VideoCallPage> createState() => _VideoCallPageState();
}

class _VideoCallPageState extends State<VideoCallPage>
    with WidgetsBindingObserver {
  final VideoCallController _videoCallController = Get.put(VideoCallController());
  bool _isControlsVisible = true;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _initializeVideoCall();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);
    
    switch (state) {
      case AppLifecycleState.resumed:
        // App came back to foreground
        break;
      case AppLifecycleState.paused:
        // App went to background
        break;
      case AppLifecycleState.detached:
        // App is being closed
        _videoCallController.leaveMeeting();
        break;
      default:
        break;
    }
  }

  Future<void> _initializeVideoCall() async {
    // Request permissions
    await _videoCallController.requestPermissions();
    
    // Generate a unique attendee ID for demo purposes
    final attendeeId = const Uuid().v4();
    
    // Join the meeting
    await _videoCallController.joinMeeting(widget.meetingId, attendeeId);
  }

  @override
  Widget build(BuildContext context) {
    // Handle orientation
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);

    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(
          children: [
            // Video tiles
            Obx(() => _buildVideoTiles()),
            
            // Meeting info header
            _buildMeetingInfo(),
            
            // Loading overlay
            Obx(() {
              if (_videoCallController.isInitialized && !_videoCallController.isConnected) {
                return _buildLoadingOverlay();
              }
              return const SizedBox.shrink();
            }),
            
            // Controls
            Obx(() {
              if (_isControlsVisible && _videoCallController.isConnected) {
                return _buildControls();
              }
              return const SizedBox.shrink();
            }),
            
            // Tap to toggle controls
            GestureDetector(
              onTap: () {
                setState(() {
                  _isControlsVisible = !_isControlsVisible;
                });
              },
              child: Container(
                color: Colors.transparent,
              ),
            ),

            // Error overlay
            Obx(() {
              if (_videoCallController.error.isNotEmpty) {
                WidgetsBinding.instance.addPostFrameCallback((_) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(_videoCallController.error),
                      backgroundColor: Theme.of(context).colorScheme.error,
                      action: SnackBarAction(
                        label: 'Dismiss',
                        onPressed: _videoCallController.clearError,
                      ),
                    ),
                  );
                });
              }
              return const SizedBox.shrink();
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildVideoTiles() {
    if (!_videoCallController.isConnected) {
      return const Center(
        child: Text(
          'Connecting to meeting...',
          style: TextStyle(color: Colors.white, fontSize: 18),
        ),
      );
    }

    return Column(
      children: [
        // Local video tile (small)
        Expanded(
          flex: 1,
          child: Container(
            margin: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white24, width: 2),
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: VideoTile(
                isLocal: true,
                isEnabled: _videoCallController.isVideoEnabled,
                tileId: _videoCallController.localVideoTileId,
              ),
            ),
          ),
        ),
        
        // Remote video tiles
        Expanded(
          flex: 2,
          child: Container(
            margin: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.white24, width: 2),
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: VideoTile(
                isLocal: false,
                isEnabled: true,
                tileId: 'remote-1',
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildMeetingInfo() {
    return Positioned(
      top: 16,
      left: 16,
      right: 16,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: Colors.black54,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Row(
          children: [
            const Icon(Icons.video_call, color: Colors.white, size: 20),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                'Meeting: ${widget.meetingId}',
                style: const TextStyle(color: Colors.white, fontSize: 14),
                overflow: TextOverflow.ellipsis,
              ),
            ),
            IconButton(
              icon: const Icon(Icons.close, color: Colors.white),
              onPressed: () {
                _showLeaveDialog();
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLoadingOverlay() {
    return Container(
      color: Colors.black54,
      child: const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            CircularProgressIndicator(color: Colors.white),
            SizedBox(height: 16),
            Text(
              'Connecting to meeting...',
              style: TextStyle(color: Colors.white, fontSize: 16),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildControls() {
    return Positioned(
      bottom: 32,
      left: 16,
      right: 16,
      child: MeetingControls(
        isAudioMuted: _videoCallController.isAudioMuted,
        isVideoEnabled: _videoCallController.isVideoEnabled,
        isScreenSharing: _videoCallController.isScreenSharing,
        onToggleAudio: () {
          _videoCallController.toggleAudioMute();
        },
        onToggleVideo: () {
          _videoCallController.toggleVideo();
        },
        onToggleScreenShare: () {
          _videoCallController.toggleScreenShare();
        },
        onLeave: () {
          _showLeaveDialog();
        },
      ),
    );
  }

  void _showLeaveDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Leave Meeting'),
        content: const Text('Are you sure you want to leave this meeting?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              _videoCallController.leaveMeeting();
              Get.back();
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
              foregroundColor: Colors.white,
            ),
            child: const Text('Leave'),
          ),
        ],
      ),
    );
  }
}