import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:uuid/uuid.dart';

import '../providers/video_call_provider.dart';
import '../widgets/video_tile.dart';
import '../widgets/meeting_controls.dart';

class VideoCallScreen extends ConsumerStatefulWidget {
  final String meetingId;

  const VideoCallScreen({
    super.key,
    required this.meetingId,
  });

  @override
  ConsumerState<VideoCallScreen> createState() => _VideoCallScreenState();
}

class _VideoCallScreenState extends ConsumerState<VideoCallScreen>
    with WidgetsBindingObserver {
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
    
    final videoCallNotifier = ref.read(videoCallStateProvider.notifier);
    
    switch (state) {
      case AppLifecycleState.resumed:
        // App came back to foreground
        break;
      case AppLifecycleState.paused:
        // App went to background
        break;
      case AppLifecycleState.detached:
        // App is being closed
        videoCallNotifier.leaveMeeting();
        break;
      default:
        break;
    }
  }

  Future<void> _initializeVideoCall() async {
    final videoCallNotifier = ref.read(videoCallStateProvider.notifier);
    
    // Initialize the service
    await videoCallNotifier.initialize();
    
    // Request permissions
    await videoCallNotifier.requestPermissions();
    
    // Generate a unique attendee ID for demo purposes
    final attendeeId = const Uuid().v4();
    
    // Join the meeting
    await videoCallNotifier.joinMeeting(widget.meetingId, attendeeId);
  }

  @override
  Widget build(BuildContext context) {
    final videoCallState = ref.watch(videoCallStateProvider);
    
    // Handle orientation
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);

    ref.listen(videoCallStateProvider, (previous, next) {
      if (next.error != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(next.error!),
            backgroundColor: Theme.of(context).colorScheme.error,
            action: SnackBarAction(
              label: 'Dismiss',
              onPressed: () {
                ref.read(videoCallStateProvider.notifier).clearError();
              },
            ),
          ),
        );
      }
    });

    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: Stack(
          children: [
            // Video tiles
            _buildVideoTiles(videoCallState),
            
            // Meeting info header
            _buildMeetingInfo(),
            
            // Loading overlay
            if (videoCallState.isInitialized && !videoCallState.isConnected)
              _buildLoadingOverlay(),
            
            // Controls
            if (_isControlsVisible && videoCallState.isConnected)
              _buildControls(videoCallState),
            
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
          ],
        ),
      ),
    );
  }

  Widget _buildVideoTiles(VideoCallState state) {
    if (!state.isConnected) {
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
                isEnabled: state.isVideoEnabled,
                tileId: state.localVideoTileId ?? 'local',
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

  Widget _buildControls(VideoCallState state) {
    return Positioned(
      bottom: 32,
      left: 16,
      right: 16,
      child: MeetingControls(
        isAudioMuted: state.isAudioMuted,
        isVideoEnabled: state.isVideoEnabled,
        isScreenSharing: state.isScreenSharing,
        onToggleAudio: () {
          ref.read(videoCallStateProvider.notifier).toggleAudioMute();
        },
        onToggleVideo: () {
          ref.read(videoCallStateProvider.notifier).toggleVideo();
        },
        onToggleScreenShare: () {
          ref.read(videoCallStateProvider.notifier).toggleScreenShare();
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
              ref.read(videoCallStateProvider.notifier).leaveMeeting();
              context.go('/home');
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