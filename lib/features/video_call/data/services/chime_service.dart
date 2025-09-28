import 'dart:async';
import 'dart:io';
import 'package:amazon_chime_sdk/amazon_chime_sdk.dart';
import 'package:permission_handler/permission_handler.dart';

class ChimeService {
  static final ChimeService _instance = ChimeService._internal();
  factory ChimeService() => _instance;
  ChimeService._internal();

  MeetingSession? _meetingSession;
  DefaultAudioVideoController? _audioVideoController;
  StreamController<VideoTileState>? _videoTileStateController;
  StreamController<AudioVideoObserver>? _observerController;

  // Getters
  MeetingSession? get meetingSession => _meetingSession;
  DefaultAudioVideoController? get audioVideoController => _audioVideoController;
  StreamController<VideoTileState>? get videoTileStateController => _videoTileStateController;

  // Initialize the service
  Future<void> initialize() async {
    _videoTileStateController = StreamController<VideoTileState>.broadcast();
    _observerController = StreamController<AudioVideoObserver>.broadcast();
  }

  // Request permissions
  Future<bool> requestPermissions() async {
    final cameraStatus = await Permission.camera.request();
    final microphoneStatus = await Permission.microphone.request();
    
    return cameraStatus.isGranted && microphoneStatus.isGranted;
  }

  // Create meeting session
  Future<bool> createMeetingSession({
    required String meetingId,
    required String attendeeId,
    String? endpointUrl,
  }) async {
    try {
      // For demo purposes, we'll create a mock meeting session
      // In a real app, you would create the meeting using Chime's backend
      
      final meetingSessionConfiguration = MeetingSessionConfiguration(
        meetingId: meetingId,
        credentials: MeetingSessionCredentials(
          attendeeId: attendeeId,
          joinToken: 'mock-join-token',
        ),
        urls: MeetingSessionURLs(
          audioHostUrl: endpointUrl ?? 'https://chime.aws/audio',
          turnControlUrl: 'https://chime.aws/turn',
          signalingUrl: 'https://chime.aws/signaling',
        ),
      );

      _meetingSession = DefaultMeetingSession(
        meetingSessionConfiguration,
        logger: ConsoleLogger(),
        audioVideoControllerFactory: DefaultAudioVideoControllerFactory(),
      );

      _audioVideoController = _meetingSession?.audioVideo;
      _setupAudioVideoObservers();

      return true;
    } catch (e) {
      print('Error creating meeting session: $e');
      return false;
    }
  }

  // Setup observers
  void _setupAudioVideoObservers() {
    _audioVideoController?.addObserver(_observerController!.stream);
  }

  // Start meeting
  Future<bool> startMeeting() async {
    try {
      if (_meetingSession == null) return false;
      
      await _audioVideoController?.start();
      await _audioVideoController?.startLocalVideo();
      await _audioVideoController?.startLocalAudio();
      
      return true;
    } catch (e) {
      print('Error starting meeting: $e');
      return false;
    }
  }

  // Stop meeting
  Future<void> stopMeeting() async {
    try {
      await _audioVideoController?.stop();
      await _audioVideoController?.stopLocalVideo();
      await _audioVideoController?.stopLocalAudio();
    } catch (e) {
      print('Error stopping meeting: $e');
    }
  }

  // Toggle audio mute
  Future<void> toggleAudioMute() async {
    try {
      if (_audioVideoController?.realtimeLocalMute ?? false) {
        await _audioVideoController?.realtimeUnmuteLocalAudio();
      } else {
        await _audioVideoController?.realtimeMuteLocalAudio();
      }
    } catch (e) {
      print('Error toggling audio mute: $e');
    }
  }

  // Toggle video
  Future<void> toggleVideo() async {
    try {
      if (_audioVideoController?.hasLocalVideo() ?? false) {
        await _audioVideoController?.stopLocalVideo();
      } else {
        await _audioVideoController?.startLocalVideo();
      }
    } catch (e) {
      print('Error toggling video: $e');
    }
  }

  // Start screen share
  Future<bool> startScreenShare() async {
    try {
      // For demo purposes, we'll simulate screen sharing
      // In a real app, you would implement actual screen sharing
      return true;
    } catch (e) {
      print('Error starting screen share: $e');
      return false;
    }
  }

  // Stop screen share
  Future<void> stopScreenShare() async {
    try {
      // For demo purposes, we'll simulate stopping screen sharing
    } catch (e) {
      print('Error stopping screen share: $e');
    }
  }

  // Get local video tile
  VideoTileState? getLocalVideoTile() {
    return _audioVideoController?.getLocalVideoTile();
  }

  // Get remote video tiles
  List<VideoTileState> getRemoteVideoTiles() {
    return _audioVideoController?.getRemoteVideoTiles() ?? [];
  }

  // Cleanup
  void dispose() {
    _videoTileStateController?.close();
    _observerController?.close();
    _meetingSession = null;
    _audioVideoController = null;
  }
}

// Mock implementation for demo purposes
class MockVideoTileState implements VideoTileState {
  @override
  int get tileId => 1;
  
  @override
  int get attendeeId => 1;
  
  @override
  bool get isLocalTile => true;
  
  @override
  bool get isContent => false;
  
  @override
  bool get isLocalPaused => false;
  
  @override
  bool get isRemotePaused => false;
  
  @override
  bool get isActiveSpeaker => false;
  
  @override
  VideoPauseState get pauseState => VideoPauseState.Unpaused;
  
  @override
  VideoStreamContentWidth get videoStreamContentWidth => VideoStreamContentWidth.High;
  
  @override
  int get videoStreamContentHeight => 720;
}