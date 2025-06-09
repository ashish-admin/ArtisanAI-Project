// frontend/lib/services/prompt_session_service.dart

import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:artisan_ai/models/prompt_session.dart';
import 'api_service.dart';

class PromptSessionService with ChangeNotifier {
  final ApiService _apiService;
  PromptSession _session = PromptSession();

  PromptSessionService(this._apiService);

  PromptSession get session => _session;

  // No changes to update methods
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
    final response = await _apiService.post(
      '/agent/start-critique',
      _session.toJson(),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to refine prompt: ${response.statusCode} ${response.body}');
    }
  }

  Future<Map<String, dynamic>> submitRefinement(String sessionId, String userResponse) async {
    final response = await _apiService.post(
      '/agent/refine-critique',
      {
        'session_id': sessionId,
        'user_response': userResponse,
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to submit refinement: ${response.statusCode} ${response.body}');
    }
  }
}