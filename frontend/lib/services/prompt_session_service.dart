// Path: frontend/lib/services/prompt_session_service.dart

import 'package:flutter/foundation.dart';
import 'package:artisan_ai/models/prompt_session.dart';
import 'package:artisan_ai/services/api_service.dart';
import 'package:dio/dio.dart'; // Ensure Dio is imported for Exception handling

class PromptSessionService with ChangeNotifier {
  final ApiService _apiService;
  PromptSession _session = PromptSession();

  PromptSessionService(this._apiService);

  PromptSession get session => _session;

  void updateGoal(String goal) {
    _session.goal = goal;
    notifyListeners();
  }

  void updateFormat(String format) {
    _session.format = format;
    notifyListeners();
  }

  void updateContext(String context) {
    _session.context = context;
    notifyListeners();
  }

  void updateConstraints(List<String> constraints) {
    _session.constraints = constraints;
    notifyListeners();
  }

  void updatePersona(String persona) {
    _session.persona = persona;
    notifyListeners();
  }

  void resetSession() {
    _session = PromptSession();
    notifyListeners();
  }

  Future<Map<String, dynamic>> refinePrompt() async {
    try {
      final response = await _apiService.post(
        '/agent/start-critique',
        _session.toJson(),
      );
      // Dio's response.data is already decoded JSON
      return response.data as Map<String, dynamic>;
    } on DioException catch (e) {
      throw Exception(
          'Failed to refine prompt: ${e.response?.statusCode} ${e.response?.data}');
    } catch (e) {
      throw Exception('An unexpected error occurred: $e');
    }
  }

  Future<Map<String, dynamic>> submitRefinement(
      String sessionId, String userResponse) async {
    try {
      final response = await _apiService.post(
        '/agent/refine-critique',
        {
          'session_id': sessionId,
          'user_response': userResponse,
        },
      );
      return response.data as Map<String, dynamic>;
    } on DioException catch (e) {
      throw Exception(
          'Failed to submit refinement: ${e.response?.statusCode} ${e.response?.data}');
    } catch (e) {
      throw Exception('An unexpected error occurred: $e');
    }
  }
}