import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/services/chime_service.dart';

final chimeServiceProvider = Provider<ChimeService>((ref) {
  return ChimeService();
});

final videoCallStateProvider = StateNotifierProvider<VideoCallNotifier, VideoCallState>((ref) {
  return VideoCallNotifier(ref.watch(chimeServiceProvider));
});

class VideoCallState {
  final bool isInitialized;
  final bool isConnected;
  final bool isAudioMuted;
  final bool isVideoEnabled;
  final bool isScreenSharing;
  final String? error;
  final String? localVideoTileId;
  final List<String> remoteVideoTileIds;

  const VideoCallState({
    this.isInitialized = false,
    this.isConnected = false,
    this.isAudioMuted = false,
    this.isVideoEnabled = true,
    this.isScreenSharing = false,
    this.error,
    this.localVideoTileId,
    this.remoteVideoTileIds = const [],
  });

  VideoCallState copyWith({
    bool? isInitialized,
    bool? isConnected,
    bool? isAudioMuted,
    bool? isVideoEnabled,
    bool? isScreenSharing,
    String? error,
    String? localVideoTileId,
    List<String>? remoteVideoTileIds,
  }) {
    return VideoCallState(
      isInitialized: isInitialized ?? this.isInitialized,
      isConnected: isConnected ?? this.isConnected,
      isAudioMuted: isAudioMuted ?? this.isAudioMuted,
      isVideoEnabled: isVideoEnabled ?? this.isVideoEnabled,
      isScreenSharing: isScreenSharing ?? this.isScreenSharing,
      error: error,
      localVideoTileId: localVideoTileId ?? this.localVideoTileId,
      remoteVideoTileIds: remoteVideoTileIds ?? this.remoteVideoTileIds,
    );
  }
}

class VideoCallNotifier extends StateNotifier<VideoCallState> {
  final ChimeService _chimeService;

  VideoCallNotifier(this._chimeService) : super(const VideoCallState());

  Future<void> initialize() async {
    try {
      await _chimeService.initialize();
      state = state.copyWith(isInitialized: true);
    } catch (e) {
      state = state.copyWith(error: 'Failed to initialize video service: $e');
    }
  }

  Future<void> requestPermissions() async {
    try {
      final hasPermissions = await _chimeService.requestPermissions();
      if (!hasPermissions) {
        state = state.copyWith(error: 'Camera and microphone permissions are required');
      }
    } catch (e) {
      state = state.copyWith(error: 'Failed to request permissions: $e');
    }
  }

  Future<void> joinMeeting(String meetingId, String attendeeId) async {
    try {
      state = state.copyWith(error: null);
      
      final success = await _chimeService.createMeetingSession(
        meetingId: meetingId,
        attendeeId: attendeeId,
      );
      
      if (success) {
        final connected = await _chimeService.startMeeting();
        state = state.copyWith(
          isConnected: connected,
          localVideoTileId: 'local-${DateTime.now().millisecondsSinceEpoch}',
        );
      } else {
        state = state.copyWith(error: 'Failed to create meeting session');
      }
    } catch (e) {
      state = state.copyWith(error: 'Failed to join meeting: $e');
    }
  }

  Future<void> toggleAudioMute() async {
    try {
      await _chimeService.toggleAudioMute();
      state = state.copyWith(isAudioMuted: !state.isAudioMuted);
    } catch (e) {
      state = state.copyWith(error: 'Failed to toggle audio: $e');
    }
  }

  Future<void> toggleVideo() async {
    try {
      await _chimeService.toggleVideo();
      state = state.copyWith(isVideoEnabled: !state.isVideoEnabled);
    } catch (e) {
      state = state.copyWith(error: 'Failed to toggle video: $e');
    }
  }

  Future<void> toggleScreenShare() async {
    try {
      if (state.isScreenSharing) {
        await _chimeService.stopScreenShare();
        state = state.copyWith(isScreenSharing: false);
      } else {
        final success = await _chimeService.startScreenShare();
        state = state.copyWith(isScreenSharing: success);
      }
    } catch (e) {
      state = state.copyWith(error: 'Failed to toggle screen share: $e');
    }
  }

  Future<void> leaveMeeting() async {
    try {
      await _chimeService.stopMeeting();
      state = state.copyWith(
        isConnected: false,
        localVideoTileId: null,
        remoteVideoTileIds: [],
      );
    } catch (e) {
      state = state.copyWith(error: 'Failed to leave meeting: $e');
    }
  }

  void clearError() {
    state = state.copyWith(error: null);
  }

  @override
  void dispose() {
    _chimeService.dispose();
    super.dispose();
  }
}