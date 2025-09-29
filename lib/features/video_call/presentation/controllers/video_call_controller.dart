import 'dart:async';
import 'package:get/get.dart';

import '../data/services/chime_service.dart';

class VideoCallController extends GetxController {
  final ChimeService _chimeService = ChimeService();

  // Observable variables
  final RxBool _isInitialized = false.obs;
  final RxBool _isConnected = false.obs;
  final RxBool _isAudioMuted = false.obs;
  final RxBool _isVideoEnabled = true.obs;
  final RxBool _isScreenSharing = false.obs;
  final RxString _error = ''.obs;
  final RxString _localVideoTileId = ''.obs;
  final RxList<String> _remoteVideoTileIds = <String>[].obs;

  // Getters
  bool get isInitialized => _isInitialized.value;
  bool get isConnected => _isConnected.value;
  bool get isAudioMuted => _isAudioMuted.value;
  bool get isVideoEnabled => _isVideoEnabled.value;
  bool get isScreenSharing => _isScreenSharing.value;
  String get error => _error.value;
  String get localVideoTileId => _localVideoTileId.value;
  List<String> get remoteVideoTileIds => _remoteVideoTileIds;

  @override
  void onInit() {
    super.onInit();
  }

  @override
  void onReady() {
    super.onReady();
    _initialize();
  }

  @override
  void onClose() {
    _chimeService.dispose();
    super.onClose();
  }

  Future<void> _initialize() async {
    try {
      await _chimeService.initialize();
      _isInitialized.value = true;
    } catch (e) {
      _error.value = 'Failed to initialize video service: $e';
    }
  }

  Future<void> requestPermissions() async {
    try {
      final hasPermissions = await _chimeService.requestPermissions();
      if (!hasPermissions) {
        _error.value = 'Camera and microphone permissions are required';
      }
    } catch (e) {
      _error.value = 'Failed to request permissions: $e';
    }
  }

  Future<void> joinMeeting(String meetingId, String attendeeId) async {
    try {
      _error.value = '';
      
      final success = await _chimeService.createMeetingSession(
        meetingId: meetingId,
        attendeeId: attendeeId,
      );
      
      if (success) {
        final connected = await _chimeService.startMeeting();
        _isConnected.value = connected;
        _localVideoTileId.value = 'local-${DateTime.now().millisecondsSinceEpoch}';
        
        if (connected) {
          _remoteVideoTileIds.add('remote-1');
        }
      } else {
        _error.value = 'Failed to create meeting session';
      }
    } catch (e) {
      _error.value = 'Failed to join meeting: $e';
    }
  }

  Future<void> toggleAudioMute() async {
    try {
      await _chimeService.toggleAudioMute();
      _isAudioMuted.value = !_isAudioMuted.value;
    } catch (e) {
      _error.value = 'Failed to toggle audio: $e';
    }
  }

  Future<void> toggleVideo() async {
    try {
      await _chimeService.toggleVideo();
      _isVideoEnabled.value = !_isVideoEnabled.value;
    } catch (e) {
      _error.value = 'Failed to toggle video: $e';
    }
  }

  Future<void> toggleScreenShare() async {
    try {
      if (_isScreenSharing.value) {
        await _chimeService.stopScreenShare();
        _isScreenSharing.value = false;
      } else {
        final success = await _chimeService.startScreenShare();
        _isScreenSharing.value = success;
      }
    } catch (e) {
      _error.value = 'Failed to toggle screen share: $e';
    }
  }

  Future<void> leaveMeeting() async {
    try {
      await _chimeService.stopMeeting();
      _isConnected.value = false;
      _localVideoTileId.value = '';
      _remoteVideoTileIds.clear();
    } catch (e) {
      _error.value = 'Failed to leave meeting: $e';
    }
  }

  void clearError() {
    _error.value = '';
  }
}